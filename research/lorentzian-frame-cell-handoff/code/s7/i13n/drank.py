from part13 import *
import numpy as np
def f2rank(vecs):
    rows = list(set(vecs)); basis = {}
    r = 0
    for x in rows:
        while x:
            hb = x.bit_length() - 1
            if hb in basis: x ^= basis[hb]
            else: basis[hb] = x; r += 1; break
    return r
dem = list(set(d[2] for d in DEM))
print('distinct demands', len(dem), 'F2 rank', f2rank(dem))
Es = list(set(d[2] for d in DEM if d[0] == 'E')); Qs = list(set(d[2] for d in DEM if d[0] == 'Q'))
print('E-sets rank', f2rank(Es), 'Q rank', f2rank(Qs))
# sign halves E+ = {u : <u,k> = <u,l>}
halves = set()
for fi, f in enumerate(part):
    for a, b in itertools.combinations(range(4), 2):
        o = [z for z in range(4) if z not in (a, b)]
        E = HYP[f[a]] & HYP[f[b]] & ~HYP[f[o[0]]] & ~HYP[f[o[1]]]
        k, l = f[o[0]], f[o[1]]
        Ep = sum(1 << u for u in bits(E) if G[u, k] == G[u, l]); Em = E & ~Ep
        halves.add(Ep); halves.add(Em)
halves.discard(0)
print('halves', len(halves), 'rank', f2rank(list(halves)), 'sizes', sorted(collections.Counter(pc(h) for h in halves).items()))
