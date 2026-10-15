"""Given an A3 (near-)partition, analyse every section of the A3-parity top: for each block B and each of its planes
(4 triangles, 3 opposite pairs) the section perp(plane) restricted to every other block B': which pieces (whole triangle /
opposite-pair cell / lines with no own cell inside the section) occur.  Routability of the A3 system: a line u in a
section is routable iff one of u's 3 cells (2 triangles + opposite pair of its block) lies inside the section.
usage: la3sec.py n a3part_n.json"""
import sys, os, json, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
n = int(sys.argv[1]); part = [tuple(x) for x in json.load(open(sys.argv[2]))]
g = Geom(n); V = g.V; G = g.G; HYP = g.HYP; bits = g.bits
pc = lambda m: bin(m).count('1')
FULL = (1 << V) - 1
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
def mask(it): return sum(1 << x for x in it)
def struct(X):
    """triangles and opposite pairs of an A3 block"""
    tris = []
    for a, b, c in itertools.combinations(X, 3):
        if G[a][b] != 0 and G[a][c] != 0 and G[b][c] != 0:
            M = np.array([g.L[a], g.L[b], g.L[c]])
            if n == 9:   # E8 via I_{9,1}: rank modulo the null vector w
                M = np.vstack([M, np.array([1] * 9 + [3])])
                if np.linalg.matrix_rank(M) == 3: tris.append((a, b, c))
            elif np.linalg.matrix_rank(M) == 2: tris.append((a, b, c))
    pairs = [(a, b) for a, b in itertools.combinations(X, 2) if G[a][b] == 0]
    assert len(tris) == 4 and len(pairs) == 3, (len(tris), len(pairs))
    return tris, pairs
blocks = [struct(X) for X in part]
blk = {}
for i, X in enumerate(part):
    for s in X: blk[s] = i
cells_of = collections.defaultdict(list)
for i, (tris, pairs) in enumerate(blocks):
    for T in tris + pairs:
        for s in T: cells_of[s].append(mask(T))
covered = set(blk)
print('blocks', len(part), 'lines covered', len(covered), 'of', V)
pat = collections.Counter(); unr = 0; tot = 0; secsz = collections.Counter()
for i, (tris, pairs) in enumerate(blocks):
    for P in tris + pairs:
        S = pm(mask(P)); secsz[(len(P), pc(S))] += 1
        for j in range(len(part)):
            if j == i: continue
            inter = [s for s in part[j] if S >> s & 1]
            tj, pj = blocks[j]
            whole_t = [T for T in tj if all(S >> s & 1 for s in T)]
            whole_p = [Q for Q in pj if all(S >> s & 1 for s in Q)]
            pat[(len(P), len(inter), len(whole_t), len(whole_p))] += 1
        for u in bits(S):
            tot += 1
            if not any(C & ~S == 0 for C in cells_of[u]): unr += 1
print('section (plane size, section size):', dict(secsz))
print('per (plane size, |S cap B\'|, #whole triangles of B\' inside, #whole pairs inside): count')
for k, v in sorted(pat.items()): print('   ', k, v)
print('unroutable (section, line) pairs', unr, 'of', tot, '(leftover lines not in blocks count as unroutable)')
