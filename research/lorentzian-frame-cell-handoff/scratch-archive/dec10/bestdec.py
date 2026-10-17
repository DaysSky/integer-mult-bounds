"""Min-cost decomposition of an F2 decoder B (v x v) into rank(B) totals: B = sum_j Q_j x P_j with {P_j} a basis of the
row space and {Q_j} the dual basis of the column space; cost_j = rank G[Q_j, P_j] (Theorem C, met by one copy).
Exhaustive over which deficient codewords (span <= 7) are used; random completions for the rest."""
import sys, itertools, random, numpy as np
from e8dec import A, G, v
def f2_solve_basis(M):
    """row-reduce: return list of independent rows (as np arrays) spanning rowspace of M."""
    M = (np.array(M) % 2).astype(np.uint8); rows = []; piv = []
    R = M.copy(); r = 0
    for c in range(R.shape[1]):
        p = [i for i in range(r, R.shape[0]) if R[i, c]]
        if not p: continue
        R[[r, p[0]]] = R[[p[0], r]]
        for i in range(R.shape[0]):
            if i != r and R[i, c]: R[i] ^= R[r]
        piv.append(c); r += 1
    return R[:r], piv
def inv2(M):
    n = len(M); X = np.concatenate([M % 2, np.eye(n, dtype=np.uint8)], 1).astype(np.uint8)
    for c in range(n):
        p = [i for i in range(c, n) if X[i, c]]
        if not p: return None
        X[[c, p[0]]] = X[[p[0], c]]
        for i in range(n):
            if i != c and X[i, c]: X[i] ^= X[c]
    return X[:, n:]
def rk(idx_a, idx_b):
    if len(idx_a) == 0 or len(idx_b) == 0: return 0
    return int(np.linalg.matrix_rank(A[idx_a] @ A[idx_b].T))
def analyse(B, trials=2000, seed=0):
    rng = random.Random(seed)
    Ub, _ = f2_solve_basis(B)            # rows: basis of row space S (w x v)
    w = len(Ub)
    # W: coefficients with B = Wc @ Ub ; solve via pivots
    _, piv = f2_solve_basis(B)
    Ub_piv = Ub[:, piv]                   # w x w, identity after RREF
    Wc = B[:, piv] % 2                    # since Ub is RREF with identity at piv: B = Wc @ Ub
    assert ((Wc @ Ub) % 2 == B % 2).all()
    span = lambda idx: np.linalg.matrix_rank(A[idx]) if len(idx) else 0
    # deficient codewords of S (m vectors) and of T (n vectors): P = m^T Ub, Q = Wc n
    defS = []; defT = []
    for bits in itertools.product((0, 1), repeat=w):
        m = np.array(bits, np.uint8)
        if not m.any(): continue
        P = np.nonzero((m @ Ub) % 2)[0]
        if span(P) <= 7: defS.append((m, P, span(P)))
        Q = np.nonzero((Wc @ m) % 2)[0]
        if span(Q) <= 7: defT.append((m, Q, span(Q)))
    print('w', w, 'deficient in S:', [(len(P), d) for _, P, d in defS], ' in T:', [(len(Q), d) for _, Q, d in defT])
    # random dual-basis decompositions biased to include deficient vectors: M columns m_j, dual n_j = rows of M^{-1}
    best = None
    cand_m = [m for m, _, _ in defS]; cand_n = [n for n, _, _ in defT]
    for it in range(trials):
        cols = []
        pool_m = cand_m[:]; rng.shuffle(pool_m)
        for m in pool_m:
            if rng.random() < 0.9:
                X = np.array(cols + [m]); 
                if len(f2_solve_basis(X)[0]) == len(cols) + 1: cols.append(m)
        while len(cols) < w:
            m = np.array([rng.randint(0, 1) for _ in range(w)], np.uint8)
            X = np.array(cols + [m])
            if len(f2_solve_basis(X)[0]) == len(cols) + 1: cols.append(m)
        M = np.array(cols).T % 2                 # w x w, columns m_j
        Mi = inv2(M)
        if Mi is None: continue
        # pieces: P_j = (M[:, j]^T Ub), Q_j = Wc @ Mi^T[:, j]  (dual: Mi rows)
        cost = 0; costs = []
        for j in range(w):
            P = np.nonzero((M[:, j] @ Ub) % 2)[0]; Q = np.nonzero((Wc @ Mi[j, :]) % 2)[0]
            c = rk(Q, P); costs.append(c); cost += c
        if best is None or cost < best[0]: best = (cost, costs)
    print('best sampled decomposition cost', best)
    return best
if __name__ == '__main__':
    B = np.load(sys.argv[1]) % 2
    analyse(B, int(sys.argv[2]) if len(sys.argv) > 2 else 500)
