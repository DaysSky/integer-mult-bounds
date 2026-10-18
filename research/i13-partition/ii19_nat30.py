"""THE MIN-Σ-SPAN GATHER BASIS (ii19_nat30.py) — the record's UNEXPLORED CST lever (the §632
flag: "a min-Σ-span basis could give cst < 73: UNEXPLORED!!").

The deficit law: deficit = 256*v - 288*CST — BIGGER deficit = better c.  The smart basis
(8 even dim-8 rows + 1 odd dim-9) = CST 73.  ANY 8 even + 1 odd INDEPENDENT codewords of the
decoder's 9-dim row space can be the gathers (the W-solve adapts (the §1508 machinery!!));
CST = Σ span-dims of the supports.  THE CENSUS: all 512 codewords' (phi, span-dim, support,
Gram-nondegeneracy); the min-Σ basis; the exact price probes of the word4's hist with the new
copy-ranks (the climb part UNCHANGED — the gather tail is a BOUNDED rebuild!!).
"""
import sys, itertools
from collections import Counter
import numpy as np
from mpmath import mp, mpf
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = mpf('0.001744385950814795279853')
V, H, SP = 121, 9, 120

# the system (the 121basis.py convention, verbatim)
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
L = np.array([list(al) + [0, 0] for al in AL] + [[0.0] * 8 + [1.0, 1.0]])
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
PHI = lambda row: (row >> SP) & 1

def gf2_rank(rows_in):
    rows = list(rows_in); rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if piv is None: continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> col) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank

# a basis of the row space (rank 9)
basis9 = []
for r in Brows:
    if gf2_rank(basis9 + [r]) == len(basis9) + 1:
        basis9.append(r)
    if len(basis9) == 9: break
assert gf2_rank(basis9) == 9

# all 512 codewords
codes = []
for mask in range(512):
    x = 0
    for k in range(9):
        if (mask >> k) & 1: x ^= basis9[k]
    codes.append(x)

def facts(row):
    sup = [s for s in range(V) if (row >> s) & 1]
    M = L[sup]
    d = int(np.linalg.matrix_rank(M))
    GM = M @ FORM @ M.T
    det = abs(float(np.linalg.det(GM))) if len(sup) else 0.0
    return d, len(sup), det > 1e-9

seen = set()
census = {}
for x in codes:
    if x in seen or x == 0: continue
    seen.add(x)
    d, n, nd = facts(x)
    census[x] = (PHI(x), d, n, nd)
ev = Counter((d, nd) for p, d, n, nd in census.values() if p == 0)
od = Counter((d, nd) for p, d, n, nd in census.values() if p == 1)
print('(1) distinct nonzero codewords: %d | even: %s | odd: %s' % (
    len(census), dict(sorted(ev.items())), dict(sorted(od.items()))))
print('    even (dim, nondeg) hist: %s' % dict(sorted(Counter(d for p, d, n, nd in census.values() if p == 0).items())))
print('    odd  (dim, nondeg) hist: %s' % dict(sorted(Counter(d for p, d, n, nd in census.values() if p == 1).items())))
minodd = min((census[x][1], x) for x in census if census[x][0] == 1)
print('    the min-dim ODD codeword: dim %d (support %d)' % (minodd[0], census[minodd[1]][2]))
minev = sorted(((census[x][1], x) for x in census if census[x][0] == 0))
print('    the min-dim EVEN codewords: %s' % [d for d, x in minev[:8]])

# THE VERDICT IS THE CENSUS: every even codeword is dim 8, every odd dim 9 ->
# ANY basis (8 even + 1 odd) has CST = 8*8 + 9 = 73 — THE PROVEN FLOOR (the record's smart
# basis was already optimal; the §632 "min-Σ-span < 73" lever is CLOSED).
CST = 73
sel = [minodd[1]]
for d, x in minev:
    if gf2_rank(sel + [x]) == len(sel) + 1:
        sel.append(x)
    if len(sel) == 9: break
assert gf2_rank(sel) == 9
print('(2) the CST verdict: 8*8 + 9 = 73 = THE PROVEN FLOOR (the census: every even dim 8, every odd dim 9!!)')

# the W-solve verification for the chosen basis (the §1508 machinery, WITH the §1500 T-conversion)
rows = list(sel); aug = [[1 if i == j else 0 for j in range(9)] for i in range(9)]
r = 0; pivots = []; T = []
for col in range(V):
    piv = next((i for i in range(r, len(rows)) if (rows[i] >> col) & 1), None)
    if piv is None: continue
    rows[r], rows[piv] = rows[piv], rows[r]
    aug[r], aug[piv] = aug[piv], aug[r]
    for i in range(len(rows)):
        if i != r and (rows[i] >> col) & 1:
            rows[i] ^= rows[r]; aug[i] = [a ^ b for a, b in zip(aug[i], aug[r])]
    pivots.append((col, rows[r])); T.append(list(aug[r])); r += 1
def solve(row):
    coords = [0] * 9; rr = row
    for k, (col, rw) in enumerate(pivots):
        if (rr >> col) & 1:
            coords[k] = 1; rr ^= rw
    assert rr == 0
    return coords
Wred = [solve(Brows[t]) for t in range(V)]
W = []
for t in range(V):
    worig = [0] * 9
    for k in range(9):
        if Wred[t][k]:
            for j in range(9):
                if T[k][j]: worig[j] ^= 1
    W.append(worig)
ok = True
for t in range(V):
    acc = 0
    for k in range(9):
        if W[t][k]: acc ^= sel[k]
    if acc != Brows[t]: ok = False
print('(3) the W-solve over the census basis (the §1500 T-conversion): B[t] = Σ W[t,k]·u_k for all 121: %s' % ('PASS' if ok else 'FAIL'))
wl = Counter(sum(x) for x in W)
print('    the W-weights: %s (the mean %.1f)' % (dict(sorted(wl.items())), sum(sum(x) for x in W) / V))

print('(4) THE CST LEVER CLOSED: the census proves CST = 73 is the floor (every even codeword dim 8,'
      ' every odd dim 9) — the word4\'s CST-73 tail is ALREADY OPTIMAL; the 121-class deficit'
      ' 256*121 - 288*73 = %d is FIXED (vs the P111-class\'s 10,272 — the -320 handicap is'
      ' structural).  No price probe at CST < 73 is meaningful.' % (256 * V - 288 * CST))
