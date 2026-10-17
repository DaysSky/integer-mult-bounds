"""Exact vector-level maximum of h = 9 root-like systems in class B1 (k in {4,5}) and B2 (k in {4,8}) that contain at
least one non-k4 line.  Coordinates: orthogonal 8-frame e_i (norm 2) and n (norm -1); a line u = sum x_i e_i / 2 +
gamma n, x in {0,+-1}^8, gamma^2 = k/2 - 2.  Products: <u,u'> = (x.x')/2 - gamma gamma'.  Work with 2<u,u'> integer:
k5 gamma = s/sqrt2 -> 2 gamma gamma' = s s'; k8 gamma = s sqrt2 -> 2 gamma gamma' = 4 s s'.  Frame lines forced (WLOG
in every >= 120-line system).  WLOG one fixed non-k4 line (signed permutations and n -> -n are transitive on them)."""
import itertools, sys, time
from ortools.sat.python import cp_model
cls = sys.argv[1] if len(sys.argv) > 1 else 'B1'; tl = float(sys.argv[2]) if len(sys.argv) > 2 else 3600
K2 = {'B1': 5, 'B2': 8}[cls]
vecs = []   # (x tuple, gtype) ; gtype: 0 for k4, s=+-1 for k2-class
for i in range(8):
    x = [0] * 8; x[i] = 2; vecs.append((tuple(x), 0, 'F'))   # frame line e_i: x_i = <e_i,e_i> = 2 -> e_i = (2 e_i)/2
for S in itertools.combinations(range(8), 4):
    for sg in itertools.product((1, -1), repeat=3):
        x = [0] * 8; x[S[0]] = 1
        for j, s in zip(S[1:], sg): x[j] = s
        vecs.append((tuple(x), 0, 'k4'))
for S in itertools.combinations(range(8), K2):
    for sg in itertools.product((1, -1), repeat=K2 - 1):
        for s in (1, -1):
            x = [0] * 8; x[S[0]] = 1
            for j, t in zip(S[1:], sg): x[j] = t
            vecs.append((tuple(x), s, 'k%d' % K2))
def ip2(a, b):  # 2 <u, u'>
    xa, sa, ka = a; xb, sb, kb = b
    d = sum(p * q for p, q in zip(xa, xb))
    if ka == 'F' or kb == 'F': return d   # frame: <e_i, u> = x_i  -> 2<.,.> = 2 x_i ... handled below
    g = 0
    if ka != 'k4' and kb != 'k4' : g = (sa * sb) if K2 == 5 else 4 * sa * sb
    return d - g
def prod(a, b):
    xa, sa, ka = a; xb, sb, kb = b
    if ka == 'F' and kb == 'F': return 0 if xa != xb else 2
    if ka == 'F': i = xa.index(2); return xb[i]
    if kb == 'F': i = xb.index(2); return xa[i]
    t = ip2(a, b)
    if t % 2: return None
    return t // 2
for v in vecs:   # norms
    if v[2] == 'F': continue
    n2 = sum(p * p for p in v[0]) - ((1 if K2 == 5 else 4) if v[2] != 'k4' else 0)
    assert n2 == 4, (v, n2)
V = len(vecs)
ok = lambda a, b: (lambda p: p is not None and abs(p) <= 1)(prod(vecs[a], vecs[b]))
u0 = next(i for i, v in enumerate(vecs) if v[2] != 'k4' and v[2] != 'F')
pool = [i for i in range(V) if vecs[i][2] == 'F' or i == u0 or (ok(i, u0) and all(ok(i, f) for f in range(8)))]
print(cls, 'pool', V, 'compatible with frame + u0:', len(pool), flush=True)
m = cp_model.CpModel(); y = {i: m.NewBoolVar('') for i in pool}
for i in range(8): m.Add(y[i] == 1)
m.Add(y[u0] == 1)
ne = 0
for a, b in itertools.combinations(pool, 2):
    if not ok(a, b): m.AddBoolOr([y[a].Not(), y[b].Not()]); ne += 1
print('conflicts', ne, flush=True)
m.Maximize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2): super().__init__(); s2.t0 = time.time()
    def on_solution_callback(s2): print('  sol %d bound %.0f (%.0fs)' % (s2.ObjectiveValue(), s2.BestObjectiveBound(), time.time() - s2.t0), flush=True)
st = s.Solve(m, CB())
print(cls, 'max lines with a non-k4 line:', s.StatusName(st), s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sel = [i for i in pool if s.Value(y[i])]
    import collections; print(collections.Counter(vecs[i][2] for i in sel))
    import pickle; pickle.dump([vecs[i] for i in sel], open('%s_best.pkl' % cls, 'wb'))
