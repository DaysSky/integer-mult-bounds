"""THE nat112: THE 121-LINE CST-VERDICT CENSUS (the large breakthrough!!)
THE QUESTION: at v=121 (the ext120 + one raw-norm-8 line x (the 184 rich 42-perp candidates!!)):
  does the W-rowspace admit DIM-<=7-SUPPORTED gather patterns (the punctured-analog (cst ~63-70!!!))
  or are all nonzero elements dim-8 (the FULL-frames (cst = 8 x the gather-count (72-80!!)))?
THE MACHINERY (the nat69-style!!): the 121-line system L = L120 + [x]:
  - the form (the raw-dot/2 (the I/2!!): the SAME lattice (the positive-definite ✓✓!!
  - PERP(t) = {s : dot(t, s) = 0} (the 42/64 asymmetries!!)
  - B0[t] = {t} | PERP(t)  (the 42-64-line patterns!!!)
  - THE ROWSPACE: the GF(2)-span of {B0[t]}: the rank + THE ELEMENT-SPAN CENSUS
    (the minimal-line-span of each nonzero element (the dim-<=7 hunt!!!))
  - THE CST-VERDICT: the gather-family: the minimal Sum-dims (the nat88-style!!)
"""
import json, itertools
from collections import Counter
from fractions import Fraction
import numpy as np

log = print
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L120 = [tuple(int(c) for c in l) for l in SPEC['lines']]
V = 120

def dot(a, b): return sum(x * y for x, y in zip(a, b))

# (1) THE SHELL (the raw-norm-8, the 42-perp rich candidates!!)
shell = []
for a in range(8):
    for b in range(a + 1, 8):
        for sa in (2, -2):
            for sb in (2, -2):
                t = [0] * 8; t[a] = sa; t[b] = sb
                shell.append(tuple(t))
for pos in itertools.combinations(range(8), 5):
    rest = [i for i in range(8) if i not in pos]
    for s2 in (2, -2):
        for signs in itertools.product((1, -1), repeat=4):
            t = [0] * 8; t[rest[0]] = s2
            for i, s in zip(rest[1:], signs): t[i] = s
            shell.append(tuple(t))
for signs in itertools.product((1, -1), repeat=8):
    shell.append(tuple(signs))
cands = []
for x in sorted(set(shell)):
    first = next((c for c in x if c != 0), 0)
    if first < 0: continue
    pc = sum(1 for l in L120 if dot(x, l) == 0)
    if pc == 42: cands.append(x)
log('(1) THE RICH CANDIDATES (the 42-perps!!): %d' % len(cands))

# (2) THE 121-LINE STRUCTURE + THE CST-VERDICT per candidate!!
def rref_gf2(rows, n):
    m = [list(r) for r in rows]; r = 0; piv = []
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                m[i] = [(a ^ b) for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
    return m[:r], piv

def span_dims_census(B0rows, Vn, limit_elems=511):
    """the rowspace's elements' line-span-dims census (the dim-<=7 hunt!!)."""
    M, piv = rref_gf2(B0rows, Vn)
    rank = len(M)
    # the elements: the 2^rank combos (cap!!): the span-dim of each element's support!!
    dims = Counter()
    elems = []
    R = len(M)
    for mask in range(1, min(1 << R, limit_elems + 1)):
        v = [0] * Vn
        for i in range(R):
            if (mask >> i) & 1:
                v = [(a ^ b) for a, b in zip(v, M[i])]
        sup = [i for i in range(Vn) if v[i]]
        if not sup: continue
        # the span-dim: the rref over the lines (the Fractions!!)
        rr, _ = rref_rational([list(L[i]) for i in sup], 8)
        d = len(rr)
        dims[d] += 1
        elems.append((d, mask, len(sup)))
    return rank, dims

def rref_rational(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r], None

log('(2) THE 121-LINE CST-VERDICT (the first 12 candidates (the structure-scan!!)):')
best = None
for xi, x in enumerate(cands[:12]):
    L = L120 + [x]; Vn = 121
    # PERP + B0!!
    B0rows = []
    perp_sizes = Counter()
    for t in range(Vn):
        P = [s for s in range(Vn) if s != t and dot(L[t], L[s]) == 0]
        perp_sizes[len(P)] += 1
        row = [0] * Vn
        row[t] = 1
        for s in P: row[s] = 1
        B0rows.append(row)
    rank, dims = span_dims_census(B0rows, Vn)
    log('    cand %2d x=%-28s: the perps %s | the B0-rank %d | the element-dims %s' %
        (xi, str(x), dict(sorted(perp_sizes.items())), rank, dict(sorted(dims.items()))))
    d7 = sum(c for d, c in dims.items() if d <= 7)
    if best is None or d7 > best[0]:
        best = (d7, x, rank, dims)
log('')
log('THE BEST-SEEN: the dim<=7-supported rowspace elements: %d (x=%s)' % (best[0], str(best[1])))
log('THE VERDICT: %s' % ('THE DIM-7 GATHERS EXIST (the punctured-analog cst!!!)' if best[0] > 0 else 'NO dim<=7 elements: the FULL-frames (cst = 8 x gathers!!)'))
