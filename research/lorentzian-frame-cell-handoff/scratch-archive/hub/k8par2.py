# Minimum parity cover of K_8 (every pair covered an odd number of times) by k-subsets: CP-SAT with XOR constraints.
import itertools
from ortools.sat.python import cp_model
pts = range(8); pairs = list(itertools.combinations(pts, 2))
for k in (3, 4, 5, 6, 7):
    subs = list(itertools.combinations(pts, k))
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in subs]
    for p in pairs:
        lits = [x[i] for i, S in enumerate(subs) if p[0] in S and p[1] in S]
        m.AddBoolXOr(lits)
    m.Minimize(sum(x)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 120; s.parameters.num_workers = 2
    r = s.Solve(m)
    sol = [subs[i] for i in range(len(subs)) if s.Value(x[i])] if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    print('k =', k, s.StatusName(r), 'min', len(sol) if sol else None, sol)
