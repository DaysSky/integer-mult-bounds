"""Current-format cost = sum_j dim span(P_j) = tr(sum_j Pi_Vj).  Check sum_j Pi_Vj (source spans) on several
decompositions: B0 (SAT), w10 pseudo-puncture (cost 72), P111 stars + 9 single-source corrections on full E8,
double-star + corrections.  Hypothesis: sum_j Pi_Vj >= 9 I (would give cost >= 72)."""
import numpy as np, itertools, random
from e8dec import A, G, v, solve
An = A / np.linalg.norm(A[0])
def proj(idx):
    if len(idx) == 0: return np.zeros((8, 8))
    U, S, Vt = np.linalg.svd(An[list(idx)], full_matrices=False); B = Vt[:(S > 1e-9).sum()]; return B.T @ B
def rep(name, Ps):
    S = sum(proj(p) for p in Ps); ev = np.linalg.eigvalsh(S)
    print('%-40s cost %d  eig(sum Pi_V) min %.3f max %.3f' % (name, sum(np.linalg.matrix_rank(An[list(p)]) if len(p) else 0 for p in Ps), ev.min(), ev.max()))
r = solve([(list(range(v)), list(range(v)))] * 9); rep('B0 9 pieces (SAT)', r[0])
# star decomposition on full E8: centres Z (affinely independent), pieces R(z_j) as sources + {z_j} corrections
N = ((G == 0) | np.eye(v, dtype=bool)).astype(np.uint8)
rng = random.Random(3)
def f2rank(M):
    M = (np.array(M) % 2).astype(np.uint8).copy(); r = 0
    for c in range(M.shape[1]):
        p = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
while True:
    Z = rng.sample(range(v), 9)
    if f2rank(N[Z]) == 9: break
stars = [[s for s in range(v) if N[z, s] and s != z] for z in Z]
rep('9 stars + 9 single-source corrections', stars + [[z] for z in Z])
rep('9 stars only (P111-type, live part)', stars)
