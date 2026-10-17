"""Exact line-level max clique for the unique (up to S8) B1 support structure with crude weight >= 125
(F4 = 7 Fano-complement 4-sets on {0..6}, F5 = F4 + {7}).  Lines: frame (8), k=4 (7 x 8), k=5 (x; z=1) (7 x 32)."""
import itertools, numpy as np, sys
from ortools.sat.python import cp_model
F4 = [(0, 1, 2, 3), (0, 1, 4, 5), (0, 2, 4, 6), (0, 3, 5, 6), (1, 2, 5, 6), (1, 3, 4, 6), (2, 3, 4, 5)]
F5 = [t + (7,) for t in F4]
L = [[2 if j == i else 0 for j in range(8)] + [0] for i in range(8)]
for T in F4:
    for sg in itertools.product((1, -1), repeat=3):
        x = [0] * 8; x[T[0]] = 1
        for j, s in zip(T[1:], sg): x[j] = s
        L.append(x + [0])
for S in F5:
    for sg in itertools.product((1, -1), repeat=5):
        x = [0] * 8
        for j, s in zip(S, sg): x[j] = s
        L.append(x + [1])
V = np.array(L); G = V[:, :8] @ V[:, :8].T - np.outer(V[:, 8], V[:, 8])
assert (np.diag(G) == 4).all()
n = len(V); m = cp_model.CpModel(); X = [m.NewBoolVar('x%d' % i) for i in range(n)]
ne = 0
for i in range(n):
    for j in range(i + 1, n):
        if G[i, j] not in (0, 2, -2): m.AddBoolOr([X[i].Not(), X[j].Not()]); ne += 1
print('lines', n, 'conflicts', ne, flush=True)
m.Maximize(sum(X)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(sys.argv[1]); s.parameters.num_workers = 2
r = s.Solve(m)
sel = [i for i in range(n) if s.Value(X[i])]
k = (V[sel, :8] != 0).sum(1)
print('status', s.StatusName(r), 'max', int(s.ObjectiveValue()), 'bound', int(s.BestObjectiveBound()), 'k counts', np.unique(k, return_counts=True), flush=True)
