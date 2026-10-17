"""Abelian frame embedding of the Braverman-He network: M_v in R^{m x m} (182 vertices),
rank(M_v - M_u) <= 1 on the 735 physical edges, M_t - M_s = I on the 157 sessions.
Alternating projection: (a) best rank-1 approximation of every edge difference, (b) weighted Laplacian least squares
for M (25 entries decouple).  usage: abel.py m restarts iters seed"""
import pickle, sys, time, numpy as np
b = pickle.load(open('../bh/bh.pkl', 'rb')); E = b['phys']; S = b['sessions']
m, R, IT, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
nV = 182; I = np.eye(m); lam = 1.0
# Laplacian over edges + sessions (gauge: vertex 0 fixed to 0)
L = np.zeros((nV, nV))
for u, v in E: L[u, u] += 1; L[v, v] += 1; L[u, v] -= 1; L[v, u] -= 1
for s, t in S: L[s, s] += lam; L[t, t] += lam; L[s, t] -= lam; L[t, s] -= lam
Lr = L[1:, 1:]; Linv = np.linalg.inv(Lr)
Eu = np.array([u for u, v in E]); Ev = np.array([v for u, v in E]); Ss = np.array([s for s, t in S]); St = np.array([t for s, t in S])
def solveM(T):
    # minimise sum_e |M_v - M_u - T_e|^2 + lam sum_q |M_t - M_s - I|^2 ; rhs per entry
    rhs = np.zeros((nV, m, m))
    np.add.at(rhs, Ev, T); np.add.at(rhs, Eu, -T)
    np.add.at(rhs, St, lam * I); np.add.at(rhs, Ss, -lam * I)
    M = np.zeros((nV, m, m)); M[1:] = np.einsum('ij,jkl->ikl', Linv, rhs[1:]); return M
def proj(Dm):
    U, s, Vt = np.linalg.svd(Dm)
    return s[:, 0, None, None] * np.einsum('ni,nj->nij', U[:, :, 0], Vt[:, 0, :]), (s[:, 1:] ** 2).sum()
rng = np.random.default_rng(seed); best = np.inf; t0 = time.time()
for r in range(R):
    M = rng.standard_normal((nV, m, m)) * 2
    for it in range(IT):
        T, off = proj(M[Ev] - M[Eu]); M = solveM(T)
    T, off = proj(M[Ev] - M[Eu]); serr = ((M[St] - M[Ss] - I) ** 2).sum()
    res = np.sqrt(off + serr)
    if res < best: best = res; print('restart', r, 'edge-offrank %.3e session %.3e total %.3e (%.0fs)' % (off, serr, res, time.time() - t0), flush=True)
    if res < 1e-9: np.save('abel_m%d_s%d.npy' % (m, seed), M); print('SOLUTION'); break
print('best %.3e' % best)
