# Exact feasibility of the B = 24 block partition (lower bound, proven by counting) for a fixed max K4 packing:
# 6 complete stars on the packing's K4s (hub free), 4 two-frame stars on 4-cycles of the leftover P graph, 14 octets,
# punctures: exactly 3 P and 1 T.  Output FEASIBLE (certificate, re-checked) or INFEASIBLE (proof for this packing).
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
P, T = g.P, g.T
tri = lambda a, b, c: T(*sorted((a, b, c)))
K4s = [tuple(b) for b in eval(sys.argv[1])] if len(sys.argv) > 1 else [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, 10), (2, 5, 8, 10), (3, 6, 9, 10)]
used = set(frozenset(e) for b in K4s for e in itertools.combinations(b, 2))
left = set(frozenset(e) for e in itertools.combinations(range(11), 2)) - used
cands = []     # (kind, lines)
for F4 in K4s:
    for h in range(11):
        if h in F4: continue
        ls = [P(a, b) for a, b in itertools.combinations(F4, 2)] + [tri(h, a, b) for a, b in itertools.combinations(F4, 2)]
        cands.append(('S3', h, F4, ls))
for F4 in itertools.combinations(range(11), 4):
    p, q, r, s = F4
    ms = [((p, q), (r, s)), ((p, r), (q, s)), ((p, s), (q, r))]
    for m1, m2 in itertools.combinations(ms, 2):
        es = list(m1) + list(m2)
        if all(frozenset(e) in left for e in es):
            for h in range(11):
                if h in F4: continue
                ls = [P(*e) for e in es] + [tri(h, *e) for e in es]
                cands.append(('S2', h, (m1, m2), ls))
for a1, a2 in itertools.combinations(range(11), 2):
    for b1, b2 in itertools.combinations(range(11), 2):
        if len({a1, a2, b1, b2}) < 4 or (b1, b2) < (a1, a2): continue
        for c1, c2 in itertools.combinations(range(11), 2):
            if len({a1, a2, b1, b2, c1, c2}) < 6 or (c1, c2) < (b1, b2): continue
            ls = [tri(x, y, z) for x in (a1, a2) for y in (b1, b2) for z in (c1, c2)]
            cands.append(('O', None, ((a1, a2), (b1, b2), (c1, c2)), ls))
print('candidates', collections.Counter(c[0] for c in cands), flush=True)
m = cp_model.CpModel()
x = [m.NewBoolVar('c%d' % i) for i in range(len(cands))]
y = [m.NewBoolVar('p%d' % u) for u in range(V)]
inc = collections.defaultdict(list)
for i, c in enumerate(cands):
    for u in c[3]: inc[u].append(x[i])
for u in range(V): m.Add(sum(inc[u]) + y[u] == 1)
m.Add(sum(y[u] for u in range(V) if g.kind[u] == 'P') == 3)
m.Add(sum(y[u] for u in range(V) if g.kind[u] == 'T') == 1)
for F4 in K4s: m.Add(sum(x[i] for i, c in enumerate(cands) if c[0] == 'S3' and c[2] == F4) == 1)
m.Add(sum(x[i] for i, c in enumerate(cands) if c[0] == 'S2') == 4)
m.Add(sum(x[i] for i, c in enumerate(cands) if c[0] == 'O') == 14)
s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 3000
r = s.Solve(m)
print('STATUS', s.StatusName(r), 'time %.1f' % s.WallTime(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [cands[i] for i in range(len(cands)) if s.Value(x[i])]
    pun = [u for u in range(V) if s.Value(y[u])]
    lines = sorted([u for c in sol for u in c[3]] + pun)
    assert lines == list(range(V))
    # re-verify each block is a set of good frames sharing pi (independent F2 check)
    exec(open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/f2lib.py').read())
    from lw import bits
    for c in sol:
        print(c[0], c[1], c[2])
    print('punctured', [(g.kind[u], g.supp[u]) for u in pun], '| blocks', len(sol))
    pickle.dump((sol, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/part24.pkl', 'wb'))
