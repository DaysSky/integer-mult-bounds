import itertools
from ortools.sat.python import cp_model
Ls = [sorted(((k + d) % 13) for d in (0, 1, 3, 9)) for k in range(13)]
m = cp_model.CpModel()
a = {(k, p): m.NewBoolVar('a%d_%d' % (k, p)) for k in range(13) for p in range(13) if p not in Ls[k]}
for k in range(13): m.AddExactlyOne([a[k, p] for p in range(13) if p not in Ls[k]])
odd = []
for x, y in itertools.combinations(range(13), 2):
    terms = [a[k, x] for k in range(13) if (k, x) in a and y in Ls[k]] + [a[k, y] for k in range(13) if (k, y) in a and x in Ls[k]]
    z = m.NewIntVar(0, 2, ''); o = m.NewBoolVar('')
    m.Add(sum(terms) == 2 * z + o); odd.append(o)
    m.Add(sum(terms) <= 3)   # leftover 10 - 3m >= 0
m.Minimize(sum(odd))
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 300
st = s.Solve(m); print(s.StatusName(st), 'min odd point pairs', s.ObjectiveValue(), 'bound', s.BestObjectiveBound())
print('apexes', [[p for p in range(13) if (k, p) in a and s.Value(a[k, p])][0] for k in range(13)])
