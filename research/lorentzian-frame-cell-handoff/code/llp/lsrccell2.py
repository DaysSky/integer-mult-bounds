"""How close can a two-cell source structure get?  For line t and cells {t,f1}, {t,f2} (f orthogonal to t): max
coverage of R(t) by F1,F2 (rank-3 frames through {t,f1}) and F3,F4 (through {t,f2}).  Per cell, all frame pairs are
enumerated and the top K unions kept; cell pairs over Stab(t)-orbit representatives of f1 and all f2.  Reports the
minimum number of uncovered lines found (heuristic upper bound on the true minimum when K is finite).
usage: lsrccell2.py K"""
import sys, itertools, collections
import numpy as np
from lgeo import *
K = int(sys.argv[1])
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(4)]
for kind, t in (('P', IDX[('P', (0, 1))]), ('T', IDX[('T', (0, 1, 2))])):
    R = HYP[t]; Rl = bits(R)
    cellbest = {}
    for f in Rl:
        frs = set()
        for x in range(V):
            if x in (t, f): continue
            m = (1 << t) | (1 << f) | (1 << x)
            if rank(m) != 3: continue
            frs.add(pp(m))
        P = [pm(F) & R for F in frs]
        unions = sorted(set(a | b for a, b in itertools.combinations(P, 2)), key=pc, reverse=True)[:K]
        cellbest[f] = unions
    # f1 orbit representatives under Stab(t): use canonical form of (t, f)
    reps = {}
    for f in Rl:
        cf = canon((1 << t, 1 << f))[0]
        reps.setdefault(cf, f)
    best = 0
    for f1 in reps.values():
        U1 = cellbest[f1]
        for f2 in Rl:
            if f2 == f1: continue
            U2 = cellbest[f2]
            m = max(pc(a | b) for a in U1 for b in U2)
            best = max(best, m)
    print(kind, '|R| =', pc(R), '| best two-cell coverage (top-%d pairs per cell):' % K, best, '-> uncovered', pc(R) - best, flush=True)
