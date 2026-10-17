"""Half and Q spans inside one complete star-D4 block and one Pasch pair of I_{11,1}: sizes, ranks, nondegeneracy of
the half span, and whether each half lies in the pencil room f-perp + u (rank 8)."""
import sys, itertools, collections, numpy as np
from fractions import Fraction
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G; LA = np.array(g.LA, dtype=float)
idx = {(g.kind[i], g.supp[i]): i for i in range(V)}
P = lambda a, b: idx[('P', tuple(sorted((a, b))))]; T = lambda a, b, c: idx[('T', tuple(sorted((a, b, c))))]
orth = lambda a, b: a != b and G[a, b] == 0
rk = lambda S: int(np.linalg.matrix_rank(LA[sorted(S)])) if S else 0
def gram_rank_nondeg(S):
    S = sorted(S); B = LA[S]
    r = np.linalg.matrix_rank(B)
    # basis of span: pick independent rows
    basis = []
    for i in range(len(S)):
        if np.linalg.matrix_rank(LA[[S[j] for j in basis] + [S[i]]]) > len(basis): basis.append(i)
    M = np.array([[G[S[a], S[b]] for b in basis] for a in basis], dtype=float)
    return r, abs(np.linalg.det(M)) > 1e-9
def unit_report(name, frames):
    hs = collections.Counter(); qs = set()
    for f in frames:
        qs.add(frozenset(u for u in range(V) if all(orth(u, x) for x in f)))
        for t, e in itertools.combinations(f, 2):
            k, l = [x for x in f if x not in (t, e)]
            E = [u for u in range(V) if orth(u, t) and orth(u, e) and not orth(u, k) and not orth(u, l)]
            for H in ([u for u in E if G[u, k] == G[u, l]], [u for u in E if G[u, k] == -G[u, l]]): hs[frozenset(H)] += 1
    print(name, 'frames', len(frames), 'distinct halves', len(hs), 'distinct Q', len(qs))
    for H, c in sorted(hs.items(), key=lambda x: len(x[0])):
        r, nd = gram_rank_nondeg(H); print('   half size', len(H), 'rank', r, 'nondeg span', nd, 'multiplicity', c)
    for Q in qs:
        r, nd = gram_rank_nondeg(Q); print('   Q size', len(Q), 'rank', r, 'nondeg', nd)
a, b, c, d, h = 0, 1, 2, 3, 4
blk = [tuple(sorted((P(p, q), P(r, s), T(p, q, h), T(r, s, h)))) for (p, q), (r, s) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))]
unit_report('star block K_4({0,1,2,3})', blk)
M = ((0, 1), (2, 3), (4, 5)); tr = [tuple(sorted((x, y, z))) for x in M[0] for y in M[1] for z in M[2]]
cl = collections.defaultdict(list)
for t in tr: cl[(M[0][0] in t) ^ (M[1][0] in t) ^ (M[2][0] in t)].append(T(*t))
unit_report('Pasch pair on matching 01|23|45', [tuple(sorted(v)) for v in cl.values()])
