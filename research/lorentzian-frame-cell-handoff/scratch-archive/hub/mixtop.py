# Mixed tops: R(t) covered by one plane section H (rank 9) and two rank-8 frames F = span(t,u,v)-perp (users = lines of W).
# Count covers by (H, F2, F3) and by (F1, F2, F3) [the latter must fail if kappa8 >= 4].
import sys, itertools, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
tname = sys.argv[1]
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]
def perpm(ls):
    m = (1 << V) - 1
    for u in ls: m &= g.HYP[u]
    return m
cand = [u for u in range(V) if u != t and abs(g.G[t, u]) <= 1]
# rank-8 frames F = W-perp with W = span(t,u,v) of rank 3 (closed line sets); key by line set
F8 = {}
for u, v in itertools.combinations(cand, 2):
    if np.linalg.matrix_rank(g.L[[t, u, v]].astype(float)) != 3: continue
    m = perpm([t, u, v]) & Rt
    if m in F8: continue
    if m == 0 or dim(m) != 8: continue
    users = [w for w in range(V) if all(abs(g.G[w, h]) < 0.5 for h in bits(m))]
    F8[m] = len(users)
H9 = {}
for u in cand:
    m = perpm([t, u]) & Rt
    if m and dim(m) == 9: H9.setdefault(m, u)
print(tname, '| rank-8 closed frames in t-perp:', len(F8), '| users dist', sorted(collections.Counter(F8.values()).items()),
      '| plane sections:', len(H9), flush=True)
F8l = sorted(F8, key=lambda m: -bin(m).count('1'))
H9l = sorted(H9, key=lambda m: -bin(m).count('1'))
# (F,F,F) covers
c3 = 0
for a, b in itertools.combinations(F8l, 2):
    rest = Rt & ~(a | b)
    for c in F8l:
        if rest & ~c == 0: c3 += 1; break
print('  covers by 3 rank-8 closed frames (pairs that extend):', c3, flush=True)
# (H,F,F) covers
cnt = 0; ex = []; uhist = collections.Counter()
for h in H9l:
    rest = Rt & ~h
    for a in F8l:
        r2 = rest & ~a
        if r2 == 0: continue
        for b in F8l:
            if r2 & ~b == 0:
                cnt += 1; uhist[(F8[a], F8[b])] += 1
                if len(ex) < 5: ex.append((bin(h).count('1'), bin(a).count('1'), bin(b).count('1'), F8[a], F8[b]))
print('  covers by plane section + 2 rank-8 frames:', cnt, '| users of the rank-8 frames:', uhist.most_common(8), '| ex', ex, flush=True)
