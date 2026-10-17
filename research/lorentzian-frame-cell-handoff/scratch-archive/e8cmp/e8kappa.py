# Compare: dimension of quadrics vanishing on the lines of E8 sections (D6 = cell perp, E6 = A2 perp, E7 = t perp).
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
L = np.array(e8.LINES, dtype=float)
G = L @ L.T
def qnull(idx):
    X = L[idx]; U, S, Vt = np.linalg.svd(X); r = int((S > 1e-9).sum()); C = X @ Vt[:r].T
    mons = list(itertools.combinations_with_replacement(range(r), 2))
    A = np.array([[c[i] * c[j] for (i, j) in mons] for c in C]); s = np.linalg.svd(A, compute_uv=False)
    return r, len(mons) - int((s > 1e-8 * s[0]).sum())
t = 0
perp = lambda S: [u for u in range(len(L)) if all(abs(G[u, s]) < 1e-9 for s in S)]
E7 = perp([t]); print('E7 lines', len(E7), 'rank/quadric null', qnull(E7))
e = next(u for u in E7); D6 = perp([t, e]); print('D6 (cell perp) lines', len(D6), qnull(D6))
a = next(u for u in range(len(L)) if abs(abs(G[t, u]) - 2) < 1e-9)   # inner product +-1 in normalized units (roots norm 8)
E6 = perp([t, a]); print('E6 (A2 perp) lines', len(E6), qnull(E6))
