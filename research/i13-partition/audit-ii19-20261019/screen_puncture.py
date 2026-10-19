"""Local search over E8 puncture sets near P111: is there a set with decoder cost per line x <= P111's 63/111
and better reach retention r2 (or the same r2 and lower x)?  Exact star cost of B0 (min-cost basis)."""
import json, os, random, sys
import numpy as np
from screen_reach import lines_of, e8_roots2, frame_cost, gf2_basis
from _common import I13
E8 = np.array(lines_of(e8_roots2()), dtype=np.int64); F = np.eye(8, dtype=np.int64)
G = E8 @ E8.T; ORTH = (G == 0); np.fill_diagonal(ORTH, False)
def evaluate(keep):
    keep = sorted(keep); L = E8[keep]; v = len(keep)
    O = ORTH[np.ix_(keep, keep)]
    perp = [sum(1 << int(j) for j in np.nonzero(O[i])[0]) for i in range(v)]
    B0 = [perp[i] | (1 << i) for i in range(v)]
    basis = gf2_basis(B0, v); cws = [0]
    for b in basis: cws = cws + [c ^ b for c in cws]
    Ll = L.tolist(); costs = sorted((frame_cost([Ll[i] for i in range(v) if (c >> i) & 1], F), c) for c in cws if c)
    piv, cst, n = {}, 0, 0
    for k, c in costs:
        x = c
        while x:
            p = x.bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; cst += k; n += 1; break
        if n == len(basis): break
    Of = O.astype(np.float32); M = Of @ Of; np.fill_diagonal(M, -1); psz = O.sum(1)
    return cst, cst / v, float((M.max(1) / np.maximum(psz, 1)).mean())
# P111's live set: map the r434 lines into this E8 coordinate system via the orthogonality pattern is not needed:
# search the puncture family directly from E8, seeded by random structured sets of 9.
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
best = {}
def record(tag, keep):
    cst, x, r2 = evaluate(keep)
    key = (len(keep))
    if key not in best or (x, -r2) < (best[key][0], -best[key][1]): best[key] = (x, r2, cst, tag)
    return cst, x, r2
v0 = len(E8)
print('E8 full', evaluate(range(v0)))
# greedy puncture: remove the line that most lowers x (ties -> highest r2), up to 18 removals
keep = set(range(v0))
for step in range(18):
    cands = rnd.sample(sorted(keep), 40)
    scored = []
    for c in cands:
        cst, x, r2 = evaluate(keep - {c}); scored.append((x, -r2, c, cst))
    scored.sort(); x, nr2, c, cst = scored[0]; keep.discard(c)
    print('v=%d  cst %d  x %.4f  r2 %.4f' % (len(keep), cst, x, -nr2), flush=True)
