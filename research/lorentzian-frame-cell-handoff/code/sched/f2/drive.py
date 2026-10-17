"""Drive splitc3 over splitlist_K4.json (sequences with some positive (seq, splits) option); price every feasible
split set; print the best per sequence.  usage: drive.py worker nworkers"""
import json, sys, subprocess, re, time
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
rows = json.load(open('../sched2/splitlist_K4_touch2.json'))
for i, (v, sq, L) in enumerate(rows):
    if i % nw != wk: continue
    ev = sorted({tuple(e) for o in L for e in o[1]})
    maxs = max(len(o[1]) for o in L)
    args = ['./splitc4', '4', '9', str(maxs)] + [str(x) for x in sq] + [str(len(ev))] + [str(x) for e in ev for x in e]
    t = time.time()
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=1800).stdout.strip()
    except subprocess.TimeoutExpired:
        print('TIMEOUT', sq, flush=True); continue
    if not out.startswith('FEASIBLE'):
        print('none %+.3f%%' % v, sq, 'maxs', maxs, 'events', len(ev), '%.0fs' % (time.time() - t), flush=True); continue
    best = None
    for s_ in re.findall(r'\[([^\]]*)\]', out):
        sp = tuple((int(a), int(b)) for a, b in re.findall(r'\((\d),(\d)\)', s_))
        sl = slots(sq, sp); p = pr(sl)
        if best is None or p > best[0]: best = (p, sp, sl)
    print('FEASIBLE %+.3f%%' % best[0], sq, best[1], best[2], 'potential %+.3f%%' % v, '%.0fs' % (time.time() - t), flush=True)
