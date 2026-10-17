# Exact T side for a fixed P side: remaining T lines (minus nT punctures) into exactly o octets + f lone TTTT frames.
import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
P, T = g.P, g.T
tri = lambda a, b, c: T(*sorted((a, b, c)))
X = 10
pack6 = [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]
hubs = [4, 7, 2, 8, 3, 0]
stars2 = [(3, ((1, 6), (9, 2), (1, 9), (2, 6))), (0, ((1, 5), (8, 3), (8, 1), (3, 5))), (5, ((2, 4), (3, 7), (2, 7), (3, 4)))]
singles = [(1, (5, 7), (8, 6)), (1, (9, 5), (6, 7))]
punP = [(0, X), (8, 4), (9, 4)]
blocks = []
for h, F4 in zip(hubs, pack6):
    p, q, r, s = F4
    blocks.append([(P(a, b), P(c, d), tri(h, a, b), tri(h, c, d)) for (a, b), (c, d) in (((p, q), (r, s)), ((p, r), (q, s)), ((p, s), (q, r)))])
for h, es in stars2:
    e1, e2, e3, e4 = es
    blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2)), (P(*e3), P(*e4), tri(h, *e3), tri(h, *e4))])
for h, e1, e2 in singles:
    blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2))])
usedL = set(u for b in blocks for f in b for u in f) | set(P(*e) for e in punP)
assert len(usedL) == sum(4 * len(b) for b in blocks) + 3
remT = [u for u in range(V) if u not in usedL]
assert all(g.kind[u] == 'T' for u in remT)
print('remaining T lines', len(remT))
NT, NO, NF = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rem = set(remT)
octs = []; lone = []
for a1, a2 in itertools.combinations(range(11), 2):
    for b1, b2 in itertools.combinations(range(11), 2):
        if len({a1, a2, b1, b2}) < 4 or (b1, b2) < (a1, a2): continue
        for c1, c2 in itertools.combinations(range(11), 2):
            if len({a1, a2, b1, b2, c1, c2}) < 6 or (c1, c2) < (b1, b2): continue
            tr = [(x, y, z) for x in (a1, a2) for y in (b1, b2) for z in (c1, c2)]
            f0 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 0)
            f1 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 1)
            if all(u in rem for u in f0 + f1): octs.append((f0, f1))
            for f in (f0, f1):
                if all(u in rem for u in f): lone.append(f)
print('octets available', len(octs), '| lone TTTT frames available', len(lone), flush=True)
m = cp_model.CpModel()
xo = [m.NewBoolVar('o%d' % i) for i in range(len(octs))]
xf = [m.NewBoolVar('f%d' % i) for i in range(len(lone))]
y = {u: m.NewBoolVar('p%d' % u) for u in remT}
inc = collections.defaultdict(list)
for i, (f0, f1) in enumerate(octs):
    for u in f0 + f1: inc[u].append(xo[i])
for i, f in enumerate(lone):
    for u in f: inc[u].append(xf[i])
for u in remT: m.Add(sum(inc[u]) + y[u] == 1)
m.Add(sum(y.values()) == NT); m.Add(sum(xo) == NO); m.Add(sum(xf) == NF)
s = cp_model.CpSolver(); s.parameters.num_workers = 8; s.parameters.max_time_in_seconds = 1800
r = s.Solve(m)
print('T side NT=%d octets=%d lone=%d: %s (%.1fs)' % (NT, NO, NF, s.StatusName(r), s.WallTime()), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for i, o in enumerate(octs):
        if s.Value(xo[i]): blocks.append(list(o))
    for i, f in enumerate(lone):
        if s.Value(xf[i]): blocks.append([f])
    pun = [P(*e) for e in punP] + [u for u in remT if s.Value(y[u])]
    assert sorted([u for b in blocks for f in b for u in f] + pun) == list(range(V))
    pickle.dump((blocks, pun), open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/part25.pkl', 'wb'))
    print('saved partition: blocks', len(blocks), collections.Counter(len(b) for b in blocks), '| punctured', len(pun))
