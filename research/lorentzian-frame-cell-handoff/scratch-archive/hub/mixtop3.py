# Union covers R(t) <= H1 u H2 u H3 by plane sections where H2, H3 can be shrunk to rank-8 subspaces:
# need a split of R - H1 into P2 <= H2, P3 <= H3 with rank(P2), rank(P3) <= 8 (lines in H2 n H3 - H1 assigned freely).
import sys, itertools, numpy as np, collections, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
tname = sys.argv[1]; t0 = time.time()
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]
def perpm(ls):
    m = (1 << V) - 1
    for u in ls: m &= g.HYP[u]
    return m
H9 = {}
for u in range(V):
    if u == t or abs(g.G[t, u]) > 1: continue
    m = perpm([t, u]) & Rt
    if m and dim(m) == 9 and m not in H9:
        H9[m] = sum(1 for w in range(V) if all(abs(g.G[w, h]) < 0.5 for h in bits(m)))
Hl = list(H9)
print(tname, 'plane sections', len(Hl), flush=True)
def rk(m): return dim(m) if m else 0
covers = 0; good = 0; ex = []; uh = collections.Counter()
for a, b, c in itertools.combinations(range(len(Hl)), 3):
    A, B, C = Hl[a], Hl[b], Hl[c]
    if (A | B | C) != Rt: continue
    covers += 1
    for (H1, H2, H3) in ((A, B, C), (B, A, C), (C, A, B)):
        rest = Rt & ~H1
        only2 = rest & H2 & ~H3; only3 = rest & H3 & ~H2; both = rest & H2 & H3
        if rk(only2) > 8 or rk(only3) > 8: continue
        # try: all shared to P2, or all to P3, or greedy
        ok = False
        for P2, P3 in ((only2 | both, only3), (only2, only3 | both)):
            if rk(P2) <= 8 and rk(P3) <= 8: ok = True; break
        if not ok:
            P2, P3 = only2, only3
            for u in bits(both):
                if rk(P2 | (1 << u)) <= 8: P2 |= 1 << u
                elif rk(P3 | (1 << u)) <= 8: P3 |= 1 << u
                else: break
            else: ok = True
        if ok:
            good += 1; uh[(H9[H1], H9[H2], H9[H3])] += 1
            if len(ex) < 5: ex.append((bin(H1).count('1'), bin(P2).count('1'), bin(P3).count('1'), H9[H1], H9[H2], H9[H3]))
print('  union covers by 3 plane sections:', covers, '| with two sections shrinkable to rank 8:', good,
      '| users (H1,H2,H3):', uh.most_common(8), '| ex', ex, '| %.0fs' % (time.time() - t0), flush=True)
