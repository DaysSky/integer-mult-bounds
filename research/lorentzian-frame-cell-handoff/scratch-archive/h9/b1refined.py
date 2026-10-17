"""B1 class refined support bound: total non-frame lines <= sum_T (8 - kill_T) + 10 |F5|, kill_T = 1 if T lies inside a
used k=5 support (a k=5 line (x;1) on S >= T forbids the k=4 class +-x|_T).  Exact max over compatible structures (CP-SAT),
then list every structure with value >= LIM (those need the line-level check)."""
import itertools, sys
from ortools.sat.python import cp_model
P = range(8)
S4 = [frozenset(c) for c in itertools.combinations(P, 4)]; S5 = [frozenset(c) for c in itertools.combinations(P, 5)]
m = cp_model.CpModel()
y = {T: m.NewBoolVar('y') for T in S4}; z = {S: m.NewBoolVar('z') for S in S5}
for a, b in itertools.combinations(S4, 2):
    if len(a & b) % 2: m.AddBoolOr([y[a].Not(), y[b].Not()])
for a, b in itertools.combinations(S5, 2):
    if len(a & b) % 2 == 0: m.AddBoolOr([z[a].Not(), z[b].Not()])
for T in S4:
    for S in S5:
        if len(T & S) % 2: m.AddBoolOr([y[T].Not(), z[S].Not()])
kill = {}
for T in S4:
    kill[T] = m.NewBoolVar('k')
    for S in S5:
        if T <= S: m.AddImplication(z[S], kill[T]) if False else m.AddBoolOr([y[T].Not(), z[S].Not(), kill[T]])
obj = sum(8 * y[T] for T in S4) - sum(kill[T] for T in S4) + sum(10 * z[S] for S in S5)
m.Add(sum(z.values()) >= 1)
m.Maximize(obj)
s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 600
r = s.Solve(m)
print('B1 refined support max (with >= 1 k5 support):', s.StatusName(r), int(s.ObjectiveValue()), 'bound', int(s.BestObjectiveBound()),
      '|F4|', sum(s.Value(y[T]) for T in S4), '|F5|', sum(s.Value(z[S]) for S in S5), '-> total <=', 8 + int(s.BestObjectiveBound()))
