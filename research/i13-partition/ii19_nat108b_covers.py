"""All triples of hyperplanes of l-perp (7-dim, holding the 63 lines of an E7) covering the 63 lines; WLOG
line-spanned hyperplanes.  Reports the covers by section sizes and whether every cover is a D4-frame triple
(the three sections are the perps of three roots x1, x2, x3 with {l, x1, x2, x3} a D4-type 4-frame).
Also the best coverage by 2 sections and by non-frame triples (the dim-1 pickup demand if a line had fewer copies)."""
import json, sys
import numpy as np
from collections import Counter
S = json.load(open('ii19_nat69_spec.json')); L = np.array(S['lines'], float); V = len(L); G = L @ L.T
l0 = 0
P = [j for j in range(V) if j != l0 and G[l0, j] == 0]
E = L[P]
def closure(ks):
    A = E[list(ks)]; u, s, vt = np.linalg.svd(A); r = int((s > 1e-9).sum()); Q = vt[:r]
    res = E - (E @ Q.T) @ Q; m = 0
    for i in np.nonzero(np.abs(res).max(axis=1) < 1e-9)[0]: m |= 1 << int(i)
    return m, r
bits = lambda m: [i for i in range(63) if (m >> i) & 1]
level = {closure([i])[0] for i in range(63)}
for dim in range(2, 7):
    nxt = set()
    for m in level:
        bs = bits(m)
        for x in range(63):
            if not (m >> x) & 1:
                mm, r = closure(bs + [x])
                if r == dim: nxt.add(mm)
    level = nxt
H = np.array(sorted(level), dtype=np.uint64)
sz = np.bitwise_count(H).astype(int)
print('hyperplanes', len(H), dict(sorted(Counter(sz.tolist()).items())), flush=True)
FULL = np.uint64((1 << 63) - 1)
rootsec = {}
for x in P:
    m = 0
    for i, t in enumerate(P):
        if t != x and G[t, x] == 0: m |= 1 << i
    rootsec[m] = x
def is_frame(trip):
    xs = [rootsec.get(m) for m in trip]
    if any(x is None for x in xs): return False
    if any(G[xs[i], xs[j]] for i in range(3) for j in range(i + 1, 3)): return False
    A = L[[l0] + xs]; Q = np.linalg.svd(A)[2][:4]
    return int((np.abs(L - (L @ Q.T) @ Q).max(axis=1) < 1e-9).sum()) == 12
covers = Counter(); nonframe = Counter(); best2 = 0; best3_nonframe = 0
for a in range(len(H)):
    U = H[a] | H
    u2 = np.bitwise_count(U).astype(int)
    best2 = max(best2, int(u2.max()))
    need = FULL & ~U
    cand = np.nonzero(np.bitwise_count(need).astype(int) <= sz.max())[0]
    cand = cand[cand >= a]
    for b in cand:
        nb = need[b]
        U3 = np.bitwise_count(H & nb).astype(int)
        cs = np.nonzero(U3 == np.bitwise_count(nb))[0]
        cs = cs[cs >= b]
        for c in cs:
            trip = [int(H[a]), int(H[b]), int(H[c])]
            key = tuple(sorted((int(sz[a]), int(sz[b]), int(sz[c]))))
            covers[key] += 1
            if not is_frame(trip): nonframe[key] += 1
print('best coverage by 2 sections: %d of 63' % best2)
print('covering triples by section sizes:', dict(covers))
print('covering triples that are NOT D4-frame triples:', dict(nonframe))
