import numpy as np, sys
from adj import ip
L = np.load(sys.argv[1]); C = np.load(sys.argv[2])
V = L[C]
G = ip(V, V)
n = len(V)
off = G[~np.eye(n, dtype=bool)]
print('lines', n, 'norms', sorted(set(np.diag(G).tolist())), 'offdiag values', sorted(set(off.tolist()))[:20], '...max', abs(off).max())
assert all((g == 0) or (g % 2) for g in off), 'even nonzero inner product!'
# window = rank over Q of the vectors (in true coords): use doubled coords -> rank same
M = np.hstack([V[:, :8].astype(float)/2, V[:, 8:].astype(float)])
print('window (Q-rank)', np.linalg.matrix_rank(M))
def rank2(M):
    M = M.copy() % 2; r = 0; rows, cols = M.shape
    for c in range(cols):
        p = [i for i in range(r, rows) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(rows):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
        if r == rows: break
    return r
B = (1 + G) % 2
print('rank_F2(J+G)', rank2(B.astype(np.int64)))
print('orth degree per line: min/mean/max', *(lambda d: (d.min(), d.mean(), d.max()))((G == 0).sum(1) - 0))
