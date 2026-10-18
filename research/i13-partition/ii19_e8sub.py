"""THE MAX-DEFICIT E8-SUBSET SCAN (ii19_e8sub.py) — THE CST-63 WINDOW!!
THE LAW: deficit = 256*v - 288*CST.  The P111 (an E8-SUBSET!!): the CST 63 (9 rets at dim-7!!)
-> the deficit 10,272 > the full-E8's 9,984 (the CST 72!!)!!  THE WINDOW: the subsets with
v as BIG as possible while the CST stays 63!!  THE CANDIDATE: v=119 (the E8 minus ONE line
(ONE orbit!!)) -> the deficit 256*119 - 288*63 = 12,320 (THE MAX EVER!!).
THE QUESTION: the subset's Brows-code's min-weight basis: 9 codewords with span <= 7 (the
dim-7 frames!!)?  (The P111's published CST 63 proves the dim-7 ret-frames are legal!!)
"""
import itertools, json, time
from collections import Counter
from fractions import Fraction
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# (0) THE STANDARD E8: the 240 roots -> the 120 lines (up-to-sign!!)
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si, sj in ((1, 1), (1, -1)):
        v = [0] * 8; v[i] = si; v[j] = sj; roots.append(v)
        roots.append([-x for x in v]) if False else None
# careful: (1,1),(1,-1) with both orders i<j: 112 root-VECTORS via 4 sign-classes?? build ALL:
roots = []
for i, j in itertools.combinations(range(8), 2):
    for si in (1, -1):
        for sj in (1, -1):
            v = [0] * 8; v[i] = si; v[j] = sj; roots.append(v)
for s in itertools.product((1, -1), repeat=8):
    if -1 in s and s.count(-1) % 2 == 0:
        roots.append([x / 2 for x in s])
    if s.count(-1) % 2 == 0 and -1 in s:
        pass
log('(0) the 112-pattern roots: %d | the half-roots: %d' % (len(roots), 128))
# the half-roots: even number of minus signs, NOT all-plus: 128-1 = 127?? +the (1/2..)^8 all-plus
half = []
for s in itertools.product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0:
        half.append([x * Fraction(1, 2) for x in s])
log('    the half-patterns (even minus): %d (the standard 128 incl. all-plus!!)' % len(half))
allr = roots + half
log('    the total root-VECTORS: %d' % len(allr))
# the LINES (up-to-sign): canonical: the first-nonnegative-positive!!
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-y for y in v)
    return tuple(v)
lines = {}
for r in allr:
    lines[canon(r)] = True
E8 = [list(k) for k in lines]
log('    THE E8 LINES: %d' % len(E8))

def ip8(a, b): return sum(x * y for x, y in zip(a, b))

def analyze(sub, nm):
    """the subset's Brows-code: the MIN-COST basis (the frame-cost = span + radical!!) -> the TRUE CST!!"""
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
    # THE FRAME-COST of every codeword: span_dim + radical_dim!!
    def cost(x):
        sup = [i for i in range(v) if (x >> i) & 1]
        if not sup: return 99, 0, 0
        rr = [[Fraction(z) for z in sub[i]] for i in sup]
        bas = []
        for row in rr:
            y = row
            for b in bas:
                p = next((c for c in range(8) if b[c] != 0), None)
                if p is not None and y[p] != 0:
                    f = y[p] / b[p]
                    y = [a - f * c for a, c in zip(y, b)]
            p = next((c for c in range(8) if y[c] != 0), None)
            if p is not None: bas.append(y)
        d = len(bas)
        # the radical of the span's form: the nullity of the Gram on the span-basis!!
        G = [[sum(a[i] * b[i] for i in range(8)) for b in bas] for a in bas]
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
                    A[i] = [a - f * b for a, b in zip(A[i], A[r0])]
            r0 += 1
        rad = d - r0
        return d + rad, d, rad
    costs = {}
    for x in cws:
        if x: costs[x] = cost(x)
    cc = Counter((c[1], c[2]) for c in costs.values())
    log('    %s: v=%d | the rank %d | the (span, radical)-census: %s' % (
        nm, v, rk, dict(sorted(cc.items()))))
    # THE MIN-COST BASIS (the greedy: exact for the independence matroid!!)
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
    log('        THE TRUE-CST %d (the costs %s) | THE DEFICIT %d (the E8: 9,984!! the 121: 9,952!! the P111: 10,272!!)' % (
        cst, [costs[x][0] for x in mw], dfc))
    return cst, dfc, mw, [costs[x] for x in mw]

# (1) THE FULL E8 (the control: the CST 72!!)
log('(1) THE CONTROL: the full E8:')
analyze(E8, 'E8-full')

# (2) THE v=119 SUBSET (the E8 minus ONE line: ONE orbit by the E8-symmetry!!)
log('(2) THE v=119 (the E8 minus line-0: one orbit!!):')
analyze(E8[1:], 'E8-1')
# (3) THE OTHER v=119 (minus a HALF-root: the second orbit?!)
half_line = next(i for i, l in enumerate(E8) if any(z == Fraction(1, 2) for z in l))
log('(3) THE v=119 (the E8 minus a HALF-root-line (the second orbit?!)):')
sub = [l for i, l in enumerate(E8) if i != half_line]
analyze(sub, 'E8-1half')
# (4) THE k=2..9 SCAN (the window-hunt: where do the spans drop to <=7?!)
log('(4) THE k=2..9 SCAN (the window-hunt: the spans <= 7 -> the CST <= 63-64!!):')
# the pair-orbits at k=2: the |ip| in {0, 1, 1/2}!!
partner1 = next(i for i, l in enumerate(E8) if i != 0 and abs(ip8(E8[0], l)) == 1)
orth = next(i for i, l in enumerate(E8) if i not in (0, partner1) and ip8(E8[0], l) == 0)
half2 = next(i for i, l in enumerate(E8) if i not in (0, partner1, orth)
             and any(z == Fraction(1, 2) for z in l))
pats = {
    'E8-2(ip1)': [0, partner1], 'E8-2(ip0)': [0, orth],
    'E8-2(iphalf)': [0, half2],
}
for nm, rm in pats.items():
    analyze([l for i, l in enumerate(E8) if i not in rm], nm)
# (5) THE k=3..9 samples (the first-k + the structured!!)
for k in (3, 4, 5, 6, 7, 8, 9):
    analyze(E8[k:], 'E8-%d(first-k)' % k)
# the P111-window probe: the k=9 at the CST-63!!  the P111 = the published subset (the CST 63!!):
# probe several k=9 structured removals: the first-9, the half-blocks, etc!!
halfs = [i for i, l in enumerate(E8) if any(z == Fraction(1, 2) for z in l)][:9]
analyze([l for i, l in enumerate(E8) if i not in halfs], 'E8-9(half-block)')
ints = [i for i, l in enumerate(E8) if not any(z == Fraction(1, 2) for z in l)][:9]
analyze([l for i, l in enumerate(E8) if i not in ints], 'E8-9(int-block)')
log('DONE — THE MAX-DEFICIT E8-SUBSET SCAN!!')
