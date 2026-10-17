"""Lower bound on decoder minrank: B restricted to a set of pairwise NON-orthogonal lines is the identity, so
minrank >= max clique of the non-orthogonality graph.  Exact CP-SAT max clique for I_{10,1}, I_{11,1}, E8."""
import sys, numpy as np, itertools
from ortools.sat.python import cp_model
def mc(V, eta, name):
    G = (V * eta) @ V.T; v = len(V)
    NO = (G % 2 == 1)
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in range(v)]
    for i in range(v):
        for j in range(i + 1, v):
            if not NO[i, j]: m.AddBoolOr([x[i].Not(), x[j].Not()])
    m.Maximize(sum(x))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 4
    st = s.Solve(m)
    print('%s: max pairwise non-orthogonal set %d (%s, bound %d)' % (name, s.ObjectiveValue(), s.StatusName(st), s.BestObjectiveBound()), flush=True)
V10 = np.load('sys_n10_t3_10.npy'); mc(V10, np.array([1]*10 + [-1]), 'I_{10,1}')
n = 11; L = []
for i, j in itertools.combinations(range(n), 2):
    x = [0]*(n+1); x[i] = 1; x[j] = -1; L.append(x)
for t in itertools.combinations(range(n), 3):
    x = [0]*(n+1)
    for i in t: x[i] = 1
    x[n] = 1; L.append(x)
mc(np.array(L), np.array([1]*11 + [-1]), 'I_{11,1}')
