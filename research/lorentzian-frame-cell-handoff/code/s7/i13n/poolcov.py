"""Pool-based per-line cover: for line u, min #rank-2 pools <u,w> (w a line) such that every demand E containing u
has some chosen w in its frame S_E (so a collector for E can pass <u,w> and pick x_u).  CP-SAT per line."""
from part13 import *
from ortools.sat.python import cp_model
import collections, random
random.seed(0)
dem_u = collections.defaultdict(list)
for k, d in enumerate(DEM):
    for u in bits(d[2]): dem_u[u].append(k)
def cover(u, tl=20):
    Ds = dem_u[u]
    m = cp_model.CpModel()
    cand = [w for w in range(V) if w != u and G[u, w] != 2 and any(DEM[k][1] >> w & 1 for k in Ds)]
    # <u,w> nondegenerate: gram det = 4 - G^2 != 0  -> |G|!=2 always for distinct lines
    x = {w: m.NewBoolVar('w%d' % w) for w in cand}
    for k in Ds:
        m.AddBoolOr([x[w] for w in cand if DEM[k][1] >> w & 1])
    m.Minimize(sum(x.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
    st = s.Solve(m)
    return int(s.ObjectiveValue()), int(s.BestObjectiveBound()), len(Ds)
out = collections.Counter()
sample = list(range(0, 78, 13)) + list(range(78, V, 29))
for u in sample:
    c, lb, nd = cover(u)
    out[c] += 1
    print(g.kind[u], g.supp[u], 'demands', nd, 'pool cover', c, 'lb', lb, flush=True)
print(sorted(out.items()))
