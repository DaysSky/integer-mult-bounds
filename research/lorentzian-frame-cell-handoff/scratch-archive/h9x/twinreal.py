"""Find frame-free multisets in symplectic F2^8 with total >= T (every Lagrangian <= 7 lines, twins allowed), then test
root-like realisability in R^{8,1} by LM (twins: orthogonal, same pattern).  Several random solver seeds."""
import itertools, sys, numpy as np, collections
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
from qreal import solve
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
T = int(sys.argv[1]); nsol = int(sys.argv[2]) if len(sys.argv) > 2 else 3
for sd in range(nsol):
    m = cp_model.CpModel(); x = {v: m.NewIntVar(0, 7, '') for v in range(1, 256)}
    for S in L: m.Add(sum(x[v] for v in S if v) <= 7)
    m.Add(sum(x.values()) >= T)
    import random; random.seed(sd)
    m.Maximize(sum(random.randint(0, 3) * x[v] for v in x))   # diversify
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 2; s.parameters.random_seed = sd
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no multiset'); continue
    pts = [v for v in x for _ in range(s.Value(x[v]))]
    N = len(pts)
    Bm = np.array([[B(a, b) for b in pts] for a in pts])
    hist = collections.Counter(s.Value(x[v]) for v in x if s.Value(x[v]))
    best = 1e9
    for seed in range(3):
        r2, z = solve(Bm, 8, 1, seed, iters=250); best = min(best, r2)
        if r2 < 1e-10: break
    print('multiset %d: lines %d, multiplicities %s, best residual^2 %.4g' % (sd, N, dict(hist), best), flush=True)
