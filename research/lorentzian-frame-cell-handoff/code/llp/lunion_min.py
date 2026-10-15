"""Minimum number of uncovered lines of R(t) by unions of 3 and of 4 plane sections through t (exhaustive, numpy).
Reports the histogram of small uncovered counts (0..3) and plane types of exact (0) covers."""
import itertools, collections
import numpy as np
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
def ptype(p):
    L = bits(p); ks = ''.join(sorted(KIND[x] for x in L))
    if len(L) == 3: return ks
    a_, b_ = L
    if ks == 'PT':
        P_ = a_ if KIND[a_] == 'P' else b_; T_ = b_ if P_ == a_ else a_
        return 'PTi' if set(SUPP[P_]) <= set(SUPP[T_]) else 'PTd'
    if ks == 'TT': return 'TT' if G[a_][b_] == 0 else 'TTs'
    return ks
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(4)]
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t)); ty = [ptype(p) for p in pl]
    Sm = [pm(p) for p in pl]
    U = np.array([words(R & ~x) for x in Sm], dtype=np.uint64)     # uncovered-by-section masks (complements in R)
    pairs = list(itertools.combinations(range(len(pl)), 2))
    UP = np.array([words((R & ~Sm[i]) & (R & ~Sm[j])) for i, j in pairs], dtype=np.uint64)
    h3 = collections.Counter(); ex3 = collections.Counter()
    for a, (i, j) in enumerate(pairs):
        cnt = np.bitwise_count(U & UP[a]).sum(axis=1)
        for k in np.nonzero(cnt <= 3)[0]:
            if k > j: h3[int(cnt[k])] += 1; ex3[(int(cnt[k]), tuple(sorted((ty[i], ty[j], ty[k]))))] += 1
    h4 = collections.Counter(); ex4 = collections.Counter()
    for a, (i, j) in enumerate(pairs):
        cnt = np.bitwise_count(UP[a + 1:] & UP[a]).sum(axis=1)
        for b in np.nonzero(cnt <= 1)[0]:
            k, l = pairs[a + 1 + int(b)]
            if len({i, j, k, l}) == 4 and (i, j) < (k, l):
                h4[int(cnt[b])] += 1
                if cnt[b] == 0: ex4[tuple(sorted((ty[i], ty[j], ty[k], ty[l])))] += 1
    print(kind, '3-section union: uncovered histogram', sorted(h3.items()), flush=True)
    for k_, v in sorted(ex3.items())[:12]: print('    ', k_, v)
    print(kind, '4-section union (counted per pair split, /3 for distinct quadruples): uncovered histogram', sorted(h4.items()), flush=True)
    for k_, v in sorted(ex4.items(), key=lambda kv: -kv[1])[:10]: print('    exact 4-cover types', k_, v)
