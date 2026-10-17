import sys, numpy as np
sys.path.insert(0, '.')
from qreal import points
from zerolm05 import solve_zero
name = sys.argv[1]; p, q = int(sys.argv[2]), int(sys.argv[3])
X, Bm = points(name)
for s in range(int(sys.argv[4])):
    r2, z = solve_zero(Bm, p, q, s, iters=int(sys.argv[5]) if len(sys.argv) > 5 else 300)
    print(name, (p, q), 'seed', s, 'residual^2 %.4g' % r2, flush=True)
    if r2 < 1e-10: np.save('%s_zero_%d%d.npy' % (name, p, q), z); break
