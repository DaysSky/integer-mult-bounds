"""Exact subspace arithmetic for frame-based bit words.  Vectors live in Q^h given by integer coordinates w.r.t.
a fixed basis with integer Gram matrix GRAM.  A subspace is stored as its RREF basis (tuple of tuples of Fractions,
normalised) -- hashable and canonical.  Line membership is cached per subspace."""
from fractions import Fraction as Fr
import numpy as np

class Space:
    def __init__(self, gram, lines):
        self.h = len(gram)
        self.GRAM = [[Fr(x) for x in row] for row in gram]
        self.lines = [tuple(Fr(x) for x in l) for l in lines]
        self.v = len(lines)
        self._lin = {}; self._nd = {}; self._dim = {}
        self.ZERO = ()
        self.FULL = self.rref([[Fr(int(i == j)) for j in range(self.h)] for i in range(self.h)])
        # float copies for fast prefilter
        self.Lf = np.array([[float(x) for x in l] for l in self.lines])
    def ip(self, x, y):
        G = self.GRAM; h = self.h
        return sum(x[i] * G[i][j] * y[j] for i in range(h) if x[i] for j in range(h) if y[j])
    def rref(self, rows):
        m = [list(map(Fr, r)) for r in rows]; r = 0; h = self.h
        for c in range(h):
            p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
            if p is None: continue
            m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
            for i in range(len(m)):
                if i != r and m[i][c] != 0:
                    f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
            r += 1
        return tuple(tuple(x) for x in m[:r])
    def span(self, *parts):
        rows = []
        for p in parts:
            if isinstance(p, int): rows.append(self.lines[p])
            elif len(p) and isinstance(p[0], tuple): rows.extend(p)     # a subspace
            elif len(p): rows.append(tuple(p))                          # a vector
        return self.rref(rows) if rows else ()
    def dim(self, S): return len(S)
    def contains_vec(self, S, x):
        if not S: return all(c == 0 for c in x)
        return len(self.rref(list(S) + [x])) == len(S)
    def sub(self, A, B):
        """A subset of B"""
        if len(A) > len(B): return False
        return len(self.rref(list(B) + list(A))) == len(B)
    def linemask(self, S):
        r = self._lin.get(S)
        if r is None:
            r = 0
            if S:
                if len(S) == self.h: r = (1 << self.v) - 1
                else:
                    for s in range(self.v):
                        if self.contains_vec(S, self.lines[s]): r |= 1 << s
            self._lin[S] = r
        return r
    def nondeg(self, S):
        r = self._nd.get(S)
        if r is None:
            k = len(S)
            M = [[self.ip(a, b) for b in S] for a in S]
            # exact det
            d = Fr(1); M = [row[:] for row in M]
            for c in range(k):
                p = next((i for i in range(c, k) if M[i][c] != 0), None)
                if p is None: d = Fr(0); break
                if p != c: M[c], M[p] = M[p], M[c]; d = -d
                d *= M[c][c]
                for i in range(c + 1, k):
                    if M[i][c] != 0:
                        f = M[i][c] / M[c][c]; M[i] = [a - f * b for a, b in zip(M[i], M[c])]
            r = (d != 0); self._nd[S] = r
        return r
    def perp(self, S):
        """orthogonal complement of S (w.r.t. GRAM) as RREF"""
        if not S: return self.FULL
        # solve (S GRAM) x = 0
        A = [[sum(s[i] * self.GRAM[i][j] for i in range(self.h)) for j in range(self.h)] for s in S]
        R = self.rref(A); piv = []
        for row in R: piv.append(next(j for j in range(self.h) if row[j] != 0))
        free = [j for j in range(self.h) if j not in piv]
        basis = []
        for f in free:
            x = [Fr(0)] * self.h; x[f] = Fr(1)
            for row, p in zip(R, piv): x[p] = -row[f]
            basis.append(x)
        return self.rref(basis)
    def line_perp(self, t): return self.perp(self.span(t))
