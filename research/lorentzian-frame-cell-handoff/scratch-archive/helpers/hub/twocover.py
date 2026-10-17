"""Exact test: can the readers of a source be covered by TWO hyperplane sections (i.e. two branch frames of any
dimension)?  Readers T(s) = lines orthogonal to s.  Two sections {t : n1.t = 0} and {t : n2.t = 0} (n1, n2 nonzero on
span T(s)) cover T(s) iff the quadratic form q(y) = (n1.y)(n2.y) vanishes on every reader, and q is then a nonzero
quadratic form on span T(s).  So: if the only quadratic form on span T(s) vanishing on all readers is 0, the branch
cover number is >= 3 (no two branches suffice in any design).  Computed exactly over Q (sympy nullspace).
If the space is nonzero we report its dimension (a 2-cover may or may not exist; S3 gives certificates for pairs).
Usage: python twocover.py n   (n = 8: E8 control)"""
import sys, itertools
import numpy as np
import sympy as sp
sys.dont_write_bytecode = True
import units as U


def test(L, G, s, Q):
    R = [t for t in range(len(L)) if t != s and G[s, t] == 0]
    M = sp.Matrix(L[R].tolist())
    B = M.T.columnspace()                               # basis of span T(s) in ambient coordinates
    Bm = sp.Matrix.hstack(*B)                           # ambient x r
    Y = [Bm.solve_least_squares(sp.Matrix(L[t].tolist())) for t in R]   # exact coordinates (consistent system)
    r = Bm.shape[1]
    idx = [(i, j) for i in range(r) for j in range(i, r)]
    A = sp.Matrix([[y[i] * y[j] * (1 if i == j else 2) for (i, j) in idx] for y in Y])
    ns = A.nullspace()
    return len(R), r, len(ns)


if __name__ == '__main__':
    n = int(sys.argv[1])
    if n == 8:
        L = U.roots_E8(); G = U.gram_doubled(L); reps = [('E8 root', 0)]; Q = None
    else:
        L, G, lab = U.lorentz_family(n)
        LN = list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 2))
        reps = [('triple', 0), ('pair', LN.index((0, 1)))]
    for name, s in reps:
        z, r, d = test(L, G, s, None)
        print('n=%d %s source: %d readers spanning %d dims; quadratic forms vanishing on all readers: dim %d -> %s' % (
            n, name, z, r, d, 'NO 2-cover (branch cover number >= 3)' if d == 0 else '2-cover not excluded'), flush=True)
