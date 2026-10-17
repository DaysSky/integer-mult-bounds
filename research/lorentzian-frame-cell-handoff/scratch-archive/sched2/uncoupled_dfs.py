"""Exact DFS for split-free schedules with UNCOUPLED junction transforms (A on X_p, X_q; B on Y_p, Y_q; A, B in
SL2(Z) with entries in [-E, E]).  Pruning: s = 2K + 1 locals, the first cannot reduce rank(XX) + rank(YY) and the total
2K must be removed, so every later local must reduce it by exactly one.  usage: uncoupled_dfs.py K E"""
import sys, itertools
import numpy as np
K = int(sys.argv[1]); E = int(sys.argv[2]); s = 2 * K + 1; n = 2 * K
X = list(range(0, n, 2)); Y = list(range(1, n, 2))
SL = [np.array([[a, b], [c, d]], dtype=object) for a in range(-E, E + 1) for b in range(-E, E + 1)
      for c in range(-E, E + 1) for d in range(-E, E + 1) if a * d - b * c == 1]
def rk(M):
    import sympy
    return sympy.Matrix(M.tolist()).rank()
def rank_int(M):
    # exact rank over Q via fraction-free elimination on python ints
    A = [list(map(int, r)) for r in M]
    rows, cols = len(A), len(A[0]) if A else 0; r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f, g = A[i][c], A[r][c]
                A[i] = [g * x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
def pot(M):
    return rank_int(M[np.ix_(X, X)]) + rank_int(M[np.ix_(Y, Y)])
def loc(M, p, rev):
    M = M.copy()
    if rev: M[2 * p] = M[2 * p] - M[2 * p + 1]
    else: M[2 * p + 1] = M[2 * p + 1] + M[2 * p]
    return M
def junc(M, p, q, A, B):
    M = M.copy(); xp, xq, yp, yq = M[2 * p].copy(), M[2 * q].copy(), M[2 * p + 1].copy(), M[2 * q + 1].copy()
    M[2 * p] = A[0, 0] * xp + A[0, 1] * xq; M[2 * q] = A[1, 0] * xp + A[1, 1] * xq
    M[2 * p + 1] = B[0, 0] * yp + B[0, 1] * yq; M[2 * q + 1] = B[1, 0] * yp + B[1, 1] * yq
    return M
sols = []; nodes = 0
def dfs(M, b, prev, used, word, P):
    global nodes
    nodes += 1
    if b == s:
        if P == 0: sols.append(list(word)); print('FOUND', word, flush=True)
        return
    for p in range(min(K, used + 1)):            # canonical pair labelling
        if s - b < 2 * (K - max(used, p + 1)) : pass
        for rev in (False, True):
            if p == prev or prev is None:
                cands = [M]
                jl = [None]
            else:
                cands = []; jl = []
                for A in SL:
                    for B in SL:
                        cands.append(junc(M, prev, p, A, B)); jl.append((A.tolist(), B.tolist()))
            seen = set()
            for M1, j in zip(cands, jl):
                M2 = loc(M1, p, rev)
                key = M2.tobytes() if M2.dtype != object else str(M2.tolist())
                if key in seen: continue
                seen.add(key)
                P2 = pot(M2)
                need = 0 if prev is None else 1
                if P - P2 != need: continue
                dfs(M2, b + 1, p, max(used, p + 1), word + [(p, 'R' if rev else 'F', j)], P2)
M0 = np.array(np.eye(n, dtype=int), dtype=object)
dfs(M0, 0, None, 0, [], 2 * K)
print('K', K, 'E', E, '|SL|', len(SL), 'nodes', nodes, 'solutions', len(sols))
