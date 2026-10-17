"""Realisability of an orthogonality pattern in R^{p,q} with FREE products on non-orthogonal pairs (only zeros
enforced, norms fixed at 2, non-orthogonal products pushed away from 0 by a soft margin |<u,v>| >= 0.5).
E8 pattern = O^+(8,2) nonsingular points.  Control: (8,0)."""
import numpy as np, sys
from scipy.optimize import least_squares
sys.path.insert(0, '.')
from qreal import points
X, Bm = points('plus-ns'); n = len(Bm)
p, q = int(sys.argv[1]), int(sys.argv[2]); h = p + q; eta = np.array([1.0]*p + [-1.0]*q)
iu = np.triu_indices(n, 1); Bv = Bm[iu]; I, J = iu
def res(z):
    U = z.reshape(n, h); G = (U*eta) @ U.T; off = G[iu]
    r_orth = np.where(Bv == 0, off, 0.0)
    r_marg = np.where(Bv == 1, np.minimum(np.abs(off) - 0.5, 0.0), 0.0)
    return np.concatenate([np.diag(G)**2 - 4, r_orth, r_marg])
best = 1e9
for seed in range(int(sys.argv[3]) if len(sys.argv) > 3 else 6):
    rng = np.random.default_rng(seed)
    sol = least_squares(res, rng.standard_normal(n*h), method='trf', max_nfev=3000, xtol=1e-14, ftol=1e-14, gtol=1e-14)
    r2 = float((res(sol.x)**2).sum()); best = min(best, r2)
    print('(%d,%d) seed %d residual^2 %.3g' % (p, q, seed, r2), flush=True)
    if r2 < 1e-12: break
print('best', best)
