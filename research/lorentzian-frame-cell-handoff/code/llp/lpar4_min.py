"""Validation + minimum defect of 4-section parity combos through t.  (1) recount the known 3-section defect-1 tops
with the same numpy machinery (pair xor ^ single section ^ R); (2) global minimum |D| over 4 distinct sections."""
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
def words(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(4)]
for kind in ('P', 'T'):
    t = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    Sm = [pm(p) for p in pl]
    S = np.array([words(x) for x in Sm], dtype=np.uint64)
    pairs = list(itertools.combinations(range(len(pl)), 2))
    X = np.array([words(Sm[i] ^ Sm[j]) for i, j in pairs], dtype=np.uint64)
    Rw = np.array(words(R), dtype=np.uint64)
    # (1) 3-section defect-1 count
    n3 = 0
    for a, (i, j) in enumerate(pairs):
        cnt = np.bitwise_count(S ^ X[a] ^ Rw).sum(axis=1)
        n3 += sum(1 for k in np.nonzero(cnt == 1)[0] if k > j)
    # (2) min defect over 4 distinct sections
    best = 999; hist = collections.Counter()
    for a, (i, j) in enumerate(pairs):
        cnt = np.bitwise_count(X[a + 1:] ^ X[a] ^ Rw).sum(axis=1)
        for b in np.nonzero(cnt <= 60)[0]:
            k, l = pairs[a + 1 + int(b)]
            if len({i, j, k, l}) == 4: hist[int(cnt[b])] += 1
        m = int(cnt.min()) if len(cnt) else 999
        best = min(best, m)
    print(kind, 'planes', len(pl), '3-section defect-1 tops', n3, '| 4-section defect histogram (<=12, counted per pair order):', sorted(hist.items())[:6], flush=True)
