"""I_{11,1} frame-cell source systems with defects.  Each line picks a 3-cover of its reader set by plane-perps:
a good 4-frame through it (its 3 mates) or, for T lines, a PPP triple (3 P lines ⊥ T whose sections cover R(T)
oddly off the mates).  Directed a->b if b in cover(a).  A defect = a->b without b->a: cell {a,b} then needs b's
content from an EXTRA branch of b (+1 register).  Minimise defects (GRP=11 Z11-invariant or GRP=1 none).
Then free-top cell-bottleneck screen (doubly forced T_C, k_C with nondegenerate nodes).  N >= 660 + defects + sum j."""
import sys, json, random, collections, itertools, pickle
from lbase import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); seed = int(sys.argv[2]); random.seed(seed)
fr = goodframes()
covers = {a: [] for a in range(V)}
for F in fr:
    for a in bits(F): covers[a].append(F & ~(1 << a))
ppp = 0
for t in range(V):
    if g.kind[t] != 'T': continue
    R = HYP[t]
    Ps = [p for p in range(V) if g.kind[p] == 'P' and R >> p & 1]
    sec = {p: R & HYP[p] for p in Ps}
    for tri in itertools.combinations(Ps, 3):
        ok = True
        for u in bits(R):
            if u in tri: continue
            if sum(1 for p in tri if sec[p] >> u & 1) % 2 == 0: ok = False; break
        if ok: covers[t].append(sum(1 << p for p in tri)); ppp += 1
print('covers per line', collections.Counter(len(v) for v in covers.values()), 'PPP total', ppp, flush=True)
M = cp_model.CpModel()
Y = {(a, i): M.NewBoolVar('') for a in range(V) for i in range(len(covers[a]))}
cov_idx = {a: {c: i for i, c in enumerate(covers[a])} for a in range(V)}
for a in range(V): M.AddExactlyOne([Y[(a, i)] for i in range(len(covers[a]))])
if len(PERMS) > 1 and os.environ.get('GRP') != '1':
    for p in PERMS:
        for a in range(V):
            for i, c in enumerate(covers[a]):
                M.Add(Y[(a, i)] == Y[(p[a], cov_idx[p[a]][act(c, p)])])
E = {}
for a in range(V):
    for b in range(V):
        if a == b: continue
        lits = [Y[(a, i)] for i, c in enumerate(covers[a]) if c >> b & 1]
        if lits: E[(a, b)] = lits
D = []
arc = {}
for (a, b), lits in E.items():
    x = M.NewBoolVar(''); M.Add(sum(lits) == x); arc[(a, b)] = x
for (a, b), x in arc.items():
    y = arc.get((b, a))
    d = M.NewBoolVar('')
    if y is None: M.Add(d == x)
    else: M.AddBoolOr([x.Not(), y, d])
    D.append(d)
M.Minimize(sum(D) * 1000 + sum(random.randint(0, 3) * v for v in Y.values()))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 2
r = sol.Solve(M)
if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no system', sol.StatusName(r)); sys.exit()
cov = {a: covers[a][next(i for i in range(len(covers[a])) if sol.Value(Y[(a, i)]))] for a in range(V)}
ndef = sum(sol.Value(d) for d in D)
print('status', sol.StatusName(r), 'defects', ndef, 'bound', int(sol.BestObjectiveBound() // 1000), flush=True)
kinds = collections.Counter(('PPP' if all(g.kind[x] == 'P' for x in bits(cov[a])) else 'frame') + g.kind[a] for a in range(V))
print('cover kinds', dict(kinds))
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
hT = collections.Counter(); hk = collections.Counter(); nodestat = collections.Counter()
for C in cells:
    s, a = list(bits(C))
    T = [t for t in range(V) if C & ~HYP[t] == 0 and not any(c != C and c & ~HYP[t] == 0 for c in cells_of[s] + cells_of[a])]
    Ns = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        if nondeg_span(N): Ns.add(N)
    best = max([sum(1 for t in T if N & ~HYP[t] == 0) for N in Ns] + [0])
    hT[len(T)] += 1; hk[len(T) - best] += 1
print('cells', len(cells), '|T_C|', dict(hT), 'k_C', dict(hk), flush=True)
json.dump({str(a): cov[a] for a in range(V)}, open('lsys_%s_%d.json' % (os.environ.get('GRP', '55'), seed), 'w'))
