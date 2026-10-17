"""Exact check: for every good 4-frame type of I_{11,1} (PPTT, TTTT) and every section, the rank of the private set
equals the rank of the section's line flat (private set spans the section), and the private sets of the two
targets of a section coincide.  Also PPP covers: private ranks."""
import sys, itertools
sys.path.insert(0, '../lword')
from geom import Geom
import numpy as np
g = Geom(11); V = g.V; G = g.G
perp = [0] * V
for t in range(V):
    for s in range(V):
        if s != t and G[t, s] == 0: perp[t] |= 1 << s
pc = lambda m: bin(m).count('1')
rk = lambda m: g.dim(m)
for lab, Phi in (('PPTT', [g.P(0, 1), g.P(2, 3), g.T(0, 1, 4), g.T(2, 3, 4)]),
                 ('TTTT', [g.T(0, 1, 2), g.T(0, 3, 4), g.T(1, 3, 5), g.T(2, 4, 5)])):
    for t, y in itertools.combinations(Phi, 2):
        o = [z for z in Phi if z not in (t, y)]
        sig = perp[t] & perp[y]
        Pt = sig & ~perp[o[0]] & ~perp[o[1]]
        Py = Pt  # same frame -> same other members
        print(lab, 'section rank', rk(sig), 'lines', pc(sig), '| private', pc(Pt), 'rank', rk(Pt), 'spans' if rk(Pt) == rk(sig) else 'PROPER')
t = g.T(0, 1, 2); ys = [g.P(3, 4), g.P(5, 6), g.P(7, 8)]
for y in ys:
    sig = perp[t] & perp[y]; o = [z for z in ys if z != y]
    Pt = sig & ~perp[o[0]] & ~perp[o[1]]
    print('PPP T012 with', y, 'section rank', rk(sig), 'private for T', pc(Pt), 'rank', rk(Pt))
