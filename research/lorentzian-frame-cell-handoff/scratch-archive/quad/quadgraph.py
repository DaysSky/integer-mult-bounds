"""Nonsingular points of O^eps(2m,2) and the B-orthogonality graph (pairs with B(a,b)=0, a!=b)."""
import itertools, numpy as np
def qform(m, eps):
    # q(x) = sum_{i<m-1} x_{2i}x_{2i+1} + (last pair: x y if eps=+1 else x^2+xy+y^2)
    def q(x):
        s = 0
        for i in range(m):
            a, b = x[2*i], x[2*i+1]
            if i == m-1 and eps == -1:
                s += a*a + a*b + b*b
            else:
                s += a*b
        return s % 2
    def B(x, y):
        s = 0
        for i in range(m):
            s += x[2*i]*y[2*i+1] + x[2*i+1]*y[2*i]
        return s % 2
    return q, B
def nonsingular(m, eps):
    q, B = qform(m, eps)
    pts = [x for x in itertools.product((0, 1), repeat=2*m) if any(x) and q(x) == 1]
    P = np.array(pts, dtype=np.int64)
    # B matrix: symplectic standard
    J = np.zeros((2*m, 2*m), dtype=np.int64)
    for i in range(m):
        J[2*i, 2*i+1] = J[2*i+1, 2*i] = 1
    Bm = (P @ J @ P.T) % 2
    return P, Bm
if __name__ == '__main__':
    for m, e in ((4, 1), (4, -1), (5, 1), (5, -1), (3, 1), (3, -1)):
        P, Bm = nonsingular(m, e)
        n = len(P); deg = ((Bm == 0).sum(1) - 1)
        print('O^%s(%d,2): %d nonsingular points, orth-degree %s' % ('+' if e > 0 else '-', 2*m, n, set(deg.tolist())))
