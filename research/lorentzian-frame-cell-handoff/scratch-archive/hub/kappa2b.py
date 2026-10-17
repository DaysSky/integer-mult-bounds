# Find 2-hyperplane covers of section line sets (existence = proof; exact verification of the split).
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
P, T = g.P, g.T
LA = g.L.astype(float)
rng = np.random.default_rng(3)
def sect(lp):
    m = (1 << V) - 1
    for u in lp: m &= g.HYP[u]
    return bits(m)
def mask(ls): return sum(1 << u for u in ls)
def find_split(H, tries=400):
    X = LA[H]; U, S, Vt = np.linalg.svd(X); r = int((S > 1e-9).sum()); B = Vt[:r]
    C = X @ B.T                                   # coordinates in span(H)
    mons = list(itertools.combinations_with_replacement(range(r), 2))
    A = np.array([[c[i] * c[j] * (1 if i == j else 2) for (i, j) in mons] for c in C])
    # null space of A (quadrics vanishing on all lines)
    _, s, vt = np.linalg.svd(A); nd = int((s < 1e-9).sum()) + max(0, len(mons) - len(s))
    Nsp = vt[len(s) - int((s < 1e-9).sum()):] if nd else None
    if nd == 0: return r, 0, None
    best = None
    for _ in range(tries):
        # try hyperplane 1 = span of r-1 random lines chosen greedily from a random order; test the rest
        order = rng.permutation(len(H))
        basis = []; 
        for i in order:
            M = np.array([C[j] for j in basis + [i]])
            if np.linalg.matrix_rank(M, 1e-9) == len(basis) + 1: basis.append(i)
            if len(basis) == r - 1: break
        n = np.linalg.svd(np.array([C[j] for j in basis]))[2][-1]
        part1 = [j for j in range(len(H)) if abs(C[j] @ n) < 1e-9]
        part2 = [j for j in range(len(H)) if abs(C[j] @ n) >= 1e-9]
        if not part2: continue
        if np.linalg.matrix_rank(C[part2], 1e-9) <= r - 1:
            best = (sorted(H[j] for j in part1), sorted(H[j] for j in part2)); break
    return r, nd, best
for tname, t in (('T012', T(0, 1, 2)), ('P01', P(0, 1))):
    reps = {}
    for u in range(V):
        if u == t: continue
        key = (g.kind[u], len(set(g.supp[u]) & set(g.supp[t])), int(round(g.G[t, u])))
        reps.setdefault(key, u)
    for key, u in sorted(reps.items()):
        H = sect([t, u]); r, nd, sp_ = find_split(H)
        if sp_:
            p1, p2 = sp_
            ok = (dim(mask(p1)) <= r - 1 and dim(mask(p2)) <= r - 1 and nondegenerate(closure(mask(p1))) and nondegenerate(closure(mask(p2))))
            print(tname, 'section with', g.kind[u], g.supp[u], 'lines', len(H), 'rank', r, '| 2-cover FOUND parts', len(p1), len(p2),
                  '| exact ranks', dim(mask(p1)), dim(mask(p2)), '| nondeg', nondegenerate(closure(mask(p1))), nondegenerate(closure(mask(p2))), flush=True)
        else:
            print(tname, 'section with', g.kind[u], g.supp[u], 'lines', len(H), 'rank', r, '| quadric null', nd, '| no 2-cover found', flush=True)
