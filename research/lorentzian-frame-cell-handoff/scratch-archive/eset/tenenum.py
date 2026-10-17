"""Enumerate all 10-cliques of the orthogonality graph of I_{11,1} (maximal orthogonal frames), classify by P-count and
by perp vector type; save list."""
import sys, collections, itertools, pickle, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
N = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: N[i] |= 1 << j
out = []
def rec(cl, cand):
    if len(cl) == 10: out.append(tuple(cl)); return
    # need 10 - len(cl) more from cand
    if bin(cand).count('1') < 10 - len(cl): return
    while cand:
        b = cand & -cand; v = b.bit_length() - 1; cand ^= b
        rec(cl + [v], cand & N[v])
        if bin(cand).count('1') < 10 - len(cl): return
for v in range(V):
    rec([v], N[v] & ~((1 << (v + 1)) - 1))
print('10-frames', len(out))
pc = collections.Counter(sum(g.kind[u] == 'P' for u in f) for f in out)
print('P-count distribution', sorted(pc.items()))
pickle.dump(out, open('tenframes.pkl', 'wb'))
