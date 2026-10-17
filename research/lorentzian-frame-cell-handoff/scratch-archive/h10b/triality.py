"""I_{11,1}: R(P(bc)) = E8(W) (lines on W = [11] minus {b,c}, degenerate) + 9 lines T(bck).  Triality check: does E8(W)
contain three nondegenerate D8 flats pairwise meeting in one common D4+D4 (24 lines), giving an odd cover (each of
the 120 lines covered once or three times)?  Then tot(E8(W)) = sum of 3 D8 totals instead of the apex 9."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
b, c = 9, 10
W = set(range(11)) - {b, c}
E = [l for l in range(V) if set(g.supp[l]) <= W]
print('E8(W) lines', len(E))
Eset = set(E)
# D4 subsystems inside E8(W): closed rank-4 flats with 12 lines, Gram nondegenerate
def flat(mask_lines):
    cm, r = g.closure(sum(1 << l for l in mask_lines)); return cm, r
orth = (G == 0)
# enumerate D4s via orthogonal 4-frames inside E: closure has 12 lines rank 4
d4s = set()
Elist = E
for a in Elist:
    for bb in Elist:
        if bb <= a or not orth[a, bb]: continue
        for cc in Elist:
            if cc <= bb or not (orth[a, cc] and orth[bb, cc]): continue
            for dd in Elist:
                if dd <= cc or not (orth[a, dd] and orth[bb, dd] and orth[cc, dd]): continue
                cm, r = flat([a, bb, cc, dd])
                lines = [l for l in range(V) if cm >> l & 1]
                if r == 4 and len(lines) == 12 and set(lines) <= Eset: d4s.add(cm)
d4s = list(d4s); print('D4 flats in E8(W):', len(d4s))
perp = lambda m: [l for l in E if all(G[l, x] == 0 for x in range(V) if m >> x & 1)]
found = 0
for m1 in d4s:
    P = perp(m1)
    cm2, r2 = flat(P)
    L2 = [l for l in range(V) if cm2 >> l & 1]
    if not (r2 == 4 and len(L2) == 12 and set(L2) <= Eset): continue
    base = m1 | cm2   # D4 + D4'
    rest = [l for l in E if not base >> l & 1]
    # D8 flats containing base: closure of base + one more line
    d8 = set()
    for l in rest:
        cm, r = flat(g.bits(base) + [l])
        lines = [x for x in range(V) if cm >> x & 1]
        if r == 8 and set(lines) <= Eset: d8.add(cm)
    d8 = list(d8)
    for A, B, C in itertools.combinations(d8, 3):
        cnt = np.zeros(V, int)
        for M in (A, B, C):
            for x in g.bits(M): cnt[x] += 1
        if all(cnt[x] % 2 == 1 for x in E) and all(cnt[x] == 0 for x in range(V) if x not in Eset):
            sizes = [bin(M).count('1') for M in (A, B, C)]
            nd = [abs(np.linalg.det(np.array([[G[i, j] for j in g.bits(M)[:0]] for i in []]) if False else 1)) for M in (A, B, C)]
            print('triality cover found: D8 sizes', sizes, 'D4+D4 lines', bin(base).count('1')); found += 1
            break
    if found: break
print('found' if found else 'none')
