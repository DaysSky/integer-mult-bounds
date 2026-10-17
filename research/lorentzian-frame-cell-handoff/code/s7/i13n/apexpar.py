"""Parity obstruction for complete-star-block + Pasch-pair partitions of I13.
Remaining T lines containing point pair {a,b} = 10 - 3 m_ab (m_ab = M_a(b) + M_b(a), M_a = sum of PG lines with
apex a); a Pasch pair covers each cross pair twice, so m_ab must be even.  CP-SAT over apex assignments."""
import itertools
from ortools.sat.python import cp_model
Ls = [sorted(((k + d) % 13) for d in (0, 1, 3, 9)) for k in range(13)]
m = cp_model.CpModel()
a = {(k, p): m.NewBoolVar('a%d_%d' % (k, p)) for k in range(13) for p in range(13) if p not in Ls[k]}
for k in range(13): m.AddExactlyOne([a[k, p] for p in range(13) if p not in Ls[k]])
for x, y in itertools.combinations(range(13), 2):
    terms = [a[k, x] for k in range(13) if (k, x) in a and y in Ls[k]] + [a[k, y] for k in range(13) if (k, y) in a and x in Ls[k]]
    z = m.NewIntVar(0, 1, 'z%d_%d' % (x, y))
    m.Add(sum(terms) == 2 * z)          # m_xy in {0, 2}
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = 600
st = s.Solve(m); print('apex assignments with every m_ab even:', s.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print([[p for p in range(13) if (k, p) in a and s.Value(a[k, p])][0] for k in range(13)])
