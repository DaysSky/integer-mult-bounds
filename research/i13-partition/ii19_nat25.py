"""THE PLANE CENSUS (ii19_nat25.py) — the shared-cell rebuild design's FIRST measurement.

The universal wall (nat24): in both existing architectures the build-pair cells are single-pair
(s1's own cell != F2 for 0/137), because s1's own cell is another helper's F2 and cells host one
pair.  The shared-cell grammar needs a dim-2 plane C hosting TWO pairs: h = (s1, s2) and
h' = (s1', s1) with F2(h) = C1(s1) = C — i.e. a plane containing >= 3 of the 121 lines
({s1', s1, s2}), OR the repeated-pair option (two helpers with the same value on one 2-line cell).

Measure: for every pair (a, b) of the word4's 121 lines, the plane span(a, b) and how many of the
121 lines lie in it.  The multiplicity histogram decides which grammar the geometry permits.
"""
import json, os, sys
from collections import Counter, defaultdict
from fractions import Fraction

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
lines = w['lines']

def rank2(a, b):
    """rref basis (as tuples) of span(a, b)."""
    m = [list(x) for x in (a, b)]
    r = 0
    for c in range(H):
        p = next((i for i in range(r, 2) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        o = 1 if r == 0 else 0
        if m[o][c] != 0:
            f = m[o][c]; m[o] = [x - f * y for x, y in zip(m[o], m[r])]
        r += 1
        if r == 2: break
    return [tuple(x) for x in m[:r]]

def in_plane(basis, c):
    """is line c in the span of basis (len <= 2 rows, rref)?"""
    m = [list(x) for x in basis] + [list(c)]
    r = 0
    for col in range(H):
        p = next((i for i in range(r, 3) if m[i][col] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        iv = 1 / m[r][col]; m[r] = [x * iv for x in m[r]]
        for i in range(3):
            if i != r and m[i][col] != 0:
                f = m[i][col]; m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r <= len(basis)

planes = {}
hist = Counter()
for a in range(V):
    for b in range(a + 1, V):
        basis = rank2(lines[a], lines[b])
        if len(basis) < 2: continue
        key = tuple(basis)
        if key not in planes:
            mem = [c for c in range(V) if c not in (a, b) and in_plane(basis, lines[c])]
            planes[key] = (a, b, mem)
            hist[len(mem) + 2] += 1
log('distinct planes spanned by line pairs: %d' % len(planes))
log('plane line-multiplicity hist: %s' % dict(sorted(hist.items())))
big = [(k, v) for k, v in planes.items() if len(v[2]) + 2 >= 3]
log('planes with >= 3 lines: %d' % len(big))
for key, (a, b, mem) in big[:12]:
    log('  plane %s: lines %d %d + %s' % (key[0][:4], a, b, mem))
