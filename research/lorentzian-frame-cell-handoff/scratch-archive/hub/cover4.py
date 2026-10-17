# Set-cover ILP: minimum number of closed rank-8 frames (W-perp, W = 3 lines incl. t; users >= 3) covering R(t);
# also with users >= 4, >= 5, >= 6.  Exact (CP-SAT OPTIMAL) within this frame family.
import sys, itertools, numpy as np, collections, time, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
from ortools.sat.python import cp_model
tname = sys.argv[1]
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]; Rl = bits(Rt)
def perpm(ls):
    m = (1 << V) - 1
    for u in ls: m &= g.HYP[u]
    return m
cand = [u for u in range(V) if u != t and abs(g.G[t, u]) <= 1]
F8 = {}
for u, v in itertools.combinations(cand, 2):
    m = perpm([t, u, v]) & Rt
    if m in F8 or m == 0: continue
    if np.linalg.matrix_rank(g.L[[t, u, v]].astype(float)) != 3: continue
    if dim(m) != 8: continue
    F8[m] = sum(1 for w in range(V) if all(abs(g.G[w, h]) < 0.5 for h in bits(m)))
print(tname, 'closed rank-8 frames', len(F8), flush=True)
for umin in (3, 4, 5, 6):
    Fs = [m for m, us in F8.items() if us >= umin]
    md = cp_model.CpModel(); x = [md.NewBoolVar('') for _ in Fs]
    for u in Rl: md.AddBoolOr([x[k] for k, m in enumerate(Fs) if m >> u & 1] or [md.NewConstant(0)])
    md.Minimize(sum(x)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
    r = s.Solve(md)
    print('  users >= %d: frames %d | min cover %s (%s)' % (umin, len(Fs), s.ObjectiveValue() if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else '-', s.StatusName(r)), flush=True)
