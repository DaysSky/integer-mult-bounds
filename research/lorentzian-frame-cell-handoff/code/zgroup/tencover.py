"""33 D10-frames covering I_{11,1}'s targets: each T(xyz) assigned to one apex in xyz and one of 3 perfect matchings of
[11]-apex; every P(ij) lies in some used frame.  Then the 10-frame top's demands (blocks = orthogonality classes of
the frame, restricted to blocks with a target user) and the per-line cell cover (min partners so that every demand
containing u contains a partner; E8 R420 = 3, I13 PG(2,3) = 6-7)."""
import sys, collections, itertools, pickle, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V; G = g.G
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]
T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
orth = lambda x, y: x != y and G[x, y] == 0
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
m = cp_model.CpModel()
y = {}
for a in range(11):
    pts = [i for i in range(11) if i != a]
    for k in range(3):
        for i, j in itertools.combinations(pts, 2): y[a, k, i, j] = m.NewBoolVar('')
        for i in pts: m.AddExactlyOne([y[a, k, min(i, j), max(i, j)] for j in pts if j != i])
for x, yy, z in itertools.combinations(range(11), 3):
    m.AddExactlyOne([y[ap, k, *sorted(set((x, yy, z)) - {ap})] for ap in (x, yy, z) for k in range(3)])
for i, j in itertools.combinations(range(11), 2):
    m.AddBoolOr([y[a, k, i, j] for a in range(11) if a not in (i, j) for k in range(3)])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 8; s.parameters.random_seed = seed
st = s.Solve(m); print('cover', s.StatusName(st), flush=True)
if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): sys.exit()
frames = []
for a in range(11):
    for k in range(3):
        M = [(i, j) for (aa, kk, i, j), v in y.items() if aa == a and kk == k and s.Value(v)]
        frames.append((a, M, [P(i, j) for i, j in M] + [T(i, j, a) for i, j in M]))
# targets: each T in its frame; each P in the first frame containing it
home = {}
for fi, (a, M, f) in enumerate(frames):
    for u in f[5:]: home[u] = fi
for fi, (a, M, f) in enumerate(frames):
    for u in f[:5]: home.setdefault(u, fi)
assert len(home) == V
tg = collections.defaultdict(set)
for u, fi in home.items(): tg[fi].add(u)
print('targets per frame', sorted(collections.Counter(len(v) for v in tg.values()).items()))
dem = []; load = 0
for fi, (a, M, f) in enumerate(frames):
    cls = collections.defaultdict(list)
    for u in range(V):
        if u in f: continue
        cls[frozenset(x for x in f if orth(u, x))].append(u)
    for sg, c in cls.items():
        users = sg & tg[fi]
        if users: dem.append((fi, frozenset(c), users)); load += len(c)
print('demands', len(dem), 'load', load, 'per line %.1f' % (load / V))
# per-line cover
memb = collections.defaultdict(list)
for di, (fi, c, us) in enumerate(dem):
    for u in c: memb[u].append(di)
covers = []
for u in range(V):
    D = memb[u]
    cand = sorted(set(w for di in D for w in dem[di][1] if w != u))
    mm = cp_model.CpModel(); z = {w: mm.NewBoolVar('') for w in cand}
    for di in D: mm.AddBoolOr([z[w] for w in dem[di][1] if w != u])
    mm.Minimize(sum(z.values()))
    ss = cp_model.CpSolver(); ss.parameters.max_time_in_seconds = 20; ss.parameters.num_workers = 4
    r = ss.Solve(mm); covers.append((int(ss.ObjectiveValue()), int(ss.BestObjectiveBound()), len(D)))
print('per-line cover (value, bound, #demands) distribution:', sorted(collections.Counter(c[:2] for c in covers).items()))
print('mean cover %.2f' % np.mean([c[0] for c in covers]), 'demands per line', sorted(collections.Counter(c[2] for c in covers).items())[:5], '...')
pickle.dump(dict(frames=frames, home=home, dem=dem), open('tencover_%d.pkl' % seed, 'wb'))
