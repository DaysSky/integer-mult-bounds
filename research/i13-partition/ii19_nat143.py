"""nat143: THE SMALL-PUNCTURE SCAN - the sweet spot between the intact sharing (rho~3.5)
and the puncture's dim-7 gift (cst=63).

For j = 1..12 (a few puncture-sets per j): (1) the B0 rank; (2) the rowspace
elements' LIVE-support-dims (the min + the counts); (3) the cst-floor (the min sum of
support-dims over the row-spanning gather families, correctly via the SPAN condition);
(4) the price model at (v=120-j, rho, cst-floor, the E8-ish hist).
"""
import json, itertools, random
import numpy as np
from collections import Counter

S = json.load(open('ii19_nat69_spec.json'))
LALL = [tuple(int(c) for c in l) for l in S['lines']]
V120 = len(LALL)
L120 = np.array(LALL, float)


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


def support_dim(mask, Larr):
    idx = [i for i in range(len(Larr)) if (mask >> i) & 1]
    if not idx:
        return 0
    return int(np.linalg.matrix_rank(np.array([Larr[i] for i in idx], float)))


def cst_floor(basis_masks, Larr, B0set, max_m=20):
    """min sum of support-dims over families (size<=max_m) whose GF(2) SPAN
    contains every B0 row. Greedy on span-growth."""
    elems = {0}
    for b in basis_masks:
        elems |= {x ^ b for x in elems}
    edims = {}
    for e in elems:
        if e:
            edims[e] = support_dim(e, Larr)
    chosen = []
    span = {0}
    total = 0
    B0list = list(B0set)
    remaining = set(B0list)
    while remaining and len(chosen) < max_m:
        best, bg = None, -1
        for e, d in edims.items():
            if d == 0:
                continue
            newspan = span | {x ^ e for x in span}
            cov = sum(1 for nm in remaining if nm in newspan)
            g = cov / d
            if g > bg:
                best, bg = e, g
        if best is None or bg <= 0:
            return None
        span |= {x ^ best for x in span}
        remaining -= {nm for nm in remaining if nm in span}
        chosen.append(best)
        total += edims[best]
    if remaining:
        return None
    return total, len(chosen)


# the W-solve feasibility note: the family must ALSO be legal gathers (the scatter:
# every target = the XOR of a subset): the span-condition is the necessary core.

print('j    v    rank  min-sup-dim  sup-dim census           cst-floor      ')
rng = random.Random(11)
results = {}
for j in (1, 2, 3, 4, 6, 8, 9, 12):
    for trial in range(2 if j <= 4 else 1):
        rem = set(rng.sample(range(V120), j))
        lv = [i for i in range(V120) if i not in rem]
        L = np.array([LALL[i] for i in lv], float)
        n = len(lv)
        G = L @ L.T
        B0 = []
        for t in range(n):
            m = 1 << t
            for q in range(n):
                if q != t and G[t, q] == 0:
                    m |= 1 << q
            B0.append(m)
        rows = [[(m >> i) & 1 for i in range(n)] for m in B0]
        rank = gf2_rank(rows)
        bas_masks = []
        bas_rows = []
        for m in B0:
            cand = bas_rows + [[(m >> i) & 1 for i in range(n)]]
            if gf2_rank(cand) > len(bas_rows):
                bas_rows = cand
                bas_masks.append(m)
        # the elements' support-dims census (sampled: the 511-ish elements)
        elems = {0}
        for b in bas_masks:
            elems |= {x ^ b for x in elems}
        sd = Counter()
        for e in elems:
            if e:
                sd[support_dim(e, L)] += 1
        cf = cst_floor(bas_masks, L, set(B0))
        print('%-4d %-4d %-5d %-12s %-24s %s' % (j, n, rank,
              min(sd) if sd else '-', dict(sorted(sd.items())), cf), flush=True)
        results.setdefault(j, []).append((n, rank, cf, dict(sd)))
json.dump({str(j): v for j, v in results.items()}, open('ii19_nat143_scan.json', 'wt'), default=str)
print('SAVED ii19_nat143_scan.json')
