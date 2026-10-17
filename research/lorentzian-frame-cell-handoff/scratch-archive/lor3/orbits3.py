"""Exact max-weight odd-or-zero systems in w^perp of I_{n,k} (k negative coords), w = (1^n; t^k), invariant under
S_{b1} x ... (positive blocks) x S_k (negative block).  norm = |x|^2 - |y|^2, <v,w> = sum x - t sum y = 0."""
import itertools, sys, math, time
from collections import Counter
from functools import lru_cache
import networkx as nx
n, k, t, R, Y = (int(a) for a in sys.argv[1:6]); NORMS = set(int(a) for a in sys.argv[6].split(','))
blocks = [int(b) for b in sys.argv[7].split(',')]; assert sum(blocks) == n
pv = list(range(-R, R+1)); nv = list(range(-Y, Y+1))
@lru_cache(maxsize=None)
def bdots(x, xp):
    cx = Counter(x); cp = Counter(xp); A = sorted(cx); B = sorted(cp); res = set()
    def rec(i, colrem, acc):
        if i == len(A): res.add(acc); return
        a = A[i]
        def dist(j, left, colrem, acc2):
            if j == len(B):
                if left == 0: rec(i+1, colrem, acc2)
                return
            for kk in range(0, min(left, colrem[j]) + 1):
                cr = colrem[:j] + (colrem[j]-kk,) + colrem[j+1:]
                dist(j+1, left-kk, cr, acc2 + kk*a*B[j])
        dist(0, cx[a], colrem, acc)
    rec(0, tuple(cp[b] for b in B), 0)
    return frozenset(res)
neg = lambda ms: tuple(sorted(-a for a in ms))
orbs = {}
for combo in itertools.product(*[list(itertools.combinations_with_replacement(pv, b)) for b in blocks]):
    sx = sum(sum(c) for c in combo); qx = sum(a*a for c in combo for a in c)
    for yc in itertools.combinations_with_replacement(nv, k):
        if sx != t*sum(yc): continue
        N = qx - sum(a*a for a in yc)
        if N in NORMS:
            o = (combo, yc); no = (tuple(neg(c) for c in combo), neg(yc)); orbs[max(o, no)] = 1
orbs = sorted(orbs)
def size(o):
    s = 1
    for c in list(o[0]) + [o[1]]:
        f = math.factorial(len(c))
        for v in Counter(c).values(): f //= math.factorial(v)
        s *= f
    return s
def lines(o):
    s = size(o)
    if tuple(neg(c) for c in o[0]) == o[0] and neg(o[1]) == o[1]: return s // 2
    return s
def dotset(o1, o2):
    S = {0}
    for c1, c2 in zip(o1[0], o2[0]): S = {a + b for a in S for b in bdots(c1, c2)}
    Sy = bdots(o1[1], o2[1])
    return {a - b for a in S for b in Sy}
ok = lambda d: d == 0 or d % 2 != 0
good = []
for o in orbs:
    Dx = {0}
    for c in o[0]: Dx = {a + b for a in Dx for b in bdots(c, c)}
    Dy = bdots(o[1], o[1])
    qx = sum(a*a for c in o[0] for a in c); qy = sum(a*a for a in o[1])
    selfneg = tuple(neg(c) for c in o[0]) == o[0] and neg(o[1]) == o[1]
    D = set()
    for dx in Dx:
        for dy in Dy:
            if dx == qx and dy == qy: continue            # same vector
            if selfneg and dx == -qx and dy == -qy: continue   # negated vector = same line
            D.add(dx - dy)
    if all(ok(d) for d in D): good.append(o)
print('orbits', len(orbs), 'self-compatible', len(good), flush=True)
G = nx.Graph()
for i, o in enumerate(good): G.add_node(i, weight=lines(o))
for i in range(len(good)):
    for j in range(i+1, len(good)):
        if all(ok(d) for d in dotset(good[i], good[j])): G.add_edge(i, j)
cl, wt = nx.max_weight_clique(G, weight='weight')
print('MAX n=%d k=%d t=%d blocks %s: lines %d (window %d)' % (n, k, t, blocks, wt, n + k - 1))
for i in cl: print('  ', good[i], lines(good[i]))
