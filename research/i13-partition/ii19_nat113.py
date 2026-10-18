"""THE nat113: THE PUNCTURED-EXTENDED (k, j)-FAMILY CENSUS (the large breakthrough!!)
THE MECHANISM (the r434's own!!): the system (the 120-k removed + the j raw-norm-8 extensions):
  the REMOVED lines' perps host the DIM-7 gathers (the cst = 7 x the gather-count!!!)
  vs the un-punctured (the FULL-frames (the 8 x!!)).
THE CENSUS: per (k, j): the v = 120 - k + j | the B0-rowspace rank | the dim<=7-supported elements
  (the cst-verdict!!) | the W-solve feasibility | THE PRICE at (v, 8, R, the cst-verdict!!).
THE CONTROL: the r434 (k=9, j=0!!): the removed-9 (read from its own line-list!!) -> the rank 9 + the dim-7s!!
"""
import json, itertools
from collections import Counter
from fractions import Fraction
import os, sys
import mpmath as mp
mp.mp.dps = 50
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price

log = print
SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
L120 = [tuple(int(c) for c in l) for l in SPEC['lines']]
def dot(a, b): return sum(x * y for x, y in zip(a, b))

# (0) THE r434's REMOVED-9 (the live-111 matched to the SPEC's 120 (the reversed-coords + the +-canonical!!))
W434 = json.load(open('ii19_pub2_p111-r434.json', 'rt'))
L434raw = W434['lines']
assert len(L434raw) == 111
def canon(c):
    t = tuple(int(x) for x in c)
    if next((x for x in t if x != 0), 1) < 0: t = tuple(-x for x in t)
    return t
def to_spec(c):
    """the hub's [2,0,...] (the e_0-first!!) -> the SPEC's [...,0,2] (the reversed!!)!!"""
    t = tuple(int(x) for x in c)[::-1]
    if next((x for x in t if x != 0), 1) < 0: t = tuple(-x for x in t)
    return t
set120c = {canon(l): i for i, l in enumerate(L120)}
L434 = [to_spec(l) for l in L434raw]
idx434 = [set120c[canon(l)] for l in L434]
removed = sorted(set(range(120)) - set(idx434))
log('(0) THE r434 REMOVED-9 (the SPEC indices!!): %s' % removed)
log('    the check: the live %d | the removed %d' % (len(idx434), len(removed)))

# (1) THE SHELL (the raw-norm-8, the 42-perp!!)
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
log('(1) THE 42-perp raw-norm-8 candidates: %d' % len(cands))

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

def system_census(L, tag):
    Vn = len(L)
    B0rows = []
    for t in range(Vn):
        P = [s for s in range(Vn) if s != t and dot(L[t], L[s]) == 0]
        row = [0] * Vn; row[t] = 1
        for s in P: row[s] = 1
        B0rows.append(row)
    M, piv = rref_gf2(B0rows, Vn)
    rank = len(M)
    # the dim<=7 hunt: the elements' span-dims (the full census (2^rank capped at 2047!!))
    dims = Counter(); d7pats = []
    R = len(M)
    for mask in range(1, min(1 << R, 2047) + 1):
        v = [0] * Vn
        for i in range(R):
            if (mask >> i) & 1:
                v = [(a ^ b) for a, b in zip(v, M[i])]
        sup = [i for i in range(Vn) if v[i]]
        if not sup: continue
        d = len(rref_rat([list(L[i]) for i in sup], 8))
        dims[d] += 1
        if d <= 7: d7pats.append((d, len(sup)))
    log('    %s: v=%d | the rank %d | the element-dims %s | the dim<=7: %d' %
        (tag, Vn, rank, dict(sorted(dims.items())), len(d7pats)))
    return rank, dims, d7pats

log('(2) THE CONTROL (the r434 (k=9, j=0!!)):')
Lc = [tuple(l) for l in L434]
rank0, dims0, d70 = system_census(Lc, 'the r434-live')

log('(3) THE +1-EXTENSIONS (the v=112-class (the r434-live + x!!)):')
best = []
for x in cands[:6]:
    Lx = L434 + [x]
    rank, dims, d7 = system_census(Lx, '+x=%s' % str(x))
    best.append((rank, len(d7), x))
log('')

log('(4) THE PRICE-MAP (the (k,j)-variants!!):')
P111 = mp.mpf('0.001733052823330162099157')
def price_at(v, cst, R, h1frac=0.44):
    mass = 8 * R + cst + 2 * v * 7
    h1 = int(mass * h1frac); h2 = int((mass - h1) * 0.82 / 2)
    rest_m = mass - h1 - 2 * h2
    h5 = rest_m // 2; h3 = rest_m - h5
    hist = {1: h1, 2: h2, 3: h3, 5: h5}
    m2 = sum(r * c for r, c in hist.items())
    hist[1] += mass - m2
    c, prof, d = price(hist, v, 8, R)
    if c is None: return None
    return c, float((c - P111) / P111) * 100

for (v, cst, R) in [(111, 63, 389), (112, 77, 392), (112, 88, 392), (112, 63, 392),
                    (113, 77, 396), (113, 91, 396), (115, 77, 403), (115, 91, 403),
                    (118, 77, 413), (120, 63, 420), (129, 77, 451), (129, 91, 451)]:
    r = price_at(v, cst, R)
    log('    v=%3d cst=%2d R=%3d: %s' % (v, cst, R, ('c = %s (%+.4f%%)' % (mp.nstr(r[0], 22), r[1])) if r else 'no-root'))
