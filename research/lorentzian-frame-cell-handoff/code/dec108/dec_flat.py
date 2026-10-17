"""Sub-110 I_{11,1} decoders from coordinate flats L(S) (lines with support inside S; rank |S| for |S| <= 8,
positive definite, 84 lines at |S| = 8) via codes containing C_11: choose flats S_k and columns a_k in F2^11 with
label(u) in span{a_k : supp(u) subset of S_k} for every line u.  cost = sum |S_k|.  CP-SAT, bilinear.
usage: dec_flat.py MAXCOST SIZES(comma) TIME"""
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V
MAXC = int(sys.argv[1]); SIZES = [int(x) for x in sys.argv[2].split(',')]; TL = float(sys.argv[3])
label = [g.binlabel(u) for u in range(V)]
supp = [set(g.supp[u]) for u in range(V)]
cands = [frozenset(S) for k in SIZES for S in itertools.combinations(range(11), k)]
print('candidates', len(cands), flush=True)
m = cp_model.CpModel()
x = [m.NewBoolVar('x%d' % j) for j in range(len(cands))]
a = [[m.NewBoolVar('') for i in range(11)] for j in range(len(cands))]
for j in range(len(cands)):
    for i in range(11): m.AddImplication(a[j][i], x[j])
m.Add(sum(len(cands[j]) * x[j] for j in range(len(cands))) <= MAXC)
for u in range(V):
    js = [j for j in range(len(cands)) if supp[u] <= cands[j]]
    c = {j: m.NewBoolVar('') for j in js}
    for j in js: m.AddImplication(c[j], x[j])
    for i in range(11):
        terms = []
        for j in js:
            p = m.NewBoolVar(''); m.AddBoolAnd([c[j], a[j][i]]).OnlyEnforceIf(p); m.AddBoolOr([c[j].Not(), a[j][i].Not()]).OnlyEnforceIf(p.Not())
            terms.append(p)
        if label[u] >> i & 1: m.AddBoolXOr(terms)
        else: m.AddBoolXOr(terms + [m.NewConstant(1)])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 3
st = s.Solve(m)
print('MAXC', MAXC, 'sizes', SIZES, s.StatusName(st), 'time', s.WallTime(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [(sorted(cands[j]), [i for i in range(11) if s.Value(a[j][i])]) for j in range(len(cands)) if s.Value(x[j])]
    print('cost', sum(len(S) for S, _ in sel), sel)
