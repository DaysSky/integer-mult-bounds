import sys, itertools, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
pc = lambda m: bin(m).count('1')
orthm = [sum(1 << j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
quads = pickle.load(open('quads.pkl', 'rb'))
def good_for(t, es):
    R = orthm[t] & ~sum(1 << e for e in es)
    a, b, c = (orthm[e] for e in es)
    # count parity: lines orthogonal to an even number (0 or 2) of es
    even = R & ~(a ^ b ^ c)
    return even == 0
good = []
types = collections.Counter()
for q in quads:
    if all(good_for(t, [e for e in q if e != t]) for t in q):
        good.append(q)
        types[tuple(sorted(g.kind[x] for x in q))] += 1
print('good 4-frames (good for all members):', len(good), dict(types))
cover = collections.Counter(x for q in good for x in q)
print('lines covered by some good frame', len(cover), 'min/max mult', min(cover.values()) if cover else 0, max(cover.values()) if cover else 0)
pickle.dump(good, open('good4.pkl', 'wb'))
# also frames good for at least one member
part = collections.Counter()
for q in quads:
    n = sum(good_for(t, [e for e in q if e != t]) for t in q)
    part[n] += 1
print('frames by #members good:', dict(part))
