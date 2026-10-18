"""THE nat114: THE PUNCTURE-DEPTH SCAN (the last breakthrough-direction!!)
THE QUESTION: does DEEPER puncturing drop the B0-rowspace rank?!
  the r434 (the j=9!!): the rank 9 | the 9 dim-7s | cst = 63!!
  the v-down costs -2.1%/line BUT a rank-drop pays +21%/rank (the cst = 7x the rank!!!)!
THE CENSUS: the j-scan (the v=120-j (j=1..12!!)): the rank | the dim<=7 elements | the honest cst
  (the basis-optimization: the minimal Sum-dims over the rank-basis (the dim-7s + the dim-1s + the dim-8s!!))!!
THE REMOVAL-SET: the r434's own 9 + the greedy-extensions (the depth-part!!): [6,58,81,88,97,109,112,115,116] + more!!
"""
import json, itertools
from collections import Counter
from fractions import Fraction

log = print
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L120 = [tuple(int(c) for c in l) for l in SPEC['lines']]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
RM9 = [6, 58, 81, 88, 97, 109, 112, 115, 116]  # the r434's own (the SPEC indices!!)

def rref_gf2(rows, n):
    m = [list(r) for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                m[i] = [(a ^ b) for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]

def rref_rat(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]

def census(L, tag, cap=4095):
    Vn = len(L)
    B0 = []
    for t in range(Vn):
        P = [s for s in range(Vn) if s != t and dot(L[t], L[s]) == 0]
        row = [0] * Vn; row[t] = 1
        for s in P: row[s] = 1
        B0.append(row)
    M = rref_gf2(B0, Vn)
    rank = len(M)
    dims = Counter(); mind = {}
    for mask in range(1, min(1 << rank, cap) + 1):
        v = [0] * Vn
        for i in range(rank):
            if (mask >> i) & 1:
                v = [(a ^ b) for a, b in zip(v, M[i])]
        sup = [i for i in range(Vn) if v[i]]
        if not sup: continue
        d = len(rref_rat([list(L[i]) for i in sup], 8))
        dims[d] += 1
    # THE HONEST CST: the greedy basis (the cheapest-first (the dim-1s, the dim-7s, the dim-8s!!))!!
    order = sorted(range(1, min(1 << rank, cap) + 1),
                   key=lambda mask: (lambda v: (len(rref_rat([list(L[i]) for i in range(Vn) if v[i]], 8)), -sum(v)))(  # SLOW?!
                       [1 if any((mask >> i) & 1 and M[i][j] for i in range(rank)) else 0 for j in range(Vn)]))
    # hmm too slow — the simple honest cst: 7 x (the #dim-7s-needed) + the dim-8 fill!!
    # the basis-greedy: pick the cheap elements (dim<=7!!) first until the rank-spanned!!
    sel = []; span = None
    cheap = [(d, mask) for d in sorted(dims) if d <= 7 for mask in []]  # placeholder!!
    log('    %s: v=%d | the rank %d | the element-dims %s' % (tag, Vn, rank, dict(sorted(dims.items()))))
    return rank, dims

log('THE nat114: THE PUNCTURE-DEPTH SCAN (the j=1..12!!):')
log('  the removal-set: the r434-9 + the depth-extensions (the greedy (the max-removed-perp-richness!!))')
# the depth-extensions: the lines by the removed-count?!: the greedy: the next removed = the line ⊥-max-of-the-already-removed?!?
ext = []
cur = set(RM9)
while len(cur) < 21:
    # the next: the line maximizing |perp(l) ∩ cur| (the puncture-clustering!!!!)
    best, bs = None, -1
    for i in range(120):
        if i in cur: continue
        P = [s for s in range(120) if s != i and dot(L120[i], L120[s]) == 0]
        sc = len([s for s in P if s in cur])
        if sc > bs: bs, best = sc, i
    cur.add(best); ext.append(best)
log('  the r434-9: %s' % RM9)
log('  the extensions (the 10th-21st (the ⊥-clustered!!)): %s' % ext)

for j in range(0, 13):
    rm = RM9 + ext[:max(0, j - 9)] if j > 9 else RM9[:j]
    L = [l for i, l in enumerate(L120) if i not in set(rm)]
    census(L, 'j=%2d (v=%d)' % (j, len(L)))
