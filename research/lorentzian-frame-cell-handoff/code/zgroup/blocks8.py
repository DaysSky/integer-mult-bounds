"""Max number of complete star-D4 blocks (apex h, 4-set S): P(ij) and T(ijh) for ij in S, pairwise line-disjoint."""
import itertools
from ortools.sat.python import cp_model
B = [(h, S) for h in range(11) for S in itertools.combinations([i for i in range(11) if i != h], 4)]
m = cp_model.CpModel(); y = [m.NewBoolVar('') for _ in B]
P = {}; T = {}
for bi, (h, S) in enumerate(B):
    for i, j in itertools.combinations(S, 2):
        P.setdefault((i, j), []).append(bi); T.setdefault(tuple(sorted((i, j, h))), []).append(bi)
for v in list(P.values()) + list(T.values()): m.AddAtMostOne([y[b] for b in v])
m.Maximize(sum(y)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 1
st = s.Solve(m); print(s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound())
print([B[b] for b in range(len(B)) if s.Value(y[b])])
