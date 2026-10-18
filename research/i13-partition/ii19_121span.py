"""THE SPAN-MINIMIZING BASIS SEARCH (the SS1515 audit's missed item 5) — 'keep pushing for frontier' (SS1531!!).

THE CROSSING NEEDS Σ-span <= ~65-67 at the honest shape (A-like per the design's own
target chains: the jumps {1: 726, 2: 121}!!) and the honest R >= 299 (the arrival
law!!); the SS1500 greedy's basis gives 73 (all 8 even rows span 8!!).  THE SEARCH:
the parity kernel's 255 nonzero rows: each support's span dim -> the span histogram ->
THE MIN-Σ-SPAN BASIS (the weighted matroid greedy: optimal for additive weights!!)
-> THE HONEST CST FLOOR + the W-verification + THE PRICE at the measured floor
(the A/B/D variants — C dropped per the audit!!; the R grid: the honest R!!).
IF some kernel rows have dim 4-7 spans (the low-weight 4/6-term combos could be
subsystem-like: A7/A6/D4!!): THE CROSSING REOPENS; if all span 8: THE PROGRAM CLOSES
ON THE NUMBERS.
"""
import sys, itertools
from collections import Counter
import numpy as np
from mpmath import mp, mpf
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V = 121
H = 9
SP = 120

# the system [the SS1419 code]
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = [list(al) + [0, 0] for al in AL]
L.append([0.0] * 8 + [1.0, 1.0])
L = np.array(L, dtype=float)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
Brows = [PERP[t] | (1 << t) for t in range(V)]

def gf2_rank(rows_in):
    rows = list(rows_in)
    rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> col) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank

PHI = lambda row: (row >> SP) & 1
cands = [k for k in range(1, V) if PHI(Brows[k]) == 1]
sel = []
cur = [Brows[0]]
for k in cands:
    if gf2_rank(cur + [Brows[k]]) == len(cur) + 1:
        sel.append(k)
        cur = cur + [Brows[k]]
        if len(sel) == 8:
            break
assert len(sel) == 8 and gf2_rank(cur) == 9
kernel_basis = [Brows[0] ^ Brows[k] for k in sel]
print('the kernel basis (the even rows): k = %s' % sel)

# ============ (1) THE 255 KERNEL ROWS: THE SPANS ============
def span_dim(row):
    sup = [s for s in range(V) if (row >> s) & 1]
    return int(np.linalg.matrix_rank(L[sup])), len(sup)

rows_all = []
for mask in range(1, 256):
    r = 0
    for b in range(8):
        if (mask >> b) & 1:
            r ^= kernel_basis[b]
    rows_all.append(r)
assert len(set(rows_all)) == 255
spans = [span_dim(r) for r in rows_all]
dims = [d for d, _ in spans]
szs = [s for _, s in spans]
print('(1) the kernel: %d nonzero rows; the span-dim histogram: %s' %
      (len(rows_all), dict(sorted(Counter(dims).items()))))
print('    the support sizes: min %d mean %.1f max %d' % (min(szs), sum(szs) / len(szs), max(szs)))
low = sorted((dims[i], szs[i], i) for i in range(255) if dims[i] <= 7)
print('    THE LOW-SPAN ROWS (dim <= 7): %d' % len(low))
for d, s, i in low[:12]:
    print('      row %d: span %d, support %d lines' % (i, d, s))

# ============ (2) THE MIN-Σ-SPAN KERNEL BASIS (the weighted matroid greedy!!) ============
order = sorted(range(255), key=lambda i: (dims[i], szs[i]))
picked = []
cur = []
for i in order:
    if gf2_rank(cur + [rows_all[i]]) == len(cur) + 1:
        picked.append(i)
        cur = cur + [rows_all[i]]
        if len(picked) == 8:
            break
assert len(picked) == 8
min_sum = sum(dims[i] for i in picked)
print('(2) THE MIN-Σ-SPAN KERNEL BASIS: the spans %s -> Σ = %d' %
      ([dims[i] for i in picked], min_sum))
