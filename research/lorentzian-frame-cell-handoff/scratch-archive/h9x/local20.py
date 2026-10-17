"""Necessary local structure of a root-like realisation of the O^-(8,2) singular quadric (119) in R^{8,1}: for a
totally singular line l, the 20 points of l^perp minus l lie in span(l)^perp = R^{5,1} as 5 cosets of 4 mutually
orthogonal vectors with all cross products +-1 (ovoid Q^-(3,2) has no collinear pairs).  Also the 54-point star
C(p) in R^{7,1}.  LM equality-only, many seeds."""
import numpy as np, sys, itertools
sys.path.insert(0, '.')
from qreal import points, solve
X, Bm = points('minus-s')
pts = [tuple(x) for x in X]; idx = {p: i for i, p in enumerate(pts)}
add = lambda a, b: tuple(u ^ v for u, v in zip(a, b))
p = pts[0]
a = next(q for q in pts if q != p and Bm[idx[p], idx[q]] == 0)
line = [p, a, add(p, a)]
assert all(q in idx for q in line)
perp = [q for q in pts if q not in line and all(Bm[idx[q], idx[l]] == 0 for l in line)]
print('line^perp points', len(perp), flush=True)
sub = [idx[q] for q in perp]; B20 = Bm[np.ix_(sub, sub)]
star = [idx[q] for q in pts if q != p and Bm[idx[p], idx[q]] == 0]; B54 = Bm[np.ix_(star, star)]
for name, Bs, sig in (('20-point l^perp', B20, (5, 1)), ('54-point star', B54, (7, 1))):
    best = 1e9
    for s in range(int(sys.argv[1]) if len(sys.argv) > 1 else 10):
        r2, z = solve(Bs, sig[0], sig[1], s, iters=3000)
        best = min(best, r2)
        if r2 < 1e-10: break
    print('%s in R^%s: best residual^2 %.4g over %d seeds' % (name, sig, best, s + 1), flush=True)
