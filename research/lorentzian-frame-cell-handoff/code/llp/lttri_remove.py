"""Minimum number r of triangle nodes to remove from the M11 triangle design (lttri_design_z11.json) so that every
retained node has >= K users in S, where S = targets lying in some removed node (a removed node turns all of its
users' sections there into non-triangle sections).  K = 2 is the proven local requirement for a zero-cost
(rank-5 fed) triangle node (lttri_rho5_minrel.py, OBJ=users).  Exact CP-SAT; counting gives r >= 40 for K = 2.
usage: lttri_remove.py [K] [time_limit]"""
import sys, json, collections
from ortools.sat.python import cp_model
K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
TL = float(sys.argv[2]) if len(sys.argv) > 2 else 600
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
tg = sorted({T for n in sol for T in n}); ti = {T: i for i, T in enumerate(tg)}
nodes_of = collections.defaultdict(list)
for ni, n in enumerate(sol):
    for T in n: nodes_of[ti[T]].append(ni)
M = cp_model.CpModel()
x = [M.NewBoolVar('') for _ in sol]; y = [M.NewBoolVar('') for _ in tg]
for t in range(len(tg)):
    for ni in nodes_of[t]: M.AddImplication(x[ni], y[t])
    M.AddBoolOr([x[ni] for ni in nodes_of[t]] + [y[t].Not()])
for ni, n in enumerate(sol):
    M.Add(sum(y[ti[T]] for T in n) >= K).OnlyEnforceIf(x[ni].Not())
M.Minimize(sum(x))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
print('K', K, '| status', sv.StatusName(st), '| min removed nodes r =', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
      '| lower bound', sv.BestObjectiveBound(), '| |S| =', sum(sv.Value(v) for v in y) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, flush=True)
