"""THE 121-FAMILY's DEFICIT LANDSCAPE (ii19_121sub.py) — THE ACTUAL WORD-DATA!!
THE DISCOVERY (ii19_nat1.py!!): the 121's lines = 120 NORM-4 lines (a=0, alpha.alpha = 4!!)
+ the special (a=1, norm 2!!) — NOT the E8's norm-2 roots!!  THE FAMILY's OWN Brows-codes:
(a) the roots-only (v=120, h=8!!): the min-frame-cost basis -> the CST/deficit!!
(b) the punctures k=1..9 (the span-window!!): the landscape!!
(c) the special-variants (the 121-k!!): the odd-ret's +9-structure!!
THE QUESTION: does the norm-4-family beat the P111's deficit 10,272?!
"""
import json, itertools, time
from collections import Counter
from fractions import Fraction
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
lines = W3['lines']
V = W3['v']
SP = 120
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

def ip8(a, b): return sum(x * y for x, y in zip(a[:8], b[:8]))
def ip9(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]

def analyze(sub, nm, h):
    """the sub's Brows-code (the sub's OWN form!!): the min-COST basis (span+radical!!)."""
    v = len(sub)
    dim = len(sub[0])
    if dim == 9 and all(l[8] == 0 for l in sub): dim = 8
    ipf = ip8 if dim == 8 else ip9
    rows = []
    for t in range(v):
        m = 1 << t
        for u in range(v):
            if u != t and ipf(sub[t], sub[u]) == 0:
                m |= 1 << u
        rows.append(m)
    bx = {}
    for r in rows:
        x = r
        while x:
            p = (x & -x).bit_length() - 1
            if p in bx: x ^= bx[p]
            else: bx[p] = x; break
    rk = len(bx)
    piv = sorted(bx.items())
    cws = set()
    for mask in range(1 << rk):
        x = 0
        for k, (p, r) in enumerate(piv):
            if (mask >> k) & 1: x ^= r
        cws.add(x)
    def cost(x):
        sup = [i for i in range(v) if (x >> i) & 1]
        if not sup: return 99, 0, 0
        rr = [[Fraction(z) for z in sub[i][:dim]] for i in sup]
        bas = []
        for row in rr:
            y = row
            for b in bas:
                p = next((c for c in range(dim) if b[c] != 0), None)
                if p is not None and y[p] != 0:
                    f = y[p] / b[p]
                    y = [a2 - f * c for a2, c in zip(y, b)]
            p = next((c for c in range(dim) if y[c] != 0), None)
            if p is not None: bas.append(y)
        d = len(bas)
        G = [[sum(a[i] * b[i] for i in range(dim)) for b in bas] for a in bas]
        if dim == 9:
            # the 9-dim form: +2a9b9!!
            G = [[G[i][j] + 2 * bas[i][8] * bas[j][8] for j in range(d)] for i in range(d)]
        A = [[Fraction(z) for z in r] for r in G]
        r0 = 0
        for c in range(d):
            p = None
            for i in range(r0, d):
                if A[i][c] != 0: p = i; break
            if p is None: continue
            A[r0], A[p] = A[p], A[r0]
            pv = A[r0][c]
            A[r0] = [z / pv for z in A[r0]]
            for i in range(d):
                if i != r0 and A[i][c] != 0:
                    f = A[i][c]
                    A[i] = [a2 - f * b for a2, b in zip(A[i], A[r0])]
            r0 += 1
        rad = d - r0
        return d + rad, d, rad
    costs = {x: cost(x) for x in cws if x}
    cc = Counter((c[1], c[2]) for c in costs.values())
    order = sorted(costs, key=lambda x: (costs[x][0], x))
    mw = []; mbx = {}
    for x in order:
        y = x
        while y:
            p = (y & -y).bit_length() - 1
            if p in mbx: y ^= mbx[p]
            else: mbx[p] = y; mw.append(x); break
        if len(mw) == rk: break
    cst = sum(costs[x][0] for x in mw)
    dfc = 256 * v - 288 * cst
    log('    %s: v=%d h=%d | the rank %d | the (span,rad)-census %s' % (
        nm, v, h, rk, dict(sorted(cc.items()))))
    log('        THE CST %d (the costs %s) | THE DEFICIT %d (the E8: 9,984!! the 121: 9,952!! the P111: 10,272!!)' % (
        cst, [costs[x][0] for x in mw], dfc))
    return cst, dfc

log('(0) the actual word-data: v=%d (the norms: %s!!)' % (
    V, dict(sorted(Counter(ip9(l, l) for l in lines).items()))))
ROOTS = lines[:120]
SPECIAL = lines[120]
log('(1) THE ROOTS-ONLY (the norm-4-class!!) v=120 h=8:')
analyze(ROOTS, 'roots-only', 8)
log('(2) THE PUNCTURES (the roots-minus-k!!):')
for k in (1, 2, 3, 5, 8, 9):
    analyze(ROOTS[k:], 'roots-%d(first-k)' % k, 8)
log('(3) THE SPECIAL-VARIANTS (the 121-minus-k: the special KEPT!!):')
for k in (1, 3, 5, 8):
    sub = ROOTS[k:] + [SPECIAL]
    analyze(sub, '121-%d(the-special-kept)' % k, 9)
log('DONE — THE 121-FAMILY DEFICIT LANDSCAPE!!')
