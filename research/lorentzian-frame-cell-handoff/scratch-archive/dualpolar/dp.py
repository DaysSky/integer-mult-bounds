"""Dual polar graph DSp(6,2): Lagrangian 3-spaces of F_2^6 (symplectic form x1y4+x2y5+x3y6+x4y1+...).
Adjacent: dim(L cap L') = 2 (Grassmann distance 1); opposite: L cap L' = 0 (distance 3).  Frames by construction (m=3).
Computes: vertex/edge counts, distance distribution, max concurrent flow (LP) for opposite-pair demands (a random
opposite matching and all opposite pairs), and spectral/local-search sparse cuts -> cut/flow ratio (necessary for coding gain)."""
import itertools, numpy as np, sys
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix
n = 6
def form(x, y):
    a = [(x >> i) & 1 for i in range(6)]; b = [(y >> i) & 1 for i in range(6)]
    return (a[0]*b[3] + a[1]*b[4] + a[2]*b[5] + a[3]*b[0] + a[4]*b[1] + a[5]*b[2]) % 2
def span(vs):
    S = {0}
    for v in vs: S |= {s ^ v for s in S}
    return frozenset(S)
lag = set()
for a in range(1, 64):
    for b in range(a + 1, 64):
        for c in range(b + 1, 64):
            S = span([a, b, c])
            if len(S) == 8 and all(form(x, y) == 0 for x in S for y in S): lag.add(S)
L = sorted(lag, key=lambda s: sorted(s)); N = len(L)
def dist(A, B): return 3 - (len(A & B).bit_length() - 1)
D = np.array([[dist(A, B) for B in L] for A in L])
print('Lagrangians', N, 'degree', int((D == 1).sum(1)[0]), 'opposite per vertex', int((D == 3).sum(1)[0]), 'edges', int((D == 1).sum() // 2))
A = (D == 1).astype(float); Opp = (D == 3)
def sparsity(S, dem):
    S = np.asarray(S, bool)
    cut = A[S][:, ~S].sum(); dcross = dem[S][:, ~S].sum()
    return cut / dcross if dcross > 0 else np.inf
def best_cut(dem, iters=3000, seed=0):
    rng = np.random.default_rng(seed)
    Lap = np.diag(A.sum(1)) - A; w, Q = np.linalg.eigh(Lap)
    best = (np.inf, None)
    for k in range(1, 12):                         # sweep along low eigenvectors
        f = Q[:, k]; o = np.argsort(f)
        for cutpos in range(1, N):
            S = np.zeros(N, bool); S[o[:cutpos]] = True
            sp = sparsity(S, dem)
            if sp < best[0]: best = (sp, S.copy())
    S = best[1].copy(); cur = best[0]
    for it in range(iters):                        # single-vertex flips, accept improvements
        v = rng.integers(N); S[v] = ~S[v]; sp = sparsity(S, dem)
        if sp <= cur and 0 < S.sum() < N: cur = sp
        else: S[v] = ~S[v]
    return min(cur, best[0])
def flow(dem_pairs):
    """max concurrent flow, edge formulation per source (aggregate commodities by source)."""
    E = [(i, j) for i in range(N) for j in range(N) if i < j and A[i, j]]; m = len(E)
    srcs = sorted(set(s for s, t in dem_pairs)); k = len(srcs)
    dem = {s: [t for s2, t in dem_pairs if s2 == s] for s in srcs}
    # variables: f[s][e,dir] >=0 ; lambda ; maximize lambda
    nv = k * 2 * m + 1; lam = nv - 1
    rows = []; b = []
    Aeq = lil_matrix((k * N, nv)); beq = np.zeros(k * N)
    for si, s in enumerate(srcs):
        for ei, (u, v) in enumerate(E):
            for d_, (a_, b_) in enumerate(((u, v), (v, u))):
                col = si * 2 * m + 2 * ei + d_
                Aeq[si * N + a_, col] -= 1; Aeq[si * N + b_, col] += 1   # net inflow
        for t in dem[s]: Aeq[si * N + t, lam] -= 1                         # sinks receive lambda each
        Aeq[si * N + s, lam] += len(dem[s])                                 # source emits
    Aub = lil_matrix((m, nv)); bub = np.ones(m)
    for si in range(k):
        for ei in range(m):
            Aub[ei, si * 2 * m + 2 * ei] = 1; Aub[ei, si * 2 * m + 2 * ei + 1] = 1
    c = np.zeros(nv); c[lam] = -1
    r = linprog(c, A_ub=csr_matrix(Aub), b_ub=bub, A_eq=csr_matrix(Aeq), b_eq=beq, bounds=(0, None), method='highs')
    return -r.fun
rng = np.random.default_rng(1)
# demand set 1: all opposite pairs (symmetric)
dem_all = Opp.astype(float); lam_all = 945 / (Opp.sum() / 2 * 3)
print('all opposite pairs: flow (symmetric, exact) %.4f, best cut sparsity found %.4f, ratio %.3f' % (lam_all, best_cut(dem_all), best_cut(dem_all) / lam_all), flush=True)
# demand set 2: random opposite matching (each vertex in at most one session)
for trial in range(3):
    order = rng.permutation(N); used = set(); pairs = []
    for u in order:
        if u in used: continue
        cand = [v for v in np.nonzero(Opp[u])[0] if v not in used]
        if cand:
            v = rng.choice(cand); used |= {u, v}; pairs.append((int(u), int(v)))
    dem = np.zeros((N, N))
    for u, v in pairs: dem[u, v] = dem[v, u] = 1
    lam = flow(pairs); bc = best_cut(dem, seed=trial)
    print('opposite matching (%d sessions): flow %.4f, best cut %.4f, cut/flow %.3f' % (len(pairs), lam, bc, bc / lam), flush=True)
