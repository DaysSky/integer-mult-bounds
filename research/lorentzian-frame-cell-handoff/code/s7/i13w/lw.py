"""I_{n,1} bit-word builder (n = env LWN, default 11; copy of lmid/lw.py) with closed line-mask frames (every frame used must be NONDEGENERATE), emitting the
bitGen/1+mut format read by the independent checker tword/gcheck.py.  Registers: x 0..v-1, y v..2v-1, helpers 2v...
Coordinates: integer basis B = (P(0,1), ..., P(9,10), T(0,1,2)) of the line lattice; form = Gram of B (h = 11)."""
import sys, os, json, gzip
from collections import Counter
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lword'))
from geom import Geom

N = int(os.environ.get('LWN', '11'))
g = Geom(N)
V = g.V
BASIS = [g.P(i, i + 1) for i in range(N - 1)] + [g.T(0, 1, 2)]
_Bm = g.L[BASIS].astype(float)
COORD = []
for s in range(V):
    c, *_ = np.linalg.lstsq(_Bm.T, g.L[s].astype(float), rcond=None)
    ci = np.rint(c).astype(int)
    assert (ci @ g.L[BASIS] == g.L[s]).all(), 'non-integral coordinates'
    COORD.append([int(x) for x in ci])
GRAM = (g.L[BASIS] @ g.eta @ g.L[BASIS].T).astype(int).tolist()
H = N
FULL = g.FULL

def bits(m):
    out = []
    while m:
        b = m & -m; out.append(b.bit_length() - 1); m ^= b
    return out

def closure(m): return g.closure(m)[0] if m else 0
def dim(m): return g.closure(m)[1] if m else 0

def _idet(M):
    """exact integer determinant (Bareiss)"""
    M = [row[:] for row in M]; n = len(M); sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None: return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]
_ND = {}
_BL = {}
def basis_lines(m):
    r = _BL.get(m)
    if r is not None: return r
    out = []; Q = []
    for s in bits(m):
        v0 = g.LA[s].copy()
        for q in Q: v0 = v0 - (v0 @ q) * q
        nv = np.linalg.norm(v0)
        if nv > 1e-7: Q.append(v0 / nv); out.append(s)
    _BL[m] = out
    return out
def nondegenerate(m):
    if m == 0: return True
    r = _ND.get(m)
    if r is None:
        bl = basis_lines(m)
        Gm = [[int(g.G[a, b]) for b in bl] for a in bl]
        r = _idet(Gm) != 0; _ND[m] = r
    return r

