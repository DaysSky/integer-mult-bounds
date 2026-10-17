"""Run the exhaustive F_2 split search (<= 3 splits, <= 1 per time) on the sequences of splitlist_K4.json, in order of
their best potential price; print every feasible split set with its slot multiset and price.
usage: runsplit.py worker nworkers"""
import json, sys, time, signal
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
from splitp import run, slots
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
wk, nw = int(sys.argv[1]), int(sys.argv[2])
rows = json.load(open('splitlist_K4.json'))
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM, h)
for i, (v, sq, L) in enumerate(rows):
    if i % nw != wk: continue
    maxs = max(len(o[1]) for o in L)
    t = time.time(); signal.alarm(600)
    try:
        res = run(sq, maxs)
        signal.alarm(0)
    except TO:
        print('TIMEOUT', sq, 'maxs', maxs, flush=True); continue
    if not res:
        print('none', '%+.3f%%' % v, sq, 'maxs', maxs, '%.0fs' % (time.time() - t), flush=True); continue
    best = []
    for sp in res:
        sl = slots(sq, sp)
        c, d = price(tuned, 111, 8, 439, 9, 4, list(sl))
        best.append((float((c / ref - 1) * 100) if c else -999, sp, sl))
    best.sort(reverse=True)
    print('FEASIBLE', sq, 'n', len(res), 'best %+.3f%%' % best[0][0], best[0][1], best[0][2], '%.0fs' % (time.time() - t), flush=True)
