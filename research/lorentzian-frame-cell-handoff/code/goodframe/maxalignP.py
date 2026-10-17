# Exact: maximum number of good frames in a pairwise compatible (aligned), line-disjoint family.
# WLOG frame i0 = (4;01|23) is in the family (a family with <= 11 punctures must contain a PPTT frame; S11 is transitive
# on PPTT frames).  Reports best family and proven upper bound; writes the best family.
import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/part/'
good = pickle.load(open(D + 'good4.pkl', 'rb')); comp = pickle.load(open(D + 'compat.pkl', 'rb'))
idx = {tuple(sorted(q)): i for i, q in enumerate(good)}
i0 = idx[tuple(sorted((g.P(0, 1), g.P(2, 3), g.T(0, 1, 4), g.T(2, 3, 4))))]
S = sorted(j for j in comp[i0].tolist() if sum(1 for u in good[j] if g.kind[u] == "P") == 2); Sset = set(S)
m = cp_model.CpModel()
x = {j: m.NewBoolVar('x%d' % j) for j in S}
inc = collections.defaultdict(list)
for j in S:
    for u in good[j]: inc[u].append(x[j])
for u in range(V):
    if u in good[i0]: continue
    m.Add(sum(inc[u]) <= 1)
n = 0
for a in S:
    ca = set(comp[a].tolist())
    for b in S:
        if b <= a or b in ca: continue
        if set(good[a]) & set(good[b]): continue
        m.AddBoolOr([x[a].Not(), x[b].Not()]); n += 1
m.Maximize(sum(x.values()))
print('candidates', len(S), '| incompatible pairs', n, flush=True)
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.best = 0
    def on_solution_callback(s):
        v = int(s.ObjectiveValue())
        if v > s.best:
            s.best = v
            fam = [i0] + [j for j in S if s.Value(x[j])]
            pickle.dump(fam, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/align/bestP.pkl', 'wb'))
            print('family size', v + 1, '| lines', 4 * (v + 1), '| bound', s.BestObjectiveBound() + 1, '| %.0fs' % s.WallTime(), flush=True)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = float(sys.argv[1])
cb = CB(); r = s.Solve(m, cb)
print('STATUS', s.StatusName(r), '| best family', int(s.ObjectiveValue()) + 1, '| upper bound', int(s.BestObjectiveBound()) + 1, flush=True)
