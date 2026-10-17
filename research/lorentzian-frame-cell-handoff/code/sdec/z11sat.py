"""Z11-invariant rank-k decoders for I_{11,1} with row weight <= w (CP-SAT).  M = P (+) I_{k-11}: points shift
cyclically, extra coordinates fixed.  U_{sigma^j u_s} = M^j U_s, W likewise (M orthogonal, so M^-T = M).
B[t, u] = <W_t, U_u>.  Constraints for orbit representatives only (invariance gives the rest)."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
k = int(sys.argv[1]); w = int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
g = Geom(11); V = g.V; n = 11
def shift(u, j):
    s = tuple(sorted((x + j) % n for x in g.supp[u]))
    return g.P(*s) if g.kind[u] == 'P' else g.T(*s)
rep_of = {}; reps = []
for u in range(V):
    if u in rep_of: continue
    reps.append(u)
    for j in range(n): rep_of[shift(u, j)] = (len(reps) - 1, j)
assert len(reps) == 20, len(reps)
m = cp_model.CpModel()
U = [[m.NewBoolVar('U%d_%d' % (r, b)) for b in range(k)] for r in range(20)]
W = [[m.NewBoolVar('W%d_%d' % (r, b)) for b in range(k)] for r in range(20)]
prod = {}
def p(r, s, a, b):
    key = (r, s, a, b)
    if key not in prod:
        x = m.NewBoolVar('')
        m.AddBoolAnd([W[r][a], U[s][b]]).OnlyEnforceIf(x)
        m.AddBoolOr([W[r][a].Not(), U[s][b].Not()]).OnlyEnforceIf(x.Not())
        prod[key] = x
    return prod[key]
def terms_of(r, u):
    s, j = rep_of[u]
    return [p(r, s, (b + j) % n, b) for b in range(n)] + [p(r, s, a, a) for a in range(n, k)]
one = m.NewConstant(1)
allrow = []
for r, t in enumerate(reps):
    rowvars = []
    for u in range(V):
        terms = terms_of(r, u)
        if u == t:
            m.AddBoolXOr(terms)                 # parity of terms is odd: B_tt = 1
        elif g.G[t, u] != 0:
            m.AddBoolXOr(terms + [one])         # parity of terms even: B_tu = 0
        else:
            y = m.NewBoolVar('')
            m.AddBoolXOr(terms + [y.Not()])     # y == parity(terms)
            rowvars.append(y)
    m.Add(sum(rowvars) <= w - 1)
    allrow.extend(rowvars)
import os
if os.environ.get('MINW'): m.Minimize(sum(allrow))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
st = s.Solve(m)
print('k', k, 'w', w, s.StatusName(st), 'products', len(prod), 'time', s.WallTime(), 'obj(sum rep rows - 20)', s.ObjectiveValue() if os.environ.get('MINW') else None, 'bound', s.BestObjectiveBound() if os.environ.get('MINW') else None, flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    Uv = [[int(s.Value(x)) for x in row] for row in U]; Wv = [[int(s.Value(x)) for x in row] for row in W]
    print('U', Uv); print('W', Wv)
