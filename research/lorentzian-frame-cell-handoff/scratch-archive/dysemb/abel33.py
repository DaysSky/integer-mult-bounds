"""Abelian frame embedding of the 33-vertex network: M_v in R^{m x m}, rank(M_v - M_u) <= 1 on every edge (weighted by
capacity), M_t - M_s = I on every message.  Alternating projection, random restarts.  usage: abel33.py m restarts iters seed"""
import pickle, sys, time, numpy as np
d = pickle.load(open('net33.pkl', 'rb')); V = d['V']; idx = {v: i for i, v in enumerate(V)}
E = [(idx[u], idx[v], c) for (u, v), c in d['cap'].items()]; S = [(idx[a], idx[b]) for a, b in d['msgs']]
m, R, IT, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
n = len(V); I = np.eye(m); lam = 1.0
L = np.zeros((n, n))
for u, v, c in E: L[u, u] += c; L[v, v] += c; L[u, v] -= c; L[v, u] -= c
for s, t in S: L[s, s] += lam; L[t, t] += lam; L[s, t] -= lam; L[t, s] -= lam
Linv = np.linalg.inv(L[1:, 1:])
Eu = np.array([u for u, v, c in E]); Ev = np.array([v for u, v, c in E]); Ec = np.array([c for u, v, c in E], float)
Ss = np.array([s for s, t in S]); St = np.array([t for s, t in S])
def solveM(T):
    rhs = np.zeros((n, m, m))
    np.add.at(rhs, Ev, Ec[:, None, None] * T); np.add.at(rhs, Eu, -Ec[:, None, None] * T)
    np.add.at(rhs, St, lam * I); np.add.at(rhs, Ss, -lam * I)
    M = np.zeros((n, m, m)); M[1:] = np.einsum('ij,jkl->ikl', Linv, rhs[1:]); return M
def proj(Dm):
    U, sv, Vt = np.linalg.svd(Dm)
    return sv[:, 0, None, None] * np.einsum('ni,nj->nij', U[:, :, 0], Vt[:, 0, :]), (Ec * (sv[:, 1:] ** 2).sum(1)).sum()
rng = np.random.default_rng(seed); best = np.inf; t0 = time.time()
for r in range(R):
    M = rng.standard_normal((n, m, m)) * 2
    for it in range(IT):
        T, off = proj(M[Ev] - M[Eu]); M = solveM(T)
    T, off = proj(M[Ev] - M[Eu]); serr = ((M[St] - M[Ss] - I) ** 2).sum(); res = np.sqrt(off + serr)
    if res < best: best = res; print('restart', r, 'edge off-rank %.3e session %.3e total %.3e (%.0fs)' % (off, serr, res, time.time() - t0), flush=True)
    if res < 1e-9: np.save('abel33_m%d_s%d.npy' % (m, seed), M); print('SOLUTION'); break
print('best %.3e' % best)
