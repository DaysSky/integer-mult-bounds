# Exact feasibility: partition of the 220 lines into exactly B blocks (good frames sharing a cell-sum plane:
# complete star, 2-frame star, single PPTT, octet, single TTTT) plus exactly NP punctured lines.
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
B, NP, TL = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
good = [tuple(sorted(q)) for q in pickle.load(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/part/good4.pkl', 'rb'))]
bypi = collections.defaultdict(list)
for q in good: bypi[frozenset({vv[q[0]] ^ vv[x] for x in q[1:]})].append(q)
cands = []
for pi, fs in bypi.items():
    for k in range(1, len(fs) + 1):
        for sub in itertools.combinations(fs, k):
            ls = [x for q in sub for x in q]
            if len(set(ls)) == len(ls): cands.append(sub)
m = cp_model.CpModel()
x = [m.NewBoolVar('b%d' % i) for i in range(len(cands))]
y = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, c in enumerate(cands):
    for q in c:
        for u in q: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
m.Add(sum(y) == NP); m.Add(sum(x) == B)
# symmetry: S11 is transitive on complete star blocks; if a complete star is used, WLOG (h=10? any) -- not imposed
s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = TL
r = s.Solve(m)
print('B', B, 'NP', NP, 'STATUS', s.StatusName(r), 'time %.1f' % s.WallTime(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [cands[i] for i in range(len(cands)) if s.Value(x[i])]
    pun = [u for u in range(V) if s.Value(y[u])]
    assert sorted([u for c in sol for q in c for u in q] + pun) == list(range(V))
    for c in sol:
        pis = {frozenset({vv[q[0]] ^ vv[z] for z in q[1:]}) for q in c}
        assert len(pis) == 1
    print(collections.Counter((len(c), ''.join(sorted(g.kind[u] for u in c[0]))) for c in sol), '| punctured', [(g.kind[u], g.supp[u]) for u in pun])
    pickle.dump((sol, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/partB%d_%d.pkl' % (B, NP), 'wb'))
