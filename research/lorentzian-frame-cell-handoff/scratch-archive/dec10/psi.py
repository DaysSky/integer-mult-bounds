"""psi(t) = sum_j <P_Uj t, P_Vj t> for decompositions; check if = 9 (would give cost >= tr = 72 via rank >= trace)."""
import numpy as np, random
from e8dec import A, G, v, solve, pairing_rank
from bestdec import f2_solve_basis, inv2
An = A / np.sqrt(2)
def proj(idx):
    if len(idx) == 0: return np.zeros((8, 8))
    M = An[idx]; U, S, Vt = np.linalg.svd(M, full_matrices=False); r = (S > 1e-9).sum(); B = Vt[:r]
    return B.T @ B
def report(name, P, Q):
    PU = [proj(q) for q in Q]; PV = [proj(p) for p in P]
    psi = np.array([sum(An[t] @ PU[j] @ PV[j] @ An[t] for j in range(len(P))) for t in range(v)])
    tr = sum(np.trace(PU[j] @ PV[j]) for j in range(len(P)))
    cost = sum(pairing_rank(p, q) for p, q in zip(P, Q))
    print('%-22s cost %d  sum tr(PU PV) %.3f  psi min %.3f max %.3f mean %.3f' % (name, cost, tr, psi.min(), psi.max(), psi.mean()))
# B0 via SAT control
r = solve([(list(range(v)), list(range(v)))] * 9); report('B0 (SAT, 9 pieces)', *r)
# window-10 decoder: random dual bases
B = np.load('B_w10_nz1.npy') % 2
Ub, piv = f2_solve_basis(B); w = len(Ub); Wc = B[:, piv] % 2
rng = random.Random(1)
for trial in range(3):
    while True:
        M = np.array([[rng.randint(0, 1) for _ in range(w)] for _ in range(w)], np.uint8)
        Mi = inv2(M)
        if Mi is not None: break
    P = [list(np.nonzero((M[:, j] @ Ub) % 2)[0]) for j in range(w)]; Q = [list(np.nonzero((Wc @ Mi[j]) % 2)[0]) for j in range(w)]
    report('w10 random gauge %d' % trial, P, Q)
