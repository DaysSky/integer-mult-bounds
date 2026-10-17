"""Frame-free h = 9 root-like systems: images in symplectic F2^8 (B = 1 exactly on non-orthogonal pairs; twins = same
image, mutually orthogonal).  Frame-free <=> every Lagrangian holds <= 7 lines (with multiplicity).  Exact ILP: max
total multiplicity; then count solutions with total >= 117 (the f = 0.5 need) up to nothing (raw), report structure."""
import itertools, sys
from ortools.sat.python import cp_model
n = 8
def B(x, y):
    s = 0
    for i in range(0, n, 2):
        s ^= (((x >> i) & 1) & ((y >> (i + 1)) & 1)) ^ (((x >> (i + 1)) & 1) & ((y >> i) & 1))
    return s
frontier = [frozenset([0])]
for d in range(4):
    nxt = set()
    for S in frontier:
        for v in range(1, 256):
            if v in S: continue
            if all(B(v, s) == 0 for s in S): nxt.add(frozenset(S | {s ^ v for s in S}))
    frontier = nxt
L = list(frontier); print('Lagrangians', len(L), flush=True)
m = cp_model.CpModel(); x = {v: m.NewIntVar(0, 7, 'm%d' % v) for v in range(1, 256)}
for S in L: m.Add(sum(x[v] for v in S if v) <= 7)
tot = sum(x.values())
target = int(sys.argv[1]) if len(sys.argv) > 1 else 0
if target:
    m.Add(tot >= target)
    # exclude the pure 0/1 case to look for twin configurations
    if len(sys.argv) > 2 and sys.argv[2] == 'twins': m.Add(sum(x.values()) >= 0); m.AddMaxEquality(m.NewIntVar(2, 7, 'mx'), list(x.values()))
else:
    m.Maximize(tot)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 3
st = s.Solve(m)
print(s.StatusName(st), 'total', s.Value(tot) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', s.BestObjectiveBound() if not target else '-')
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    import collections; print('multiplicity histogram', collections.Counter(s.Value(x[v]) for v in x))
