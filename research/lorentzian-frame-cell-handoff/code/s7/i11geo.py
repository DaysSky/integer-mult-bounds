"""I_{11,1} lines in the 11-dim line-coordinate basis (as lw.py): exact Space."""
import sys, itertools
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'zw'))
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
import numpy as np
from geom import Geom
from space import Space
g = Geom(11); V = g.V
BASIS = [g.P(i, i + 1) for i in range(10)] + [g.T(0, 1, 2)]
Bm = g.L[BASIS].astype(float)
COORD = []
for s in range(V):
    c, *_ = np.linalg.lstsq(Bm.T, g.L[s].astype(float), rcond=None)
    ci = np.rint(c).astype(int); assert (ci @ g.L[BASIS] == g.L[s]).all(); COORD.append([int(x) for x in ci])
GRAM = (g.L[BASIS] @ g.eta @ g.L[BASIS].T).astype(int).tolist()
S = Space(GRAM, COORD)
def amb_to_coord(x):
    """ambient R^{11,1} vector (must lie in w-perp) -> line-basis coordinates (Fractions)"""
    from fractions import Fraction as Fr
    A = [[Fr(int(Bm[j][i])) for j in range(11)] + [Fr(x[i])] for i in range(12)]
    r = 0
    for c in range(11):
        p = next(i for i in range(r, 12) if A[i][c] != 0)
        A[r], A[p] = A[p], A[r]; iv = 1 / A[r][c]; A[r] = [a * iv for a in A[r]]
        for i in range(12):
            if i != r and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    assert A[11][11] == 0
    return [A[i][11] for i in range(11)]