cst_min = min_sum + 9
print('    THE HONEST CST FLOOR = %d + 9 (the odd row: FORCED!!) = %d  (the greedy basis: 73!!)' %
      (min_sum, cst_min))
copy_dims = [dims[i] for i in picked] + [9]

# ============ (3) THE W-VERIFICATION OF THE MIN-BASIS ============
basis = [rows_all[i] for i in picked] + [Brows[0]]
assert gf2_rank(basis) == 9
rows = list(basis)
aug = [[1 if i == j else 0 for j in range(9)] for i in range(9)]
r = 0
pivots = []
T = []
for col in range(V):
    piv = next((i for i in range(r, len(rows)) if (rows[i] >> col) & 1), None)
    if piv is None:
        continue
    rows[r], rows[piv] = rows[piv], rows[r]
    aug[r], aug[piv] = aug[piv], aug[r]
    for i in range(len(rows)):
        if i != r and (rows[i] >> col) & 1:
            rows[i] ^= rows[r]
            aug[i] = [a ^ b for a, b in zip(aug[i], aug[r])]
    pivots.append((col, rows[r]))
    T.append(list(aug[r]))
    r += 1
def solve(row):
    coords = [0] * 9
    rr = row
    for k, (col, rw) in enumerate(pivots):
        if (rr >> col) & 1:
            coords[k] = 1
            rr ^= rw
    assert rr == 0, 'the residual!!'
    return coords
Wred = [solve(Brows[t]) for t in range(V)]
W = []
for t in range(V):
    worig = [0] * 9
    for k in range(9):
        if Wred[t][k]:
            for j in range(9):
                if T[k][j]:
                    worig[j] ^= 1
    W.append(worig)
ok = True
for t in range(V):
    acc = 0
    for k in range(9):
        if W[t][k]:
            acc ^= basis[k]
    if acc != Brows[t]:
        ok = False
print('(3) THE W-VERIFICATION (the min-Σ-span basis): %s' % ('PASS!!' if ok else 'FAIL!!'))
wl = Counter(sum(w) for w in W)
print('    the W-weights: %s (the mean %.1f)' % (dict(sorted(wl.items())), sum(sum(w) for w in W) / V))

# ============ (4) THE PRICE AT THE MEASURED FLOOR (the R grid: the honest R!!) ============
def hist_exact(R, variant, cst_m):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    if variant == 'A':
        fr = [(1, 1.0)]
    elif variant == 'B':
        fr = [(1, 0.50), (2, 0.25), (5, 0.25)]
    else:  # D
        fr = [(1, 0.262), (2, 0.571), (4, 0.048), (5, 0.119)]
    fl = {r: f * climb / r for r, f in fr}
    hist = {r: int(n) for r, n in fl.items()}
    mass = sum(r * n for r, n in hist.items())
    rem = int(climb) - mass
    while rem > 0:
        elig = [(fl[r] - int(fl[r]), r) for r in fl if r <= rem]
        if not elig:
            elig = [(0.0, r) for r in sorted(fl) if r <= rem]
        _, rr = max(elig)
        hist[rr] += 1
        rem -= rr
    for d in copy_dims:
        hist[d] = hist.get(d, 0) + 1
    mass = sum(r * n for r, n in hist.items())
    return hist, mass, int(climb + cst_m)

print()
print('(4) THE PRICE AT THE MEASURED CST FLOOR = %d (C dropped per the audit!!)' % cst_min)
for R in (299, 310, 325, 350):
    line = '  R %3d: ' % R
    for var in ('A', 'B', 'D'):
        hist, mass, ident = hist_exact(R, var, cst_min)
        assert mass == ident, (var, R, mass, ident)
        c, prof, d = pprice(hist, V, H, R)
        if c is None:
            line += '%s NO-ROOT  ' % var
        else:
            pct = (float(c) / FRONTIER - 1) * 100
            line += '%s %+.2f%%  ' % (var, pct)
    print(line)
print('DONE')
