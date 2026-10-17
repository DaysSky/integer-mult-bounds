# B = 25, 4 punctures: by the mod-4 point-degree argument the only possible configuration is
# pP = 1, pT = 3 with the 4 punctured supports partitioning the 11 points, s3 = 5, s2 = 6, s1 = 0, o = 13, f = 1.
# The punctured P line is fixed to P(9,10) (S11 is transitive on P lines).  Exact feasibility.
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
good = [tuple(sorted(q)) for q in pickle.load(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/part/good4.pkl', 'rb'))]
bypi = collections.defaultdict(list)
for q in good: bypi[frozenset({vv[q[0]] ^ vv[x] for x in q[1:]})].append(q)
cands = []
for pi, fs in bypi.items():
    for k in range(1, len(fs) + 1):
        for sub in itertools.combinations(fs, k):
            ls = [x for q in sub for x in q]
            if len(set(ls)) == len(ls): cands.append(sub)
typ = lambda c: (len(c), 'P' if any(g.kind[u] == 'P' for u in c[0]) else 'T')
m = cp_model.CpModel()
x = [m.NewBoolVar('b%d' % i) for i in range(len(cands))]
y = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, c in enumerate(cands):
    for q in c:
        for u in q: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
pP = g.P(9, 10)
for u in range(V):
    if g.kind[u] == 'P': m.Add(y[u] == (1 if u == pP else 0))
for p in range(11): m.Add(sum(y[u] for u in range(V) if p in g.supp[u]) == 1)
need = {(3, 'P'): 5, (2, 'P'): 6, (1, 'P'): 0, (2, 'T'): 13, (1, 'T'): 1}
for k, n in need.items(): m.Add(sum(x[i] for i, c in enumerate(cands) if typ(c) == k) == n)
s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = float(sys.argv[1])
r = s.Solve(m)
print('B=25 restricted: STATUS', s.StatusName(r), 'time %.1f' % s.WallTime(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [list(cands[i]) for i in range(len(cands)) if s.Value(x[i])]
    pun = [u for u in range(V) if s.Value(y[u])]
    assert sorted([u for c in sol for q in c for u in q] + pun) == list(range(V))
    print(collections.Counter(typ(c) for c in sol), [(g.kind[u], g.supp[u]) for u in pun])
    pickle.dump((sol, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/part25.pkl', 'wb'))
