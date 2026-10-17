"""Local realisability tests for frame-free multisets in symplectic F2^8 (h = 9, ambient R^{8,1}): pick k mutually
orthogonal lines (k = 3, 4); the lines orthogonal to all of them must embed root-like in R^{8-k,1}.  LM on the small
induced configuration (several seeds).  A failure certifies (numerically) that the whole multiset is not realisable."""
import itertools, sys, numpy as np, random, collections
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
from zerolm05 import solve_zero as solve
n = 8
def B(x, y):
    s = 0
    for i in range(0, n, 2):
        s ^= (((x >> i) & 1) & ((y >> (i + 1)) & 1)) ^ (((x >> (i + 1)) & 1) & ((y >> i) & 1))
    return s
frontier = [frozenset([0])]
for d in range(4):
    nxt = set()
    for S in frontier:
        for v in range(1, 256):
            if v in S: continue
            if all(B(v, s) == 0 for s in S): nxt.add(frozenset(S | {s ^ v for s in S}))
    frontier = nxt
L = list(frontier)
T = int(sys.argv[1]); nms = int(sys.argv[2]); MAXL = int(sys.argv[3]); PP = int(sys.argv[4])
for sd in range(100, 100 + nms):
    m = cp_model.CpModel(); x = {v: m.NewIntVar(0, MAXL, '') for v in range(1, 256)}
    for S in L: m.Add(sum(x[v] for v in S if v) <= MAXL)
    m.Add(sum(x.values()) >= T); m.Add(sum(x.values()) <= T + 2)
    random.seed(sd); m.Maximize(sum(random.randint(0, 3) * x[v] for v in x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 2; s.parameters.random_seed = sd
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no multiset', flush=True); continue
    pts = [v for v in x for _ in range(s.Value(x[v]))]; N = len(pts)
    Bm = np.array([[B(a, b) if i != j else 0 for j, b in enumerate(pts)] for i, a in enumerate(pts)])
    orth = (Bm == 0); np.fill_diagonal(orth, False)
    hist = dict(collections.Counter(s.Value(x[v]) for v in x if s.Value(x[v])))
    print('multiset %d: %d lines, multiplicities %s' % (sd, N, hist), flush=True)
    rng = random.Random(sd); worst = 0; tested = 0
    for trial in range(400):
        k = rng.choice((3, 4))
        # random orthogonal k-set
        a = rng.randrange(N); S = [a]
        cand = [j for j in range(N) if orth[a, j]]
        while len(S) < k and cand:
            b = rng.choice(cand); S.append(b); cand = [j for j in cand if orth[b, j] and j != b]
        if len(S) < k: continue
        sub = [j for j in range(N) if j not in S and all(orth[j, t] for t in S)]
        if len(sub) < 12: continue
        Bs = Bm[np.ix_(sub, sub)]
        best = 1e9
        for (pp, qq) in ((PP - k, 1), (PP - k + 1, 0)):
            for seed in range(3):
                r2, z = solve(Bs, pp, qq, seed, iters=400); best = min(best, r2)
                if r2 < 1e-9: break
            if best < 1e-9: break
        tested += 1; worst = max(worst, best)
        if best > 1e-3:
            print('   k=%d, %d lines in common perp: NOT realisable in R^{%d,1} (best residual^2 %.3g) -> multiset excluded' % (k, len(sub), PP - k, best), flush=True)
            break
        if tested >= 25: break
    else:
        pass
    if worst <= 1e-3: print('   %d local tests all realisable (inconclusive)' % tested, flush=True)
