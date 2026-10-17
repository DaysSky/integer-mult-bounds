"""Zero-pattern realisability of the nonsingular points of O^eps(8,2): find nonzero-norm vectors in R^{p,q}
(p + q = 9 or 8) with <v_a, v_b> = 0 exactly when omega(a, b) = 0, and |<v_a, v_b>| >= margin otherwise.
Control: eps = +, R^{8,0} must recover E8 (residual ~ 0).  usage: realize.py eps p q margin seeds iters"""
import sys, itertools, numpy as np
from scipy.optimize import least_squares
import scipy.sparse as sp
eps, p, q, margin, seeds, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
n = 4
def omega(a, b): return sum(((a >> (2 * i)) & 1) * ((b >> (2 * i + 1)) & 1) + ((a >> (2 * i + 1)) & 1) * ((b >> (2 * i)) & 1) for i in range(n)) % 2
def Q(a):   # hyperbolic pairs x_i y_i, plus (for minus type) x_3^2 + x_3 y_3 + y_3^2 on the last pair
    s = 0
    for i in range(n):
        x, y = (a >> (2 * i)) & 1, (a >> (2 * i + 1)) & 1
        s += x * y if (eps == '+' or i < n - 1) else (x + x * y + y)
    return s % 2
pts = [a for a in range(1, 256) if Q(a) == 1]
N = len(pts)
Om = np.array([[omega(a, b) for b in pts] for a in pts])
zero_pairs = [(i, j) for i in range(N) for j in range(i + 1, N) if Om[i, j] == 0]
non_pairs = [(i, j) for i in range(N) for j in range(i + 1, N) if Om[i, j] == 1]
print('eps', eps, 'nonsingular points', N, 'orthogonal pairs', len(zero_pairs), 'non-orthogonal', len(non_pairs), flush=True)
d = p + q; sig = np.array([1.0] * p + [-1.0] * q)
zi = np.array(zero_pairs); ni = np.array(non_pairs)
def res(x):
    V = x.reshape(N, d); W = V * sig
    r1 = np.einsum('ij,ij->i', V[zi[:, 0]], W[zi[:, 1]])
    nr = np.einsum('ij,ij->i', V, W)
    r2 = np.abs(nr) - 2.0          # |norm| = 2 (sign free)
    pr = np.abs(np.einsum('ij,ij->i', V[ni[:, 0]], W[ni[:, 1]]))
    r3 = np.minimum(pr - margin, 0.0)
    return np.concatenate([r1, r2, r3])
def jac(x):
    V = x.reshape(N, d); W = V * sig
    nr = np.einsum('ij,ij->i', V, W); pr = np.einsum('ij,ij->i', V[ni[:, 0]], W[ni[:, 1]])
    rows, cols, vals = [], [], []
    m1 = len(zi)
    k = np.arange(m1)
    for (a, b) in ((0, 1), (1, 0)):
        for c in range(d):
            rows.append(k); cols.append(zi[:, a] * d + c); vals.append(W[zi[:, b], c])
    ka = np.arange(N) + m1
    for c in range(d):
        rows.append(ka); cols.append(np.arange(N) * d + c); vals.append(2 * np.sign(nr) * W[:, c])
    act = (np.abs(pr) - margin) < 0
    kn = np.arange(len(ni)) + m1 + N
    sg = np.sign(pr) * act
    for (a, b) in ((0, 1), (1, 0)):
        for c in range(d):
            rows.append(kn); cols.append(ni[:, a] * d + c); vals.append(sg * W[ni[:, b], c])
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(m1 + N + len(ni), N * d))
best = None
for s in range(seeds):
    rng = np.random.default_rng(s)
    x0 = rng.normal(size=N * d) * 0.6
    sol = least_squares(res, x0, jac=jac, max_nfev=iters, xtol=1e-15, ftol=1e-15, gtol=1e-15, tr_solver='lsmr')
    r = res(sol.x); val = float(r @ r)
    V = sol.x.reshape(N, d); W = V * sig; nr = np.einsum('ij,ij->i', V, W)
    print('seed %d residual^2 %.3e  (orth part %.2e, norm part %.2e, margin part %.2e)  timelike lines %d' % (s, val,
          float(r[:len(zi)] @ r[:len(zi)]), float(r[len(zi):len(zi) + N] @ r[len(zi):len(zi) + N]), float(r[len(zi) + N:] @ r[len(zi) + N:]),
          int((nr < 0).sum())), flush=True)
    if best is None or val < best[0]: best = (val, sol.x)
np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/ominus/best_%s_%d%d.npy' % (eps, p, q), best[1])
print('best residual^2 %.3e' % best[0], flush=True)
