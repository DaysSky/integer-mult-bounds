"""Decoder feasibility for a fixed piece family on I_{11,1} (current format: cost = sum of real ranks of the pieces'
spans; nondegenerate closure checked separately).  Target t is served iff e_t|N'(t) is in the F2 span of the pieces'
indicators restricted to N'(t) = {t} u NO(t).  Row weight = min over solutions of |sum of chosen pieces| (enumerated
over the solution coset when small)."""
import itertools, numpy as np
n = 11
LINES = []
for i, j in itertools.combinations(range(n), 2):
    x = [0]*(n+1); x[i], x[j] = 1, -1; LINES.append(('P', (i, j), x))
for t in itertools.combinations(range(n), 3):
    x = [0]*(n+1)
    for i in t: x[i] = 1
    x[n] = 1; LINES.append(('T', t, x))
V = np.array([l[2] for l in LINES]); v = len(V)
eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T
NO = (G % 2 == 1)               # non-orthogonal (odd product), diagonal False (norm 2)
IDX = {(l[0], l[1]): k for k, l in enumerate(LINES)}
def rank_of(idx):
    return int(np.linalg.matrix_rank(V[list(idx)].astype(float))) if len(idx) else 0
def gram_det_nonzero(idx):
    M = V[list(idx)].astype(float)
    # nondegenerate span? compute Gram of a basis of the span
    U, s, Wt = np.linalg.svd(M, full_matrices=False); r = int((s > 1e-9).sum()); B = Wt[:r]
    g = (B*eta) @ B.T
    return abs(np.linalg.det(g)) > 1e-9
def perm_line(k, p):
    typ, pts, _ = LINES[k]
    q = tuple(sorted(p[a] for a in pts))
    return IDX[(typ, q)]
def f2_solve(A, b):
    """Solve A x = b over F2 (A: m x k uint8).  Returns (particular or None, nullspace basis list)."""
    A = A.copy() % 2; b = b.copy() % 2; m, k = A.shape
    M = np.concatenate([A, b[:, None]], 1).astype(np.uint8)
    piv = []; r = 0
    for c in range(k):
        p = next((i for i in range(r, m) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(m):
            if i != r and M[i, c]: M[i] ^= M[r]
        piv.append(c); r += 1
        if r == m: break
    if any(M[i, k] for i in range(r, m)): return None, []
    x = np.zeros(k, np.uint8)
    for i, c in enumerate(piv): x[c] = M[i, k]
    free = [c for c in range(k) if c not in piv]
    null = []
    for f in free:
        z = np.zeros(k, np.uint8); z[f] = 1
        for i, c in enumerate(piv): z[c] = M[i, f]
        null.append(z)
    return x, null
def check(pieces, maxnull=14, want_rows=True):
    """pieces: list of index lists.  Returns (all_served, n_unserved, row weights list or None)."""
    P = np.zeros((len(pieces), v), np.uint8)
    for j, S in enumerate(pieces): P[j, list(S)] = 1
    bad = 0; rows = []
    for t in range(v):
        Np = [t] + list(np.nonzero(NO[t])[0])
        A = P[:, Np].T; b = np.zeros(len(Np), np.uint8); b[0] = 1
        x, null = f2_solve(A, b)
        if x is None: bad += 1; continue
        if want_rows:
            best = None
            if len(null) <= maxnull:
                for mask in range(1 << len(null)):
                    z = x.copy()
                    for i in range(len(null)):
                        if mask >> i & 1: z ^= null[i]
                    w = int(((z @ P) % 2).sum())
                    if best is None or w < best: best = w
            else:
                best = int(((x @ P) % 2).sum())
            rows.append(best)
    return bad == 0, bad, rows
