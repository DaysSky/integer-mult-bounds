import numpy as np, random, itertools
from e8dec import A, G, v, pairing_rank
from bestdec import f2_solve_basis, inv2
An = A / np.linalg.norm(A[0])
def proj(idx):
    if len(idx) == 0: return np.zeros((8, 8))
    U, S, Vt = np.linalg.svd(An[idx], full_matrices=False); B = Vt[:(S > 1e-9).sum()]; return B.T @ B
B = np.load('B_w10_nz1.npy') % 2
Ub, piv = f2_solve_basis(B); w = len(Ub); Wc = B[:, piv] % 2
span = lambda idx: np.linalg.matrix_rank(A[idx]) if len(idx) else 0
defS = [np.array(b, np.uint8) for b in itertools.product((0, 1), repeat=w) if any(b) and span(np.nonzero((np.array(b) @ Ub) % 2)[0]) <= 7]
rng = random.Random(0); best = None
for it in range(3000):
    cols = []
    for m in defS:
        X = np.array(cols + [m])
        if len(f2_solve_basis(X)[0]) == len(cols) + 1: cols.append(m)
    while len(cols) < w:
        m = np.array([rng.randint(0, 1) for _ in range(w)], np.uint8)
        if len(f2_solve_basis(np.array(cols + [m]))[0]) == len(cols) + 1: cols.append(m)
    M = np.array(cols).T % 2; Mi = inv2(M)
    P = [list(np.nonzero((M[:, j] @ Ub) % 2)[0]) for j in range(w)]; Q = [list(np.nonzero((Wc @ Mi[j]) % 2)[0]) for j in range(w)]
    cost = sum(pairing_rank(p, q) for p, q in zip(P, Q))
    if best is None or cost < best[0]: best = (cost, P, Q)
    if cost <= 72: break
cost, P, Q = best
PU = [proj(q) for q in Q]; PV = [proj(p) for p in P]
psi = np.array([sum(An[t] @ PU[j] @ PV[j] @ An[t] for j in range(w)) for t in range(v)])
print('cost', cost, 'piece costs', [pairing_rank(p, q) for p, q in zip(P, Q)], 'sum tr', round(sum(np.trace(PU[j] @ PV[j]) for j in range(w)), 3))
print('psi values', sorted(set(np.round(psi, 3))))
S = sum(PU[j] @ PV[j] for j in range(w)); print('eigen/sv of sum PU PV:', np.round(np.linalg.svd(S)[1], 3))
