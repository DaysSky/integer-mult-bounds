import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb'))
m = cp_model.CpModel()
x = [m.NewBoolVar('x%d' % i) for i in range(len(good))]
y = [m.NewBoolVar('y%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, q in enumerate(good):
    for u in q: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
m.Minimize(sum(y))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 8
r = s.Solve(m)
print(s.StatusName(r), 'punctured', s.ObjectiveValue(), 'bound', s.BestObjectiveBound())
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [good[i] for i in range(len(good)) if s.Value(x[i])]
    pun = [u for u in range(V) if s.Value(y[u])]
    print('frames', len(sol), 'types', collections.Counter(''.join(sorted(g.kind[v] for v in q)) for q in sol))
    print('punctured', [(g.kind[u], g.supp[u]) for u in pun])
    pickle.dump((sol, pun), open('goodpart.pkl', 'wb'))
