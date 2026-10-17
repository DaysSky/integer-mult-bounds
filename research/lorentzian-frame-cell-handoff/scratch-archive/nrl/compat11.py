"""Non-root-like extensions of I_{11,1}: lattice vectors x = (x_1..x_11; x_f) in w-perp (w = (1^11; 3)), even nonzero
norm, small coordinates, whose products with all 220 I_{11,1} lines are odd or zero.  Up to S11 (sorted coords)."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); L = g.L; eta = np.array([1] * 11 + [-1])
B = int(sys.argv[1]) if len(sys.argv) > 1 else 2
found = []
vals = list(range(-B, B + 1))
for xs in itertools.combinations_with_replacement(vals, 11):
    s = sum(xs)
    if s % 3: continue
    xf = s // 3                         # w-perp: sum x_i - 3 x_f... with eta: x.w = sum x_i - 3 x_f = 0
    x = np.array(list(xs) + [xf])
    nrm = int((x * eta) @ x)
    if nrm == 0 or nrm % 2: continue
    # all S11 images give the same multiset of products with the S11-invariant line set, so test canonical only
    p = L @ (eta * x)
    if all(v == 0 or v % 2 for v in p):
        isline = any((L == x).all(1)) or any((L == -x).all(1))
        found.append((nrm, xs, xf, isline, int((p == 0).sum())))
found.sort()
print('compatible canonical vectors (norm, coords, f, is-line, #orth):', len(found))
for r in found[:40]: print(r)
