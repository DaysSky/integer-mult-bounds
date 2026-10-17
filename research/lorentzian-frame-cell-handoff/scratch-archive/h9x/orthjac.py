"""E8 orthogonality pattern (O+(8,2) nonsingular) in R^{p,q}: zeros on orthogonal pairs, norms in {+2,-2}
(residual G_ii^2 - 4) or +2, non-orthogonal products free.  Analytic-Jacobian LM, several seeds."""
import numpy as np, sys
from scipy.optimize import least_squares
sys.path.insert(0, '.')
from qreal import points
X, Bm = points('plus-ns'); n = len(Bm)
p, q, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; h = p + q; eta = np.array([1.0]*p + [-1.0]*q)
I, J = np.nonzero(np.triu(Bm == 0, 1)); m = len(I)
def res(z):
    U = z.reshape(n, h); Ue = U*eta
    nr = (U*Ue).sum(1)
    r0 = nr**2 - 4 if mode == 'pm' else nr - 2
    r1 = (U[I]*Ue[J]).sum(1)
    return np.concatenate([r0, r1])
def jac(z):
    U = z.reshape(n, h); Ue = U*eta; nr = (U*Ue).sum(1)
    Jm = np.zeros((n + m, n*h))
    f = (4*nr if mode == 'pm' else 2*np.ones(n))
    for a in range(n): Jm[a, a*h:(a+1)*h] = f[a]*Ue[a]
    rows = n + np.arange(m)
    for k in range(h):
        Jm[rows, I*h + k] = Ue[J, k]; Jm[rows, J*h + k] = Ue[I, k]
    return Jm
best = 1e9
for seed in range(int(sys.argv[4])):
    rng = np.random.default_rng(seed)
    sol = least_squares(res, rng.standard_normal(n*h)*0.7, jac=jac, method='lm', max_nfev=600, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    r = res(sol.x); r2 = float((r**2).sum()); best = min(best, r2)
    U = sol.x.reshape(n, h); G = (U*eta) @ U.T
    nonorth = np.abs(G[np.triu(Bm == 1, 1)])
    print('(%d,%d,%s) seed %d residual^2 %.3g; non-orth |product| min %.3g; timelike lines %d' % (p, q, mode, seed, r2, nonorth.min(), (np.diag(G) < 0).sum()), flush=True)
    if r2 < 1e-12: np.save('e8pat_%d%d_%s.npy' % (p, q, mode), U); break
