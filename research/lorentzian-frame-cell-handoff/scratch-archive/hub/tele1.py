# Telescoping A3 tops: T(ijk) collectors 1,2 take N(A3-perp) then N(Q1-perp), N(Q2-perp).  A triangle section
# Q = {T(ab x), T(ab y), P(xy)} is taken by its two T users (each arriving with N(A3-perp) of its own A3) and the P user
# contributes c = N(Q-perp) + N(A3-perp) + N(A3'-perp).  Check rank(c) and whether 3 contributions of P(xy) can sum to R(P(xy)).
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
P, T = g.P, g.T
def perp(ls):
    m = (1 << V) - 1
    for u in ls: m &= g.HYP[u]
    return m
def A3(a, b, x, y, z):     # T(ab.) on {x,y,z} + P on {x,y,z}
    return [T(a, b, x), T(a, b, y), T(a, b, z), P(x, y), P(x, z), P(y, z)]
def rk(m): return dim(m) if m else 0
x, y = 2, 3
R = g.HYP[P(x, y)]
others = [p for p in range(11) if p not in (x, y)]
opts = []      # per pair ab: list of (c, rank, m, m')
for a, b in itertools.combinations(others, 2):
    Q = [T(a, b, x), T(a, b, y), P(x, y)]
    Qp = perp(Q)
    rest = [p for p in others if p not in (a, b)]
    for m in rest:
        for m2 in rest:
            if m2 == m: continue
            c = Qp ^ perp(A3(a, b, x, y, m)) ^ perp(A3(a, b, y, x, m2))
            opts.append(((a, b), m, m2, c, rk(c), bin(c).count('1')))
from collections import Counter
print('triangle sections through P(2,3):', len(set(o[0] for o in opts)), '| options', len(opts))
print('rank of contributor piece c:', Counter(o[4] for o in opts), '| sizes', Counter(o[5] for o in opts).most_common(5))
# can 3 contributions (distinct pairs ab) sum to R(P(xy))?
byab = {}
for o in opts: byab.setdefault(o[0], []).append(o)
hits = 0; tried = 0
abs_ = list(byab)
for trip in itertools.combinations(abs_, 3):
    for o1 in byab[trip[0]]:
        for o2 in byab[trip[1]]:
            s12 = o1[3] ^ o2[3]
            need = s12 ^ R
            for o3 in byab[trip[2]]:
                tried += 1
                if o3[3] == need: hits += 1; print('HIT', o1[:3], o2[:3], o3[:3])
print('triples tried', tried, 'hits', hits)
