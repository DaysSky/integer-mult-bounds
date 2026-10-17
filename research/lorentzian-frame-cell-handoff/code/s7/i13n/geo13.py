"""I_{13,1} geometry: lines, perps, closures, A2s, cells, sections."""
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
import numpy as np
g = Geom(13); V = g.V; G = g.G; HYP = g.HYP; FULL = g.FULL
bits = g.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
def cl(m): return g.closure(m)[0] if m else 0
def rk(m): return g.closure(m)[1] if m else 0
# vector lookup
vecs = {tuple(g.L[i]): i for i in range(V)}
def lineof(vec):
    t = tuple(int(x) for x in vec)
    if t in vecs: return vecs[t]
    t2 = tuple(-x for x in t)
    return vecs.get(t2)
# A2s: pairs (a,b) with G = +-1 and a -+ b a line
A2 = set()
for a in range(V):
    for b in range(a + 1, V):
        if abs(G[a, b]) == 1:
            c = lineof(g.L[a] - np.sign(G[a, b]) * g.L[b])
            if c is not None: A2.add(tuple(sorted((a, b, c))))
A2 = sorted(A2)
CELLS = [(a, b) for a in range(V) for b in range(a + 1, V) if G[a, b] == 0]
if __name__ == '__main__':
    print('v', V, 'h', g.h, 'A2s', len(A2), 'cells', len(CELLS))
    from collections import Counter
    print('A2 types', Counter(''.join(sorted(g.kind[x] for x in t)) for t in A2))
    print('cell types', Counter(''.join(sorted(g.kind[x] for x in t)) for t in CELLS))
    # section sizes
    cnt = Counter()
    for t in A2[:2000]:
        m = sum(1 << x for x in t); cnt[(''.join(sorted(g.kind[x] for x in t)), pc(pm(m)))] += 1
    print('A2 section sizes', cnt)
    cnt = Counter()
    for t in CELLS[:20000]:
        m = sum(1 << x for x in t); cnt[(''.join(sorted(g.kind[x] for x in t)), pc(pm(m)))] += 1
    print('cell section sizes', cnt)
