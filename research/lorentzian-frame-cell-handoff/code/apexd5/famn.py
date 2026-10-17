"""Apex-D5 family on 10 points: F a set of 5-subsets; for every pair bc and every pair xy disjoint from bc,
#{S in F : S n bc = empty, xy in S} must be odd.  Also variants with k-subsets (k = 4..8).  F2 feasibility +
minimum weight (CP-SAT)."""
import itertools, sys
from ortools.sat.python import cp_model
import sys
n = int(sys.argv[1])
for k in [int(x) for x in sys.argv[2].split(",")]:
    subs = list(itertools.combinations(range(n), k))
    eqs = []
    for b, c in itertools.combinations(range(n), 2):
        for x, y in itertools.combinations([i for i in range(n) if i not in (b, c)], 2):
            eqs.append([j for j, S in enumerate(subs) if b not in S and c not in S and x in S and y in S])
    # F2 feasibility
    rows = []
    for e in eqs:
        r = sum(1 << j for j in e) | (1 << len(subs)); rows.append(r)
    piv = {}
    for r in rows:
        x = r
        while x & ((1 << len(subs)) - 1):
            p = (x & ((1 << len(subs)) - 1)).bit_length() - 1
            if p in piv: x ^= piv[p]
            else: piv[p] = x; break
        else:
            if x: print('k', k, 'INFEASIBLE (inconsistent)'); break
    else:
        m = cp_model.CpModel(); v = [m.NewBoolVar('') for _ in subs]
        for e in eqs: m.AddBoolXOr([v[j] for j in e])
        m.Minimize(sum(v)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 120; s.parameters.num_workers = 2
        st = s.Solve(m)
        print('k', k, 'feasible; min family size', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), s.StatusName(st), flush=True)
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): pass
