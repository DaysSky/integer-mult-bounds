"""Per-line cell cover (min partners so that every demand containing u contains a partner) for 4-frame tops:
demands = Q-part (perp to all 4) and the 6 E-sets of every frame.  Usage: coverline.py i11 | e8"""
import sys, collections, itertools, pickle, numpy as np
from ortools.sat.python import cp_model
mode = sys.argv[1]
if mode == 'i11':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
    from geom import Geom
    g = Geom(11); V = g.V; GG = g.G
    frames, pun = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/goodframe/goodpart.pkl', 'rb'))
    live = [u for u in range(V) if u not in set(pun)]
    orth = lambda a, b: a != b and GG[a, b] == 0
else:
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    from geom import Geom as GE
    frames = GE().frames4; live = list(range(e8.V)); orth = lambda a, b: a != b and e8.GI[a, b] == 0
dem = []
for f in frames:
    dem.append(frozenset(u for u in live if all(orth(u, x) for x in f)))
    for t, e in itertools.combinations(f, 2):
        o = [x for x in f if x not in (t, e)]
        dem.append(frozenset(u for u in live if orth(u, t) and orth(u, e) and not orth(u, o[0]) and not orth(u, o[1])))
dem = [d for d in dem if d]
print('demands', len(dem), 'load', sum(map(len, dem)), 'per line %.1f' % (sum(map(len, dem)) / len(live)))
memb = collections.defaultdict(list)
for di, d in enumerate(dem):
    for u in d: memb[u].append(di)
res = []
for u in live[:int(sys.argv[2]) if len(sys.argv) > 2 else None]:
    D = memb[u]; cand = sorted(set(w for di in D for w in dem[di] if w != u))
    mm = cp_model.CpModel(); z = {w: mm.NewBoolVar('') for w in cand}
    for di in D: mm.AddBoolOr([z[w] for w in dem[di] if w != u])
    mm.Minimize(sum(z.values()))
    ss = cp_model.CpSolver(); ss.parameters.max_time_in_seconds = 30; ss.parameters.num_workers = 4
    ss.Solve(mm); res.append((int(ss.ObjectiveValue()), int(ss.BestObjectiveBound())))
print('per-line cover (value, bound):', sorted(collections.Counter(res).items()), 'mean %.2f' % np.mean([r[0] for r in res]))
