"""Root-like realizability (LM, equality-only) of F2 quadric point sets: vectors u_a in R^{p,q} (h = p+q) with
<u_a,u_a> = 2, <u_a,u_b> = 0 if B(a,b) = 0, (<u_a,u_b>)^2 = 1 if B(a,b) = 1.
Sets: 'plus-ns' = O+(8,2) nonsingular (120, E8 control at (8,0)); 'minus-s' = O-(8,2) singular (119, frame-free
extremal at h = 9); 'minus-ns' = O-(8,2) nonsingular (136); 'plus-s' (135)."""
import numpy as np, sys, itertools, time
PM = False
from scipy.optimize import least_squares
def qform(kind):
    if kind == 'plus':
        return lambda x: (x[0]&x[1]) ^ (x[2]&x[3]) ^ (x[4]&x[5]) ^ (x[6]&x[7])
    return lambda x: (x[0]&x[1]) ^ (x[2]&x[3]) ^ (x[4]&x[5]) ^ x[6] ^ (x[6]&x[7]) ^ x[7]
def points(name):
    typ, sing = name.split('-')
    q = qform(typ)
    pts = [x for x in itertools.product((0, 1), repeat=8) if any(x) and q(x) == (0 if sing == 's' else 1)]
    X = np.array(pts)
    Bm = np.zeros((len(pts), len(pts)), dtype=int)
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            c = tuple(u ^ v for u, v in zip(a, b))
            Bm[i, j] = q(c) ^ q(a) ^ q(b)
    return X, Bm
def solve(Bm, p, qn, seed, iters=2000):
    n = len(Bm); h = p + qn; eta = np.array([1.0] * p + [-1.0] * qn)
    iu = np.triu_indices(n, 1); B = Bm[iu]
    rng = np.random.default_rng(seed)
    def res(z):
        U = z.reshape(n, h); G = (U * eta) @ U.T
        off = G[iu]
        r1 = np.where(B == 0, off, off * off - 1)
        r0 = np.diag(G)**2 - 4 if PM else np.diag(G) - 2
        return np.concatenate([r0, r1])
    I, J = iu
    def jac(z):
        U = z.reshape(n, h); G = (U * eta) @ U.T; off = G[iu]
        m = len(I); Jm = np.zeros((n + m, n * h))
        Ue = U * eta
        dg = (U * Ue).sum(1)
        for a in range(n): Jm[a, a * h:(a + 1) * h] = (4 * dg[a] if PM else 2) * Ue[a]
        f = np.where(B == 0, 1.0, 2 * off)[:, None]
        rows = n + np.arange(m)
        for k in range(h):
            Jm[rows, I * h + k] = f[:, 0] * Ue[J, k]
            Jm[rows, J * h + k] = f[:, 0] * Ue[I, k]
        return Jm
    z0 = rng.standard_normal(n * h) * 0.8
    sol = least_squares(res, z0, jac=jac, method='lm', max_nfev=iters, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    r = res(sol.x); return float((r ** 2).sum()), sol.x
if __name__ == '__main__':
    name = sys.argv[1]; p, qn = int(sys.argv[2]), int(sys.argv[3]); seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    X, Bm = points(name)
    deg0 = (Bm == 0).sum(1) - 1
    print(name, 'points', len(Bm), 'orth-degree', set(deg0.tolist()), 'signature', (p, qn), flush=True)
    for s in range(seeds):
        t = time.time(); r2, z = solve(Bm, p, qn, s)
        print('  seed %d residual^2 %.4g (%.0fs)' % (s, r2, time.time() - t), flush=True)
        if r2 < 1e-8:
            np.save('%s_%d_%d_sol.npy' % (name, p, qn), z); break
