# Enumerate 2-hyperplane covers (F_a, F_b) of a section line set H (lines(H) = F_a u F_b, both rank r-1 flats).
# Decomposable quadrics in the vanishing space: pencil case solved via cubic det(U^T Q(l) U); general case via random
# restarts of an alternating projection.  Every reported split is verified exactly (ranks + closure + nondegeneracy).
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
LA = g.L.astype(float)
rng = np.random.default_rng(5)
def mask(ls): return sum(1 << u for u in ls)
def sect(lp):
    m = (1 << V) - 1
    for u in lp: m &= g.HYP[u]
    return bits(m)
def setup(H):
    X = LA[H]; U, S, Vt = np.linalg.svd(X); r = int((S > 1e-9).sum()); B = Vt[:r]
    C = X @ B.T
    mons = list(itertools.combinations_with_replacement(range(r), 2))
    A = np.array([[c[i] * c[j] * (1 if i == j else 2) for (i, j) in mons] for c in C])
    _, s, vt = np.linalg.svd(A)
    rkA = int((s > 1e-8 * s[0]).sum())
    N = vt[rkA:]
    def sym(v):
        Q = np.zeros((r, r))
        for k, (i, j) in enumerate(mons): Q[i, j] = Q[j, i] = v[k]
        return Q
    return C, r, [sym(v) for v in N]
def split_from_Q(H, C, Q):
    w, Vv = np.linalg.eigh(Q); idx = np.argsort(-np.abs(w))
    if abs(w[idx[2]]) > 1e-6 * abs(w[idx[0]]): return None
    s1, s2 = w[idx[0]], w[idx[1]]
    if s1 * s2 >= 0: return None
    v1, v2 = Vv[:, idx[0]], Vv[:, idx[1]]
    l1 = np.sqrt(abs(s1)) * v1 + np.sqrt(abs(s2)) * v2; l2 = np.sqrt(abs(s1)) * v1 - np.sqrt(abs(s2)) * v2
    Fa = [H[k] for k in range(len(H)) if abs(C[k] @ l1) < 1e-7 * np.linalg.norm(l1) * np.linalg.norm(C[k])]
    Fb = [H[k] for k in range(len(H)) if abs(C[k] @ l2) < 1e-7 * np.linalg.norm(l2) * np.linalg.norm(C[k])]
    if set(Fa) | set(Fb) != set(H): return None
    return tuple(sorted(Fa)), tuple(sorted(Fb))
def all_covers(H, tries=3000):
    C, r, Ns = setup(H)
    found = set()
    d = len(Ns)
    if d == 0: return r, 0, []
    for _ in range(tries):
        c = rng.normal(size=d)
        if d >= 2:
            # pencil through two random members; roots of det(U^T Q U) common to several U
            c2 = rng.normal(size=d)
            Qa = sum(ci * Ni for ci, Ni in zip(c, Ns)); Qb = sum(ci * Ni for ci, Ni in zip(c2, Ns))
            U = rng.normal(size=(r, 3))
            # det(U^T (Qa + l Qb) U) cubic in l
            ls = np.linspace(-3, 3, 7)
            vals = [np.linalg.det(U.T @ (Qa + l * Qb) @ U) for l in ls[:4]]
            coef = np.polyfit(ls[:4], vals, 3)
            for root in np.roots(coef):
                if abs(root.imag) > 1e-6: continue
                Q = Qa + root.real * Qb
                sp_ = split_from_Q(H, C, Q)
                if sp_: found.add(sp_)
        else:
            sp_ = split_from_Q(H, C, Ns[0])
            if sp_: found.add(sp_)
    return r, d, sorted(found)
if __name__ == '__main__':
    t = g.T(0, 1, 2)
    for u in (g.T(0, 1, 3), g.P(0, 3)):
        H = sect([t, u]); r, d, cov = all_covers(H, 600)
        print('section', g.supp[u], 'lines', len(H), 'null', d, 'covers', [(len(a), len(b), len(set(a) & set(b)), dim(mask(a)), dim(mask(b))) for a, b in cov])
