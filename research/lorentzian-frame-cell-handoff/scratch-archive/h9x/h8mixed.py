"""h = 8 Lorentzian MIXED-SIGN root-like systems (norms +2 and -2, products 0/+-1) containing a spacelike orthogonal
7-frame e_1..e_7 (norm 2), n timelike unit (n^2 = -1).  u = sum x_i e_i / 2 + g n, x_i = <u,e_i> in {0,+-1}.
spacelike: |x|^2/2 - g^2 = 2 ; timelike: |x|^2/2 - g^2 = -2.  2<u,u'> = x.x' - 2 g g'.
Classes (g g' rational): A' = {k4s g=0, k5s g=1/sqrt2, k0t g=sqrt2, k5t g=3/sqrt2};  B' = {k4s, k6s g=1, k4t g=2}.
Work with s = g*sqrt2 (A': 0, 1, 2, 3) or g (B': 0, 1, 2); 2gg' = s s' (A') or 2 g g' (B').  Exact CP-SAT max clique,
frame forced, one non-k4s line fixed WLOG per type (run for each type)."""
import itertools, sys, collections
from ortools.sat.python import cp_model
cls = sys.argv[1]; D = 7
def lines_A():
    out = []
    for i in range(D):
        x = [0]*D; x[i] = 2; out.append((tuple(x), 0, 'F'))
    for k, s, tag in ((4, 0, 'k4s'), (5, 1, 'k5s'), (0, 2, 'k0t'), (5, 3, 'k5t')):
        for S in itertools.combinations(range(D), k):
            for sg in itertools.product((1, -1), repeat=k):
                for gs in ((1, -1) if s else (1,)):
                    x = [0]*D
                    for j, t in zip(S, sg): x[j] = t
                    v = (tuple(x), gs*s, tag)
                    neg = (tuple(-a for a in x), -gs*s, tag)
                    if neg not in out and v not in out: out.append(v)
    return out
def lines_B():
    out = []
    for i in range(D):
        x = [0]*D; x[i] = 2; out.append((tuple(x), 0, 'F'))
    for k, s, tag in ((4, 0, 'k4s'), (6, 1, 'k6s'), (4, 2, 'k4t')):
        for S in itertools.combinations(range(D), k):
            for sg in itertools.product((1, -1), repeat=k):
                for gs in ((1, -1) if s else (1,)):
                    x = [0]*D
                    for j, t in zip(S, sg): x[j] = t
                    v = (tuple(x), gs*s, tag); neg = (tuple(-a for a in x), -gs*s, tag)
                    if neg not in out and v not in out: out.append(v)
    return out
L = lines_A() if cls == 'A' else lines_B()
def norm2(a):   # 2<u,u>
    x, s, t = a
    if t == 'F': return 4   # e_i: 2*2
    return sum(c*c for c in x) - (s*s if cls == 'A' else 2*s*s)
def ip2(a, b):
    xa, sa, ta = a; xb, sb, tb = b
    if ta == 'F' and tb == 'F': return 0 if xa != xb else 4
    if ta == 'F': return 2 * xb[xa.index(2)]
    if tb == 'F': return 2 * xa[xb.index(2)]
    return sum(p*q for p, q in zip(xa, xb)) - (sa*sb if cls == 'A' else 2*sa*sb)
for a in L:
    assert norm2(a) in (4, -4), (a, norm2(a))
ok = lambda i, j: ip2(L[i], L[j]) in (0, 2, -2)
types = sorted(set(t for _, _, t in L) - {'F', 'k4s'})
print(cls, 'lines in pool', len(L), 'types', types, flush=True)
best_all = 0
for ty in types:
    u0 = next(i for i, a in enumerate(L) if a[2] == ty)
    pool = [i for i in range(len(L)) if L[i][2] == 'F' or i == u0 or (ok(i, u0) and all(ok(i, f) for f in range(D)))]
    m = cp_model.CpModel(); y = {i: m.NewBoolVar('') for i in pool}
    for i in range(D): m.Add(y[i] == 1)
    m.Add(y[u0] == 1)
    for a, b in itertools.combinations(pool, 2):
        if not ok(a, b): m.AddBoolOr([y[a].Not(), y[b].Not()])
    m.Maximize(sum(y.values())); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
    st = s.Solve(m); sel = [i for i in pool if s.Value(y[i])]
    print('  with a %s line: max %d (%s, bound %d), mix %s' % (ty, s.ObjectiveValue(), s.StatusName(st), s.BestObjectiveBound(), dict(collections.Counter(L[i][2] for i in sel))), flush=True)
