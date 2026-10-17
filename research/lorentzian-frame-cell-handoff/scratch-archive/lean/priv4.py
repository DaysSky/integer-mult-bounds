"""FOREIGN sharing only (sections with no target in common). List the 2-flat covers of each section's private set (PPTT and TTTT frames), by which other sections share the
flats; report flat rank and line count."""
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
def names(m): return ' '.join(name(s) for s in g.bits(m))
pc = lambda m: bin(m).count('1')
orth = [set(np.nonzero(G[t] == 0)[0].tolist()) - {t} for t in range(V)]
allsec = [(p, q) for p in range(V) for q in orth[p] if p < q]
def study(Phi, label):
    for t, y in itertools.combinations(Phi, 2):
        o = [z for z in Phi if z not in (t, y)]
        sig = perp[t] & perp[y]
        P = sig & ~perp[o[0]] & ~perp[o[1]]
        flats = collections.defaultdict(list)
        for (p, q) in allsec:
            if {p, q} & {t, y}: continue
            F = sig & perp[p] & perp[q]
            if F & P: flats[F].append((p, q))
        fl = list(flats)
        covers = []
        for a, b in itertools.combinations(fl, 2):
            if (a | b) & P == P: covers.append((a, b))
        # minimal by total lines
        covers.sort(key=lambda ab: pc(ab[0]) + pc(ab[1]))
        print('==', label, name(t), name(y), 'private', pc(P), '#covers', len(covers))
        print('   private:', names(P))
        seen = 0
        for a, b in covers[:4]:
            for F in (a, b):
                print('     flat lines', pc(F), 'rank', g.dim(F), 'priv', pc(F & P), 'shared with', [(name(p), name(q)) for p, q in flats[F]][:8])
            print('     --')
pptt = [g.P(0, 1), g.P(2, 3), g.T(0, 1, 4), g.T(2, 3, 4)]
tttt = [g.T(0, 1, 2), g.T(0, 3, 4), g.T(1, 3, 5), g.T(2, 4, 5)]
study(pptt, 'PPTT'); study(tttt, 'TTTT')
