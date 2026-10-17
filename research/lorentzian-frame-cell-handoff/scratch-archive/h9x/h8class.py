"""h = 8 Lorentzian (R^{7,1}) root-like systems containing an orthogonal 7-frame: exact vector-level maxima per class
(k4 + kK, K in {5, 6, 7}) with at least one timelike-using line.  u = sum x_i e_i / 2 + gamma n, e_i^2 = 2, n^2 = -1,
gamma^2 = k/2 - 2; 2<u,u'> = x.x' - 2 gamma gamma'.  K=5: 2gg' = s s'; K=6: 2gg' = 2 s s'; K=7: 2gg' = 3 s s'."""
import itertools, sys, time, collections
from ortools.sat.python import cp_model
K2 = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1200
D = 7
gg = {5: 1, 6: 2, 7: 3}[K2]
vecs = []
for i in range(D):
    x = [0] * D; x[i] = 2; vecs.append((tuple(x), 0, 'F'))
for S in itertools.combinations(range(D), 4):
    for sg in itertools.product((1, -1), repeat=3):
        x = [0] * D; x[S[0]] = 1
        for j, s in zip(S[1:], sg): x[j] = s
        vecs.append((tuple(x), 0, 'k4'))
for S in itertools.combinations(range(D), K2):
    for sg in itertools.product((1, -1), repeat=K2 - 1):
        for s in (1, -1):
            x = [0] * D; x[S[0]] = 1
            for j, t in zip(S[1:], sg): x[j] = t
            vecs.append((tuple(x), s, 'k%d' % K2))
def prod(a, b):
    xa, sa, ka = a; xb, sb, kb = b
    if ka == 'F' and kb == 'F': return 0 if xa != xb else 2
    if ka == 'F': return xb[xa.index(2)]
    if kb == 'F': return xa[xb.index(2)]
    t = sum(p * q for p, q in zip(xa, xb)) - (gg * sa * sb if ka != 'k4' and kb != 'k4' else 0)
    return None if t % 2 else t // 2
ok = lambda a, b: (lambda p: p is not None and abs(p) <= 1)(prod(vecs[a], vecs[b]))
u0 = next(i for i, v in enumerate(vecs) if v[2] not in ('k4', 'F'))
pool = [i for i in range(len(vecs)) if vecs[i][2] == 'F' or i == u0 or (ok(i, u0) and all(ok(i, f) for f in range(D)))]
m = cp_model.CpModel(); y = {i: m.NewBoolVar('') for i in pool}
for i in range(D): m.Add(y[i] == 1)
m.Add(y[u0] == 1)
for a, b in itertools.combinations(pool, 2):
    if not ok(a, b): m.AddBoolOr([y[a].Not(), y[b].Not()])
m.Maximize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 2
st = s.Solve(m)
sel = [i for i in pool if s.Value(y[i])]
print('h=8 class {4,%d} with a 7-frame and a timelike line: %s %d (bound %d), pool %d, mix %s' % (K2, s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), len(pool), dict(collections.Counter(vecs[i][2] for i in sel))), flush=True)
