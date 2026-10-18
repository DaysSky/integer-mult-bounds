"""I_{13,1} base: good 4-frames, parity census, group actions.  Mirrors lcell/lbase.py but parametric in n
(Geom(n), n = 13: v = 78 P + 286 T = 364 lines, h = 13)."""
import sys, os, pickle, itertools, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N = int(os.environ.get('N13', '13'))

class G13:
    def __init__(self, n):
        self.n = n
        L, self.kind, self.supp = [], [], []
        for a, b in itertools.combinations(range(n), 2):
            v = [0] * (n + 1); v[a] = 1; v[b] = -1
            L.append(v); self.kind.append('P'); self.supp.append((a, b))
        for T in itertools.combinations(range(n), 3):
            v = [0] * (n + 1)
            for i in T: v[i] = 1
            v[n] = 1
            L.append(v); self.kind.append('T'); self.supp.append(T)
        self.L = np.array(L, dtype=np.int64)
        self.LA = self.L.astype(float)
        self.V = len(L)
        eta = np.eye(n + 1, dtype=np.int64); eta[n, n] = -1
        self.G = self.L @ eta @ self.L.T
        self.HYP = []
        for t in range(self.V):
            m = 0
            for s in np.nonzero(self.G[t] == 0)[0]: m |= 1 << int(s)
            self.HYP.append(m)
        self.h = int(np.linalg.matrix_rank(self.LA))
        self.idx = {(k, s): i for i, (k, s) in enumerate(zip(self.kind, self.supp))}
    @staticmethod
    def bits(mask):
        out = []
        while mask:
            b = mask & -mask; out.append(b.bit_length() - 1); mask ^= b
        return out
    def P(self, a, b):
        a, b = min(a, b), max(a, b); return self.idx[('P', (a, b))]
    def T(self, *abc):
        return self.idx[('T', tuple(sorted(abc)))]

g = G13(N)
V = g.V
QR13 = [a for a in range(1, N) if pow(a, (N - 1) // 2, N) == 1]  # quadratic residues mod 13: 1,3,4,9,10,12
GROUP = [(a, b) for a in QR13 for b in range(N)]  # affine group x -> a x + b, order 6*13 = 78

def line_img(s, a, b):
    k, sp = g.kind[s], g.supp[s]
    img = tuple(sorted((a * i + b) % N for i in sp))
    return g.idx[(k, img)]

PERMS = [[line_img(s, a, b) for s in range(V)] for (a, b) in GROUP]

def act(mask, p):
    m = 0
    for s in g.bits(mask): m |= 1 << p[s]
    return m

def orbit_mask(mask): return sorted(set(act(mask, p) for p in PERMS))
def canon_mask(mask): return min(act(mask, p) for p in PERMS)

_ND = {}
def nondeg_span(mask):
    """True iff span of the lines in mask is a nondegenerate subspace."""
    if mask in _ND: return _ND[mask]
    B = []
    for i in g.bits(mask):
        if np.linalg.matrix_rank(g.LA[B + [i]]) > len(B): B.append(i)
    Gm = np.array([[g.G[a, b] for b in B] for a in B], dtype=float)
    r = abs(round(np.linalg.det(Gm))) > 0 if B else True
    _ND[mask] = r; return r

def goodframes():
    """4-tuples of pairwise orthogonal lines with sum in 2L (the I11,1 good-frame definition)."""
    fr = []
    for a in range(V):
        for b in range(a + 1, V):
            if g.G[a, b] != 0: continue
            for c in range(b + 1, V):
                if g.G[a, c] or g.G[b, c]: continue
                for d in range(c + 1, V):
                    if g.G[a, d] or g.G[b, d] or g.G[c, d]: continue
                    s = g.L[[a, b, c, d]].sum(axis=0)
                    if all(x % 2 == 0 for x in s): fr.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    return sorted(fr)

if __name__ == '__main__':
    print('n', N, 'v', V, 'P', sum(1 for k in g.kind if k == 'P'), 'T', sum(1 for k in g.kind if k == 'T'), 'h', g.h)
    p13 = os.path.join(HERE, 'goodframes13.pkl')
    if os.path.exists(p13):
        fr = pickle.load(open(p13, 'rb'))
    else:
        fr = goodframes(); pickle.dump(fr, open(p13, 'wb'))
    print('good 4-frames', len(fr))
    # type census by P-count
    cnt = collections.Counter()
    for F in fr:
        cnt[sum(1 for s in g.bits(F) if g.kind[s] == 'P')] += 1
    print('P-count census', dict(sorted(cnt.items())))
    # nondegeneracy
    nd = sum(1 for F in fr if not nondeg_span(F))
    print('degenerate frames', nd, 'of', len(fr))
    # per-line frame counts
    per = collections.Counter()
    for F in fr:
        for s in g.bits(F): per[s] += 1
    by_kind = collections.defaultdict(collections.Counter)
    for s, c in per.items(): by_kind[g.kind[s]][c] += 1
    print('frames per line by kind', {k: dict(sorted(v.items())) for k, v in by_kind.items()})
    # parity obstructions that killed I11,1
    nP = sum(1 for k in g.kind if k == 'P')
    print('P lines', nP, '-> P-P perfect matching', 'possible (even)' if nP % 2 == 0 else 'IMPOSSIBLE (odd)')
    # T-T degree sum: sum over T lines of (#T mates) if every T in a PPTT-type frame needs a T mate etc.
    # I11 argument: with all P in PPTT frames, P-T edges force 55 T into PPTT and 110 into TTTT; degree sum odd.
    # For n=13 recount: count T-T orthogonal pairs and P-T orthogonal pairs.
    TT = sum(1 for s in range(V) for t in range(s + 1, V) if g.kind[s] == 'T' and g.kind[t] == 'T' and g.G[s, t] == 0)
    PT = sum(1 for s in range(V) for t in range(s + 1, V) if g.kind[s] != g.kind[t] and g.G[s, t] == 0)
    PP = sum(1 for s in range(V) for t in range(s + 1, V) if g.kind[s] == 'P' and g.kind[t] == 'P' and g.G[s, t] == 0)
    print('orthogonal pairs: PP', PP, 'PT', PT, 'TT', TT)
    # in good frames: PPTT holds 2 P + 2 T (PT edges 2, TT edge 1); TTTT holds 0 P (TT edges 6)
    # if a frames split x PPTT + y TTTT: 2x = nP -> x = nP/2 (needs nP even), TT degrees: x*1 + y*6 even?
    print('PPTT frames needed', nP / 2)
