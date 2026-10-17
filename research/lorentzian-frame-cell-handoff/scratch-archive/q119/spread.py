"""Does the O^-(8,2) quadric (119 singular points) admit a spread of totally singular planes (17 Fano planes
partitioning the points)?  Exact cover by CP-SAT.  Also count t.s. planes and lines."""
import itertools, sys
sys.path.insert(0, '../h9x')
from qreal import points
from ortools.sat.python import cp_model
X, Bm = points('minus-s')
pts = [tuple(int(a) for a in x) for x in X]; idx = {p: i for i, p in enumerate(pts)}
add = lambda a, b: tuple(u ^ v for u, v in zip(a, b))
planes = set()
for i, j in itertools.combinations(range(len(pts)), 2):
    if Bm[i, j]: continue
    k = idx[add(pts[i], pts[j])]
    for l in range(len(pts)):
        if l in (i, j, k) or Bm[i, l] or Bm[j, l]: continue
        S = {i, j, k, l, idx[add(pts[i], pts[l])], idx[add(pts[j], pts[l])], idx[add(add(pts[i], pts[j]), pts[l])]}
        if len(S) == 7: planes.add(frozenset(S))
planes = list(planes); print('t.s. planes', len(planes), flush=True)
m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in planes]
for p in range(len(pts)): m.AddExactlyOne([x[a] for a, P in enumerate(planes) if p in P])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 2
st = s.Solve(m); print('plane spread:', s.StatusName(st), flush=True)
