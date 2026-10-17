import numpy as np, sys, time
from f2conf import points
from realize import realize
P, Q, B = points('+')
S0, _, _ = points('+', 0)          # singular nonzero vectors of Q+
def orth(L):
    n = len(L); return np.array([[a is not b and (i != j) and B(L[i], L[j]) == 0 for j in range(n)] for i in range(n)])
def O(L):
    n = len(L); M = np.array([[B(a, b) for b in L] for a in L]); o = (M == 0); np.fill_diagonal(o, False); return o
t = time.time()
for h, neg in ((8, 0), (9, 0), (9, 1)):
    r, X = realize(O(P), h, neg, seeds=2)
    print('E8 pattern h', h, 'neg', neg, 'res^2 %.2e' % r, '%.0fs' % (time.time()-t), flush=True)
for extra in (S0[0], P[0]):
    L = P + [extra]
    for h, neg in ((9, 0), (9, 1)):
        for sg in (1, -1):
            signs = [1]*120 + [sg]
            r, X = realize(O(L), h, neg, signs=signs, seeds=3)
            print('E8 +', 'singular' if extra is S0[0] else 'twin', 'h', h, 'neg', neg, 'sign', sg, 'res^2 %.3e' % r,
                  '%.0fs' % (time.time()-t), flush=True)
