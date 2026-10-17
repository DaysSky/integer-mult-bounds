"""Joint CP-SAT: 13 complete PPTT star-D4 blocks on the PG(2,3) lines L_k (apex p_k free, p_k not in L_k) plus a
tiling of all remaining T lines by complete Pasch pairs (8 transversals of a perfect matching of a 6-set)."""
from part13 import *
import collections
from ortools.sat.python import cp_model
frames, per_frame, cnt = pickle.load(open('halfshare.pkl', 'rb'))
byhalf = collections.defaultdict(list)
for i, hs in enumerate(per_frame):
    for hh in hs: byhalf[hh].append(i)
pairs = set()
for i, f in enumerate(frames):
    if g.kind[f[0]] == 'T' and g.kind[f[1]] == 'T':
        c = collections.Counter(j for hh in per_frame[i] for j in byhalf[hh] if j != i)
        js = [j for j, k in c.items() if k == len(per_frame[i])]
        pairs.add(tuple(sorted((i, js[0]))))
pairs = sorted(pairs); pp = [tuple(sorted(set(frames[i]) | set(frames[j]))) for i, j in pairs]
Ls = [sorted(((k + d) % 13) for d in (0, 1, 3, 9)) for k in range(13)]
m = cp_model.CpModel()
a = {(k, p): m.NewBoolVar('a%d_%d' % (k, p)) for k in range(13) for p in range(13) if p not in Ls[k]}
for k in range(13): m.AddExactlyOne([a[k, p] for p in range(13) if p not in Ls[k]])
b = [m.NewBoolVar('b%d' % q) for q in range(len(pp))]
cover = collections.defaultdict(list)
for (k, p), var in a.items():
    for x, y in itertools.combinations(Ls[k], 2): cover[g.T(x, y, p)].append(var)
for q, lines in enumerate(pp):
    for l in lines: cover[l].append(b[q])
for l in range(78, V): m.AddExactlyOne(cover[l])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 1500; s.parameters.num_workers = 4
st = s.Solve(m); print('joint blocks + Pasch pairs:', s.StatusName(st), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    newpart = []
    for k in range(13):
        p = [p for p in range(13) if p not in Ls[k] and s.Value(a[k, p])][0]
        W = Ls[k]
        for (u, w), (y, z) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
            newpart.append((g.P(u, w), g.P(y, z), g.T(u, w, p), g.T(y, z, p)))
        print('block', k, 'L', W, 'apex', p)
    for q in range(len(pp)):
        if s.Value(b[q]): newpart += [frames[pairs[q][0]], frames[pairs[q][1]]]
    assert sorted(l for f in newpart for l in f) == list(range(V))
    pickle.dump(newpart, open('pgpasch_partition.pkl', 'wb')); print('saved', len(newpart), 'frames')
