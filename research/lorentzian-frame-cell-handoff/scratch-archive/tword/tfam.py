"""Triple family T_h: lines t_T (T in C([h],3)), form B = I - J/9 on Q^h (Lorentzian for h >= 10)."""
import itertools
from fractions import Fraction as Fr
from space import Space

class TFam:
    def __init__(self, h):
        self.h = h
        self.trip = list(itertools.combinations(range(h), 3))
        self.idx = {T: i for i, T in enumerate(self.trip)}
        self.v = len(self.trip)
        self.vec = [[1 if k in T else 0 for k in range(h)] for T in self.trip]
        B = [[Fr(1 if i == j else 0) - Fr(1, 9) for j in range(h)] for i in range(h)]
        self.S = Space(B)
        self.line_space = [self.S.span([self.vec[i]]) for i in range(self.v)]
        self.FULL = self.S.FULL
        self._perp = {}
    def meet(self, i, j): return len(set(self.trip[i]) & set(self.trip[j]))
    def reader(self, t, s): return s != t and self.meet(t, s) == 1      # <t_S, t_T> = |S cap T| - 1 = 0
    def readers(self, t): return [s for s in range(self.v) if self.reader(t, s)]
    def tperp(self, t):
        r = self._perp.get(t)
        if r is None:
            r = self.S.perp(self.line_space[t]); self._perp[t] = r
        return r
    def binlabel(self, s): return sum(1 << k for k in self.trip[s])   # centre decoder: B0 = M M^T mod 2
    def span_lines(self, idxs): return self.S.span([self.vec[i] for i in idxs])
