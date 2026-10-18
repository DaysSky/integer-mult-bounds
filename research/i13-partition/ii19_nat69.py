"""THE EXTENSION-WORD BUILD STAGE 1 (ii19_nat69.py) — the delivery census (the v=120!!).

THE TARGET: the v=120 extension word (nat67's system!!) at (120, 8, R ~ 276!!) — the
frontier-shape model price **+45.94%**!! THE JUDGE: gcheck.py (the control PASS ✓✓!!).
HERE: (1) THE DECODER (the 120-system's perp-pattern rank (the 9?!)) + THE 9-GATHER BASIS
+ THE W-SOLVE (the scatter rows!!); (2) THE FRAMES (the P111-format (h=8!!): the
singletons + the t-perps (the nondegenerate Grams!!)); (3) THE ECONOMY MAP (nat67's
pieces/carriers + the per-target read-structure!!); (4) THE EMISSION SPEC (ii19_nat69_spec.json!!).
"""
import os, sys, itertools, json
from collections import Counter, defaultdict
import numpy as np
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

E67 = json.load(open('ii19_nat67_ext120.json', 'rt'))
lines = [tuple(x) for x in E67['lines']]
V = len(lines)
H = 8
log('(0) THE EXTENSION SYSTEM: v %d | the ranks' % V)
G = [[sum(a[i] * b[i] for i in range(8)) for b in lines] for a in lines]
log('    the norms: %s (the raw!!)' % dict(sorted(Counter(G[s][s] for s in range(V)).items())))
PERP = [set(s for s in range(V) if s != t and G[s][t] == 0) for t in range(V)]
log('    the perps: %s' % dict(sorted(Counter(len(p) for p in PERP).items())))

# (1) THE DECODER + THE W!!
B0 = np.array([[1 if (s == t or s in PERP[t]) else 0 for s in range(V)] for t in range(V)], dtype=np.uint8)
def gf2_rank(M):
    M = M.copy(); rr = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(rr, rows) if M[i][c]), None)
        if p is None: continue
        M[[rr, p]] = M[[p, rr]]
        for i in range(rows):
            if i != rr and M[i][c]:
                M[i] ^= M[rr]
        rr += 1
    return rr
rank_B = gf2_rank(B0)
log('(1) THE DECODER RANK: %d (the nat67: 9!!)' % rank_B)
M2 = np.concatenate([B0.copy(), np.eye(V, dtype=np.uint8)], axis=1)
rr = 0; piv_rows = {}
for c in range(V):
    p = next((i for i in range(rr, V) if M2[i][c]), None)
    if p is None: continue
    M2[[rr, p]] = M2[[p, rr]]
    piv_rows[c] = rr
    for i in range(V):
        if i != rr and M2[i][c]:
            M2[i] ^= M2[rr]
    rr += 1
BASIS_IDX = [(c, [i for i in range(V) if M2[r][V + i]]) for c, r in piv_rows.items()]
BASM = np.array([np.bitwise_xor.reduce(B0[list(o)], axis=0) if len(o) > 1 else B0[o[0]]
                 for c, o in BASIS_IDX])
W = np.zeros((V, len(BASIS_IDX)), dtype=np.uint8)
for t in range(V):
    for k, (c, o) in enumerate(BASIS_IDX):
        if B0[t][c]:
            W[t][k] = 1
chk = (W.astype(int) @ BASM.astype(int) % 2 == B0).all()
wpw = Counter(int(x) for x in W.sum(axis=1))
log('    the basis: %d | THE W-SOLVE: %s | the W-weights: %s' % (
    len(BASIS_IDX), bool(chk), dict(sorted(wpw.items()))))
# the gathers' VALUES (the line-sets!!)
for k, (c, o) in enumerate(BASIS_IDX):
    val = np.bitwise_xor.reduce(B0[list(o)], axis=0) if len(o) > 1 else B0[o[0]]
    log('    the gather %d (pivot %d, %d rows): %d lines' % (k, c, len(o), int(val.sum())))

# (2) THE FRAMES (the P111-format (h=8!!)): 0 = empty, 1 = FULL, the singletons, the t-perps!!
def rref(rows, n):
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
def gram_det(basis):
    n = len(basis)
    A = [[sum(basis[i][k2] * basis[j][k2] for k2 in range(8)) for j in range(n)] for i in range(n)]
    A = [[Fraction(x) for x in row] for row in A]
    det = Fraction(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return Fraction(0)
        if p != c:
            A[c], A[p] = A[p], A[c]; det = -det
        det *= A[c][c]
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return det
# the t-perp frames: the 7-dim perp-SPACES (the normals' complements (the nondegenerate!!))
def perp_basis(t):
    al = list(lines[t])
    # the nullspace of [al] (7-dim!!)
    piv = next((c for c in range(8) if al[c] != 0), None)
    ns = []
    for f in range(8):
        if f == piv: continue
        v = [Fraction(0)] * 8
        v[f] = Fraction(1)
        v[piv] = -Fraction(al[f], al[piv])
        ns.append(v)
    return ns
frames = [[]]
frames.append([[1 if i == j else 0 for j in range(8)] for i in range(8)])   # FULL
fidx_full = 1
SINGLE = []
for s in range(V):
    frames.append([[int(x) for x in lines[s]]])
    SINGLE.append(len(frames) - 1)
TPERP = []
ndeg = 0
for t in range(V):
    b = perp_basis(t)
    if gram_det(b) == 0:
        ndeg += 1
        continue
    frames.append([[int(x) for x in row] for row in b])
    TPERP.append(len(frames) - 1)
log('(2) THE FRAMES: FULL + %d singletons + %d t-perps (the nondegenerate %d/%d!!)' % (
    V, len(TPERP), V - ndeg, V))
if ndeg:
    log('    !! the degenerate perps: %d (the basis-fix needed!!)' % ndeg)
json.dump({'lines': [list(l) for l in lines], 'frames': frames, 'SINGLE': SINGLE,
           'TPERP': TPERP, 'W': W.tolist(), 'BASIS_IDX': [(c, o) for c, o in BASIS_IDX],
           'PERP': [sorted(p) for p in PERP]},
          open('ii19_nat69_spec.json', 'w'))
log('(4) saved ii19_nat69_spec.json (the emission spec!!)')
