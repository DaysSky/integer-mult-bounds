"""Pasch pairs (TTTT frames sharing all 12 halves) and an exact tiling of the T lines outside the 13 PG(2,3)
PPTT blocks by Pasch pairs (CP-SAT).  Also: tiling with free choice of the PPTT blocks."""
from part13 import *
import collections
from ortools.sat.python import cp_model
frames, per_frame, cnt = pickle.load(open('halfshare.pkl', 'rb'))
fidx = {f: i for i, f in enumerate(frames)}
byhalf = collections.defaultdict(list)
for i, hs in enumerate(per_frame):
    for hh in hs: byhalf[hh].append(i)
partner = {}
for i, f in enumerate(frames):
    if g.kind[f[0]] != 'T' or g.kind[f[1]] != 'T': continue
    c = collections.Counter(j for hh in per_frame[i] for j in byhalf[hh] if j != i)
    js = [j for j, k in c.items() if k == len(per_frame[i])]
    assert len(js) == 1, (i, c.most_common(3))
    partner[i] = js[0]
pairs = sorted(set(tuple(sorted((i, j))) for i, j in partner.items()))
print('Pasch pairs', len(pairs))
pp = [tuple(sorted(set(frames[i]) | set(frames[j]))) for i, j in pairs]
print('lines per pair', collections.Counter(len(p) for p in pp))
pptt = part[:39]
used = set(l for f in pptt for l in f); rest = set(range(V)) - used
cand = [k for k, p in enumerate(pp) if set(p) <= rest]
print('pairs inside the 208 remaining T lines', len(cand))
m = cp_model.CpModel(); x = {k: m.NewBoolVar('p%d' % k) for k in cand}
for l in rest: m.AddExactlyOne([x[k] for k in cand if l in pp[k]])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 900; s.parameters.num_workers = 4
st = s.Solve(m); print('tiling with PG blocks fixed:', s.StatusName(st), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [k for k in cand if s.Value(x[k])]
    newpart = pptt + [frames[i] for k in sel for i in pairs[k]]
    assert sorted(l for f in newpart for l in f) == list(range(V))
    pickle.dump(newpart, open('pgpasch_partition.pkl', 'wb')); print('saved pgpasch_partition.pkl')
