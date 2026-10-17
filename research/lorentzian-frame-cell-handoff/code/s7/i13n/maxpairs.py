"""Max number of complete Pasch pairs in a TTTT tiling of the T lines left by 13 PG(2,3) star blocks (apex free).
Bound from parity: pairs {a,b} with odd leftover count need an unpaired frame."""
from part13 import *
import collections, sys
from ortools.sat.python import cp_model
frames, per_frame, cnt = pickle.load(open('halfshare.pkl', 'rb'))
byhalf = collections.defaultdict(list)
for i, hs in enumerate(per_frame):
    for hh in hs: byhalf[hh].append(i)
TT = [i for i, f in enumerate(frames) if g.kind[f[0]] == 'T' and g.kind[f[1]] == 'T']
partner = {}
for i in TT:
    c = collections.Counter(j for hh in per_frame[i] for j in byhalf[hh] if j != i)
    partner[i] = [j for j, k in c.items() if k == len(per_frame[i])][0]
Ls = [sorted(((k + d) % 13) for d in (0, 1, 3, 9)) for k in range(13)]
m = cp_model.CpModel()
a = {(k, p): m.NewBoolVar('a%d_%d' % (k, p)) for k in range(13) for p in range(13) if p not in Ls[k]}
for k in range(13): m.AddExactlyOne([a[k, p] for p in range(13) if p not in Ls[k]])
FIX = [12, 7, 1, 1, 1, 7, 12, 11, 7, 7, 1, 2, 11] if len(sys.argv) > 2 and sys.argv[2] == 'fix' else None
if FIX:
    for k in range(13): m.Add(a[k, FIX[k]] == 1)
x = {i: m.NewBoolVar('f%d' % i) for i in TT}
cover = collections.defaultdict(list)
for (k, p), var in a.items():
    for u, w in itertools.combinations(Ls[k], 2): cover[g.T(u, w, p)].append(var)
for i in TT:
    for l in frames[i]: cover[l].append(x[i])
for l in range(78, V): m.AddExactlyOne(cover[l])
pairs = sorted(set(tuple(sorted((i, partner[i]))) for i in TT))
y = []
for i, j in pairs:
    v = m.NewBoolVar(''); m.AddImplication(v, x[i]); m.AddImplication(v, x[j]); y.append(v)
m.Maximize(sum(y))
if len(sys.argv) > 2 and sys.argv[2] == 'hint':
    pg = pickle.load(open('pg23_partition.pkl', 'rb'))
    fset = {tuple(sorted(f)): i for i, f in enumerate(frames)}
    pgT = set(fset[tuple(sorted(f))] for f in pg[39:])
    for (k, p), var in a.items(): m.AddHint(var, 1 if p == (k + 4) % 13 else 0)
    for i in TT: m.AddHint(x[i], 1 if i in pgT else 0)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = int(sys.argv[1])
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self): print('  incumbent', self.ObjectiveValue(), 'bound', self.BestObjectiveBound(), flush=True)
st = s.Solve(m, CB())
print(s.StatusName(st), 'pairs', s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    newpart = []
    for k in range(13):
        p = [p for p in range(13) if (k, p) in a and s.Value(a[k, p])][0]; W = Ls[k]
        for (u, w), (yy, z) in [((W[0], W[1]), (W[2], W[3])), ((W[0], W[2]), (W[1], W[3])), ((W[0], W[3]), (W[1], W[2]))]:
            newpart.append((g.P(u, w), g.P(yy, z), g.T(u, w, p), g.T(yy, z, p)))
    newpart += [frames[i] for i in TT if s.Value(x[i])]
    assert sorted(l for f in newpart for l in f) == list(range(V))
    pickle.dump(newpart, open('maxpairs_partition.pkl', 'wb'))
