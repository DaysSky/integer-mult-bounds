"""Compact Z11-invariant Lorentzian source-system search: variables only for the 20 line-orbit representatives
(cover of p(r) = p(cover(r))).  Covers: good 4-frames through the line or (T lines) PPP triples.  Minimise defects
(arcs a->b without b->a; each costs one extra branch register), optionally with random tie-break; then screen."""
import sys, os, json, random, collections, itertools
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); seed = int(sys.argv[2]); n = int(sys.argv[3]) if len(sys.argv) > 3 else 1; random.seed(seed)
fr = goodframes()
covers = {a: [] for a in range(V)}
for F in fr:
    for a in bits(F): covers[a].append(F & ~(1 << a))
for t in range(V):
    if g.kind[t] != 'T' or os.environ.get('NOPPP') == '1': continue
    R = HYP[t]; Ps = [p for p in range(V) if g.kind[p] == 'P' and R >> p & 1]; sec = {p: R & HYP[p] for p in Ps}
    for tri in itertools.combinations(Ps, 3):
        if all(sum(1 for p in tri if sec[p] >> u & 1) % 2 == 1 for u in bits(R) if u not in tri):
            covers[t].append(sum(1 << p for p in tri))
rep_of = {}; to_rep = {}
for a in range(V):
    imgs = [(p[a], p) for p in PERMS]
    r = min(x for x, _ in imgs); rep_of[a] = r
reps = sorted(set(rep_of.values()))
# permutation mapping rep r -> a
pmap = {}
for a in range(V):
    for p in PERMS:
        if p[rep_of[a]] == a: pmap[a] = p; break
inv = lambda p: [p.index(i) for i in range(V)]
pinv = {a: inv(pmap[a]) for a in range(V)}
print('reps', len(reps), flush=True)
M = cp_model.CpModel()
Y = {(r, i): M.NewBoolVar('') for r in reps for i in range(len(covers[r]))}
for r in reps: M.AddExactlyOne([Y[(r, i)] for i in range(len(covers[r]))])
def arc(a, b):
    """literal-sum: a->b holds (b in cover(a)); cover(a) = pmap[a](cover(rep(a)))"""
    r = rep_of[a]; bb = pinv[a][b]          # b in p(c) <=> p^-1(b) in c
    return [Y[(r, i)] for i, c in enumerate(covers[r]) if c >> bb & 1]
D = []
for r in reps:
    for b in range(V):
        if b == r: continue
        ab = arc(r, b)
        if not ab: continue
        ba = arc(b, r)
        d = M.NewBoolVar('')
        if not ba: M.Add(d == sum(ab))
        else: M.AddBoolOr([d] + [x.Not() for x in []] + [M.NewBoolVar('').Not()] * 0) if False else None
        if ba:
            x = M.NewBoolVar(''); M.Add(sum(ab) == x); y = M.NewBoolVar(''); M.Add(sum(ba) == y)
            M.AddBoolOr([x.Not(), y, d])
        D.append(d)
if os.environ.get('NOFULL') == '1':
    # forbid neighbours sharing the line's frame (no two lines of a cell choose the same frame)
    for r in reps:
        for i, c in enumerate(covers[r]):
            F = c | (1 << r)
            for b in bits(c):
                rb = rep_of[b]; Fb = act(F, pinv[b])         # b chooses F iff rep(b) chooses p_b^-1(F) minus rep
                cb = Fb & ~(1 << rb)
                j = next((jj for jj, cc in enumerate(covers[rb]) if cc == cb), None)
                if j is not None: M.AddBoolOr([Y[(r, i)].Not(), Y[(rb, j)].Not()])
obj = sum(D)
for k in range(n):
    M.Minimize(obj * 1000 + sum(random.randint(0, 5) * v for v in Y.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4; sol.parameters.random_seed = seed * 10 + k
    st = sol.Solve(M)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('none', sol.StatusName(st)); break
    cov = {}
    for a in range(V):
        r = rep_of[a]; c = covers[r][next(i for i in range(len(covers[r])) if sol.Value(Y[(r, i)]))]
        cov[a] = act(c, pmap[a])
    nd = sum(1 for a in range(V) for b in bits(cov[a]) if not cov[b] >> a & 1)
    kinds = collections.Counter(('PPP' if all(g.kind[x] == 'P' for x in bits(cov[a])) else 'frame') + g.kind[a] for a in range(V))
    print('sol', k, sol.StatusName(st), 'defects', nd, 'bound', int(sol.BestObjectiveBound() // 1000) * 11, 'kinds', dict(kinds), flush=True)
    fn = 'lsys3%s%s_%d_%d.json' % ('np' if os.environ.get('NOPPP') == '1' else '', 'nf' if os.environ.get('NOFULL') == '1' else '', seed, k)
    json.dump({str(a): cov[a] for a in range(V)}, open(fn, 'w')); print('saved', fn, flush=True)
