import json, sys, subprocess, re, time, os
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
sys.path.insert(0, '../sched2')
from genprice import price

K4, S9 = 4, 9
def slots(sq, sp):
    out = []
    for r in range(K4):
        actv = [j for j in range(S9) if sq[j] == r]; lv = 0
        cuts = sorted(b for (q, b) in sp if q == r)
        for j in actv + [S9]:
            if j > lv:
                pts = [lv] + [x for x in cuts if lv < x < j] + [j]
                out += [(pts[i + 1] - pts[i]) * 7 for i in range(len(pts) - 1)]
            lv = j + 1
    return tuple(sorted(out, reverse=True))
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
cache = {}
def pr(sl):
    if sl not in cache:
        c, d = price(tuned, 111, 8, 439, 9, 4, list(sl)); cache[sl] = float((c / ref - 1) * 100) if c else -999
    return cache[sl]
wk, nw = int(sys.argv[1]), int(sys.argv[2])
rows = json.load(open('../sched2/splitlist_passive_iv.json'))
byseq = {}
for v, sq, sp, sl in rows: byseq.setdefault(tuple(sq), []).append((v, sp))
seqs = sorted(byseq.items(), key=lambda kv: -max(x[0] for x in kv[1]))
import ast
done = set()
for line in open('dp_round1.log'):
    if line.startswith('none'):
        done.add(tuple(ast.literal_eval(line[line.index('['):line.index(']') + 1])))
seqs = [kv for kv in seqs if kv[0] not in done]
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
