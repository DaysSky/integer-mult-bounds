"""All unordered line triples (u1,u2,u3) whose sections R(t) cap u_i^perp cover R(t), for t = P(0,1) and T(0,1,2) of
I_{11,1}; printed by combinatorial type."""
import sys, itertools, collections
sys.path.insert(0, '../lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
def name(s): return g.kind[s] + ''.join('%x' % i for i in g.supp[s])
for t in (g.P(0, 1), g.T(0, 1, 2)):
    rd = [s for s in range(V) if s != t and G[t, s] == 0]
    idx = {s: i for i, s in enumerate(rd)}; full = (1 << len(rd)) - 1
    M = {}
    for u in range(V):
        if u == t: continue
        m = 0
        for s in rd:
            if s != u and G[u, s] == 0: m |= 1 << idx[s]
        M[u] = m
    us = [u for u in M if G[t, u] == 0]
    covs = [c for c in itertools.combinations(us, 3) if (M[c[0]] | M[c[1]] | M[c[2]]) == full]
    print(name(t), 'readers', len(rd), '#covers', len(covs))
    typ = collections.Counter()
    ex = {}
    for c in covs:
        k = tuple(sorted(g.kind[u] for u in c))
        typ[k] += 1; ex.setdefault(k, []).append(c)
    for k, n in typ.items():
        print('  ', k, n, 'e.g.', [' '.join(name(u) for u in c) for c in ex[k][:6]])
    # also non-orthogonal u
    us2 = list(M)
    n2 = sum(1 for c in itertools.combinations(us2, 3) if (M[c[0]] | M[c[1]] | M[c[2]]) == full)
    print('   covers using any lines', n2)
