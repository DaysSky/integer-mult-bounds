"""nat183: THE CORRECTED DEEPER-SHELL 241-LINE CENSUS.
The (x,a)-lattice, form x.x' + 2aa': the norm-2 lines (120 roots + special = 121)
+ THE NORM-4 DEEPER SHELL: the (root, 1)-class: 120 lines!!
The census: the perps, the B0-rank (with a CAP -- no 2^rank hang!), the cst-floor if small.
"""
from itertools import combinations, product
from collections import Counter
import numpy as np

# the E8 roots: 112 integer + 128 half-integer = 240 vectors -> 120 lines (verified!)
roots = []
for i in range(8):
    for j in range(i+1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v8 = [0.0]*8; v8[i] = float(si); v8[j] = float(sj)
                roots.append(v8)
for signs in product([1, -1], repeat=8):
    if signs.count(-1) % 2 == 0:
        roots.append([s*0.5 for s in signs])
assert len(roots) == 240
lines120 = []
seen = set()
for r in roots:
    t = tuple(r); neg = tuple(-x for x in r)
    if t in seen or neg in seen: continue
    seen.add(t); lines120.append(t)
assert len(lines120) == 120
print('the E8 lines: %d OK' % len(lines120), flush=True)

# the 241-line deeper-shell system
lines = [l + (0.0,) for l in lines120]        # the roots at a=0 (norm 2)
lines.append((0.0,)*8 + (1.0,))                # the special (norm 2)
lines += [l + (1.0,) for l in lines120]        # the deeper shell (root, 1): norm 4!!
V = len(lines)
print('THE DEEPER-SHELL SYSTEM: v=%d (121 + 120 norm-4!!)' % V, flush=True)

def ip(a, b):
    return sum(x*y for x, y in zip(a[:8], b[:8])) + 2*a[8]*b[8]

norms = Counter(int(ip(l, l)//2) for l in lines)
print('the norms (x/2): %s' % dict(sorted(norms.items())), flush=True)
M = np.array([list(l) for l in lines], dtype=float)
print('the span dim: %d' % np.linalg.matrix_rank(M), flush=True)

perp = [frozenset(j for j in range(V) if j != i and ip(lines[i], lines[j]) == 0) for i in range(V)]
pc = Counter(len(p) for p in perp)
print('the perp-counts: %s (the mean %.1f)' % (dict(sorted(pc.items())), sum(len(p) for p in perp)/V), flush=True)

# the B0-rows: {t} U perp(t) -- the GF(2) rank (THE DECISIVE!!)
B0 = []
for t in range(V):
    row = 1 << t
    for j in perp[t]: row |= 1 << j
    B0.append(row)
def gf2_rank(rows):
    rs = list(rows); rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rs)) if (rs[i] >> col) & 1), None)
        if piv is None: continue
        rs[rank], rs[piv] = rs[piv], rs[rank]
        for i in range(len(rs)):
            if i != rank and (rs[i] >> col) & 1: rs[i] ^= rs[rank]
        rank += 1
    return rank
rank = gf2_rank(B0)
print('THE DECODER RANK: %d (of v=%d)' % (rank, V), flush=True)
print('vs the 121: rank 9!! vs the 361: rank 241 (the kill!!)', flush=True)

if rank <= 24:
    # the rowspace + the support-dims + the greedy cst-floor
    cur = [0]
    for r in B0:
        cur = cur + [c ^ r for c in cur]
    elems = sorted(set(cur))[1:]
    print('the rowspace: %d elements' % len(elems), flush=True)
    def support_dim(mask):
        ls = [i for i in range(V) if (mask >> i) & 1]
        if not ls: return 0
        return int(np.linalg.matrix_rank(np.array([list(lines[i]) for i in ls], dtype=float)))
    supd = Counter(support_dim(e) for e in elems)
    print('THE SUPPORT-DIMS: %s' % dict(sorted(supd.items())), flush=True)
    need = set(B0); chosen = []; cur_span = [0]
    while need:
        best, bd = None, -1.0
        for e in elems:
            if e in chosen: continue
            new = sum(1 for nm in need if not any((c == nm) for c in cur_span) and (nm & e) == nm)
            d = support_dim(e)
            g = new/max(d, 1)
            if g > bd: bd, best = g, e
        if best is None: break
        chosen.append(best)
        cur_span = cur_span + [c ^ best for c in cur_span]
        need = {nm for nm in need if not any(c == nm for c in cur_span)}
    print('THE CST-FLOOR (the greedy): total %d with %d gathers' % (
        sum(support_dim(c) for c in chosen), len(chosen)), flush=True)
else:
    print('the rank > 24: the hyperbolic signature -- the rowspace/cst analysis skipped (the rank IS the verdict!!)', flush=True)
