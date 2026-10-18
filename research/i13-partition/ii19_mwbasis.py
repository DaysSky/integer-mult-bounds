"""THE MIN-WEIGHT-BASIS LEVER (ii19_mwbasis.py) — THE CST's TRUE FLOOR!!
THE Brows-CODE (rank 9 over GF(2), length 121!!): the rets = ANY 9 independent codewords
(the SS1492 was ONE basis — NOT the min-weight one!!).  THE CST = Sum(the rets' frame-dims)
~ Sum(1 + the support-span-dims!!) -> THE MIN-WEIGHT BASIS = THE CST-COLLAPSE!!
"""
import json, itertools, time
from collections import Counter
from fractions import Fraction
W4 = json.load(open('ii19_own_word4.json', 'rt'))
V, H = W4['v'], W4['h']
lines = W4['lines']
SP = 120
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
# the Brows (the B0-rows!!)
Brows = []
for t in range(V):
    m = 1 << t
    for u in range(V):
        if u != t and ip121(lines[t], lines[u]) == 0:
            m |= 1 << u
    Brows.append(m)

# the code: the span of the 121 rows (rank 9!!) -> the 512 codewords!!
basis = {}
rank = 0
for r in Brows:
    x = r
    while x:
        p = (x & -x).bit_length() - 1
        if p in basis: x ^= basis[p]
        else:
            basis[p] = x; rank += 1
            break
log('(0) the Brows-code: rank %d (the pivot-basis %d rows!!)' % (rank, len(basis)))
assert rank == 9
# ALL the codewords: the 2^9 combos of the basis!!
piv = sorted(basis.items())
cws = []
for mask in range(1 << 9):
    x = 0
    for k, (p, r) in enumerate(piv):
        if (mask >> k) & 1: x ^= r
    cws.append(x)
log('(1) the codewords: %d | the distinct: %d' % (len(cws), len(set(cws))))
wts = Counter(bin(x).count('1') for x in cws)
log('    the weight-distribution: %s' % dict(sorted(wts.items())))
odd = [x for x in cws if (x >> SP) & 1]
even = [x for x in cws if not (x >> SP) & 1]
log('    the odd codewords: %d (the weights %s) | the even: %d (the weights %s)' % (
    len(odd), dict(sorted(Counter(bin(x).count('1') for x in odd).items())),
    len(even), dict(sorted(Counter(bin(x).count('1') for x in even).items()))))
log('    the MIN-WEIGHT odd: %d | the MIN-WEIGHT even: %d' % (
    min(bin(x).count('1') for x in odd), min(bin(x).count('1') for x in even)))

# (2) THE MIN-WEIGHT BASIS: the 9 lightest independent codewords!!
cands = sorted(set(cws), key=lambda x: (bin(x).count('1'), x))
mw = []
bx = {}
for x in cands:
    y = x
    while y:
        p = (y & -y).bit_length() - 1
        if p in bx: y ^= bx[p]
        else:
            bx[p] = y; mw.append(x)
            break
    if len(mw) == 9: break
log('(2) THE MIN-WEIGHT BASIS: the weights %s (the SUM of weights %d!!)' % (
    [bin(x).count('1') for x in mw], sum(bin(x).count('1') for x in mw)))
for j, x in enumerate(mw):
    sup = [i for i in range(V) if (x >> i) & 1]
    log('    mw[%d]: the weight %d | the support %s%s' % (
        j, len(sup), sup[:14], '...' if len(sup) > 14 else ''))

# (3) THE FRAME-DIMS: each ret's frame must contain its support-lines -> the span-dim!!
def span_dim(sup):
    rows = [[Fraction(lines[i][k]) for k in range(9)] for i in sup]
    r0 = 0
    for c in range(9):
        p = None
        for i in range(r0, len(rows)):
            if rows[i][c] != 0: p = i; break
        if p is None: continue
        rows[r0], rows[p] = rows[p], rows[r0]
        pv = rows[r0][c]
        rows[r0] = [z / pv for z in rows[r0]]
        for i in range(len(rows)):
            if i != r0 and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r0])]
        r0 += 1
    return r0
log('(3) THE FRAME-DIMS (the support-spans!!):')
cst_mw = 0
for j, x in enumerate(mw):
    sup = [i for i in range(V) if (x >> i) & 1]
    d = span_dim(sup)
    cst_mw += d
    log('    mw[%d]: the weight %d -> the span-dim %d' % (j, len(sup), d))
log('    THE CST (the min-weight basis!!) = %d vs the word4-73 vs the census-floor-73!!' % cst_mw)
log('    THE DEFICIT: 256*121 - 288*%d = %d (the word4: 9,952!!)' % (
    cst_mw, 256 * 121 - 288 * cst_mw))

# (4) THE NONDEGENERACY: each support's Gram must be nondegenerate (the frame legality!!)
def gram_det(sup):
    n = len(sup)
    G = [[ip121(lines[sup[a]], lines[sup[b]]) for b in range(n)] for a in range(n)]
    A = [[Fraction(z) for z in r] for r in G]
    d = Fraction(1)
    for c in range(n):
        p = None
        for i in range(c, n):
            if A[i][c] != 0: p = i; break
        if p is None: return 0
        if p != c: A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return d
bad = 0
for j, x in enumerate(mw):
    sup = [i for i in range(V) if (x >> i) & 1]
    if gram_det(sup) == 0:
        bad += 1
        log('    mw[%d]: DEGENERATE Gram (the frame needs the +1!!)' % j)
log('(4) the degenerate supports: %d/9 (each needs the +1-dim (the radical-kill!!))' % bad)
log('DONE — THE MIN-WEIGHT-BASIS LEVER!!')
