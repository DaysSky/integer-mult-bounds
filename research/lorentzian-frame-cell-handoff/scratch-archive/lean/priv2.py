"""For a good 4-frame Phi and section sigma=(t,y), the private set P = lines perp t,y but not perp either other frame
member.  Can P be covered by the line sets of TWO flats sigma cap sigma' with sigma' = (t',y') another orthogonal pair
(any good-frame section, or any orthogonal pair)?  Exhaustive."""
import sys, itertools, collections
sys.path.insert(0, '../lword')
from geom import Geom
import numpy as np
g = Geom(11); V = g.V; G = g.G
perp = [0] * V
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and G[t, s] == 0: m |= 1 << s
    perp[t] = m
def name(s): return g.kind[s] + ''.join('%x' % i for i in g.supp[s])
pc = lambda m: bin(m).count('1')
# all good frames -> set of section pairs that occur in good frames
orth = [set(np.nonzero(G[t] == 0)[0].tolist()) - {t} for t in range(V)]
goodsec = set()
for a in range(V):
    for b in orth[a]:
        if b <= a: continue
        for c in orth[a] & orth[b]:
            if c <= b: continue
            for d in orth[a] & orth[b] & orth[c]:
                if d <= c: continue
                if all(x % 2 == 0 for x in g.L[[a, b, c, d]].sum(axis=0)):
                    for p, q in itertools.combinations((a, b, c, d), 2): goodsec.add((p, q))
print('distinct good-frame sections', len(goodsec))
allsec = [(p, q) for p in range(V) for q in orth[p] if p < q]
print('orthogonal pairs', len(allsec))
def study(Phi, pool, label):
    out = []
    for t, y in itertools.combinations(Phi, 2):
        o = [z for z in Phi if z not in (t, y)]
        sig = perp[t] & perp[y]
        P = sig & ~perp[o[0]] & ~perp[o[1]]
        flats = set()
        for (p, q) in pool:
            if {p, q} == {t, y}: continue
            F = sig & perp[p] & perp[q]
            if F & P: flats.add(F & P)
        # remove dominated
        fl = sorted(flats, key=pc, reverse=True)
        keep = []
        for f in fl:
            if not any((f | k) == k for k in keep): keep.append(f)
        best = 0; ex = None
        for a, b in itertools.combinations(keep, 2):
            c = pc((a | b) & P)
            if c > best: best, ex = c, (a, b)
        if keep and pc(keep[0]) > best: best = pc(keep[0])
        out.append((name(t), name(y), pc(sig), pc(P), best, len(keep)))
        print(label, name(t), name(y), 'section', pc(sig), 'private', pc(P), 'best 2-flat cover', best,
              'COVERED' if best == pc(P) else '', flush=True)
    return out
pptt = [g.P(0, 1), g.P(2, 3), g.T(0, 1, 4), g.T(2, 3, 4)]
tttt = [g.T(0, 1, 2), g.T(0, 3, 4), g.T(1, 3, 5), g.T(2, 4, 5)]
for Phi, lab in ((pptt, 'PPTT'), (tttt, 'TTTT')):
    study(Phi, goodsec, lab + '/goodsec')
    study(Phi, allsec, lab + '/anypair')
