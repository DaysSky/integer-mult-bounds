"""[lor7 variant: t = "free" drops the w-perp constraint, i.e. all vectors of I_{n,1}, window n+1]
Exact max-weight odd-or-zero systems in w^perp of I_{n,1} (w = (1^n; t)), invariant under a Young subgroup
S_{b1} x ... x S_{bk} of S_n.  Vector (x; y): sum x = t*y, norm |x|^2 - y^2 in NORMS.  Lines v ~ -v.
Orbit pair compatible iff every achievable x.sigma(x') - y y' is 0 or odd (identity / negation excluded within an orbit)."""
import itertools, sys, math, json, time
from collections import Counter
from functools import lru_cache
import networkx as nx
n = int(sys.argv[1]); t = sys.argv[2]; t = None if t == 'free' else int(t); R = int(sys.argv[3]); Y = int(sys.argv[4])
NORMS = set(int(a) for a in sys.argv[5].split(',')); blocks = [int(b) for b in sys.argv[6].split(',')]
assert sum(blocks) == n
vals = list(range(-R, R+1))
@lru_cache(maxsize=None)
def block_multisets(b):
    return list(itertools.combinations_with_replacement(vals, b))
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
            for k in range(0, min(left, colrem[j]) + 1):
                cr = colrem[:j] + (colrem[j]-k,) + colrem[j+1:]
                dist(j+1, left-k, cr, acc2 + k*a*B[j])
        dist(0, cx[a], colrem, acc)
    rec(0, tuple(cp[b] for b in B), 0)
    return frozenset(res)
def neg(ms): return tuple(sorted(-a for a in ms))
orbs = []
for y in range(-Y, Y+1):
    for combo in itertools.product(*[block_multisets(b) for b in blocks]):
        s = sum(sum(c) for c in combo)
        if t is not None and s != t*y: continue
        N = sum(a*a for c in combo for a in c) - y*y
        if N in NORMS: orbs.append((combo, y))
canon = {}
for (cmb, y) in orbs:
    ncmb = tuple(neg(c) for c in cmb)
    canon[max((cmb, y), (ncmb, -y))] = 1
orbs = sorted(canon)
def osize(cmb):
    s = 1
    for c in cmb:
        f = math.factorial(len(c))
        for k in Counter(c).values(): f //= math.factorial(k)
        s *= f
    return s
def lines(o):
    cmb, y = o
    s = osize(cmb)
    if y == 0 and tuple(neg(c) for c in cmb) == cmb: return s // 2
    return s
def dotset(o1, o2):
    S = {0}
    for c1, c2 in zip(o1[0], o2[0]):
        S = {a + b for a in S for b in bdots(c1, c2)}
    return {d - o1[1]*o2[1] for d in S}
ok = lambda d: d == 0 or d % 2 != 0
t0 = time.time()
good = []
for o in orbs:
    D = dotset(o, o)
    N = sum(a*a for c in o[0] for a in c) - o[1]**2
    D.discard(N)
    if o[1] == 0 and tuple(neg(c) for c in o[0]) == o[0]: D.discard(-N)
    if all(ok(d) for d in D): good.append(o)
print('orbits', len(orbs), 'self-compatible', len(good), '%.0fs' % (time.time()-t0), flush=True)
G = nx.Graph()
for i, o in enumerate(good): G.add_node(i, weight=lines(o))
for i in range(len(good)):
    for j in range(i+1, len(good)):
        if all(ok(d) for d in dotset(good[i], good[j])): G.add_edge(i, j)
print('edges', G.number_of_edges(), '%.0fs' % (time.time()-t0), flush=True)
cl, wt = nx.max_weight_clique(G, weight='weight')
print('MAX invariant system under blocks', blocks, ': lines', wt, '%.0fs' % (time.time()-t0))
for i in cl: print('  ', good[i], lines(good[i]))
_ = (dict(n=n, t=t, blocks=blocks, lines=wt, orbits=[[list(map(list, good[i][0])), good[i][1]] for i in cl]),
          None)
