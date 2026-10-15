"""Sample 4-section union covers of R(t) (plane sections through t; in-chain section + 3 delivered; <= 3 uncovered
lines allowed for the rank<=2 read): per section the exclusive lines and whether a PROPER closed node contains them."""
import itertools, collections, random
from lgeo import *
random.seed(7)
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]
    found = 0; stat = collections.Counter(); tries = 0
    while found < 3000 and tries < 3000000:
        tries += 1
        q = random.sample(range(len(pl)), 4)
        U = S[q[0]] | S[q[1]] | S[q[2]] | S[q[3]]
        if pc(R & ~U) > 3: continue
        found += 1
        for a in q:
            others = 0
            for b in q:
                if b != a: others |= S[b]
            ex = S[a] & ~others
            N = pp(ex) if ex else 0
            stat[(pc(ex) // 5 * 5, 'proper' if N != S[a] else 'whole')] += 1
    print('target', KIND[t], '4-covers sampled', found, 'of', tries, 'tries')
    for k, v in sorted(stat.items()): print('   |excl| bucket, closure:', k, v)
