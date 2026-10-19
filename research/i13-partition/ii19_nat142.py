"""nat142: THE LATTICE/DECODER CENSUS - the genuine breakthrough hunt.

For each candidate system: the B0-matrix (rows {t} u perp(t)), the GF(2)-rank,
and the cst-floor (the min sum of support-dims over the row-spanning gather families).
Candidates: (a) the r434's own puncture (v=111); (b) the alternative 9-punctures
(sampled); (c) the deeper punctures j=10..16; (d) D8; (e) B8.
"""
import json, itertools, random
import numpy as np
from collections import Counter

S = json.load(open('ii19_nat69_spec.json'))
LALL = [tuple(int(c) for c in l) for l in S['lines']]
V120 = len(LALL)
L120 = np.array(LALL, float)
G120 = L120 @ L120.T


def gf2_rank(rows):
    m = [list(r) for r in rows]
    rank = 0
    cols = len(m[0]) if m else 0
    for c in range(cols):
        piv = None
        for i in range(rank, len(m)):
            if m[i][c]:
                piv = i
                break
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        for i in range(len(m)):
            if i != rank and m[i][c]:
                m[i] = [(a ^ b) for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


def span_elems(basis, n):
    """all GF(2) combos of the basis rows -> bitmasks"""
    out = {0}
    for b in basis:
        out |= {x ^ b for x in out}
    return out


def support_dim(mask, Larr):
    """the rank (over Q) of the line-vectors in the mask"""
    idx = [i for i in range(len(Larr)) if (mask >> i) & 1]
    if not idx:
        return 0
    return int(np.linalg.matrix_rank(np.array([Larr[i] for i in idx], float)))


def cst_floor(basis, Larr, need_masks):
    """the min sum of support-dims over the gather families whose GF(2) span
    covers all the need_masks (the B0-rows). Enumerate the span's elements,
    greedily pick low-dim high-coverage."""
    elems = span_elems(basis, len(Larr))
    edims = {}
    for e in elems:
        if e:
            edims[e] = support_dim(e, Larr)
    # greedy: repeatedly pick the element maximizing (new coverage / dim)
    covered = set()
    total = 0
    k = 0
    while True:
        need = need_masks - covered
        if not need:
            break
        best, bs = None, 0
        for e, d in edims.items():
            if d == 0:
                continue
            cov = sum(1 for nm in need if (nm & e) == nm)
            s = cov / d
            if s > bs:
                best, bs = e, s
        if best is None:
            return None
        covered.update(nm for nm in need if (nm & best) == nm)
        total += edims[best]
        k += 1
    return total, k


def census(name, lines):
    n = len(lines)
    L = np.array(lines, float)
    G = L @ L.T
    # B0: the rows {t} u perp(t)  (bitmasks)
    B0 = []
    for t in range(n):
        m = 1 << t
        for j in range(n):
            if j != t and G[t, j] == 0:
                m |= 1 << j
        B0.append(m)
    # the GF(2) rank of the B0-rows: rank them as rows
    rows = [[(m >> i) & 1 for i in range(n)] for m in B0]
    rank = gf2_rank(rows)
    # a basis: the first rank independent rows -> as masks
    bas_rows = []
    bas_masks = []
    for m in B0:
        cand = bas_rows + [[(m >> i) & 1 for i in range(n)]]
        if gf2_rank(cand) > len(bas_rows):
            bas_rows = cand
            bas_masks.append(m)
    need = set(B0)
    cf = cst_floor(bas_masks, L, need)
    perps = int((G == 0).sum(axis=1).mean()) - 1
    print('%-28s v=%-4d perps~%-3d rank=%-3d cst-floor=%s' % (name, n, perps, rank, cf), flush=True)
    return rank, cf


# (a) the r434's own puncture
removed = {6, 58, 81, 88, 97, 109, 112, 115, 116}
live = [i for i in range(V120) if i not in removed]
census('r434 puncture (9)', [LALL[i] for i in live])

# (b) the alternative 9-punctures (random samples)
rng = random.Random(7)
for trial in range(8):
    rem = set(rng.sample(range(V120), 9))
    lv = [i for i in range(V120) if i not in rem]
    census('random puncture %s' % sorted(rem), [LALL[i] for i in lv])

# (c) the deeper punctures (the r434's + extra random)
for j in (2, 4, 8):
    rem = removed | set(rng.sample([i for i in range(V120) if i not in removed], j))
    lv = [i for i in range(V120) if i not in rem]
    census('r434 +%d deeper' % j, [LALL[i] for i in lv])

# (d) D8: the roots +-ei+-ej (norm 2), the lines = the pairs {r,-r}
d8 = []
for i in range(8):
    for j in range(i+1, 8):
        for s1 in (1, -1):
            for s2 in (1, -1):
                v8 = [0]*8
                v8[i] = s1
                v8[j] = s2
                if tuple(v8) not in [tuple(-np.array(x)) for x in d8]:
                    d8.append(v8)
census('D8 (112 roots)', d8)

# (e) B8: the D8 roots + the +-ei (norm 1)
b8 = list(d8)
for i in range(8):
    for s in (1, -1):
        v8 = [0]*8
        v8[i] = s
        if tuple(v8) not in [tuple(-np.array(x)) for x in b8]:
            b8.append(v8)
census('B8 (norm<=2 lines)', b8)
