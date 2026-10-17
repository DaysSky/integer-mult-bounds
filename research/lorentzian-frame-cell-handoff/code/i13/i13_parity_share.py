"""Parity covers of R(t) minimising the NODE SHARE sum_F 60/|F| (|F| = lines of the frame = potential users), i.e.
the contribution of target t to the node count if every line of each chosen frame uses it.  Exact CP-SAT (time-
limited; reports bound).  usage: python3 i13_parity_share.py KIND seconds"""
import sys, pickle, collections
from lgeo13 import *
from ortools.sat.python import cp_model
kind = sys.argv[1]; TL = float(sys.argv[2])
t, FL, PL = pickle.load(open('i13_frames_%s.pkl' % kind, 'rb'))
R = HYP[t]
cov = collections.defaultdict(list)
for i, P in enumerate(PL):
    for s in bits(P): cov[s].append(i)
def nm(s): return KIND[s] + ''.join('%x' % i for i in SUPP[s])
W = {3: 20, 4: 15, 5: 12, 6: 10}
M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in FL]
for s in bits(R): M.AddBoolXOr([x[i] for i in cov[s]])
M.Minimize(sum(W[pc(FL[i])] * x[i] for i in range(len(FL))))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M)
print(kind, sv.StatusName(st), '| min share*60 =', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
      '(share %.3f)' % (sv.ObjectiveValue() / 60) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else '', '| bound', sv.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [i for i in range(len(FL)) if sv.Value(x[i])]
    print('  sections', len(sel), '| lines per frame', sorted(pc(FL[i]) for i in sel), flush=True)
    for i in sel: print('   |perp| %d  %s' % (pc(PL[i]), ' '.join(nm(s) for s in bits(FL[i]))), flush=True)
    tot = 0
    for i in sel: tot ^= PL[i]
    assert tot == R
