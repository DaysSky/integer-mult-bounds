"""Top contents for E8 bit (D6-triple tops on the 5-pair D4 partition):
for target a in 4-frame {a,b,c,d}: class_x(a) = readers of a orthogonal to x and to no other frame-mate (x in b,c,d).
Study: sizes, how class sets split over blocks, spans, and sharing (same set needed by which targets)."""
import sys, collections, itertools, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from geom import Geom
G = Geom()
V = e8.V; GI = e8.GI
ORTH = [set(o) for o in e8.ORTH]
cls = {}
for f in G.frames4:
    for a in f:
        mates = [x for x in f if x != a]
        for x in mates:
            others = [y for y in mates if y != x]
            S = frozenset(r for r in ORTH[a] if r in ORTH[x] and r not in ORTH[others[0]] and r not in ORTH[others[1]] and r not in f)
            cls[(a, x)] = S
sizes = collections.Counter(len(S) for S in cls.values())
print('class sizes', dict(sizes))
# is class_x(a) == class_a(x)?
same = sum(1 for (a, x), S in cls.items() if cls[(x, a)] == S)
print('class_x(a) == class_a(x):', same, 'of', len(cls))
# spans and block distribution
a, x = next(iter(cls))
S = cls[(a, x)]
print('example class: span dim', e8.dim(sum(1 << s for s in S)), 'blocks', collections.Counter(G.blk[s] for s in S))
# distinct class sets and how many (target, mate) pairs need each
distinct = collections.Counter(cls.values())
print('distinct class sets', len(distinct), 'multiplicities', collections.Counter(distinct.values()))
# F2 rank of all class sets and of the 180 'pair contents'
def f2rank(vs):
    piv = {}
    r = 0
    for v in vs:
        while v:
            p = v.bit_length() - 1
            if p in piv: v ^= piv[p]
            else: piv[p] = v; r += 1; break
    return r
vecs = [sum(1 << s for s in S) for S in distinct]
print('F2 rank of the distinct class sums:', f2rank(vecs))
# chunking: intersect a class with 4-dim flats spanned by its lines? measure: for each class, how its lines split by block
blkcnt = collections.Counter(tuple(sorted(collections.Counter(G.blk[s] for s in S).values())) for S in distinct)
print('block-split patterns of class sets:', dict(blkcnt))
json.dump({'%d_%d' % k: sorted(v) for k, v in cls.items()}, open('classes.json', 'w'))
