"""Good-frame partition (<= 4 uncovered lines) maximising frames inside complete F2 blocks:
star-D4 blocks K_h(F4) (3 frames sharing the cell-sum plane) and matching octets (2 frames)."""
import sys, pickle, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
from ortools.sat.python import cp_model
g = Geom(11); V = g.V
vv = pickle.load(open('vv.pkl', 'rb'))
good = [tuple(sorted(q)) for q in pickle.load(open('../part/good4.pkl', 'rb'))]
fidx = {q: i for i, q in enumerate(good)}
def plane(q):
    t = q[0]; return frozenset(vv[t] ^ vv[x] for x in q[1:])
byplane = collections.defaultdict(list)
for i, q in enumerate(good): byplane[plane(q)].append(i)
blocks = [tuple(fs) for fs in byplane.values() if len(fs) >= 2]
sizes = collections.Counter(len(b) for b in blocks)
print('frames', len(good), '| planes', len(byplane), '| blocks by size', dict(sizes))
m = cp_model.CpModel()
x = [m.NewBoolVar('f%d' % i) for i in range(len(good))]
u = [m.NewBoolVar('u%d' % l) for l in range(V)]
inc = collections.defaultdict(list)
for i, q in enumerate(good):
    for l in q: inc[l].append(x[i])
for l in range(V): m.Add(sum(inc[l]) + u[l] == 1)
m.Add(sum(u) <= 4)
bv = []
for b in blocks:
    y = m.NewBoolVar('')
    for i in b: m.AddImplication(y, x[i])
    bv.append((y, len(b)))
m.Maximize(sum(y * k for y, k in bv))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(sys.argv[1]); s.parameters.num_workers = 8
r = s.Solve(m)
print(s.StatusName(r), 'frames in complete blocks', s.ObjectiveValue(), 'bound', s.BestObjectiveBound())
sol = [good[i] for i in range(len(good)) if s.Value(x[i])]
unc = [l for l in range(V) if s.Value(u[l])]
cb = [blocks[k] for k, (y, kk) in enumerate(bv) if s.Value(y)]
print('frames', len(sol), 'complete blocks', collections.Counter(len(b) for b in cb), 'uncovered', [(g.kind[l], g.supp[l]) for l in unc])
pickle.dump((sol, unc, [[good[i] for i in b] for b in cb]), open('blockpart.pkl', 'wb'))
