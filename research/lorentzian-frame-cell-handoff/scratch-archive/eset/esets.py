"""E-set structure of a good-frame partition (I_{11,1}): E(t,e) = lines perp t, e and NOT perp the other two frame
members.  Stats: sizes, F2 rank of all E-set vectors, rank of Phi-perp vectors, and how many distinct 'atoms'
(classes of lines with identical E-set membership patterns) there are: atoms = minimal pieces from which every
E-set is a disjoint union (an aligned design would have few large atoms)."""
import sys, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
frames, pun = pickle.load(open(sys.argv[1], 'rb'))
live = [u for u in range(V) if u not in set(pun)]
orth = lambda a, b: a != b and G[a, b] == 0
E = {}
for f in frames:
    for i, t in enumerate(f):
        for e in f[i + 1:]:
            o = [x for x in f if x not in (t, e)]
            E[(t, e)] = frozenset(u for u in live if orth(u, t) and orth(u, e) and not orth(u, o[0]) and not orth(u, o[1]))
print('frames', len(frames), 'punctured', len(pun), 'sections', len(E), 'E sizes', sorted(collections.Counter(len(s) for s in E.values()).items()))
# atoms
memb = collections.defaultdict(list)
for k, s in E.items():
    for u in s: memb[u].append(k)
atoms = collections.Counter(tuple(sorted(v)) for v in memb.values())
print('lines in some E-set', len(memb), 'atoms (distinct membership patterns)', len(atoms))
# F2 rank of E-set vectors
idx = {u: i for i, u in enumerate(live)}
vecs = [sum(1 << idx[u] for u in s) for s in E.values()]
basis = []
for x in vecs:
    for b in basis: x = min(x, x ^ b)
    if x: basis.append(x)
print('F2 rank of E-set vectors', len(basis), 'of', len(live), 'lines')
# per line: number of E-sets containing it
print('E-sets per line: ', sorted(collections.Counter(len(v) for v in memb.values()).items()))
