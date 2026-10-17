"""Rigorous per-line lower bound on the cell-sharing cover over ALL good-frame partitions of I_{13,1}.
For a line u: choose a partition (x_g, exact cover of all 364 lines by good frames) and partners y_v; every chosen
frame g (u not in g) with >= 2 lines orthogonal to u yields the demand d_g(u) = {v : pattern_g(v) = pattern_g(u)}
(Q-part or E-set containing u), which must contain a partner.  min sum y_v = best possible cover of u.
E8 analogue gives 3 (frame-mates).  argv: line kind P|T, time limit."""
import sys, pickle, itertools, collections, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(13); V = g.V; G = g.G
frames, comp_lists, kinds = pickle.load(open('../i13a/compat13.pkl', 'rb'))
orth = (G == 0); np.fill_diagonal(orth, False)
kind = sys.argv[1] if len(sys.argv) > 1 else 'T'; tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
relax = len(sys.argv) > 3 and sys.argv[3] == 'relax'
u = g.P(0, 1) if kind == 'P' else g.T(0, 1, 2)
F = np.array([list(q) for q in frames])
m = cp_model.CpModel()
x = [m.NewBoolVar('x%d' % i) for i in range(len(frames))]
y = {v: m.NewBoolVar('y%d' % v) for v in range(V) if v != u}
by = collections.defaultdict(list)
for i, q in enumerate(frames):
    for l in q: by[l].append(i)
for l in range(V):
    if relax and not (orth[u, l] or l == u): m.Add(sum(x[i] for i in by[l]) <= 1)
    else: m.AddExactlyOne([x[i] for i in by[l]])
nd = 0; dsz = []
OT = orth[:, F]  # V x nf x 4
for i, q in enumerate(frames):
    if u in q: continue
    pu = orth[u, list(q)]
    if pu.sum() < 2: continue
    same = np.all(OT[:, i, :] == pu, axis=1); same[u] = False
    d = np.nonzero(same)[0]
    dsz.append(len(d)); nd += 1
    m.AddBoolOr([x[i].Not()] + [y[int(v)] for v in d])
print('line', g.kind[u], g.supp[u], 'demand constraints', nd, 'demand size range', min(dsz), max(dsz), 'relax' if relax else '', flush=True)
m.Minimize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4; s.parameters.log_search_progress = False
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2): super().__init__(); s2.t0 = time.time()
    def on_solution_callback(s2):
        print('  sol %d bound %.1f (%.0fs)' % (s2.ObjectiveValue(), s2.BestObjectiveBound(), time.time() - s2.t0), flush=True)
st = s.Solve(m, CB())
print('status', s.StatusName(st), 'obj', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    pv = [v for v in y if s.Value(y[v])]
    print('partners', [(g.kind[v], g.supp[v], int(orth[u, v])) for v in pv])
    own = [frames[i] for i in by[u] if s.Value(x[i])][0]
    print('own frame', [(g.kind[v], g.supp[v]) for v in own])
