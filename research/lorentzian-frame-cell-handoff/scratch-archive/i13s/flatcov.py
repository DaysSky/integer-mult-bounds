"""Flat-model per-line cover on a FIXED partition: demands of u = section flats {x,y}^perp (E-type, u perp exactly
x,y of frame g) and Q-flats g^perp (u perp all of g); partner v covers a demand iff v lies in the flat.  Exact CP-SAT
per line orbit (Z13).  Also the full-section variant: Q-frames contribute their 6 section flats."""
import sys, pickle, itertools, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(13); V = g.V; orth = (g.G == 0); np.fill_diagonal(orth, False)
part = pickle.load(open(sys.argv[1], 'rb')) if len(sys.argv) > 1 else pickle.load(open('../i13a/pg23_partition.pkl', 'rb'))
frame_of = {u: f for f in part for u in f}
def shift(l, k):
    return g.idx[(g.kind[l], tuple(sorted((x + k) % 13 for x in g.supp[l])))]
reps = []; seen = set()
for l in range(V):
    if l in seen: continue
    reps.append(l); seen |= {shift(l, k) for k in range(13)}
def cover(u, full):
    dem = []
    for f in part:
        if u in f: continue
        pi = [x for x in f if orth[u, x]]
        if len(pi) < 2: continue
        if len(pi) == 4 and full:
            for a, b in itertools.combinations(f, 2): dem.append((a, b))
        else: dem.append(tuple(pi))
    m = cp_model.CpModel(); y = {v: m.NewBoolVar('') for v in range(V) if v != u}
    for d in dem:
        m.AddBoolOr([y[v] for v in y if all(orth[v, x] for x in d)])
    m.Minimize(sum(y.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 60; s.parameters.num_workers = 2
    st = s.Solve(m); return int(s.ObjectiveValue()), int(s.BestObjectiveBound()), len(dem)
for full in (False, True):
    res = [cover(u, full) for u in reps]
    print('%s: per-orbit cover' % ('full sections' if full else 'E-sections + Q-flats'), [r[0] for r in res], 'bounds', [r[1] for r in res], 'mean %.2f' % np.mean([r[0] for r in res]), flush=True)
