import sys, json, itertools, collections
exec(open('e8a3quad.py').read().split('# candidate nodes')[0])
E6 = [P for P in secs if pc(P) == 3]
stats = collections.Counter(); best = []
for k in (2, 3, 4):
    nodes = {}
    for P in E6:
        for grp in itertools.combinations(pieces[P], k):
            m = 0
            for C in grp: m |= C
            F, r = e8.closure(m)
            nodes[F] = r
    res = collections.Counter()
    for F, r in nodes.items():
        served = [P for P in E6 if F & ~pm(P) == 0]
        pin = collections.Counter(sum(1 for C in pieces[P] if C & ~F == 0) for P in served)
        res[(r, pc(F), len(served), tuple(sorted(pin.items())))] += 1
    print('k =', k, 'distinct closures', len(nodes))
    for key, v in sorted(res.items(), key=lambda kv: (-kv[0][2], kv[0][0]))[:8]: print('    (rank, lines, E6 served, pieces-inside dist):', key, 'x', v)
