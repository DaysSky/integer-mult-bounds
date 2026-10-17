"""Minimum PARITY covers in I_{13,1}: the fewest nondegenerate rank-3 frames F through t whose perps XOR to 1_{R(t)}
(every line of R(t) covered an odd number of times; perps lie inside R(t)).  Exact CP-SAT (AddBoolXOr per line).
With such a cover every user of a node can take the full section as its part (copies, automatic in-chain hosting).
usage: python3 i13_parity.py KIND [maxK]"""
import sys, pickle, collections
from lgeo13 import *
from ortools.sat.python import cp_model
kind = sys.argv[1]; maxK = int(sys.argv[2]) if len(sys.argv) > 2 else 8
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]
cov = collections.defaultdict(list)
for i, P in enumerate(PL):
    for s in bits(P): cov[s].append(i)
def nm(s): return KIND[s] + ''.join('%x' % i for i in SUPP[s])
M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in FL]
for s in bits(R): M.AddBoolXOr([x[i] for i in cov[s]] + [M.NewConstant(0)] if False else [x[i] for i in cov[s]])
M.Add(sum(x) <= maxK)
M.Minimize(sum(x))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 1800; sv.parameters.num_workers = 4
st = sv.Solve(M)
print(kind, 'status', sv.StatusName(st), '| min parity sections', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
      '| bound', sv.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [i for i in range(len(FL)) if sv.Value(x[i])]
    for i in sel: print('  |perp| %d  frame: %s' % (pc(PL[i]), ' '.join(nm(s) for s in bits(FL[i]))), flush=True)
    tot = 0
    for i in sel: tot ^= PL[i]
    assert tot == R
