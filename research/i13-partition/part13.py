"""Partition of the I_{13,1} lines into good 4-frames: Z13-invariant exact cover (frame orbits under translation),
then optionally a no-symmetry run (GRPSYM=0).  Mirrors the I11,1 finding that no partition exists there."""
import os, collections
from ortools.sat.python import cp_model
import base13 as B

g, V = B.g, B.V
p13 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'goodframes13.pkl')
import pickle
fr = pickle.load(open(p13, 'rb'))

# Z13 translation orbits of frames (translations are x -> x + k)
zperms = [B.PERMS[B.GROUP.index((1, k))] for k in range(B.N)]

def tact(mask, k):
    return B.act(mask, zperms[k % B.N])

seen = {}
orbits = []
for F in fr:
    if F in seen: continue
    o = []
    m = F
    for k in range(B.N):
        if m not in seen:
            seen[m] = True; o.append(m)
        m = B.act(m, zperms[k])
    if o: orbits.append(sorted(o))
print('frame orbits (Z13)', len(orbits), 'of', len(fr), 'frames')

# line orbits under Z13
lo = {}
lorbits = []
for s in range(V):
    if s in lo: continue
    o = []
    for k in range(B.N):
        img = B.line_img(s, 1, k)
        lo[img] = len(lorbits); o.append(img)
    lorbits.append(o)
print('line orbits', len(lorbits), 'lines keyed', len(lo))

# each frame orbit covers each line-orbit 0 or 13 times
cov = []
for oi, o in enumerate(orbits):
    c = collections.Counter()
    for F in o:
        for s in g.bits(F): c[lo[s]] += 1
    cov.append(c)

model = cp_model.CpModel()
x = [model.NewBoolVar(f'o{i}') for i in range(len(orbits))]
for j in range(len(lorbits)):
    model.Add(sum(cov[i][j] * x[i] for i in range(len(orbits)) if j in cov[i]) == 13)
model.Add(sum(x) == 7)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = float(os.environ.get('TMAX', '300'))
solver.parameters.num_search_workers = 8
st = solver.Solve(model)
print('Z13 partition:', solver.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = [orbits[i] for i in range(len(orbits)) if solver.Value(x[i])]
    print('frames chosen', sum(len(o) for o in chosen))
    kinds = collections.Counter()
    for o in chosen:
        kc = collections.Counter()
        for F in o:
            for s in g.bits(F):
                if g.kind[s] == 'P': kc['P'] += 1
        kinds[kc['P'] // 13] += 1
    print('orbit P-counts (x13 frames each)', dict(kinds))
    # verify exact cover
    cover = collections.Counter()
    for o in chosen:
        for F in o:
            for s in g.bits(F): cover[s] += 1
    print('cover counts', collections.Counter(cover.values()), 'lines covered', len(cover))
else:
    print('no Z13-invariant partition exists')
