"""Real Grassmannian relaxation: U_v (10x5 orthonormal) for 182 vertices; edges need dim(U_u cap U_v) >= 4
(4 principal angles = 0); sessions need U_s, U_t complementary (all principal angles > 0).
Alternating projection: K_e = best common 4-space of each edge; U_v = top-5 eigenspace of sum_e P_{K_e} - mu * sum_sessions P_{U_partner}.
Report edge residual (sum of 4 smallest sin^2) and min over sessions of the smallest singular value of [U_s U_t].
usage: realgrass.py m restarts iters mu seed"""
import pickle, sys, time, numpy as np
d0 = pickle.load(open('net33.pkl', 'rb')); VV = d0['V']; ix = {v: i for i, v in enumerate(VV)}; E = [(ix[u], ix[v]) for (u, v), c in d0['cap'].items() for _ in range(1)]; S = [(ix[a], ix[b]) for a, b in d0['msgs']]
m, R, IT, mu, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
n = 2 * m; V = len(VV); rng = np.random.default_rng(seed)
inc = [[] for _ in range(V)]; ses = [[] for _ in range(V)]
for k, (u, v) in enumerate(E): inc[u].append(k); inc[v].append(k)
for s, t in S: ses[s].append(t); ses[t].append(s)
def orth(A): q, _ = np.linalg.qr(A); return q[:, :m]
def edge_stats(U):
    res = 0.0; K = []
    for u, v in E:
        M = U[u].T @ U[v]; Y, sv, Zt = np.linalg.svd(M)       # cos of principal angles = sv (desc)
        res += (1 - sv[:m - 1] ** 2).sum()
        P = U[u] @ Y[:, :m - 1]; Q = U[v] @ Zt.T[:, :m - 1]
        K.append(orth(P + Q)[:, :m - 1] if m > 1 else None)
    return res, K
def ses_min(U):
    return min(np.linalg.svd(np.hstack([U[s], U[t]]), compute_uv=False)[-1] for s, t in S)
best = None; t0 = time.time()
for r in range(R):
    U = [orth(rng.standard_normal((n, m))) for _ in range(V)]
    for it in range(IT):
        res, K = edge_stats(U)
        newU = []
        for v in range(V):
            A = np.zeros((n, n))
            for k in inc[v]: A += K[k] @ K[k].T
            for w in ses[v]: A -= mu * U[w] @ U[w].T
            wv, Q = np.linalg.eigh(A); newU.append(Q[:, -m:])
        U = newU
    res, _ = edge_stats(U); sm = ses_min(U)
    print('restart %d edge residual %.3e  min session singular value %.3e  (%.0fs)' % (r, res, sm, time.time() - t0), flush=True)
    if best is None or res < best[0]: best = (res, sm)
    if res < 1e-10 and sm > 1e-3: pickle.dump(U, open('realgrass_m%d_s%d.pkl' % (m, seed), 'wb')); print('SOLUTION'); break
print('best', best)
