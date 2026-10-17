"""The 20-point local configuration of the O^-(8,2) quadric (5 cosets of 4 mutually orthogonal, cross pairs
non-orthogonal) in R^{5,1} with FREE nonzero products (non-root-like).  Zero-pattern LM, margins 0.3 / 0.05 / 0.01:
if the residual scales like margin^2 the pattern forces zeros; if it reaches ~0 it is realisable."""
import numpy as np, sys
sys.path.insert(0, '.')
from qreal import points
import zerolm
X, Bm = points('minus-s')
pts = [tuple(x) for x in X]; idx = {p: i for i, p in enumerate(pts)}
add = lambda a, b: tuple(u ^ v for u, v in zip(a, b))
p = pts[0]; a = next(q for q in pts if q != p and Bm[idx[p], idx[q]] == 0)
line = [p, a, add(p, a)]
perp = [q for q in pts if q not in line and all(Bm[idx[q], idx[l]] == 0 for l in line)]
sub = [idx[q] for q in perp]; B20 = Bm[np.ix_(sub, sub)]
for mg in (0.3, 0.05, 0.01):
    best = 1e9
    for sig in ((5, 1), (6, 0)):
        for s in range(6):
            r2, z = zerolm.solve_zero(B20, sig[0], sig[1], s, iters=2000, margin=mg); best = min(best, r2)
            if r2 < 1e-12: break
        if best < 1e-12: print('margin', mg, sig, 'REALISABLE', flush=True); break
    print('margin %.2f: best residual^2 %.3g' % (mg, best), flush=True)
