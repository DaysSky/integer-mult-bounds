"""Fast exact-enough span closure of a line mask in I_{11,1}: QR of the generating lines, residual test of all lines
(integer vectors of norm <= 12; residuals are 0 or >= ~0.1, threshold 1e-6).  Cross-checked against lw.closure."""
import numpy as np, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lmid'))
import lw
LA = lw.g.LA.astype(float); V = lw.V
_C = {}
def fclosure(m):
    r = _C.get(m)
    if r is not None: return r
    b = lw.bits(m)
    U, sv, _ = np.linalg.svd(LA[b].T, full_matrices=False)   # SVD basis: correct for dependent generators
    Q = U[:, sv > 1e-9]
    res = LA - (LA @ Q) @ Q.T
    inside = np.nonzero(np.einsum('ij,ij->i', res, res) < 1e-6)[0]
    out = 0
    for s in inside: out |= 1 << int(s)
    _C[m] = out
    return out
if __name__ == '__main__':
    import random
    random.seed(1)
    import itertools
    for _ in range(300):
        k = random.randint(1, 6)
        m = 0
        for s in random.sample(range(V), k): m |= 1 << s
        assert fclosure(m) == lw.closure(m), m
    # dependent generator sets: coordinate flats and A2 triangles
    for S in [(0, 1, 2), (0, 1, 2, 3), tuple(range(7)), tuple(range(8))]:
        m = 0
        for a, b in itertools.combinations(S, 2): m |= 1 << lw.g.P(a, b)
        for a, b, c in itertools.combinations(S, 3): m |= 1 << lw.g.T(a, b, c)
        assert fclosure(m) == lw.closure(m) == m, S
    m = (1 << lw.g.P(0, 1)) | (1 << lw.g.P(0, 2)) | (1 << lw.g.P(1, 2))
    assert fclosure(m) == lw.closure(m)
    print('fclosure agrees with lw.closure on 300 random masks (up to 6 lines) and on dependent sets (coordinate flats, A2)')
