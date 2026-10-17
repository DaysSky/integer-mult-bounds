"""Numerical search for orthogonal representations over C (bilinear form) of a graph:
find r_a in C^h with r_a . r_b = 0 on edges, r_a . r_a = 1.  Levenberg-Marquardt (scipy trf, sparse Jacobian)."""
import numpy as np, sys, time
from scipy.optimize import least_squares
from scipy.sparse import coo_matrix
def solve(n, edges, h, seed=0, real=False, iters=200, x0=None):
    rng = np.random.default_rng(seed)
    E = np.array(edges); ne = len(E)
    nv = 2*h if not real else h
    def unpack(z):
        Z = z.reshape(n, nv)
        return (Z[:, :h], Z[:, h:]) if not real else (Z, np.zeros_like(Z))
    def res(z):
        X, Y = unpack(z)
        a, b = E[:, 0], E[:, 1]
        re = (X[a]*X[b]).sum(1) - (Y[a]*Y[b]).sum(1)
        im = (X[a]*Y[b]).sum(1) + (Y[a]*X[b]).sum(1)
        nre = (X*X).sum(1) - (Y*Y).sum(1) - 1
        nim = 2*(X*Y).sum(1)
        out = [re, nre] if real else [re, im, nre, nim]
        return np.concatenate(out)
    def jac(z):
        X, Y = unpack(z)
        a, b = E[:, 0], E[:, 1]
        rows, cols, vals = [], [], []
        r0 = 0
        ar = np.arange(ne)
        def put(rr, vv, cc_base, which):
            # rr: residual idx array (ne,), vv: (ne,h) values, cc_base: vertex idx array, which: 0 for X block, 1 for Y block
            for k in range(h):
                rows.append(rr); cols.append(cc_base*nv + which*h + k); vals.append(vv[:, k])
        # re = Xa.Xb - Ya.Yb
        put(r0 + ar, X[b], a, 0); put(r0 + ar, X[a], b, 0)
        if not real:
            put(r0 + ar, -Y[b], a, 1); put(r0 + ar, -Y[a], b, 1)
        r0 += ne
        if not real:
            # im = Xa.Yb + Ya.Xb
            put(r0 + ar, Y[b], a, 0); put(r0 + ar, X[b], a, 1); put(r0 + ar, Y[a], b, 0); put(r0 + ar, X[a], b, 1)
            r0 += ne
        av = np.arange(n)
        put(r0 + av, 2*X, av, 0)
        if not real: put(r0 + av, -2*Y, av, 1)
        r0 += n
        if not real:
            put(r0 + av, 2*Y, av, 0); put(r0 + av, 2*X, av, 1); r0 += n
        R = np.concatenate(rows); C = np.concatenate(cols); V = np.concatenate(vals)
        return coo_matrix((V, (R, C)), shape=(r0, n*nv)).tocsr()
    z0 = rng.standard_normal(n*nv) / np.sqrt(h) if x0 is None else x0
    t = time.time()
    sol = least_squares(res, z0, jac=jac, method='trf', tr_solver='lsmr', max_nfev=iters, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    r = res(sol.x)
    return float(np.sqrt((r**2).sum())), sol.x, time.time() - t
if __name__ == '__main__':
    from quadgraph import nonsingular
    m, e, h = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    real = len(sys.argv) > 4 and sys.argv[4] == 'real'
    P, Bm = nonsingular(m, e)
    n = len(P)
    edges = [(i, j) for i in range(n) for j in range(i+1, n) if Bm[i, j] == 0]
    print('n', n, 'edges', len(edges), 'h', h, 'real' if real else 'complex', flush=True)
    for seed in range(int(sys.argv[5]) if len(sys.argv) > 5 else 3):
        r, x, t = solve(n, edges, h, seed=seed, real=real, iters=int(sys.argv[6]) if len(sys.argv) > 6 else 300)
        print('seed', seed, 'residual %.3e' % r, '%.0fs' % t, flush=True)
