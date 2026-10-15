"""Line-system geometry for I_{n,1} odd-or-zero units (A_{n-1} roots e_a - e_b and triples e_a+e_b+e_c+f), in R^{n,1}
with eta = diag(1,..,1,-1).  Frames are closed line masks (flats of the line matroid); dims are vector ranks."""
import itertools
import numpy as np

class Geom:
    def __init__(self, n):
        self.n = n
        L, self.kind, self.supp = [], [], []
        for a, b in itertools.combinations(range(n), 2):
            v = [0] * (n + 1); v[a] = 1; v[b] = -1; L.append(v); self.kind.append('P'); self.supp.append((a, b))
        for T in itertools.combinations(range(n), 3):
            v = [0] * (n + 1)
            for i in T: v[i] = 1
            v[n] = 1; L.append(v); self.kind.append('T'); self.supp.append(T)
        self.L = np.array(L, dtype=np.int64); self.LA = self.L.astype(float)
        self.V = len(L)
        eta = np.eye(n + 1, dtype=np.int64); eta[n, n] = -1; self.eta = eta
        self.G = self.L @ eta @ self.L.T
        self.FULL = (1 << self.V) - 1
        self.idx = {(k, s): i for i, (k, s) in enumerate(zip(self.kind, self.supp))}
        self.HYP = []
        for t in range(self.V):
            m = 0
            for s in np.nonzero(self.G[t] == 0)[0]: m |= 1 << int(s)
            self.HYP.append(m)
        self._cache = {}
        # rank of all lines
        self.h = int(np.linalg.matrix_rank(self.LA))
    def P(self, a, b):
        a, b = min(a, b), max(a, b); return self.idx[('P', (a, b))]
    def T(self, *abc):
        return self.idx[('T', tuple(sorted(abc)))]
    @staticmethod
    def bits(mask):
        out = []
        while mask:
            b = mask & -mask; out.append(b.bit_length() - 1); mask ^= b
        return out
    def closure(self, mask):
        r = self._cache.get(mask)
        if r is not None: return r
        idx = self.bits(mask)
        if not idx: return (0, 0)
        A = self.LA[idx]
        u, s, vt = np.linalg.svd(A, full_matrices=False)
        k = int((s > 1e-9).sum()); Q = vt[:k]
        res = self.LA - (self.LA @ Q.T) @ Q
        cm = 0
        for i in np.nonzero(np.abs(res).max(axis=1) < 1e-9)[0]: cm |= 1 << int(i)
        r = (cm, k); self._cache[mask] = r; self._cache[cm] = r
        return r
    def dim(self, mask): return self.closure(mask)[1]
    def lines_of(self, pred):
        m = 0
        for i in range(self.V):
            if pred(self.kind[i], self.supp[i]): m |= 1 << i
        return m
    def readers(self, t):
        return [s for s in range(self.V) if s != t and self.G[t, s] == 0]
    def binlabel(self, s):
        """binary label u_s in F2^n: a triple's indicator, a pair's complement"""
        if self.kind[s] == 'T': return sum(1 << i for i in self.supp[s])
        return ((1 << self.n) - 1) ^ sum(1 << i for i in self.supp[s])

if __name__ == '__main__':
    g = Geom(11)
    print('v', g.V, 'h', g.h)
    # decoder check: P = U U^T mod 2 equals pattern (1 on diagonal and where G = 0, else 0)
    ok = all(((bin(g.binlabel(s) & g.binlabel(t)).count('1') & 1) == (1 if (s == t or g.G[s, t] == 0) else 0))
             for s in range(g.V) for t in range(g.V))
    print('decoder U U^T == J + G mod 2:', ok)
    # centre totals: gathered A_i, frame and rank
    cst = 0
    for i in range(g.n):
        A = [s for s in range(g.V) if g.binlabel(s) >> i & 1]
        m = sum(1 << s for s in A); cm, k = g.closure(m)
        cst += k
        assert cm == m, 'total frame contains extra lines'
        print('total', i, 'gathered', len(A), 'rank', k, 'closed', cm == m)
    print('cst', cst, 'x', cst / g.V)
