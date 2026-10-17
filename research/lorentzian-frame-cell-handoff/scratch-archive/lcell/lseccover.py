"""Per target (Z11 reps): minimum number of plane sections {t,x}-perp (nondegenerate planes through t) whose union
routes all of R(t) (u routed by section S iff some source cell of u lies inside S).  Exact ILP (set cover).
Also the same with arbitrary nondegenerate flats replaced by ... (sections only here).  Deliveries >= cover - 1."""
import sys, os, json, collections
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
for fn in sys.argv[1:]:
    cov = {int(k): v for k, v in json.load(open(fn)).items()}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    reps = sorted(set(min(p[t] for p in PERMS) for t in range(V)))
    out = []
    for t in reps:
        planes = set()
        for x in range(V):
            if x != t:
                Q = closure((1 << t) | (1 << x))
                if nondeg_span(Q): planes.add(Q)
        secs = [perp(Q) for Q in sorted(planes)]
        M = cp_model.CpModel(); y = [M.NewBoolVar('') for _ in secs]
        for u in bits(HYP[t]):
            lits = [y[i] for i, S in enumerate(secs) if any(c & ~S == 0 for c in cells_of[u])]
            M.AddBoolOr(lits) if lits else M.AddBoolOr([])
        M.Minimize(sum(y))
        s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 2
        r = s.Solve(M)
        out.append((g.kind[t], int(s.ObjectiveValue()) if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, s.StatusName(r)[0]))
    print(fn, 'min sections routing R(t) per target rep:', out, flush=True)
