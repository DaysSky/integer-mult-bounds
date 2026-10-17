"""E8 R420 partition: Q-part sharing and per-line cover with demands = sign halves + Q-parts."""
import sys, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom as GE
from ortools.sat.python import cp_model
frames = GE().frames4; GI = e8.GI; V = e8.V
orth = lambda a, b: a != b and GI[a, b] == 0
Qs = collections.Counter(); dem = set()
for f in frames:
    Q = frozenset(u for u in range(V) if all(orth(u, x) for x in f)); Qs[Q] += 1; dem.add(Q)
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = [u for u in range(V) if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)]
        dem.add(frozenset(u for u in E if GI[u, k] == GI[u, l])); dem.add(frozenset(u for u in E if GI[u, k] == -GI[u, l]))
print('Q-part sharing (frames per Q):', sorted(collections.Counter(Qs.values()).items()), 'distinct demands', len(dem))
memb = collections.defaultdict(list); dem = list(dem)
for di, d_ in enumerate(dem):
    for u in d_: memb[u].append(di)
res = []
for u in range(V):
    D = memb[u]; cand = sorted(set(w for di in D for w in dem[di] if w != u))
    mm = cp_model.CpModel(); z = {w: mm.NewBoolVar('') for w in cand}
    for di in D: mm.AddBoolOr([z[w] for w in dem[di] if w != u])
    mm.Minimize(sum(z.values())); ss = cp_model.CpSolver(); ss.parameters.max_time_in_seconds = 20; ss.parameters.num_workers = 1
    ss.Solve(mm); res.append((int(ss.ObjectiveValue()), int(ss.BestObjectiveBound())))
print('per-line cover (halves + Q):', sorted(collections.Counter(res).items()))
