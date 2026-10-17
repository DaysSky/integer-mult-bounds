import sys, os, pickle, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid'); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lbuild')
import lw
from lw import g, bits, V
from fastcl import fclosure
pc = lambda m: bin(m).count('1')
choice = pickle.load(open(sys.argv[1], 'rb'))
blocks = collections.defaultdict(list)
for t, (a, b, c, d) in choice.items():
    tris = [Q for Q in (a, b, c) if pc(Q) == 3]
    pairs = [Q for Q in (a, b, c) if pc(Q) == 2]
    if len(tris) == 2 and len(pairs) == 1:
        A3 = fclosure(tris[0] | tris[1]); blocks[A3].append(t)
typ = collections.Counter(); supp = collections.Counter()
for A3, ts in blocks.items():
    L = bits(A3)
    kinds = ''.join(sorted(g.kind[x] for x in L))
    pts = set()
    for x in L: pts |= set(g.supp[x])
    typ[(kinds, len(pts), len(ts))] += 1
    supp[frozenset(pts)] += 1
print('block types (kinds, #points, #targets):', dict(typ))
print('distinct point supports', len(supp), 'max blocks per support', max(supp.values()))
