import sys, itertools, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
P, T = g.P, g.T
tri = lambda a, b, c: T(*sorted((a, b, c)))
X = 10
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/blk/'
psides = pickle.load(open(D + 'psides_O6.pkl', 'rb'))
pack6 = [(0, 1, 2, 3), (0, 4, 5, 6), (0, 7, 8, 9), (1, 4, 7, X), (2, 5, 8, X), (3, 6, 9, X)]
def octet_frames(m):
    (a1, a2), (b1, b2), (c1, c2) = m
    tr = [(x, y, z) for x in (a1, a2) for y in (b1, b2) for z in (c1, c2)]
    f0 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 0)
    f1 = tuple(tri(*t) for t in tr if (int(t[0] == a2) + int(t[1] == b2) + int(t[2] == c2)) % 2 == 1)
    return f0, f1
ALL_OCT = []
for a1, a2 in itertools.combinations(range(11), 2):
    for b1, b2 in itertools.combinations(range(11), 2):
        if len({a1, a2, b1, b2}) < 4 or (b1, b2) < (a1, a2): continue
        for c1, c2 in itertools.combinations(range(11), 2):
            if len({a1, a2, b1, b2, c1, c2}) < 6 or (c1, c2) < (b1, b2): continue
            ALL_OCT.append(octet_frames(((a1, a2), (b1, b2), (c1, c2))))
for k, (hubs, stars2, singles, punP, O) in enumerate(psides[int(sys.argv[1]):int(sys.argv[2])], start=int(sys.argv[1])):
    blocks = []
    for h, F4 in zip(hubs, pack6):
        p, q, r, s = F4
        blocks.append([(P(a, b), P(c, d), tri(h, a, b), tri(h, c, d)) for (a, b), (c, d) in (((p, q), (r, s)), ((p, r), (q, s)), ((p, s), (q, r)))])
    for h, F4, es in stars2:
        e1, e2, e3, e4 = [tuple(sorted(e)) for e in es]
        blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2)), (P(*e3), P(*e4), tri(h, *e3), tri(h, *e4))])
    for h, e1, e2 in singles:
        e1, e2 = tuple(sorted(e1)), tuple(sorted(e2))
        blocks.append([(P(*e1), P(*e2), tri(h, *e1), tri(h, *e2))])
    e0 = tuple(sorted(punP[0])); pun = [P(*e0)]
    usedL = set(u for b in blocks for f in b for u in f) | set(pun)
    remT = [u for u in range(V) if u not in usedL]; rem = set(remT)
    octs = [(f0, f1) for f0, f1 in ALL_OCT if all(u in rem for u in f0 + f1)]
    lone = list(set(f for f0, f1 in ALL_OCT for f in (f0, f1) if all(u in rem for u in f) and set(p for u in f for p in g.supp[u]) == set(O)))
    m = cp_model.CpModel()
    xo = [m.NewBoolVar('o%d' % i) for i in range(len(octs))]; xf = [m.NewBoolVar('f%d' % i) for i in range(len(lone))]
    y = {u: m.NewBoolVar('p%d' % u) for u in remT}
    inc = collections.defaultdict(list)
    for i, (f0, f1) in enumerate(octs):
        for u in f0 + f1: inc[u].append(xo[i])
    for i, f in enumerate(lone):
        for u in f: inc[u].append(xf[i])
    for u in remT: m.Add(sum(inc[u]) + y[u] == 1)
    others = [p for p in range(11) if p not in e0]
    for p in others: m.Add(sum(y[u] for u in remT if p in g.supp[u]) == 1)
    for u in remT:
        if set(g.supp[u]) & set(e0): m.Add(y[u] == 0)
    m.Add(sum(xf) == 1)
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.max_time_in_seconds = float(sys.argv[3])
    r = s.Solve(m)
    print('P side %d: O=%s | octets %d lone %d | %s (%.0fs)' % (k, sorted(O), len(octs), len(lone), s.StatusName(r), s.WallTime()), flush=True)
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for i, o in enumerate(octs):
            if s.Value(xo[i]): blocks.append(list(o))
        for i, f in enumerate(lone):
            if s.Value(xf[i]): blocks.append([f])
        pun += [u for u in remT if s.Value(y[u])]
        assert sorted([u for b in blocks for f in b for u in f] + pun) == list(range(V))
        pickle.dump((blocks, pun), open(D + 'partC.pkl', 'wb'))
        print('saved partC: blocks', len(blocks), collections.Counter(len(b) for b in blocks), '| punctured', [(g.kind[u], g.supp[u]) for u in pun])
        break
