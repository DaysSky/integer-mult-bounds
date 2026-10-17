"""Score a decoder code for a line system.  C = span of pieces (line subsets); cost = sum of piece costs (frame rank
of each piece: rank of its span, +1 if that span is degenerate).  For each target t the lightest valid row is the
lightest codeword r with t in r and r inside N[t] = {t} u R(t).  Returns (cost, feasible, load = sum (|r_t| - 1)).
Generic: lines given by a Gram matrix G (numpy, exact small ints)."""
import numpy as np, itertools
class System:
    def __init__(self, G, L=None):
        self.G = np.array(G); self.v = len(G)
        self.N = [(1 << t) | sum(1 << s for s in range(self.v) if s != t and self.G[t, s] == 0) for t in range(self.v)]
        self.L = L
    def rows(self, basis, wmax=None):
        """lightest valid row weight per target over all codewords of span(basis) (basis must be independent)."""
        v = self.v; best = [None] * v; k = len(basis)
        N = self.N
        c = 0
        for i in range(1, 1 << k):
            c ^= basis[(i & -i).bit_length() - 1]             # Gray code walk
            w = c.bit_count()
            if wmax is not None and w > wmax: continue
            # valid targets: t in c with c subset N[t]  <=>  t in c and t in N[s] for all s in c
            T = c; x = c
            while x and T:
                b = x & -x; s = b.bit_length() - 1; x ^= b
                T &= N[s]
            while T:
                b = T & -T; t = b.bit_length() - 1; T ^= b
                if best[t] is None or w < best[t]: best[t] = w
        return best
def independent(vecs):
    piv = {}; out = []
    for x0 in vecs:
        x = x0
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; out.append(x0); break
    return out
