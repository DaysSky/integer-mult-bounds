"""Compatibility of A3 pairs: B, B' (disjoint) are compatible iff for every plane P of B, perp(P) meets B' in a union of
B' cells (empty, an opposite pair, a triangle, or all of B'), and vice versa.  Stats on random pairs + pickle of the
full compatibility lists if feasible.  usage: la3compat.py n [full]"""
import sys, os, json, itertools, collections, random, time, pickle
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
n = int(sys.argv[1]); FULLRUN = len(sys.argv) > 2
g = Geom(n); V = g.V; G = g.G; HYP = g.HYP; bits = g.bits
pc = lambda m: bin(m).count('1')
FM = (1 << V) - 1
def pm(m):
    r = FM
    for s in bits(m): r &= HYP[s]
    return r
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
w = np.array([1] * n + [3]); NULLW = (n == 9)
def third(a, b):
    out = set()
    if G[a][b] == 0: return out
    for sg in (1, -1):
        v = g.L[a] - sg * g.L[b]
        for k in (range(-3, 4) if NULLW else (0,)):
            c = VEC.get(tuple(int(x) for x in (v + k * w)))
            if c is not None and c not in (a, b): out.add(c)
    return out
A2 = set()
for a in range(V):
    for b in range(a + 1, V):
        for c in third(a, b): A2.add(frozenset((a, b, c)))
tri_of = collections.defaultdict(list)
for T in A2:
    for x in T: tri_of[x].append(T)
A3 = set()
for t in range(V):
    for T1, T2 in itertools.combinations(tri_of[t], 2):
        s = set(T1) | set(T2)
        if len(s) != 5: continue
        a, b = [x for x in T1 if x != t]; c, d = [x for x in T2 if x != t]
        for (p, q), (r, s2) in (((a, c), (b, d)), ((a, d), (b, c))):
            for e in third(p, q) & third(r, s2):
                six = frozenset((t, a, b, c, d, e))
                if len(six) == 6 and G[t][e] == 0 and sum(1 for T in tri_of[t] if T <= six) == 2:
                    A3.add(six)
A3 = sorted(tuple(sorted(x)) for x in A3)
info = []
for X in A3:
    six = set(X)
    tris = sorted({T for s in X for T in tri_of[s] if T <= six})
    pairs = [(a, b) for a, b in itertools.combinations(X, 2) if G[a][b] == 0]
    assert len(tris) == 4 and len(pairs) == 3
    m = sum(1 << x for x in X)
    allowed = {0, m} | {sum(1 << x for x in T) for T in tris} | {(1 << a) | (1 << b) for a, b in pairs}
    planes = [pm(sum(1 << x for x in T)) for T in tris] + [pm((1 << a) | (1 << b)) for a, b in pairs]
    info.append((m, allowed, planes))
print('A3', len(A3), flush=True)
def compat(i, j):
    mi, ai, pi = info[i]; mj, aj, pj = info[j]
    if mi & mj: return False
    for S in pi:
        if (S & mj) not in aj: return False
    for S in pj:
        if (S & mi) not in ai: return False
    return True
random.seed(1)
c = 0; d = 0
for _ in range(20000):
    i, j = random.randrange(len(A3)), random.randrange(len(A3))
    if info[i][0] & info[j][0]: continue
    d += 1; c += compat(i, j)
print('random disjoint pairs', d, 'compatible fraction %.4f' % (c / max(d, 1)), flush=True)
if FULLRUN:
    t0 = time.time()
    nb = [[] for _ in A3]
    for i in range(len(A3)):
        for j in range(i + 1, len(A3)):
            if compat(i, j): nb[i].append(j); nb[j].append(i)
        if i % 500 == 0: print(i, '%.0fs' % (time.time() - t0), flush=True)
    pickle.dump(dict(A3=A3, nb=nb), open('a3compat_%d.pkl' % n, 'wb'))
    print('degrees', collections.Counter(len(x) for x in nb).most_common(8))
