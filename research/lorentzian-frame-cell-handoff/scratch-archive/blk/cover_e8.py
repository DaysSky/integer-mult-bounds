import sys, itertools, collections
sys.path.insert(0, '.')
import e8
from geom import Geom
from ortools.sat.python import cp_model
G = Geom(); GI = e8.GI; V = e8.V
dem = []
for f in G.frames4:
    dem.append(G.blocks[G.comp[G.blk[f[0]]]])
    for x, y in itertools.combinations(f, 2):
        o = [z for z in f if z not in (x, y)]
        E = 0
        for s in e8.bits(G.D6[(x, y) if x < y else (y, x)]):
            if GI[s, o[0]] != 0 and GI[s, o[1]] != 0: E |= 1 << s
        dem.append(E)
dem = list(set(dem))
mem = collections.defaultdict(set)
for i, d in enumerate(dem):
    for u in e8.bits(d): mem[u].add(i)
res = []
for u in range(V):
    Du = sorted(mem[u])
    m = cp_model.CpModel()
    xv = {v: m.NewBoolVar('v%d' % v) for v in range(V) if v != u and mem[u] & mem[v]}
    sv = {d: m.NewBoolVar('s%d' % d) for d in Du}
    for d in Du: m.Add(sum(xv[v] for v in xv if d in mem[v]) + sv[d] >= 1)
    m.Minimize(sum(xv.values()) + sum(sv.values()))
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 20
    r = s.Solve(m); res.append((int(s.ObjectiveValue()), s.StatusName(r)))
print('E8 set-cover parts per line: mean %.2f min %d max %d' % (sum(r[0] for r in res) / V, min(r[0] for r in res), max(r[0] for r in res)), collections.Counter(r[1] for r in res))
