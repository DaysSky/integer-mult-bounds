"""Exact rational subspaces of Q^h with a symmetric bilinear form B (Fractions).  A subspace is stored canonically
as its reduced row echelon basis (tuple of tuples of Fractions); the canonical tuple is hashable and serves as the
frame key.  Used for general (non-port-spanned) frames: the paper's labels are nondegenerate subspaces."""
from fractions import Fraction as Fr

def rref(rows, ncols):
    m = [list(map(Fr, r)) for r in rows if any(r)]
    piv = []; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
        if r == len(m): break
    return tuple(tuple(row) for row in m[:r]), tuple(piv)

class Space:
    def __init__(self, B):
        self.B = [list(map(Fr, row)) for row in B]; self.h = len(B)
        self._join = {}; self._nd = {}
        self.ZERO = (); self.FULL = rref([[1 if i == j else 0 for j in range(self.h)] for i in range(self.h)], self.h)[0]
    def span(self, vecs):
        return rref(vecs, self.h)[0]
    def dim(self, U): return len(U)
    def join(self, U, V):
        key = (U, V) if id(U) <= id(V) else (V, U)
        r = self._join.get((U, V))
        if r is None:
            r = self.span(list(U) + list(V)); self._join[(U, V)] = r
        return r
    def contains_vec(self, U, x):
        return len(self.span(list(U) + [x])) == len(U)
    def subset(self, U, V):
        return len(self.join(U, V)) == len(V)
    def ip(self, x, y):
        return sum(x[i] * sum(self.B[i][j] * y[j] for j in range(self.h)) for i in range(self.h))
    def gram_det(self, U):
        k = len(U)
        if k == 0: return Fr(1)
        G = [[self.ip(U[i], U[j]) for j in range(k)] for i in range(k)]
        # exact determinant by elimination
        det = Fr(1); M = [row[:] for row in G]
        for c in range(k):
            p = next((i for i in range(c, k) if M[i][c] != 0), None)
            if p is None: return Fr(0)
            if p != c: M[c], M[p] = M[p], M[c]; det = -det
            det *= M[c][c]
            for i in range(c + 1, k):
                if M[i][c] != 0:
                    f = M[i][c] / M[c][c]; M[i] = [a - f * b for a, b in zip(M[i], M[c])]
        return det
    def nondegenerate(self, U):
        r = self._nd.get(U)
        if r is None:
            r = self.gram_det(U) != 0; self._nd[U] = r
        return r
    def perp(self, U):
        """orthogonal complement of U in Q^h under B"""
        if not U: return self.FULL
        # solve <u, y> = 0 for all u in U:  rows (u^T B)
        rows = [[sum(u[i] * self.B[i][j] for i in range(self.h)) for j in range(self.h)] for u in U]
        R, piv = rref(rows, self.h)
        free = [c for c in range(self.h) if c not in piv]
        basis = []
        for f in free:
            y = [Fr(0)] * self.h; y[f] = Fr(1)
            for r, pc in zip(R, piv): y[pc] = -r[f]
            basis.append(y)
        return self.span(basis)
    @staticmethod
    def to_int_rows(U):
        """integer rows spanning U (each RREF row scaled by the lcm of its denominators)"""
        from math import lcm
        out = []
        for row in U:
            L = 1
            for x in row: L = lcm(L, x.denominator)
            out.append([int(x * L) for x in row])
        return out
