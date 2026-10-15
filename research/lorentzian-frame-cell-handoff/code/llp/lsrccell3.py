"""RIGOROUS version of lsrccell2: proves an upper bound on the coverage of R(t) by two-cell source structures
(F1,F2 through cell {t,f1}; F3,F4 through {t,f2}).  Per cell all 2-frame unions are enumerated and sorted; for a cell
pair the maximum |U1 u U2| is searched over the top-K lists, and pairs outside them are bounded by
s_K(c1) + max|U(c2)| (and symmetrically), with K doubled until the bound is <= the threshold or K covers everything.
Reports the exact maximum coverage (so the exact minimum number of uncovered lines).  f1 over Stab(t)-orbit
representatives, f2 over all lines orthogonal to t.  usage: lsrccell3.py"""
import itertools
from lgeo import *
for kind, t in (('P', IDX[('P', (0, 1))]), ('T', IDX[('T', (0, 1, 2))])):
    R = HYP[t]; Rl = bits(R)
    U = {}
    for f in Rl:
        frs = set()
        for x in range(V):
            if x in (t, f): continue
            m = (1 << t) | (1 << f) | (1 << x)
            if rank(m) != 3: continue
            frs.add(pp(m))
        P = list(set(pm(F) & R for F in frs))
        un = sorted(set(a | b for a, b in itertools.combinations(P, 2)) | set(P), key=pc, reverse=True)
        U[f] = un
    reps = {}
    for f in Rl: reps.setdefault(canon((1 << t, 1 << f))[0], f)
    best_overall = 0
    for f1 in reps.values():
        for f2 in Rl:
            if f2 == f1: continue
            A, B = U[f1], U[f2]; K = 50
            while True:
                kA, kB = min(K, len(A)), min(K, len(B))
                best = max(pc(a | b) for a in A[:kA] for b in B[:kB])
                bound = 0
                if kA < len(A): bound = max(bound, pc(A[kA]) + pc(B[0]))
                if kB < len(B): bound = max(bound, pc(A[0]) + pc(B[kB]))
                if bound <= best: break
                K *= 2
            best_overall = max(best_overall, best)
    print(kind, '|R| =', pc(R), '| EXACT max two-cell coverage:', best_overall, '-> min uncovered', pc(R) - best_overall, flush=True)
