"""Max number of I_{11,1} lines in a nondegenerate subspace of each rank r (lower bounds from structured families:
spans of line subsets drawn from sections, flats, apex D's, D10, I10, t-perps, and closures of their pairwise
intersections)."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G; LA = np.array(g.LA, dtype=float)
eta = np.array([1.0] * 11 + [-1.0])
def closure_info(mask):
    idx = np.nonzero(mask)[0]
    B = LA[idx]; r = int(np.linalg.matrix_rank(B))
    # closure: all lines in span
    U, sv, Vt = np.linalg.svd(B.T, full_matrices=False)
    Q = U[:, :r]
    proj = LA @ Q @ Q.T if r else np.zeros_like(LA)
    inspan = np.all(np.abs(proj - LA) < 1e-8, axis=1)
    # nondegeneracy of span: Gram of an orthonormal (Euclidean) basis under eta
    if r:
        Gm = Q.T @ np.diag(eta) @ Q; nd = abs(np.linalg.det(Gm)) > 1e-9
    else: nd = True
    return r, int(inspan.sum()), nd
OM = np.array([[i != j and G[i, j] == 0 for j in range(V)] for i in range(V)])
best = {}
def consider(mask):
    r, n, nd = closure_info(mask)
    if nd and n > best.get(r, (0,))[0]: best[r] = (n,)
for p in range(V):
    consider(OM[p])
    for q in range(p + 1, V):
        if OM[p, q]: consider(OM[p] & OM[q])
for k in range(3, 11):
    for S in list(itertools.combinations(range(11), k))[:300]:
        S = set(S); consider(np.array([set(g.supp[u]) <= S for u in range(V)]))
print('max lines found per rank (nondegenerate):', sorted((r, v[0]) for r, v in best.items()))
