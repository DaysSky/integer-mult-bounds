import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
orth = [set(j for j in range(V) if j != i and G[i, j] == 0) for i in range(V)]
print('deg', min(len(o) for o in orth), max(len(o) for o in orth))
quads = []
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        ab = orth[a] & orth[b]
        for c in ab:
            if c <= b: continue
            for d in ab & orth[c]:
                if d <= c: continue
                quads.append((a, b, c, d))
print('orthogonal 4-sets', len(quads))
import pickle; pickle.dump(quads, open('quads.pkl', 'wb'))
