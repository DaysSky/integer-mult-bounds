import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
V = g.V; G = g.G
R = [set(s for s in range(V) if s != t and G[t, s] == 0) for t in range(V)]
def good4(t):
    out = []
    Rt = sorted(R[t])
    for a, b, c in itertools.combinations(Rt, 3):
        if G[a, b] or G[a, c] or G[b, c]: continue
        S = [R[t] & R[x] for x in (a, b, c)]
        if set().union(*S) | set() >= R[t] - {a, b, c} and (S[0] | S[1] | S[2] | {a, b, c}) >= R[t]:
            out.append((a, b, c))
    return out
for t in (g.P(0, 1), g.T(0, 1, 2)):
    fr = good4(t)
    print(g.kind[t], g.supp[t], '|R(t)|', len(R[t]), 'good 4-frames', len(fr))
    stats = collections.Counter()
    for a, b, c in fr[:2000]:
        S = [R[t] & R[x] for x in (a, b, c)]
        cnt = collections.Counter()
        for u in R[t]:
            k = sum(u in s for s in S); cnt[k] += 1
        key = (tuple(sorted(len(s) for s in S)), tuple(sorted(cnt.items())), tuple(sorted((g.kind[a], g.kind[b], g.kind[c]))))
        stats[key] += 1
    for k, n in stats.most_common(8): print('   sizes', k[0], 'multiplicity profile', k[1], 'types', k[2], 'x', n)
