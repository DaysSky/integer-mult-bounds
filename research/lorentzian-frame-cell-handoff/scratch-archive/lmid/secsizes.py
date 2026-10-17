import sys, os, collections, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, g, G
pc = lambda m: bin(m).count('1')
P = lambda i, j: g.P(i, j); T = lambda i, j, k: g.T(i, j, k)
def perp(m):
    r = (1 << V) - 1
    for s in bits(m): r &= HYP[s]
    return r
def typ(s): return 'P' if s < 55 else 'T'
# orthogonal pair types and A2 planes
cnt = collections.Counter(); a2 = collections.Counter()
for a in range(V):
    for b in range(a + 1, V):
        ip = int(G[a][b])
        key = ''.join(sorted(typ(a) + typ(b)))
        if ip == 0:
            cnt[(key, pc(perp((1 << a) | (1 << b))))] += 1
for k, v in sorted(cnt.items()): print('cell', k, v)
# A2 planes: triples pairwise |ip|=1 lying in a rank-2 space: c = a +- b
lines = g.L
import numpy as np
seen = set()
for a in range(V):
    for b in range(a + 1, V):
        if abs(int(G[a][b])) != 1: continue
        for c in range(b + 1, V):
            if abs(int(G[a][c])) != 1 or abs(int(G[b][c])) != 1: continue
            M = np.array([lines[a], lines[b], lines[c]])
            if np.linalg.matrix_rank(M) == 2:
                key = ''.join(sorted(typ(a) + typ(b) + typ(c)))
                a2[(key, pc(perp((1 << a) | (1 << b) | (1 << c))))] += 1
for k, v in sorted(a2.items()): print('A2', k, v)
print('|R(P)|', pc(HYP[0]), '|R(T)|', pc(HYP[100]))
