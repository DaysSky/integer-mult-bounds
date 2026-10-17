"""E8 control for coverlb.py: per-line min cover over ALL good-4-frame partitions of the 120 E8 lines."""
import sys, itertools, collections, numpy as np
sys.path.insert(0, '../e8cal')
import e8
from ortools.sat.python import cp_model
V = e8.V; GI = e8.GI
orth = (GI == 0); np.fill_diagonal(orth, False)
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
print('4-frames', len(fr), 'good', len(frames), flush=True)
u = 0
m = cp_model.CpModel(); x = [m.NewBoolVar('x%d' % i) for i in range(len(frames))]
y = {v: m.NewBoolVar('y%d' % v) for v in range(V) if v != u}
by = collections.defaultdict(list)
for i, q in enumerate(frames):
    for l in q: by[l].append(i)
for l in range(V): m.AddExactlyOne([x[i] for i in by[l]])
nd = 0
for i, q in enumerate(frames):
    if u in q: continue
    pu = orth[u, list(q)]
    if pu.sum() < 2: continue
    same = np.all(orth[:, list(q)] == pu, axis=1); same[u] = False
    m.AddBoolOr([x[i].Not()] + [y[int(v)] for v in np.nonzero(same)[0]]); nd += 1
m.Minimize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
st = s.Solve(m)
print('E8 per-line min cover over all partitions:', s.StatusName(st), s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), 'demand constraints', nd)
