"""I_{13,1} lines (78 P + 286 T) with S13 canonical forms for tuples of line sets.
canon(masks) -> (canonical tuple of masks, a permutation of points realising it).
Port of llp/lgeo.py (n = 11 -> 13); exact, no invariant shortcuts."""
import sys, os, itertools, functools
import numpy as np

N = int(os.environ.get('NW', '13'))

class LG:
    def __init__(self, n):
        import itertools as it
        L, kind, supp = [], [], []
        for a, b in it.combinations(range(n), 2):
            v = [0] * (n + 1); v[a] = 1; v[b] = -1
            L.append(v); kind.append('P'); supp.append((a, b))
        for T in it.combinations(range(n), 3):
            v = [0] * (n + 1)
            for i in T: v[i] = 1
            v[n] = 1
            L.append(v); kind.append('T'); supp.append(T)
        self.n = n
        self.LA = np.array(L, dtype=np.int64).astype(float)
        self.L = np.array(L, dtype=np.int64)
        self.V = len(L)
        eta = np.eye(n + 1, dtype=np.int64); eta[n, n] = -1
        self.G = self.L @ eta @ self.L.T
        self.HYP = []
        for t in range(self.V):
            m = 0
            for s in np.nonzero(self.G[t] == 0)[0]: m |= 1 << int(s)
            self.HYP.append(m)
        self.FULL = (1 << self.V) - 1
        self.bits = LG.bits
        self.pc = LG.pc
        self.KIND = kind; self.SUPP = supp; self.IDX = {(k, s): i for i, (k, s) in enumerate(zip(kind, supp))}
        # transposition images of lines
        self.TRL = {}
        for x, y in it.combinations(range(n), 2):
            perm = list(range(n)); perm[x], perm[y] = y, x
            self.TRL[(x, y)] = [self.img_line(s, perm) for s in range(self.V)]
    @staticmethod
    def bits(mask):
        out = []
        while mask:
            b = mask & -mask; out.append(b.bit_length() - 1); mask ^= b
        return out
    @staticmethod
    def pc(m): return bin(m).count('1')
    def P(self, a, b):
        a, b = min(a, b), max(a, b); return self.IDX[('P', (a, b))]
    def T(self, *abc):
        return self.IDX[('T', tuple(sorted(abc)))]
    def pm(self, m):
        r = self.FULL
        for s in self.bits(m): r &= self.HYP[s]
        return r
    def pp(self, m): return self.pm(self.pm(m))
    def rank(self, m):
        b = self.bits(m)
        return int(np.linalg.matrix_rank(self.LA[b])) if b else 0
    def img_line(self, s, perm):
        return self.IDX[(self.KIND[s], tuple(sorted(perm[i] for i in self.SUPP[s])))]
    def act(self, m, perm):
        r = 0
        for s in self.bits(m): r |= 1 << self.img_line(s, perm)
        return r
    def act_tr(self, m, x, y):
        tl = self.TRL[(min(x, y), max(x, y))]
        r = 0
        for s in self.bits(m): r |= 1 << tl[s]
        return r

g = LG(N); V = g.V; n = N; HYP = g.HYP; FULL = g.FULL
bits, pc, pm, pp, rank, act = g.bits, g.pc, g.pm, g.pp, g.rank, g.act
KIND, SUPP, IDX = g.KIND, g.SUPP, g.IDX
act_tr = g.act_tr

def _refine(col, masks_lines):
    """col: list of ints (point colours).  masks_lines: list over masks of list of point-tuples.  Equitable refinement."""
    while True:
        sig = []
        for x in range(n):
            parts = [col[x]]
            for mi, ml in enumerate(masks_lines):
                lst = []
                for pts in ml:
                    if x in pts:
                        lst.append((len(pts), tuple(sorted(col[y] for y in pts if y != x))))
                lst.sort(); parts.append(tuple(lst))
            sig.append(tuple(parts))
        keys = sorted(set(sig))
        new = [keys.index(sig[x]) for x in range(n)]
        if len(set(new)) == len(set(col)):
            return new
        col = new

def canon(masks):
    masks = tuple(masks)
    ml = [[SUPP[s] for s in bits(m)] for m in masks]
    best = [None, None]
    def leaf(col):
        perm = col[:]
        img = tuple(act(m, perm) for m in masks)
        if best[0] is None or img < best[0]: best[0] = img; best[1] = perm
    def rec(col):
        col = _refine(col, ml)
        if len(set(col)) == n: leaf(col); return
        cls = {}
        for x in range(n): cls.setdefault(col[x], []).append(x)
        cands = [c for c in cls.values() if len(c) > 1]
        cmin = min(cands, key=lambda c: (len(c), col[c[0]]))
        reps = []
        for x in cmin:
            tw = False
            for y in reps:
                if all(act_tr(m, x, y) == m for m in masks): tw = True; break
            if not tw: reps.append(x)
        for x in reps:
            c2 = [2 * c for c in col]
            c2[x] = 2 * col[x] - 1 if col[x] > 0 else -1
            keys = sorted(set(c2)); c2 = [keys.index(c) for c in c2]
            rec(c2)
    rec([0] * n)
    return best[0], best[1]
