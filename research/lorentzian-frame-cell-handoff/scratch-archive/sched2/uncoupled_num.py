"""Split-free schedules with UNCOUPLED junction transforms diag(A, B) (A on the two X registers, B on the two Y
registers of the consecutive pairs).  Numeric feasibility: least squares on the XX and YY blocks of the middle product,
det(A)^2 = det(B)^2 = 1.  usage: uncoupled_num.py K restarts"""
import sys, itertools
import numpy as np
from scipy.optimize import least_squares
K = int(sys.argv[1]); NR = int(sys.argv[2]); s = 2 * K + 1; n = 2 * K
rng = np.random.default_rng(1)
def loc(p, rev):
    M = np.eye(n)
    if rev: M[2 * p, 2 * p + 1] = -1      # X_p -= Y_p
    else: M[2 * p + 1, 2 * p] = 1         # Y_p += X_p
    return M
def junc(p, q, A, B):
    M = np.eye(n)
    for (i, j), a in np.ndenumerate(A): M[2 * (p, q)[i], 2 * (p, q)[j]] = a
    for (i, j), b in np.ndenumerate(B): M[2 * (p, q)[i] + 1, 2 * (p, q)[j] + 1] = b
    return M
X = list(range(0, n, 2)); Y = list(range(1, n, 2))
def seqs():
    for sq in itertools.product(range(K), repeat=s):
        # canonical: pairs appear in order of first use, all pairs used
        firsts = []
        for p in sq:
            if p not in firsts: firsts.append(p)
        if firsts != list(range(K)): continue
        yield sq
found = []
tot = 0
for sq in seqs():
    nj = sum(1 for b in range(1, s) if sq[b] != sq[b - 1])
    for fr in itertools.product((False, True), repeat=s):
        tot += 1
        def res(z):
            M = loc(sq[0], fr[0]); k = 0; r = []
            for b in range(1, s):
                if sq[b] != sq[b - 1]:
                    A = z[8 * k:8 * k + 4].reshape(2, 2); B = z[8 * k + 4:8 * k + 8].reshape(2, 2); k += 1
                    M = junc(sq[b - 1], sq[b], A, B) @ M
                    r += [np.linalg.det(A) ** 2 - 1, np.linalg.det(B) ** 2 - 1]
                M = loc(sq[b], fr[b]) @ M
            r += list(M[np.ix_(X, X)].ravel()) + list(M[np.ix_(Y, Y)].ravel())
            return np.array(r)
        best = None
        for _ in range(NR):
            z0 = rng.normal(size=8 * nj) * 1.5
            try: sol = least_squares(res, z0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=4000)
            except Exception: continue
            c = np.max(np.abs(sol.fun)) if len(sol.fun) else 0
            if best is None or c < best[0]: best = (c, sol.x)
            if c < 1e-9: break
        if best and best[0] < 1e-9:
            found.append((sq, fr, best[1]))
            print('FOUND', sq, ''.join('R' if f else 'F' for f in fr), np.round(best[1], 4), flush=True)
print('K', K, 'systems', tot, 'feasible', len(found))
