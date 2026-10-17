"""Flat-model per-line cover over ALL good-frame partitions: demand of u from chosen frame g (u not in g, >= 2 lines
of g orthogonal to u) is the FLAT {lines orthogonal to every line of pi_g(u)} (section {x,y}^perp or Q-flat g^perp):
some partner v of u must lie in it (a register carrying x_u whose first rank>=2 frame is span{u,v} can only enter
flats containing v).  argv: E8 | T | P, time limit."""
import sys, pickle, itertools, collections, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from ortools.sat.python import cp_model
which = sys.argv[1]; tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
if which == 'E8':
    sys.path.insert(0, '../e8cal'); import e8; sys.path.pop(0)
    GI = e8.GI; orth = (GI == 0); np.fill_diagonal(orth, False); V = e8.V; u = 0
    fr = []
    for a in range(V):
        for b, c, d in itertools.combinations([x for x in range(a + 1, V) if orth[a, x]], 3):
            if orth[b, c] and orth[b, d] and orth[c, d]: fr.append((a, b, c, d))
    def good(q):
        for t in q:
            es = [e for e in q if e != t]
            for l in range(V):
                if l in q or not orth[t, l]: continue
                if sum(orth[l, e] for e in es) % 2 == 0: return False
        return True
    frames = [q for q in fr if good(q)]
else:
    from geom import Geom
    g = Geom(13); V = g.V; orth = (g.G == 0); np.fill_diagonal(orth, False)
    frames, _, _ = pickle.load(open('../i13a/compat13.pkl', 'rb'))
    u = g.T(0, 1, 2) if which == 'T' else g.P(0, 1)
m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(len(frames))]
y = {v: m.NewBoolVar('y%d' % v) for v in range(V) if v != u}
by = collections.defaultdict(list)
for i, q in enumerate(frames):
    for l in q: by[l].append(i)
for l in range(V): m.AddExactlyOne([x[i] for i in by[l]])
nd = 0; cache = {}
for i, q in enumerate(frames):
    if u in q: continue
    pi = tuple(l for l in q if orth[u, l])
    if len(pi) < 2: continue
    if pi not in cache:
        ok = np.all(orth[:, list(pi)], axis=1); ok[u] = False
        cache[pi] = [int(v) for v in np.nonzero(ok)[0]]
    m.AddBoolOr([x[i].Not()] + [y[v] for v in cache[pi]]); nd += 1
m.Minimize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
st = s.Solve(m)
print('%s flat-model per-line min cover: %s obj %s bound %s (demand constraints %d)' % (which, s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), nd), flush=True)
