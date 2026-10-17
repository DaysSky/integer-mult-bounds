"""Exact decoder cost of a row space S (rows of B): matroid greedy over all 2^dim - 1 vectors of S, cost of a
vector = real rank of the span of its support lines (same convention as h10/deccost.py).  usage: scost.py B.npy"""
import sys, numpy as np, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
def coord(x):
    v = np.zeros(12)
    s = g.supp[x]
    if g.kind[x] == 'P': v[s[0]] = 1; v[s[1]] = -1
    else: v[11] = 1; v[list(s)] = 1
    return v
C = np.array([coord(x) for x in range(V)])
Gc = C[:, :11] @ C[:, :11].T - np.outer(C[:, 11], C[:, 11])
assert ((Gc != 0) == (g.G != 0)).all(), 'coordinates do not reproduce the orthogonality pattern'
def rref(A):
    A = A.copy() % 2; r = 0
    for col in range(A.shape[1]):
        p = next((i for i in range(r, A.shape[0]) if A[i, col]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, col]: A[i] ^= A[r]
        r += 1
    return A[:r]
def cost_of_space(S):
    k = S.shape[0]
    vecs = []
    for m in range(1, 2 ** k):
        coeff = np.array([(m >> i) & 1 for i in range(k)])
        v = (coeff @ S) % 2
        rk = np.linalg.matrix_rank(C[v.astype(bool)])
        vecs.append((rk, int(v.sum()), m, v))
    vecs.sort(key=lambda t: (t[0], t[1]))
    basis = []; cost = 0; chosen = []
    for rk, w, m, v in vecs:
        if rref(np.array(basis + [v])).shape[0] > len(basis):
            basis.append(v); cost += rk; chosen.append((rk, w))
            if len(basis) == k: break
    return cost, chosen, collections_count([t[0] for t in vecs])
def collections_count(a):
    import collections; return sorted(collections.Counter(a).items())
if __name__ == '__main__':
    B = np.load(sys.argv[1]).astype(np.int64)
    S = rref(B)
    cost, chosen, dist = cost_of_space(S)
    print('dim', S.shape[0], 'cost', cost, 'pieces (rank, weight)', chosen)
    print('rank distribution of all nonzero vectors', dist)
