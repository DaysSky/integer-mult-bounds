"""Full-E8 decoder = 9 stars (sources R(z_j), readers F_j = {t : S_tj = 1}) + correction X on the 9 columns z_j.
X(t, j) = S_tj must hold on constrained entries (t non-orth to z_j or t = z_j); other entries free.
Min correction cost with rectangles (Q, P), P subset of Z, cost = dim span{profile_t|P : t in Q} (profile_t = (t.z_j)_j).
Here: rectangles of cost <= 1 (profiles restricted to P all multiples of one vector), exact CP-SAT."""
import sys, itertools, random, numpy as np
from ortools.sat.python import cp_model
from e8dec import G, v, A
sys.path.insert(0, '.')
def classes():
    # class of a line in F2^8: coordinates of the (doubled) vector mod ... use Gram mod 2 rank factorisation
    M = (G % 2).astype(np.uint8)
    # basis rows of M over F2 -> coordinates
    R = M.copy(); piv = []; r = 0
    for c in range(v):
        p = [i for i in range(r, v) if R[i, c]]
        if not p: continue
        R[[r, p[0]]] = R[[p[0], r]]
        for i in range(v):
            if i != r and R[i, c]: R[i] ^= R[r]
        piv.append(c); r += 1
    return M[:, piv], r      # coords of line t: B(t, basis lines) -- injective linear image of the class
def run(seed, tl=300):
    rng = random.Random(seed)
    C, r = classes()           # C[t] in F2^8 (functional coordinates): B(c_t, c_s) = ?  use affine-function view directly
    # affine functions on lines: N[x](s) = 1 + G[x,s] mod 2 ; pick 9 lines whose N-rows (+ all-ones) are independent
    N = ((G == 0) | np.eye(v, dtype=bool)).astype(np.uint8)   # N[x] rows = B0 rows
    while True:
        Z = rng.sample(range(v), 9)
        Mz = N[Z]
        # solve S_t: N[t] = sum_j S_tj N[z_j] over F2 (unique if independent)
        Aug = np.concatenate([Mz.T, N.T], 1) % 2      # v x (9 + v)
        R = Aug.copy(); prow = 0; piv = []
        for c in range(9):
            p = [i for i in range(prow, v) if R[i, c]]
            if not p: break
            R[[prow, p[0]]] = R[[p[0], prow]]
            for i in range(v):
                if i != prow and R[i, c]: R[i] ^= R[prow]
            piv.append(c); prow += 1
        if len(piv) == 9: break
    S = R[:9, 9:].T % 2                                 # S[t, j]
    assert ((S @ Mz) % 2 == N).all()
    prof = np.array([[int(G[t, z]) for z in Z] for t in range(v)])      # products (2 on the diagonal)
    cons = [(t, j) for t in range(v) for j in range(9) if prof[t, j] != 0]
    # cost of the 9 star pieces
    def prk(a, b): return int(np.linalg.matrix_rank(A[a] @ A[b].T)) if len(a) and len(b) else 0
    star_cost = sum(prk(np.nonzero(S[:, j])[0], [s for s in range(v) if G[s, Z[j]] == 0 and s != Z[j]]) for j in range(9))
    m = cp_model.CpModel(); u = {}; y = {}
    terms = {(t, j): [] for (t, j) in cons}
    for k in range(1, 1 << 9):
        P = [j for j in range(9) if (k >> j) & 1]
        dirs = {}
        for t in range(v):
            pr = prof[t, P]
            if not pr.any(): continue
            nz = pr[np.nonzero(pr)[0][0]]; key = tuple((pr * np.sign(nz)).tolist()) if True else None
            # normalise direction: divide by gcd and sign
            g = np.gcd.reduce(np.abs(pr[pr != 0])); key = tuple((pr // g * np.sign(nz)).tolist())
            dirs.setdefault(key, []).append(t)
        for key, ts in dirs.items():
            uv = m.NewBoolVar(''); u[k, key] = uv
            for t in ts:
                yv = m.NewBoolVar(''); m.AddImplication(yv, uv); y[t, k, key] = yv
                for j in P:
                    if (t, j) in terms: terms[t, j].append(yv)
    for (t, j), lits in terms.items():
        target = int(S[t, j])
        if lits: m.AddBoolXOr(lits + ([m.NewConstant(1)] if target == 0 else []))
        elif target: m.Add(0 == 1)
    m.Minimize(sum(u.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 2
    st = sol.Solve(m)
    print('seed', seed, 'stars cost', star_cost, 'constrained entries', len(cons), 'correction (cost-1 rectangles):',
          sol.StatusName(st), int(sol.ObjectiveValue()) if st in (2, 4) else None, 'bound', int(sol.BestObjectiveBound()), '-> total <=',
          star_cost + int(sol.ObjectiveValue()) if st in (2, 4) else None, flush=True)
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    run(s, float(sys.argv[3]))