class LWord:
    def __init__(self):
        self.nh = 0; self.cur = {}; self.content = {}; self.path = {}
        for s in range(V):
            self.cur[s] = 1 << s; self.content[s] = 1 << s; self.path[s] = [1 << s]
        for t in range(V):
            self.cur[V + t] = 0; self.content[V + t] = 1 << (V + t); self.path[V + t] = [0]
        self.A, self.B = [], []; self.ret = []; self.phase = 'A'; self.role = {}
    def helper(self, role=''):
        r = 2 * V + self.nh; self.nh += 1
        self.cur[r] = 0; self.content[r] = 1 << r; self.path[r] = [0]; self.role[r] = role
        return r
    def climb(self, r, F):
        a = self.cur[r]
        if a == F: return
        assert a & ~F == 0, ('frame not nested', r, self.role.get(r))
        assert dim(F) > dim(a), ('no rank increase', r)
        assert nondegenerate(F), ('degenerate frame', r)
        self.cur[r] = F; self.path[r].append(F)
    def gate(self, F, dst, srcs):
        regs = [dst] + list(srcs); assert len(set(regs)) == len(regs)
        if V <= dst < 2 * V: assert self.phase == 'B'
        for r in srcs: assert not (V <= r < 2 * V)
        for r in regs: self.climb(r, F)
        for s in srcs: self.content[dst] ^= self.content[s]
        xs = self.content[dst] & ((1 << V) - 1)
        if not (V <= dst < 2 * V): assert xs & ~F == 0, 'content outside frame'
        (self.A if self.phase == 'A' else self.B).append((F, dst, list(srcs)))
    def xpart(self, r): return self.content[r] & ((1 << V) - 1)
    def finish(self):
        for r in list(self.cur):
            if V <= r < 2 * V: self.climb(r, g.HYP[r - V])
            else: self.climb(r, FULL)
    def histogram(self, copy_ranks):
        Hh = Counter()
        for r, p in self.path.items():
            ds = [dim(F) for F in p]
            for a, b in zip(ds, ds[1:]): Hh[b - a] += 1
        for c in copy_ranks: Hh[c] += 1
        return Hh
    def emit(self, scatter_rows, ret_frames, path):
        nreg = 2 * V + self.nh
        frames = {}
        def fid(F):
            if F not in frames: frames[F] = len(frames)
            return frames[F]
        fid(0); fid(FULL)
        A = [[fid(F), d, list(s)] for F, d, s in self.A]
        B = [[fid(F), d, list(s)] for F, d, s in self.B]
        dv = [0] * nreg
        for r in range(2 * V, nreg): dv[r] = 1 << (r - 2 * V)
        for _, d, srcs in A:
            for s in srcs: dv[d] ^= dv[s]
        cdirt = [dv[q] for q in self.ret]
        for t in range(V):
            for k in scatter_rows[t]: dv[V + t] ^= cdirt[k]
        for _, d, srcs in B:
            for s in srcs: dv[d] ^= dv[s]
        D = []
        for t in range(V):
            m = dv[V + t]; srcs = []
            while m:
                b = m & -m; srcs.append(2 * V + b.bit_length() - 1); m ^= b
            if srcs: D.append([fid(0), V + t, srcs])
        Cl = [[fid(FULL), d, srcs] for _, d, srcs in reversed(A + B) if d < V or d >= 2 * V]
        for F in ret_frames: fid(F)
        for r in range(V): fid(1 << r)
        for t in range(V): fid(g.HYP[t])
        fr = [None] * len(frames)
        for F, i in frames.items():
            fr[i] = [COORD[s] for s in basis_lines(F)]
        start = [fid(1 << s) for s in range(V)] + [fid(0)] * (V + self.nh)
        final = [fid(FULL)] * V + [fid(g.HYP[t]) for t in range(V)] + [fid(FULL)] * self.nh
        w = dict(format='bitGen/1+mut', family='I_{%d,1} frame-cell' % N, h=H, v=V, R=self.nh,
                 lines=COORD, form={'num': GRAM, 'den': 1}, frames=fr, start=start, final=final,
                 ret=list(self.ret), ret_frames=[fid(F) for F in ret_frames],
                 scatter=[list(r) for r in scatter_rows], D=D, A=A, B=B, C=Cl)
        with gzip.open(path, 'wt') as fh: json.dump(w, fh)
        return w

def frame_alg(w, F, inputs, outputs, tagname=''):
    """At frame F: registers `inputs` (all with x-content inside F) are combined so that for each required output
    vector (x-bitmask) some register holds it exactly; returns ({output index: register}, dead registers).
    Uses fresh helpers (empties) only for outputs dependent on already-assigned ones."""
    regs = list(inputs)
    piv = {}            # pivot bit -> register (current reduced basis carriers)
    zeros = []
    for r in regs:
        x = w.xpart(r); srcs = []
        while x:
            hb = x.bit_length() - 1
            if hb in piv: srcs.append(piv[hb]); x ^= w.xpart(piv[hb])
            else: break
        if srcs: w.gate(F, r, srcs)
        x = w.xpart(r)
        if x: piv[x.bit_length() - 1] = r
        else: zeros.append(r)
    # basis carriers: register -> vector; keep a row-reduced representation for solving
    carriers = list(piv.values())
    assigned = {}
    free_basis = set(carriers)
    def solve(o):
        """express o as XOR of current carrier vectors (carriers independent); returns list of carriers"""
        # Gaussian elimination on the fly
        rows = [(w.xpart(c), 1 << i) for i, c in enumerate(carriers)]
        red = {}
        for vec, tag in rows:
            while vec:
                hb = vec.bit_length() - 1
                if hb in red: vec ^= red[hb][0]; tag ^= red[hb][1]
                else: red[hb] = (vec, tag); break
        x = o; tag = 0
        while x:
            hb = x.bit_length() - 1
            assert hb in red, 'output not in span at frame'
            x ^= red[hb][0]; tag ^= red[hb][1]
        return [carriers[i] for i in range(len(carriers)) if tag >> i & 1]
    res = {}
    order = sorted(range(len(outputs)), key=lambda k: 0)
    for k in order:
        o = outputs[k]
        K = solve(o)
        free = [c for c in K if c in free_basis]
        if free:
            c = free[0]
            others = [d for d in K if d != c]
            if others: w.gate(F, c, others)
            free_basis.discard(c); res[k] = c
        else:
            z = zeros.pop() if zeros else w.helper('empty@' + tagname)
            w.gate(F, z, K)
            res[k] = z
    dead = list(free_basis) + zeros
    return res, dead
