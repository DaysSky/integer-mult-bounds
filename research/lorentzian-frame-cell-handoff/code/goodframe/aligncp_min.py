"""Exact: does an aligned good-frame partition exist (<= 4 punctured lines, every E-set even on every frame)?
WLOG P(01) lies in frame (4;01|23) or is punctured (all P lines and all PPTT frames through a P line are equivalent
under S11; the punctured case is handled by PUNCT01=1)."""
import sys, os, pickle, numpy as np, collections, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); n = len(good); comp = pickle.load(open('compat.pkl', 'rb'))
idx = {tuple(sorted(q)): i for i, q in enumerate(good)}
i0 = idx[tuple(sorted((g.P(0, 1), g.P(2, 3), g.T(0, 1, 4), g.T(2, 3, 4))))]
S = sorted(comp[i0].tolist()); Sset = set(S)
print('candidates', len(S), flush=True)
m = cp_model.CpModel()
x = {j: m.NewBoolVar('x%d' % j) for j in S}
p = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for j in S:
    for u in good[j]: inc[u].append(x[j])
fixed = set(good[i0])
for u in range(V):
    if u in fixed: m.Add(p[u] == 0); continue
    m.Add(sum(inc[u]) + p[u] == 1)
m.Minimize(sum(p))
# parity: punctured lines: 1 P + 3 T or 3 P + 1 T
npair = 0
for a in S:
    ca = set(comp[a].tolist())
    for b in S:
        if b <= a or b in ca: continue
        if set(good[a]) & set(good[b]): continue
        m.AddBoolOr([x[a].Not(), x[b].Not()]); npair += 1
print('incompatible disjoint pairs', npair, flush=True)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 1800; s.parameters.num_workers = 8
r = s.Solve(m)
print(s.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [i0] + [j for j in S if s.Value(x[j])]
    pun = [u for u in range(V) if s.Value(p[u])]
    print("obj", s.ObjectiveValue(), "bound", s.BestObjectiveBound()); print("frames", len(sol), 'punctured', [(g.kind[u], g.supp[u]) for u in pun])
    pickle.dump((sol, pun), open('aligned_part_min.pkl', 'wb'))
