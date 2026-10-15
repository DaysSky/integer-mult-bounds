"""For t = P line 0 and T line 100: over all pairs of plane sections through t (users include t), the minimum number
of uncovered lines of R(t); and whether the uncovered set fits in one rank-<=2 frame (line / plane) inside t-perp."""
import pickle, itertools, collections
from lgeo import *
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    secs = [(p, pm(p)) for p in pl]
    best = collections.Counter(); bestm = 999; ex = None
    for (p1, s1), (p2, s2) in itertools.combinations(secs, 2):
        unc = R & ~(s1 | s2)
        k = pc(unc)
        best[k] += 1
        if k < bestm: bestm = k; ex = (p1, p2, unc)
    print('target', 'P' if t < 55 else 'T', '|R|', pc(R), 'planes', len(pl), 'min uncovered by 2 sections', bestm,
          'distribution (smallest 6):', sorted(best.items())[:6])
    p1, p2, unc = ex
    print('   example uncovered lines', [(KIND[s], SUPP[s]) for s in bits(unc)], 'rank', rank(unc))
