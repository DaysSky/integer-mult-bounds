import sys, itertools, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
frames, sols = pickle.load(open('z11part.pkl', 'rb'))
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
pc = lambda m: bin(m).count('1')
phi = {x: f for f in frames for x in f}
stats = collections.Counter()
perps = collections.Counter()
for f in frames:
    P = orthm[f[0]] & orthm[f[1]] & orthm[f[2]] & orthm[f[3]]
    perps[P] += 1
    for t in f:
        es = [e for e in f if e != t]
        R = orthm[t]
        Es = []
        for e in es:
            o = [x for x in es if x != e]
            E = R & orthm[e] & ~orthm[o[0]] & ~orthm[o[1]]
            Es.append(pc(E))
        two = sum(1 for s in g.bits(R) if s not in es and sum(1 for e in es if G[s, e] == 0) in (0, 2))
        stats[(g.kind[t], pc(R), pc(P), tuple(sorted(Es)), two)] += 1
for k, v in sorted(stats.items()): print(k, v)
print('distinct frame perps', len(perps), 'max frames sharing a perp', max(perps.values()))
