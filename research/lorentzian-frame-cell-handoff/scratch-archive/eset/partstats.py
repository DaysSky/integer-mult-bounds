"""Alignment statistics of an I_{11,1} good-frame partition pickle (frames, punctured): half sharing, Q sharing, load,
per-line cell cover with demands = Q-parts + E-sets (E8 R420: 3).  usage: partstats.py PART.pkl"""
import sys, collections, itertools, pickle
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V; G = g.G
frames, pun = pickle.load(open(sys.argv[1], 'rb')); live = [u for u in range(V) if u not in set(pun)]
orth = lambda a, b: a != b and G[a, b] == 0
halves = collections.Counter(); Qs = collections.Counter(); Es = []
for f in frames:
    Q = frozenset(u for u in live if all(orth(u, x) for x in f)); Qs[Q] += 1
    for t, e in itertools.combinations(f, 2):
        k, l = [x for x in f if x not in (t, e)]
        E = frozenset(u for u in live if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)); Es.append(E)
        halves[frozenset(u for u in E if G[u, k] == G[u, l])] += 1; halves[frozenset(u for u in E if G[u, k] == -G[u, l])] += 1
print('frames', len(frames), 'punctured', len(pun))
print('half sharing (multiplicity: #halves):', sorted(collections.Counter(halves.values()).items()), 'distinct', len(halves))
print('Q sharing:', sorted(collections.Counter(Qs.values()).items()))
dem = list(set(Es) | set(Qs)); load = sum(map(len, dem))
hl = sum(len(H) for H in halves) + sum(len(Q) for Q in Qs)
print('distinct E/Q demands', len(dem), 'load %.1f/line' % (load / len(live)), '| half+Q load %.1f/line' % (hl / len(live)))
if '--cover' in sys.argv:
    memb = collections.defaultdict(list)
    for di, d_ in enumerate(dem):
        for u in d_: memb[u].append(di)
    res = []
    for u in live:
        D = memb[u]; cand = sorted(set(w for di in D for w in dem[di] if w != u))
        mm = cp_model.CpModel(); z = {w: mm.NewBoolVar('') for w in cand}
        for di in D: mm.AddBoolOr([z[w] for w in dem[di] if w != u])
        mm.Minimize(sum(z.values())); ss = cp_model.CpSolver(); ss.parameters.max_time_in_seconds = 20; ss.parameters.num_workers = 1
        ss.Solve(mm); res.append((int(ss.ObjectiveValue()), int(ss.BestObjectiveBound())))
    print('per-line cover:', sorted(collections.Counter(res).items()))
