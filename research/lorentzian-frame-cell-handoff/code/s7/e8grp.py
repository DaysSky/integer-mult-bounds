"""E8 with the 4-group cover: assign targets to groups to minimise total entries sum_s |groups(s)| (CP-SAT)."""
import numpy as np
from e8geo import e8_roots
from ortools.sat.python import cp_model
L = e8_roots(); n = len(L); G = L @ L.T // 4
Z = [(-1, 1, -1, 1, -1, 1, 1, -1), (2, 2, 0, 0, 0, 0, 0, 0), (-1, 1, 1, 3, 1, -1, -1, 1), (-1, 1, 1, -1, -3, -3, 1, 1)]
perp = [[t for t in range(n) if (L[t] @ np.array(z)) == 0] for z in Z]
print('group sizes (possible)', [len(p) for p in perp])
m = cp_model.CpModel()
a = {(t, g): m.NewBoolVar('') for g in range(4) for t in perp[g]}
for t in range(n): m.AddExactlyOne([a[t, g] for g in range(4) if (t, g) in a])
need = {(s, g): m.NewBoolVar('') for s in range(n) for g in range(4)}
R = [[u for u in range(n) if u != s and G[s, u] == 0] for s in range(n)]
for s in range(n):
    for g in range(4):
        for t in R[s]:
            if (t, g) in a: m.AddImplication(a[t, g], need[s, g])
m.Minimize(sum(need.values()))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 4
r = sv.Solve(m)
print(sv.StatusName(r), 'sum_s |groups(s)| =', sv.ObjectiveValue(), 'bound', sv.BestObjectiveBound(), '-> frame-0 entries', sv.ObjectiveValue() - n)
print('group sizes', [sum(sv.Value(a[t, g]) for t in perp[g]) for g in range(4)])
