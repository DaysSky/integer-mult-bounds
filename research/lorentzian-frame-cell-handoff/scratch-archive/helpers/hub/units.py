"""Exact line systems used by the S3 screens (integer coordinates, exact Gram matrices).

Every unit is returned as (L, G, name) with L an integer v x n matrix of line representatives and G the exact integer
Gram matrix of the unit's bilinear form (diagonal 2).  The F2 decoder pattern of #595 is: B_TT = 1 and B_TS = 0 whenever
G_TS != 0 (non-orthogonal lines); the entries at orthogonal pairs are free.

Families
  * ADE root systems A_n, D_n, E6, E7, E8 (doubled coordinates, G = L L^T / 4).
    E6 is the root lines orthogonal to an A2 = <a, b>, a = (1/2)^8, b = e1 + e2 (a.b = 1), as in #630;
    the archived #620 screen used b = e1 - e2 (a.b = 0), which gives D6.
  * Triple family T_h (upstream 03-motifs.tex, bit construction): the C(h,3) indicator vectors t_T of 3-subsets of [h]
    with the form I - J/9, so G_ST = |S n T| - 1 (diagonal 2).
  * Lorentzian I_{n,1} (n odd, #634 note 3): e_A + e_{n+1} (|A| = 3) and e_i - e_j, Lorentz form diag(1^n, -1).
"""
import itertools

import numpy as np


def roots_A(n):
    R = []
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            r = [0] * (n + 1); r[i] = 2; r[j] = -2; R.append(r)
    return np.array(R, dtype=np.int64)


def roots_D(n):
    R = []
    for i in range(n):
        for j in range(i + 1, n):
            for s in (1, -1):
                r = [0] * n; r[i] = 2; r[j] = 2 * s; R.append(r)
    return np.array(R, dtype=np.int64)


def roots_E8():
    """120 lines, doubled coordinates: +-2e_i +-2e_j (one sign class per line) and (+-1)^8 with an even number of
    minus signs and first coordinate +1."""
    R = [list(r) for r in roots_D(8)]
    for sg in itertools.product((1, -1), repeat=8):
        if sg[0] == 1 and sg.count(-1) % 2 == 0:
            R.append(list(sg))
    return np.array(R, dtype=np.int64)


def perp(R, w):
    return R[(R @ np.asarray(w, dtype=np.int64)) == 0]


A_VEC = np.ones(8, dtype=np.int64)                     # (1/2)^8 doubled
B_E6 = np.array([2, 2, 0, 0, 0, 0, 0, 0])              # e1 + e2 doubled; a.b = 4/4 = 1  -> A2 with a
B_D6 = np.array([2, -2, 0, 0, 0, 0, 0, 0])             # e1 - e2 doubled; a.b = 0         -> A1 + A1 (archived "E6")


def roots_E7():
    return perp(roots_E8(), A_VEC)


def roots_E6():
    return perp(perp(roots_E8(), A_VEC), B_E6)


def roots_D6_archived():
    return perp(perp(roots_E8(), A_VEC), B_D6)


def gram_doubled(L):
    G4 = L @ L.T
    assert (G4 % 4 == 0).all()
    G = G4 // 4
    assert (np.diag(G) == 2).all()
    return G


def triple_family(h):
    """lines t_T, T in C([h],3); G_ST = |S n T| - 1 (form I - J/9)."""
    T = list(itertools.combinations(range(h), 3))
    M = np.zeros((len(T), h), dtype=np.int64)
    for i, t in enumerate(T):
        M[i, list(t)] = 1
    G = M @ M.T - 1
    return M, G, T


def lorentz_family(n):
    """I_{n,1}: e_A + e_{n+1} (|A| = 3) and e_i - e_j; Lorentz Gram; binary labels: A, resp. [n] minus {i, j}."""
    vecs, labels = [], []
    for A in itertools.combinations(range(n), 3):
        v = [0] * (n + 1)
        for a in A:
            v[a] = 1
        v[n] = 1
        vecs.append(v); labels.append([1 if i in A else 0 for i in range(n)])
    for i, j in itertools.combinations(range(n), 2):
        v = [0] * (n + 1); v[i] = 1; v[j] = -1
        vecs.append(v); labels.append([0 if k in (i, j) else 1 for k in range(n)])
    L = np.array(vecs, dtype=np.int64)
    Q = np.diag([1] * n + [-1]).astype(np.int64)
    G = L @ Q @ L.T
    return L, G, np.array(labels, dtype=np.int64)


