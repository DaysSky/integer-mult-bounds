"""Zero-pattern realisability (non-root-like allowed): vectors in R^{p,q}, norms^2 = 4 (norm +-2 after scaling),
<u,v> = 0 exactly on orthogonal pairs, |<u,v>| >= 0.3 on the others (soft margin).  Analytic-Jacobian LM."""
import numpy as np
from scipy.optimize import least_squares
def solve_zero(Bm, p, q, seed, iters=400, margin=0.3):
    n = len(Bm); h = p + q; eta = np.array([1.0]*p + [-1.0]*q)
    I0, J0 = np.nonzero(np.triu(Bm == 0, 1)); I1, J1 = np.nonzero(np.triu(Bm == 1, 1))
    def res(z):
        U = z.reshape(n, h); Ue = U*eta; nr = (U*Ue).sum(1)
        p0 = (U[I0]*Ue[J0]).sum(1); p1 = (U[I1]*Ue[J1]).sum(1)
        return np.concatenate([nr**2 - 4, p0, np.minimum(np.abs(p1) - margin, 0.0)])
    def jac(z):
        U = z.reshape(n, h); Ue = U*eta; nr = (U*Ue).sum(1)
        m0, m1 = len(I0), len(I1)
        Jm = np.zeros((n + m0 + m1, n*h))
        for a in range(n): Jm[a, a*h:(a+1)*h] = 4*nr[a]*Ue[a]
        r = n + np.arange(m0)
        for k in range(h):
            Jm[r, I0*h + k] = Ue[J0, k]; Jm[r, J0*h + k] = Ue[I0, k]
        p1 = (U[I1]*Ue[J1]).sum(1); act = (np.abs(p1) < margin).astype(float)*np.sign(p1)
        r = n + m0 + np.arange(m1)
        for k in range(h):
            Jm[r, I1*h + k] = act*Ue[J1, k]; Jm[r, J1*h + k] = act*Ue[I1, k]
        return Jm
    rng = np.random.default_rng(seed)
    sol = least_squares(res, rng.standard_normal(n*h)*0.7, jac=jac, method='lm', max_nfev=iters, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    r = res(sol.x); return float((r**2).sum()), sol.x
