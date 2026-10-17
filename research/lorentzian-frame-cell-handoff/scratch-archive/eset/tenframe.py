"""10-frames of I_{11,1}: apex a, perfect matching of the other 10 points -> {P(2i,2i+1), T(2i,2i+1,a)} (perp = D10
normal (1^10,2;4)).  Class structure: tau(u) = frame members perp u.  Stats: |tau| distribution, distinct classes,
class sizes/ranks; parity (lines perp t with |tau - t| even = not covered by the pair-section parity identity)."""
import sys, collections, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G; LA = np.array(g.LA, dtype=float)
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]
T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
orth = lambda x, y: x != y and G[x, y] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
a = 10; M = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
f = [P(i, j) for i, j in M] + [T(i, j, a) for i, j in M]
assert all(orth(x, y) for x, y in itertools.combinations(f, 2))
tau = {u: frozenset(x for x in f if orth(u, x)) for u in range(V) if u not in f}
print('|tau| distribution', sorted(collections.Counter(len(s) for s in tau.values()).items()))
cls = collections.defaultdict(list)
for u, s in tau.items(): cls[s].append(u)
print('distinct classes', len(cls), 'sizes', sorted(collections.Counter(len(c) for c in cls.values()).items()))
print('class (|sigma|, size, rank):', sorted(collections.Counter((len(s), len(c), rk(c)) for s, c in cls.items()).items()))
for t in f[:1] + f[5:6]:
    Rt = [u for u in range(V) if orth(u, t)]
    bad = [u for u in Rt if u not in f and len(tau[u] - {t}) % 2 == 0]
    print('target', g.kind[t], g.supp[t], '|R(t)|', len(Rt), 'lines with even |tau - t| (parity-uncovered):', len(bad),
          'classes containing t:', sum(1 for s in cls if t in s))
