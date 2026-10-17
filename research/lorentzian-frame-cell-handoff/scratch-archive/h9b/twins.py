import numpy as np, sys, time
from f2conf import points
from orth_eq import solve
P, Q, B = points('+')
n0 = len(P)
M = np.array([[B(a, b) for b in P] for a in P])
def pattern(tw):
    # lines: E8 (120) + twins of lines in tw (same class); twin pairs orthogonal; pattern by class
    cls = list(range(n0)) + list(tw)
    n = len(cls)
    O = np.array([[M[cls[i], cls[j]] == 0 for j in range(n)] for i in range(n)]); np.fill_diagonal(O, False)
    return O
t = time.time()
print('control E8 h=8:', ['%.1e/%.2f' % solve(pattern([]), 8, 0, seed=s)[::2] for s in range(2)], flush=True)
rng = np.random.default_rng(0)
for k in (1, 2, 4, 8, 12):
    tw = [int(x) for x in rng.choice(n0, k, replace=False)]
    O = pattern(tw)
    for h, neg in ((9, 1), (9, 0), (10, 1)):
        best = min((solve(O, h, neg, seed=s, iters=600) for s in range(4)), key=lambda r: r[0])
        print('E8 + %2d twins, h=%d neg=%d: res^2 %.2e, min |nonorth product| %.3f  (%.0fs)' % (k, h, neg, best[0], best[2], time.time()-t), flush=True)
