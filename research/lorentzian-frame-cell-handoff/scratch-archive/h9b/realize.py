"""Numerical faithful orthogonal representation: vectors x_a in R^{p,q} (p+q = h) with <x_a,x_b> = 0 iff pattern says
orthogonal (a != b), |<x_a,x_b>| >= DELTA otherwise, <x_a,x_a> = sign_a * 2.  LM (least_squares, analytic sparse jac).
realize(Orth (bool matrix, True = must be orthogonal), h, neg, signs=None, seeds, delta) -> best residual^2, X."""
import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import csr_matrix
def realize(Orth, h, neg=1, signs=None, seeds=3, delta=0.3, maxfev=3000, X0=None, rng=None):
    n = len(Orth)
    eta = np.array([1.0]*(h-neg) + [-1.0]*neg)
    iu, ju = np.triu_indices(n, 1)
    mo = Orth[iu, ju]; io, jo = iu[mo], ju[mo]; inn, jnn = iu[~mo], ju[~mo]
    s = np.full(n, 2.0) if signs is None else 2.0*np.asarray(signs, float)
    A = np.concatenate([io, np.arange(n), inn]); Bv = np.concatenate([jo, np.arange(n), jnn])
    m = len(A)
    rows = np.repeat(np.arange(m), 2*h)
    cols = np.concatenate([(A[:, None]*h + np.arange(h)), (Bv[:, None]*h + np.arange(h))], 1).ravel()
    n1, n2 = len(io), n
    def res(z):
        X = z.reshape(n, h); Y = X*eta
        p = (Y[A]*X[Bv]).sum(1)
        r = p.copy(); r[n1:n1+n2] -= s
        q = p[n1+n2:]; r[n1+n2:] = np.minimum(0, np.abs(q) - delta)
        return r
    def jac(z):
        X = z.reshape(n, h); Y = X*eta
        w = np.ones(m)
        q = (Y[A[n1+n2:]]*X[Bv[n1+n2:]]).sum(1)
        w[n1+n2:] = np.where(np.abs(q) < delta, np.sign(q), 0.0)
        dA = Y[Bv]*w[:, None]; dB = Y[A]*w[:, None]
        data = np.concatenate([dA, dB], 1).ravel()
        J = csr_matrix((data, (rows, cols)), shape=(m, n*h))
        return J
    best = (np.inf, None)
    rng = rng or np.random.default_rng(1)
    for sd in range(seeds):
        z0 = rng.normal(size=n*h) if X0 is None or sd > 0 else X0.ravel()
        out = least_squares(res, z0, jac=jac, method='trf', max_nfev=maxfev, xtol=1e-13, ftol=1e-13, gtol=1e-13,
                            x_scale='jac')
        r = (out.fun**2).sum()
        if r < best[0]: best = (r, out.x.reshape(n, h))
        if r < 1e-14: break
    return best
