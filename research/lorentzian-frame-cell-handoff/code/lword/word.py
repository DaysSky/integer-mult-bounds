"""Generic bit-word builder for a line system (geom.Geom): registers x 0..v-1, y v..2v-1, helpers 2v...
Frames are closed line masks; climbs must be nested; gates act at a common frame (closure of the given mask).
Content is tracked over columns x | y | helper dirt.  build() emits D (frame-0 dirt compensation), A, scatter, B,
C (literal reverse at FULL of every z-destination gate) and final frames, as in the hub's bitE8/1 + mut format, and
the local paid histogram (each climb = one child of rank delta-dim; each scatter COPY = one child of the total's rank)."""
from collections import Counter

class Word:
    def __init__(self, g):
        self.g = g; V = g.V; self.V = V
        self.nh = 0; self.cur = {}; self.content = {}; self.path = {}
        for s in range(V):
            self.cur[s] = 1 << s; self.content[s] = 1 << s; self.path[s] = [1 << s]
        for t in range(V):
            self.cur[V + t] = 0; self.content[V + t] = 1 << (V + t); self.path[V + t] = [0]
        self.A, self.B = [], []; self.ret = []; self.phase = 'A'; self.role = {}
    def helper(self, role=''):
        r = 2 * self.V + self.nh; self.nh += 1
        self.cur[r] = 0; self.content[r] = 1 << r; self.role[r] = role; self.path[r] = [0]
        return r
    def climb(self, r, F):
        F = self.g.closure(F)[0] if F else 0
        a = self.cur[r]
        if a == F: return
        assert (a & ~F) == 0, ('frame not nested', r)
        self.cur[r] = F; self.path[r].append(F)
    def gate(self, F, dst, srcs):
        V = self.V
        F = self.g.closure(F)[0]
        regs = [dst] + list(srcs)
        assert len(set(regs)) == len(regs)
        if V <= dst < 2 * V: assert self.phase == 'B', 'target written before the scatter'
        for r in regs:
            if V <= r < 2 * V and r != dst: raise AssertionError('target used as a source')
            self.climb(r, F)
        for s in srcs: self.content[dst] ^= self.content[s]
        (self.A if self.phase == 'A' else self.B).append((F, dst, list(srcs)))
    def xpart(self, r): return self.content[r] & ((1 << self.V) - 1)
    def finish_frames(self):
        """final climbs: z registers to FULL, targets to t-perp"""
        g = self.g; V = self.V
        for r in list(self.cur):
            if V <= r < 2 * V: self.climb(r, g.HYP[r - V])
            else: self.climb(r, g.FULL)
    def local_histogram(self, copy_ranks):
        g = self.g; H = Counter()
        for r, p in self.path.items():
            dims = [g.dim(F) for F in p]
            for a, b in zip(dims, dims[1:]):
                assert b > a; H[b - a] += 1
        for c in copy_ranks: H[c] += 1
        return H
    def build(self, scatter_rows):
        """scatter_rows[t] = list of indices into self.ret.  Returns dict with D, A, B, C, frames, start, final."""
        g = self.g; V = self.V; nreg = 2 * V + self.nh
        frames = {}
        def fid(mask):
            if mask not in frames: frames[mask] = len(frames)
            return frames[mask]
        fid(0); fid(g.FULL)
        A = [[fid(F), d, list(s)] for F, d, s in self.A]
        B = [[fid(F), d, list(s)] for F, d, s in self.B]
        dv = [0] * nreg
        for r in range(2 * V, nreg): dv[r] = 1 << (r - 2 * V)
        for f, d, srcs in A:
            for s in srcs: dv[d] ^= dv[s]
        cdirt = [dv[q] for q in self.ret]
        for t in range(V):
            for k in scatter_rows[t]: dv[V + t] ^= cdirt[k]
        for f, d, srcs in B:
            for s in srcs: dv[d] ^= dv[s]
        D = []
        for t in range(V):
            m = dv[V + t]; srcs = []
            while m:
                b = m & -m; srcs.append(2 * V + b.bit_length() - 1); m ^= b
            if srcs: D.append([fid(0), V + t, srcs])
        Cl = [[fid(g.FULL), d, srcs] for f, d, srcs in reversed(A + B) if d < V or d >= 2 * V]
        fr = [None] * len(frames)
        for mk, i in frames.items(): fr[i] = g.bits(mk)
        start = [fid(1 << s) for s in range(V)] + [fid(0)] * (V + self.nh)
        final = [fid(g.FULL)] * V + [fid(g.HYP[t]) for t in range(V)] + [fid(g.FULL)] * self.nh
        return dict(format='bitLor/1+mut', n=g.n, h=g.h, v=V, R=self.nh, lines=[list(map(int, r)) for r in g.L],
                    eta=[list(map(int, r)) for r in g.eta], frames=fr, start=start, final=final, ret=list(self.ret),
                    scatter=[list(r) for r in scatter_rows], D=D, A=A, B=B, C=Cl)
