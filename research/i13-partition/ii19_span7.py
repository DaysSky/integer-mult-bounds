"""THE SPAN-7 STRUCTURE (ii19_span7.py) — THE PUNCTURE-DESIGN THEORY!!
WHICH codeword does removing line L free?!  For the v=119 puncture: find the span-7
codeword, print its support + the 7-dim subspace, and check: is it supported INSIDE
perp(L) (the 63 lines ⊥ L)?!  THE THEORY-CHECK -> then the puncture-design!!
"""
import json, itertools, time
from collections import Counter
from fractions import Fraction
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
lines = W3['lines']
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

def ip8(a, b): return sum(x * y for x, y in zip(a[:8], b[:8]))

def span_basis(sup, sub):
    rr = [[Fraction(z) for z in sub[i][:8]] for i in sup]
    bas = []
    for row in rr:
        y = row
        for b in bas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and y[p] != 0:
                f = y[p] / b[p]
                y = [a2 - f * c for a2, c in zip(y, b)]
        p = next((c for c in range(8) if y[c] != 0), None)
        if p is not None: bas.append(y)
    return bas

ROOTS = lines[:120]

def analyze7(sub, nm):
    """the span-7 codewords: print their supports!!"""
    v = len(sub)
    rows = []
    for t in range(v):
        m = 1 << t
        for u in range(v):
            if u != t and ip8(sub[t], sub[u]) == 0:
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
    out = []
    for x in sorted(cws):
        if not x: continue
        sup = [i for i in range(v) if (x >> i) & 1]
        d = len(span_basis(sup, sub))
        if d <= 7:
            out.append((d, len(sup), sup, x))
    log('%s: v=%d | the span<=7 codewords: %d' % (nm, v, len(out)))
    for d, w, sup, x in out:
        log('    the span %d | the weight %d | the support %s' % (d, w, sup))
    return out

# (1) THE v=119 PUNCTURE (remove OUR line-0!!): the span-7 codeword!!
sub = ROOTS[1:]
log('(1) THE v=119 (minus OUR line 0!!):')
o = analyze7(sub, 'roots-1')
# the theory-check: the support ⊆ perp(line-0)?!
perp0 = [i for i in range(1, 120) if ip8(ROOTS[0], ROOTS[i]) == 0]
log('    the perp(line-0) (the 63 lines!!): %s' % perp0)
if o:
    d, w, sup, x = o[0]
    log('    THE THEORY-CHECK: the support ⊆ perp(line-0)?? %s' % (
        all((i + 1) in perp0 for i in sup)))
# (2) THE v=118 (minus 0 + the next): the TWO span-7s!!
sub2 = ROOTS[2:]
log('(2) THE v=118 (minus 0,1!!):')
o2 = analyze7(sub2, 'roots-2')
perp1 = [i for i in range(2, 120) if ip8(ROOTS[1], ROOTS[i]) == 0]
for d, w, sup, x in o2:
    log('    the span-%d support %s | ⊆perp(line-0)? %s | ⊆perp(line-1)? %s' % (
        d, sup, all((i + 2) in perp0 for i in sup), all((i + 2) in perp1 for i in sup)))
log('DONE — THE SPAN-7 STRUCTURE!!')
