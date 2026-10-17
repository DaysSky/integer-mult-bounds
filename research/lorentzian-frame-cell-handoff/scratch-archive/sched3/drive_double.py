import json, sys, subprocess, re, time, os
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
sys.path.insert(0, '../sched2')
from genprice import price
from splitp import slots
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
cache = {}
def pr(sl):
    if sl not in cache:
        c, d = price(tuned, 111, 8, 439, 9, 4, list(sl)); cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
wk, nw = int(sys.argv[1]), int(sys.argv[2])
rows = json.load(open('../sched2/splitlist_double.json'))
byseq = {}
for v, sq, sp, sl in rows: byseq.setdefault(tuple(sq), []).append((v, sp))
seqs = sorted(byseq.items(), key=lambda kv: -max(x[0] for x in kv[1]))
env = dict(os.environ, PERTIME='2')
for i, (sq, L) in enumerate(seqs):
    if i % nw != wk: continue
    ev = sorted({tuple(e) for _, sp in L for e in sp}); maxs = max(len(sp) for _, sp in L)
    args = ['./splitc5', '4', '9', str(maxs)] + [str(x) for x in sq] + [str(len(ev))] + [str(x) for e in ev for x in e]
    t = time.time()
    try: out = subprocess.run(args, capture_output=True, text=True, timeout=3600, env=env).stdout.strip()
    except subprocess.TimeoutExpired: print('TIMEOUT', list(sq), flush=True); continue
    if not out.startswith('FEASIBLE'):
        print('none %+.3f%%' % max(x[0] for x in L), list(sq), '%.0fs' % (time.time() - t), flush=True); continue
    best = None
    for s_ in re.findall(r'\[([^\]]*)\]', out):
        sp = tuple((int(a), int(b)) for a, b in re.findall(r'\((\d),(\d)\)', s_))
        sl = slots(list(sq), sp); p = pr(sl)
        if best is None or p > best[0]: best = (p, sp, sl)
    print('FEASIBLE %+.3f%%' % best[0], list(sq), best[1], best[2], '%.0fs' % (time.time() - t), flush=True)
