"""Equality-only orthogonal representation (real, signature (p,q)): <x_a,x_b> = 0 on required-orthogonal pairs,
<x_a,x_a> = s_a.  LM with analytic sparse Jacobian.  Returns residual and X; faithfulness (non-orth products away from 0)
is checked separately."""
import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import csr_matrix
def solve(Orth, h, neg, signs=None, seed=0, iters=400, X0=None):
    n = len(Orth); eta = np.array([1.0]*(h-neg) + [-1.0]*neg)
    iu, ju = np.triu_indices(n, 1); mo = Orth[iu, ju]
    A = np.concatenate([iu[mo], np.arange(n)]); Bv = np.concatenate([ju[mo], np.arange(n)])
    s = np.concatenate([np.zeros(mo.sum()), np.full(n, 2.0) if signs is None else 2.0*np.asarray(signs, float)])
    m = len(A)
    rows = np.repeat(np.arange(m), 2*h)
    cols = np.concatenate([(A[:, None]*h + np.arange(h)), (Bv[:, None]*h + np.arange(h))], 1).ravel()
    def res(z):
        X = z.reshape(n, h); return ((X[A]*eta)*X[Bv]).sum(1) - s
    def jac(z):
        X = z.reshape(n, h); Y = X*eta
        data = np.concatenate([Y[Bv], Y[A]], 1).ravel()
        return csr_matrix((data, (rows, cols)), shape=(m, n*h))
    rng = np.random.default_rng(seed)
    z0 = rng.normal(size=n*h)/np.sqrt(h) if X0 is None else X0.ravel()
    out = least_squares(res, z0, jac=jac, method='trf', tr_solver='lsmr', max_nfev=iters, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    X = out.x.reshape(n, h)
    G = (X*eta) @ X.T
    nonorth = ~Orth & ~np.eye(n, dtype=bool)
    mn = np.abs(G[nonorth]).min() if nonorth.any() else np.inf
    return float((out.fun**2).sum()), X, mn
