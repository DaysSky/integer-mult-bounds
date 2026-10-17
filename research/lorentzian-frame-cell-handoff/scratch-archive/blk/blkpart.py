# Partition lines into blocks = sets of good frames sharing a cell-sum plane (same 4-dim W):
# complete star (3 frames), 2-frame star, octet (2 TTTT frames), lone frame; minimise number of blocks (+punctures).
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
from ortools.sat.python import cp_model
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
good = pickle.load(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/part/good4.pkl', 'rb'))
good = [tuple(sorted(q)) for q in good]
bypi = collections.defaultdict(list)
for q in good:
    pi = frozenset({vv[q[0]] ^ vv[x] for x in q[1:]})
    bypi[pi].append(q)
print('good frames', len(good), '| pi classes', len(bypi), collections.Counter(len(v) for v in bypi.values()))
cands = []        # (frames tuple)
for pi, fs in bypi.items():
    # all nonempty sets of pairwise disjoint frames in this class
    for k in range(1, len(fs) + 1):
        for sub in itertools.combinations(fs, k):
            ls = [x for q in sub for x in q]
            if len(set(ls)) == len(ls): cands.append(sub)
print('candidate blocks', len(cands), collections.Counter(len(c) for c in cands))
W1 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
m = cp_model.CpModel()
x = [m.NewBoolVar('b%d' % i) for i in range(len(cands))]
y = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, c in enumerate(cands):
    for q in c:
        for u in q: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
m.Add(sum(y) <= int(sys.argv[2]) if len(sys.argv) > 2 else 4)
# cost: 13 hub registers per block (12 layers + Q); punctured lines cost ~PUN each
PUN = 40
m.Minimize(sum(13 * x[i] for i in range(len(cands))) + PUN * sum(y))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = float(sys.argv[3]) if len(sys.argv) > 3 else 120; s.parameters.num_workers = 8
r = s.Solve(m)
print(s.StatusName(r), 'obj', s.ObjectiveValue(), 'bound', s.BestObjectiveBound())
sol = [cands[i] for i in range(len(cands)) if s.Value(x[i])]
pun = [u for u in range(V) if s.Value(y[u])]
print('blocks', len(sol), collections.Counter((len(c), ''.join(sorted(g.kind[u] for u in c[0]))) for c in sol), '| punctured', [(g.kind[u], g.supp[u]) for u in pun])
pickle.dump((sol, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/blkpart.pkl', 'wb'))