# ------------------------------------------------------------------ exact linear algebra
def rank_q(rows):
    """exact rank over Q (fraction-free Bareiss-style elimination on Python ints)."""
    import math
    red = []
    for r in rows:
        r = [int(x) for x in r]
        for pc, rr in red:
            if r[pc]:
                f, g = r[pc], rr[pc]
                r = [g * x - f * y for x, y in zip(r, rr)]
                c = math.gcd(*r)
                if c > 1:
                    r = [x // c for x in r]
        pc = next((j for j, x in enumerate(r) if x), None)
        if pc is not None:
            red.append((pc, r))
    return len(red)


def rank_mod_p(M, p):
    """rank of an integer matrix over F_p (p prime)."""
    A = (np.array(M, dtype=object) % p).tolist()
    rk, rows, cols = 0, len(A), len(A[0]) if A else 0
    for c in range(cols):
        piv = next((i for i in range(rk, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        inv = pow(A[rk][c], p - 2, p)
        A[rk] = [(x * inv) % p for x in A[rk]]
        for i in range(rows):
            if i != rk and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk


def f2_rank(M):
    rows = [int(''.join('1' if x & 1 else '0' for x in row[::-1]) or '0', 2) for row in np.asarray(M)]
    basis = {}
    for x in rows:
        while x:
            hb = x.bit_length() - 1
            if hb in basis:
                x ^= basis[hb]
            else:
                basis[hb] = x
                break
    return len(basis)


def gram_rank(G, idx):
    """rank over Q of the principal block G[idx, idx] (= pairing rank of span(idx) with itself)."""
    if len(idx) == 0:
        return 0
    return rank_q(G[np.ix_(idx, idx)].tolist())


def nonorth_clique(G):
    """exact maximum set of pairwise non-orthogonal lines (identity block of the pattern => minrank lower bound)."""
    import networkx as nx
    v = len(G)
    H = nx.Graph()
    H.add_nodes_from(range(v))
    H.add_edges_from((i, j) for i in range(v) for j in range(i + 1, v) if G[i, j] != 0)
    best, _ = nx.max_weight_clique(H, weight=None)
    return sorted(best)


def _query(args):
    solver, v, pattern, c, clique = args
    out = solver(v, pattern, None, c, 'none', clique)
    if out['result'] == 'SAT':
        B = out['B']
        assert all(B[i, i] == 1 for i in range(v)) and all(B[i, j] == 0 for i, j in pattern)
    return out['result'], out['sec']


def minrank_f2(G, clique, cmax, solver=None, timeout=300):
    """exact F_2 minrank of the pattern of G (B_TT = 1, B_TS = 0 where G_TS != 0), asymmetric decoders allowed.
    Asks SAT for c = |clique|, |clique| + 1, ... < cmax; each query fixes the GL(c, F_2) gauge U_K = W_K = [I | 0] on
    the clique K (solve_asym of #595's minrank_sat.py; a SAT answer is re-checked on the returned B).  A query that does
    not finish within `timeout` seconds is recorded as 'TIMEOUT' and the search stops there.
    Returns (lo, hi, log): the minrank lies in [lo, hi]; lo == hi when it is determined (hi = cmax is attained by a
    known decoder)."""
    import multiprocessing as mp
    v = len(G)
    pattern = [(i, j) for i in range(v) for j in range(v) if i != j and G[i, j] != 0]
    log = {}
    lo = len(clique)
    ctx = mp.get_context('fork')
    for c in range(len(clique), cmax):
        with ctx.Pool(1) as pool:
            res = pool.apply_async(_query, ((solver, v, pattern, c, list(clique)),))
            try:
                r, sec = res.get(timeout)
            except mp.TimeoutError:
                log[c] = ('TIMEOUT', timeout)
                pool.terminate()
                return lo, cmax, log
        log[c] = (r, sec)
        if r == 'SAT':
            return c, c, log
        lo = c + 1
    return cmax, cmax, log
