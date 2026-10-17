# For block demands (Q and layers of every block with a 4-dim W; lone frames: Q and the 6 E-sets):
# for each line u, the number of demands containing u, and the best partner v (max demands containing both).
import sys, pickle, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
HYP = g.HYP
exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
blocks, pun = pickle.load(open(sys.argv[1], 'rb'))
dem = []
B2 = lambda x, y: (1 << x) | (1 << y)
for fs in [[f] for b in blocks for f in b]:
    Wv = span([vv[x] for q in fs for x in q])
    if len(Wv) == 16:
        NW = N(Wv); dem.append(NW)
        pi = {vv[fs[0][0]] ^ vv[x] for x in fs[0][1:]}
        for a, b, c in itertools.combinations(list(Wv - {0}), 3):
            S = frozenset(span([a, b, c]))
            if len(S) == 8 and not pi <= S:
                Sl = sum(1 << lineof[w] for w in S if w in lineof)
                if any(all(vv[u] in S for u in (x, y)) for q in fs for x, y in itertools.combinations(q, 2)):
                    dem.append(N(S) & ~NW)
    else:
        q = fs[0]; U = 0
        for u in q: U |= 1 << u
        Q = pm(U); dem.append(Q)
        for x, y in itertools.combinations(q, 2): dem.append(pm(B2(x, y)) & ~Q & ~U)
dem = list(set(dem))
mem = collections.defaultdict(set)
for i, d in enumerate(dem):
    for u in bits(d): mem[u].add(i)
nd = [len(mem[u]) for u in range(V) if mem[u]]
best = []
for u in range(V):
    if not mem[u]: continue
    b = max((len(mem[u] & mem[v]), v) for v in range(V) if v != u)
    best.append(b[0])
print('demands', len(dem), '| demands per line: mean %.1f min %d max %d' % (sum(nd) / len(nd), min(nd), max(nd)))
print('best partner shares: mean %.1f min %d max %d' % (sum(best) / len(best), min(best), max(best)), '| distribution', sorted(collections.Counter(best).items()))
# per line: minimum number of partners whose shared-demand sets PARTITION the line's demand set (exact cover, CP-SAT),
# allowing singles (cost 1 per uncovered demand).  Per-line relaxation (ignores consistency between lines).
from ortools.sat.python import cp_model
res = []
for u in range(V):
    if not mem[u]: continue
    Du = sorted(mem[u])
    parts = {}
    for v in range(V):
        if v == u: continue
        S = frozenset(mem[u] & mem[v])
        if len(S) >= 2: parts[v] = S
    m = cp_model.CpModel()
    xv = {v: m.NewBoolVar('v%d' % v) for v in parts}
    sv = {d: m.NewBoolVar('s%d' % d) for d in Du}
    for d in Du:
        m.Add(sum(xv[v] for v in parts if d in parts[v]) + sv[d] == 1)
    m.Minimize(sum(xv.values()) + sum(sv.values()))
    s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 20
    r = s.Solve(m)
    res.append((int(s.ObjectiveValue()), sum(s.Value(sv[d]) for d in Du), s.StatusName(r)))
print('per-line exact cover cost (cells+singles): mean %.2f min %d max %d' % (sum(r[0] for r in res) / len(res), min(r[0] for r in res), max(r[0] for r in res)),
      '| singles mean %.2f' % (sum(r[1] for r in res) / len(res)), '| statuses', collections.Counter(r[2] for r in res))
