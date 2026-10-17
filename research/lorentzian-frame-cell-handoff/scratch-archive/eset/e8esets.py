import sys, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/subspace16-r420/vendor/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom(); V = e8.V; GI = e8.GI
E = {}
for c in G.cells:
    o = [x for x in G.phi[c[0]] if x not in c]
    E[c] = frozenset(s for s in e8.bits(G.D6[c]) if GI[s, o[0]] != 0 and GI[s, o[1]] != 0)
print('sections', len(E), 'E sizes', sorted(collections.Counter(len(s) for s in E.values()).items()))
memb = collections.defaultdict(list)
for k, s in E.items():
    for u in s: memb[u].append(k)
atoms = collections.Counter(tuple(sorted(v)) for v in memb.values())
print('lines in some E-set', len(memb), 'atoms', len(atoms), 'atom sizes', sorted(collections.Counter(atoms.values()).items()))
vecs = [sum(1 << u for u in s) for s in E.values()]
basis = []
for x in vecs:
    for b in basis: x = min(x, x ^ b)
    if x: basis.append(x)
print('F2 rank of E-set vectors', len(basis), 'of', V)
print('E-sets per line', sorted(collections.Counter(len(v) for v in memb.values()).items()))
