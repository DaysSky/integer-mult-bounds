"""Orbit types of rank-3 frames through t (T(012), P(01)) under Stab(t) in S13: canonical form of (t, F) via lgeo13.canon.
Prints per orbit: size, |F-perp|, nondegenerate?, frame lines (kinds/supports of a representative).
usage: python3 i13_frametypes.py"""
import itertools, collections
import numpy as np
from lgeo13 import *
eta = np.diag([1.0] * n + [-1.0])
def basis(m):
    M = np.zeros((0, n + 1))
    for s in bits(m):
        M2 = np.vstack([M, g.LA[s]])
        if np.linalg.matrix_rank(M2) > M.shape[0]: M = M2
    return M
def nondeg(m):
    B = basis(m); return abs(np.linalg.det(B @ eta @ B.T)) > 1e-6
def nm(s): return KIND[s] + ''.join('%x' % i for i in SUPP[s])
for kind, t in (('T', IDX[('T', (0, 1, 2))]), ('P', IDX[('P', (0, 1))])):
    seen = set(); orbs = collections.OrderedDict()
    for a, b in itertools.combinations([s for s in range(V) if s != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if F in seen: continue
        seen.add(F)
        key = canon((1 << t, F))[0]
        if key not in orbs: orbs[key] = [0, F]
        orbs[key][0] += 1
    print(kind, 'frames', len(seen), 'orbits', len(orbs), flush=True)
    rows = []
    for key, (cnt, F) in orbs.items():
        rows.append((pc(pm(F)), cnt, nondeg(F), ' '.join(nm(s) for s in bits(F))))
    for r in sorted(rows, reverse=True): print('  |perp| %3d  orbit %5d  nondeg %-5s  lines: %s' % r, flush=True)
