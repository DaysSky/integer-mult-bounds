"""THE SMART-BASIS CONSTRUCTION — the measured cst + the price re-run (SS1492!!).

THE SS1492 HONEST BAND: at the pivot basis (cst=81): dead (-16% to -41%!!); at the smart
basis (cst=73: 8 dim-8 rows + 1 dim-9): THE BAND STRADDLES THE FRONTIER (C: +2.77%/+3.66%,
D: +5.20%!!).  AND THE SMART BASIS IS PROVABLE: the parity map phi (the column-120 bit:
whether the special line (0,1,1) is in the support!!) on the 9-dim row space: the kernel
(THE EVEN COMBINATIONS: e.g. B[0]^B[k]: the specials cancel!!): dim 8: every kernel row's
support contains NO special line -> its span <= dim 8!!!  SO a basis {8 even rows (dim
<= 8) + 1 odd row (dim 9, FORCED: the special in the support!!)}: THE CST <= 73!!!

THIS SCRIPT: (1) the even-subspace basis (the ker(phi)!!); (2) the MEASURED SPANS (each
basis row's support's span dim!!); (3) THE MEASURED CST (Σ dims!!); (4) the W-matrix +
the verification (B[t] = Σ W[t,k]·u_k for all 121!!); (5) THE PRICE RE-RUN AT THE
MEASURED CST (the mass-exact hists: the floor + the largest-remainder with the r<=rem
constraint (the SS1492 mOFF bug fixed!!)) -> THE HONEST VERDICT.
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
SP = 120   # the special line index!!

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
G = L @ np.diag([1, 1, 1, 1, 1, 1, 1, 1, 0, 1]) @ L.T if False else None
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
print('the 121-line system: %d lines' % V)

Brows = [PERP[t] | (1 << t) for t in range(V)]
PHI = lambda row: (row >> SP) & 1   # the parity: the special in the support?!

# ============ (1) THE EVEN-SUBSPACE BASIS ============
# the row space: dim 9 (measured SS1406!!); the kernel of phi: dim 8.
# THE CONSTRUCTION: the odd row: B[0] (phi=1!!); the even rows: B[0]^B[k] (phi=0!!).
# the independence: {B[0]^B[1], ..., B[0]^B[8], B[0]} spans the same as {B[0..8]}!!
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
# pick 8 indices k so that {B[0], B[k1..k8]} is independent (rank 9!!)
cands = []
for k in range(1, V):
    if PHI(Brows[k]) == 1:   # the odd rows only (the roots!!)
        cands.append(k)
# THE SS1496 FIX: the greedy must APPEND ONLY RANK-INCREASING candidates (the first 9
# B-rows are DEPENDENT (the D4-ish line ordering!!): the naive append accumulated them!!)
sel = []
cur = [Brows[0]]
for k in cands:
    if gf2_rank(cur + [Brows[k]]) == len(cur) + 1:
        sel.append(k)
        cur = cur + [Brows[k]]
        if len(sel) == 8:
            break
print('(1) the basis: the odd row B[0] + the even rows B[0]^B[k] for k = %s' % sel)
assert len(sel) == 8 and gf2_rank(cur) == 9, 'the independence!!'
basis = [Brows[0] ^ Brows[k] for k in sel] + [Brows[0]]   # 8 even + 1 odd!!
print('    the even rows: phi=0: %s; the odd row: phi=1: %s' %
      ([PHI(b) for b in basis[:8]], PHI(basis[8])))

# ============ (2) THE MEASURED SPANS ============
def span_dim(row):
    sup = [s for s in range(V) if (row >> s) & 1]
    return int(np.linalg.matrix_rank(L[sup])), len(sup)
dims_spans = [span_dim(b) for b in basis]
print('(2) the basis rows: the (span dim, support size) [THE SS1500 LABEL FIX: span_dim returns (rank, len)!!]: %s' % dims_spans)
cst = sum(d for d, _ in dims_spans)
print('    THE MEASURED CST = %d (the pivot basis: 81; the SS1492 modeled: 73)' % cst)

# ============ (3) THE W-MATRIX + THE VERIFICATION (THE SS1500 FIX: the coords' frame!!) ============
# THE SS1500 BUG: the solve's coords are relative to the REDUCED pivot rows (rw_k!!), NOT
# the ORIGINAL basis -> the verification XORed the wrong rows!!  THE FIX: the augmented
# reduction (the tracking: rw = Σ aug[i][j]·basis[j]!!) -> the T matrix (THE SNAPSHOT at
# the collection!!) -> W_orig = W_red × T: the coordinates over MY gathers (the even rows
# + the odd row!!) — THE ONES THE BUILD'S SCATTER NEEDS!!!
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
    """the coords over the REDUCED rows (rw_k = Σ_j T[k][j]·basis[j]!!)"""
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
print('(3) THE W-VERIFICATION (the SS1500 coords-frame fix!!): B[t] = Σ W[t,k]·u_k over MY gathers for all %d targets: %s' % (V, 'PASS!!' if ok else 'FAIL!!'))
wl = Counter(sum(w) for w in W)
print('    the W-weights over the even/odd gathers: %s (the mean %.1f)' % (dict(sorted(wl.items())), sum(sum(w) for w in W) / V))

# ============ (4) THE PRICE RE-RUN AT THE MEASURED CST ============
def hist_exact(R, variant, cst_m):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    if variant == 'A':
        fr = [(1, 1.0)]
    elif variant == 'B':
        fr = [(1, 0.50), (2, 0.25), (5, 0.25)]
    elif variant == 'C':
        fr = [(1, 0.30), (2, 0.20), (5, 0.50)]
    else:
        fr = [(1, 0.262), (2, 0.571), (4, 0.048), (5, 0.119)]
    fl = {r: f * climb / r for r, f in fr}
    hist = {r: int(n) for r, n in fl.items()}
    mass = sum(r * n for r, n in hist.items())
    rem = int(climb + cst_m - mass - cst_m)   # the climb's deficit (>= 0!!)
    # the +1s: the largest remainder among the ranks with r <= rem (THE FIX!!)
    while rem > 0:
        elig = [(fl[r] - int(fl[r]), r) for r in fl if r <= rem]
        if not elig:
            elig = [(0.0, r) for r in sorted(fl) if r <= rem]
        _, r = max(elig)
        hist[r] += 1
        rem -= r
    # the copies: the measured basis: the rows' dims!!
    for d, _ in dims_spans:
        hist[d] = hist.get(d, 0) + 1
    return hist, sum(r * n for r, n in hist.items()), int(climb + cst_m)

print()
print('(4) THE PRICE RE-RUN AT THE MEASURED CST = %d (the mass-exact hists!!)' % cst)
best = None
for R in (286, 300, 325, 350):
    line = '  R %3d: ' % R
    for var in ('A', 'B', 'C', 'D'):
        hist, mass, ident = hist_exact(R, var, cst)
        assert mass == ident, (var, R, mass, ident)
        c, prof, d = pprice(hist, V, H, R)
        if c is None:
            line += '%s NO-ROOT  ' % var
        else:
            pct = (float(c) / FRONTIER - 1) * 100
            line += '%s %+.2f%%  ' % (var, pct)
            if best is None or float(c) > best[0]:
                best = (float(c), R, var, pct)
    print(line)
print('THE BEST: %s variant, R=%d: c = %.9f (%+.2f%% vs frontier) — %s' %
      (best[2], best[1], best[0], best[3],
       'ABOVE THE FRONTIER: THE CROSSING AT THE SMART BASIS!!' if best[0] > FRONTIER
       else 'below the frontier'))
print('DONE')
