"""Apex families with mixed subset sizes (I_{n,1}, m = n - 1 points per apex): f(S) for 2 <= |S| <= m-2 ... m;
condition: for all disjoint pairs xy, bc: #{S in F: xy in S, S n bc = empty} odd.  Objectives: load per apex
(sum over S of lines 2*C(|S|,2)) and #sets.  Users of K_h(S) = 2*C(m-|S|,2).  usage: fammix.py m TIME"""
import itertools, sys
from ortools.sat.python import cp_model
m_ = int(sys.argv[1]); TL = float(sys.argv[2])
subs = [S for k in range(2, m_ + 1) for S in itertools.combinations(range(m_), k)]
eqs = []
for b, c in itertools.combinations(range(m_), 2):
    for x, y in itertools.combinations([i for i in range(m_) if i not in (b, c)], 2):
        eqs.append([j for j, S in enumerate(subs) if b not in S and c not in S and x in S and y in S])
md = cp_model.CpModel(); v = [md.NewBoolVar('') for _ in subs]
for e in eqs: md.AddBoolXOr([v[j] for j in e])
lines = [2 * len(S) * (len(S) - 1) // 2 for S in subs]
users = [2 * (m_ - len(S)) * (m_ - len(S) - 1) // 2 for S in subs]
md.Minimize(sum((lines[j] + users[j]) * v[j] for j in range(len(subs))))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 2
st = s.Solve(md)
print('m', m_, s.StatusName(st), 'min load+deliveries per apex', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [subs[j] for j in range(len(subs)) if s.Value(v[j])]
    import collections
    print('  load', sum(lines[j] for j in range(len(subs)) if s.Value(v[j])), 'sets by size', sorted(collections.Counter(len(S) for S in sel).items()),
          'deliveries per apex (sum users)', sum(users[j] for j in range(len(subs)) if s.Value(v[j])))
