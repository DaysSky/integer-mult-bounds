"""THE PUNCTURE-HUNT (ii19_phunt.py) — THE CST-63 9-SET!!
THE THEORY (ii19_span7!!): removing L frees 1_{perp(L)} (the span-7 star-indicator!!).
THE DESIGN: 9 lines whose PUNCTURED star-indicators are INDEPENDENT -> the 9-span-7 basis
-> THE CST 63 -> THE DEFICIT 10,272 (the P111-class!!).
THE HUNT: randomized 9-sets + the min-cost-basis scoring (the target CST 63!!).
"""
import json, random, time
from collections import Counter
from fractions import Fraction
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
lines = W3['lines']
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

def ip8(a, b): return sum(x * y for x, y in zip(a[:8], b[:8]))
ROOTS = lines[:120]

def cst_of(rm):
    """the punctured system (remove the rm-lines!!): the min-frame-cost basis -> the CST!!"""
    sub = [l for i, l in enumerate(ROOTS) if i not in rm]
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
    if rk != 9:
        return None, rk
    piv = sorted(bx.items())
    # the span-7 shortcut: count the codewords with span <= 7 + their independence!!
    cws = set()
    for mask in range(1 << 9):
        x = 0
        for k, (p, r) in enumerate(piv):
            if (mask >> k) & 1: x ^= r
        cws.add(x)
    def spand(x):
        sup = [i for i in range(v) if (x >> i) & 1]
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
        return len(bas)
    c7 = [x for x in cws if x and spand(x) <= 7]
    # the independence among the c7!!
    indep = []
    ibx = {}
    for x in sorted(c7, key=lambda z: (bin(z).count('1'), z)):
        y = x
        while y:
            p = (y & -y).bit_length() - 1
            if p in ibx: y ^= ibx[p]
            else: ibx[p] = y; indep.append(x); break
    return (9 - len(indep)) * 8 + len(indep) * 7 if len(indep) >= 1 else 72, len(indep)

log('(0) THE HUNT: the randomized 9-sets (the target: the CST 63 = 9 independent span-7s!!)')
best = (99, None)
random.seed(111)
tried = set()
for trial in range(400):
    rm = tuple(sorted(random.sample(range(120), 9)))
    if rm in tried: continue
    tried.add(rm)
    cst, n7 = cst_of(set(rm))
    if cst is None:
        continue
    if cst < best[0]:
        best = (cst, rm)
        log('    the trial %d: rm=%s -> the CST %d (the indep span-7s: %d!!) %s' % (
            trial, list(rm), cst, n7, 'THE TARGET HIT!!!' if cst <= 63 else ''))
        if cst <= 63:
            break
log('(1) THE BEST: the CST %d | rm=%s (the indep span-7s %d!!)' % (
    best[0], list(best[1]) if best[1] else None, 9 - (72 - best[0]) if best[0] < 72 else 0))
log('DONE — THE PUNCTURE-HUNT!!')
