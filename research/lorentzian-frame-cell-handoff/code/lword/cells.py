"""Good 4-frames of I_{11,1} (pairwise orthogonal, half-sum in the lattice Z^{n,1}) and the structure of the cell
needer flats {t,e}^perp: sizes, ranks, and which sub-flats are shared between needer flats."""
import itertools, collections, numpy as np
from geom import Geom
g = Geom(11); V = g.V; G = g.G
orth = [set(np.nonzero(G[t] == 0)[0].tolist()) - {t} for t in range(V)]
# enumerate orthogonal 4-sets containing line 0 type examples, and count all good frames
def good(f):
    s = g.L[list(f)].sum(axis=0)
    return all(x % 2 == 0 for x in s)
frames = []
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        for c in orth[a] & orth[b]:
            if c <= b: continue
            for d in orth[a] & orth[b] & orth[c]:
                if d <= c: continue
                if good((a, b, c, d)): frames.append((a, b, c, d))
print('good 4-frames', len(frames))
typ = collections.Counter(tuple(sorted(g.kind[x] for x in f)) for f in frames)
print('types', dict(typ))
# needer flat sizes for each cell in good frames
sz = collections.Counter()
for f in frames[:2000]:
    for t, e in itertools.combinations(f, 2):
        N = orth[t] & orth[e]
        sz[(g.kind[t] + g.kind[e], len(N))] += 1
print('cell needer sizes (kind pair, #lines):', dict(sz))
# per-line: how many good frames contain it
cnt = collections.Counter(x for f in frames for x in f)
print('frames per line: pairs', collections.Counter(cnt[i] for i in range(55)), 'triples', collections.Counter(cnt[i] for i in range(55, V)))
