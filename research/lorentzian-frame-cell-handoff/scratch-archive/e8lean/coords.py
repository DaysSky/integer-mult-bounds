"""Put one design D6 of the R420 partition into D6 coordinates (lines = +-e_i +- e_j) and print the roles of the
lines (E / d-cell / B-perp) by coordinate pair; classify the design cells inside H."""
import sys, itertools, collections
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V
c2 = G.cells[0]; H = G.D6[c2]; Hl = e8.bits(H); E = G.esum(c2)
L = {s: np.array(e8.LINES[s], dtype=float) for s in Hl}
cand = []
for a, b in itertools.combinations(Hl, 2):
    if e8.GI[a, b] != 0: continue
    for v in (L[a] + L[b], L[a] - L[b]):
        v = v / 2
        nz = sum(1 for s in Hl if abs(L[s] @ v) > 1e-9)
        if nz == 10 and not any(np.allclose(v, c) or np.allclose(v, -c) for c in cand):
            cand.append(v)
print('axis candidates', len(cand))
ax = np.array(cand[:6]); assert len(cand) == 6
def coord(s):
    x = ax @ L[s] / (ax[0] @ ax[0])
    idx = [i for i in range(6) if abs(x[i]) > 1e-9]
    return tuple(idx), tuple(int(np.sign(x[i])) for i in idx)
role = {}
for s in Hl:
    if E >> s & 1: role[s] = 'E'
    elif s in G.dcell[c2]: role[s] = 'd'
    elif G.blk[s] == G.comp[G.cblk[c2]]: role[s] = 'Q'
    else: role[s] = '?'
bypair = collections.defaultdict(list)
for s in Hl:
    p, sg = coord(s); bypair[p].append(role[s])
for p in sorted(bypair): print(p, bypair[p])
print('design cells inside H:')
for c in G.cells:
    if G.cmask[c] & ~H == 0:
        print('  ', c, [coord(s) for s in c], [role[s] for s in c], 'block', G.cblk[c])
