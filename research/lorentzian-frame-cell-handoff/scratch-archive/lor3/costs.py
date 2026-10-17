"""Bit and complex copy costs (label/functional decoders, matroid greedy) for an extended Lorentzian unit.
Bit: decoder P = J + Bbar over F2 (binary rows (1, class)); totals = F2 functionals phi; gathers {S: phi(b_S)=1};
     beta = Q-rank of gathered real labels.  Greedy over all F2 functionals (2^c), F2-independent basis.
Complex: decoder = real Gram (rank h); totals = real functionals f (candidates: eta r_U, coordinate axes);
     gathers {S: f(r_S) != 0}; beta = F2-rank of gathered binary labels; greedy Q-independent basis."""
import json, sys, itertools, numpy as np
d = json.load(open(sys.argv[1])); eta = np.array(d['eta']); R = np.array(d['R']); S = np.array(d['S'], dtype=np.int64)
v = len(R)
Bbin = np.hstack([np.ones((v, 1), dtype=np.int64), S]) % 2          # binary labels, P = Bbin Bbin^T mod 2 (eta = I mod 2)
def f2rank(M):
    M = (M % 2).astype(np.uint8).copy(); r = 0
    for c in range(M.shape[1]):
        p = np.flatnonzero(M[r:, c]) if r < M.shape[0] else []
        if len(p) == 0: continue
        p = p[0] + r; M[[r, p]] = M[[p, r]]
        rows = np.flatnonzero(M[:, c]); rows = rows[rows != r]; M[rows] ^= M[r]
        r += 1
        if r == M.shape[0]: break
    return r
qrank = lambda A: np.linalg.matrix_rank(A, tol=1e-8) if len(A) else 0
# ---- bit side: totals phi in the row space of Bbin (combinations of labels); gathered g = Bbin phi
P = (Bbin @ Bbin.T) % 2; cP = f2rank(P); nb = Bbin.shape[1]
# basis of row space of Bbin
rowsp = []
for r in Bbin:
    if f2rank(np.array(rowsp + [r])) > len(rowsp): rowsp.append(r)
    if len(rowsp) == f2rank(Bbin): break
rowsp = np.array(rowsp)
cands = []
for coef in itertools.product((0, 1), repeat=len(rowsp)):
    c = np.array(coef)
    if not c.any(): continue
    phi = (c @ rowsp) % 2
    g = (Bbin @ phi) % 2
    if not g.any(): continue
    cands.append((qrank(R[g == 1]), tuple(g)))
cands.sort()
basis = []; cost = 0
for beta, g in cands:
    if f2rank(np.array(basis + [g])) > len(basis):
        basis.append(g); cost += beta
        if len(basis) == cP: break
print('BIT: rank P =', cP, 'totals', len(basis), 'cst =', cost, 'x = %.4f' % (cost / v), 'window', qrank(R))
# ---- complex side: real functionals
h = qrank(R)
fc = [eta @ r for r in R] + [np.eye(len(eta))[i] for i in range(len(eta))]
cc = []
for f in fc:
    g = np.abs(R @ f) > 1e-9
    if g.any(): cc.append((f2rank(Bbin[g]), f))
cc.sort(key=lambda z: z[0])
basis = []; cost = 0
for beta, f in cc:
    M = np.array(basis + [f])
    # independence relative to the label space: functionals restricted to span(R)
    if qrank(M @ R.T) > len(basis):
        basis.append(f); cost += beta
        if len(basis) == h: break
print('COMPLEX: c =', len(basis), 'cst =', cost, 'x = %.4f' % (cost / v), 'binary window', f2rank(Bbin))
