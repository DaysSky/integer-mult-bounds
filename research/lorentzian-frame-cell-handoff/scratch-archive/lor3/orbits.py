"""S_n-invariant odd-or-zero systems in w^perp of I_{n,1}, w = (1^n; t) (t chosen so w^perp is even).
Vectors (x; y): sum x = t*y (so <(x;y), w> = sum x - t y = 0), norm = |x|^2 - y^2.
Orbits under S_n = (sorted multiset of x, y).  Lines: v ~ -v.
Compatibility between orbits: every achievable dot product x.sigma(x') - y y' is 0 or odd."""
import itertools, sys, math, numpy as np
from collections import Counter
from functools import lru_cache
n = int(sys.argv[1]); t = int(sys.argv[2]); R = int(sys.argv[3]); Y = int(sys.argv[4])
norms = set(int(a) for a in sys.argv[5].split(','))
vals = list(range(-R, R+1))
def multisets():
    for y in range(-Y, Y+1):
        for comb in itertools.combinations_with_replacement(vals, n):
            if sum(comb) != t*y: continue
            N = sum(c*c for c in comb) - y*y
            if N in norms:
                yield (tuple(comb), y)
orbs = list(multisets())
# canonical line: identify (x;y) with (-x;-y): keep the lexicographically larger of (sorted x, y) and (sorted -x, -y)
canon = {}
for (x, y) in orbs:
    nx = tuple(sorted(-a for a in x)); key = max((x, y), (nx, -y))
    canon[key] = 1
orbs = sorted(canon)
def orbit_size(x):
    c = Counter(x); s = math.factorial(n)
    for k in c.values(): s //= math.factorial(k)
    return s
def line_count(x, y):
    s = orbit_size(x)
    # if -x (sorted) == x and y == 0 then orbit is closed under negation: lines = s/2
    if tuple(sorted(-a for a in x)) == x and y == 0: return s // 2
    return s
def dots(x, xp):
    """set of achievable sum_i x_i xp_sigma(i) over permutations sigma."""
    cx = Counter(x); cp = Counter(xp)
    A = sorted(cx); B = sorted(cp)
    res = set()
    # enumerate contingency tables row by row
    def rec(i, colrem, acc):
        if i == len(A):
            res.add(acc); return
        a = A[i]; need = cx[a]
        # distribute 'need' among columns with remaining capacity
        def dist(j, left, colrem, acc2):
            if j == len(B):
                if left == 0: rec(i+1, colrem, acc2)
                return
            b = B[j]
            for k in range(0, min(left, colrem[j]) + 1):
                cr = list(colrem); cr[j] -= k
                dist(j+1, left-k, tuple(cr), acc2 + k*a*b)
        dist(0, need, colrem, acc)
    rec(0, tuple(cp[b] for b in B), 0)
    return res
def ok_val(d): return d == 0 or d % 2 != 0
def compat(o1, o2, same):
    (x, y), (xp, yp) = o1, o2
    S1 = dots(x, xp); vals1 = {d - y*yp for d in S1}
    # also consider the negated representative of o2 (lines): dot with -v' is negated -> same parity/zero test
    if same:
        # exclude the identity pairing(s) giving the same vector: those give dot = |x|^2 - y^2 = norm (even, nonzero) -> must skip
        # a pair of distinct vectors in the orbit gives some other value; but distinct permutations of x can give the same dot as identity
        # handle by checking whether value 'norm' arises only from sigma(x)=x: approximate: count dot==norm achievable by a permutation moving x
        N = sum(a*a for a in x) - y*y
        vals1 = set(vals1)
        # check if norm achievable by a different vector: dot(x, sigma x) = |x|^2 iff sigma x = x (Cauchy-Schwarz equality) -> only identity
        vals1.discard(N)
        # -v is the same line: dot = -N, achievable only by sigma x = -x
        if tuple(sorted(-a for a in x)) == x and y == 0: vals1.discard(-N)
    return all(ok_val(d) for d in vals1)
print('orbits', len(orbs), flush=True)
good = [o for o in orbs if compat(o, o, True)]
print('self-compatible orbits', len(good), flush=True)
W = [line_count(*o) for o in good]
import networkx as nx
G = nx.Graph()
for i, o in enumerate(good): G.add_node(i, weight=W[i])
for i in range(len(good)):
    for j in range(i+1, len(good)):
        if compat(good[i], good[j], False): G.add_edge(i, j)
print('compat edges', G.number_of_edges(), flush=True)
cl, wt = nx.max_weight_clique(G, weight='weight')
print('MAX S_n-invariant system: lines', wt)
for i in cl: print('  ', good[i], W[i])
