"""Necessary condition (both pattern and flat demand models): every reader l of u outside u's own frame lies in some
demand of u, and a partner v in that demand is orthogonal to l.  So R(u) minus u's 3 frame-mates must be covered by
the perps R(v) of the partners.  Min k (exact CP-SAT), I_{13,1} T and P lines, E8 control."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from ortools.sat.python import cp_model
def solve(orth, u, frames_u, name):
    V = len(orth); R = [l for l in range(V) if orth[u, l]]
    best = None
    m = cp_model.CpModel()
    y = {v: m.NewBoolVar('y%d' % v) for v in range(V) if v != u}
    z = [m.NewBoolVar('z%d' % i) for i in range(len(frames_u))]
    m.AddExactlyOne(z)
    for l in R:
        own = [z[i] for i, q in enumerate(frames_u) if l in q]
        m.AddBoolOr(own + [y[v] for v in y if orth[v, l]])
    m.Minimize(sum(y.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 4
    st = s.Solve(m)
    print('%s: |R(u)| %d, min partners covering R(u)\\mates: %s %d (bound %d); max |R(u)&R(v)| %d' % (
        name, len(R), s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(),
        max(int((orth[u] & orth[v]).sum()) for v in range(V) if v != u)), flush=True)
sys.path.insert(0, '../e8cal'); import e8; sys.path.pop(0)
GI = e8.GI; o8 = (GI == 0); np.fill_diagonal(o8, False)
fr8 = [q for q in itertools.combinations([x for x in range(e8.V) if o8[0, x]], 3) if all(o8[a, b] for a, b in itertools.combinations(q, 2))]
solve(o8, 0, fr8, 'E8')
from geom import Geom
import pickle
g = Geom(13); G = g.G; o13 = (G == 0); np.fill_diagonal(o13, False)
frames, _, _ = pickle.load(open('../i13a/compat13.pkl', 'rb'))
for nm, u in (('I13 T', g.T(0, 1, 2)), ('I13 P', g.P(0, 1))):
    fu = [tuple(x for x in q if x != u) for q in frames if u in q]
    solve(o13, u, fu, nm)
