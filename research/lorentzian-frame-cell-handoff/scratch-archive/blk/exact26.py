# B = 26 with 4 punctures (pP=1, pT=3, punctured supports partition the points), complete stars on the unique
# 6-packing: (s3,s2,s1) = (6,3,3), o = 13, f = 1.  Exact feasibility; gives a usable block partition.
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
X = 10
pack6 = [frozenset(b) for b in [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]]
good = [tuple(sorted(q)) for q in pickle.load(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/part/good4.pkl', 'rb'))]
bypi = collections.defaultdict(list)
for q in good: bypi[frozenset({vv[q[0]] ^ vv[x] for x in q[1:]})].append(q)
cands = []
for pi, fs in bypi.items():
    for k in range(1, len(fs) + 1):
        for sub in itertools.combinations(fs, k):
            ls = [x for q in sub for x in q]
            if len(set(ls)) != len(ls): continue
            if k == 3:
                F4 = frozenset(p for u in ls if g.kind[u] == 'P' for p in g.supp[u])
                if F4 not in pack6: continue
            cands.append(sub)
typ = lambda c: (len(c), 'P' if any(g.kind[u] == 'P' for u in c[0]) else 'T')
m = cp_model.CpModel()
x = [m.NewBoolVar('b%d' % i) for i in range(len(cands))]
y = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, c in enumerate(cands):
    for q in c:
        for u in q: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
m.Add(sum(y[u] for u in range(V) if g.kind[u] == 'P') == 1)
for p in range(11): m.Add(sum(y[u] for u in range(V) if p in g.supp[u]) == 1)
need = {(3, 'P'): 6, (2, 'P'): 3, (1, 'P'): 3, (2, 'T'): 13, (1, 'T'): 1}
for k, n in need.items(): m.Add(sum(x[i] for i, c in enumerate(cands) if typ(c) == k) == n)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = float(sys.argv[1])
r = s.Solve(m)
print('B=26 (6,3,3): STATUS', s.StatusName(r), 'time %.1f' % s.WallTime(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [list(cands[i]) for i in range(len(cands)) if s.Value(x[i])]
    pun = [u for u in range(V) if s.Value(y[u])]
    assert sorted([u for c in sol for q in c for u in q] + pun) == list(range(V))
    print(collections.Counter(typ(c) for c in sol), [(g.kind[u], g.supp[u]) for u in pun])
    pickle.dump((sol, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/part26.pkl', 'wb'))
