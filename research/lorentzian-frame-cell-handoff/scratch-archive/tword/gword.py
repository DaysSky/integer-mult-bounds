"""Bit word builder with GENERAL frames (nondegenerate subspaces, canonical RREF tuples).  Registers: x 0..v-1,
y v..2v-1, helpers 2v...  Every climb must be nested (old subset of new, strictly larger) and every frame used must be
nondegenerate.  Content is tracked over columns x | y | helper dirt.  build() emits D, A, scatter, B, C (literal reverse
at FULL of all z-destination gates of A and B), start/final frames, and the local histogram."""
from collections import Counter

class GWord:
    def __init__(self, fam):
        self.f = fam; S = fam.S; v = fam.v; self.v = v; self.S = S
        self.nh = 0; self.cur = {}; self.content = {}; self.path = {}
        for s in range(v):
            self.cur[s] = fam.line_space[s]; self.content[s] = 1 << s; self.path[s] = [fam.line_space[s]]
        for t in range(v):
            self.cur[v + t] = (); self.content[v + t] = 1 << (v + t); self.path[v + t] = [()]
        self.A, self.B = [], []; self.ret = []; self.phase = 'A'; self.role = {}
    def helper(self, role=''):
        r = 2 * self.v + self.nh; self.nh += 1
        self.cur[r] = (); self.content[r] = 1 << r; self.path[r] = [()]; self.role[r] = role
        return r
    def climb(self, r, F):
        a = self.cur[r]
        if a == F: return
        assert self.S.subset(a, F), ('frame not nested', r, self.role.get(r))
        assert len(F) > len(a)
        assert self.S.nondegenerate(F), ('degenerate frame', r)
        self.cur[r] = F; self.path[r].append(F)
    def gate(self, F, dst, srcs):
        v = self.v
        regs = [dst] + list(srcs); assert len(set(regs)) == len(regs)
        if v <= dst < 2 * v: assert self.phase == 'B', 'target written before the scatter'
        for r in srcs: assert not (v <= r < 2 * v), 'target used as a source'
        for r in regs: self.climb(r, F)
        for s in srcs: self.content[dst] ^= self.content[s]
        (self.A if self.phase == 'A' else self.B).append((F, dst, list(srcs)))
    def xpart(self, r): return self.content[r] & ((1 << self.v) - 1)
    def finish(self):
        for r in list(self.cur):
            if self.v <= r < 2 * self.v: self.climb(r, self.f.tperp(r - self.v))
            else: self.climb(r, self.f.FULL)
    def local_histogram(self, copy_ranks):
        H = Counter()
        for r, p in self.path.items():
            for a, b in zip(p, p[1:]): H[len(b) - len(a)] += 1
        for c in copy_ranks: H[c] += 1
        return H
    def build(self, scatter_rows, ret_frames):
        f = self.f; S = self.S; v = self.v; nreg = 2 * v + self.nh
        frames = {}
        def fid(F):
            if F not in frames: frames[F] = len(frames)
            return frames[F]
        fid(()); fid(f.FULL)
        A = [[fid(F), d, list(s)] for F, d, s in self.A]
        B = [[fid(F), d, list(s)] for F, d, s in self.B]
        dv = [0] * nreg
        for r in range(2 * v, nreg): dv[r] = 1 << (r - 2 * v)
        for _, d, srcs in A:
            for s in srcs: dv[d] ^= dv[s]
        cdirt = [dv[q] for q in self.ret]
        for t in range(v):
            for k in scatter_rows[t]: dv[v + t] ^= cdirt[k]
        for _, d, srcs in B:
            for s in srcs: dv[d] ^= dv[s]
        D = []
        for t in range(v):
            m = dv[v + t]; srcs = []
            while m:
                b = m & -m; srcs.append(2 * v + b.bit_length() - 1); m ^= b
            if srcs: D.append([fid(()), v + t, srcs])
        Cl = [[fid(f.FULL), d, srcs] for _, d, srcs in reversed(A + B) if d < v or d >= 2 * v]
        for F in ret_frames: fid(F)
        fr = [None] * len(frames)
        for F, i in frames.items(): fr[i] = S.to_int_rows(F)
        start = [fid(f.line_space[s]) for s in range(v)] + [fid(())] * (v + self.nh)
        final = [fid(f.FULL)] * v + [fid(f.tperp(t)) for t in range(v)] + [fid(f.FULL)] * self.nh
        return dict(format='bitGen/1+mut', family='T_h', h=f.h, v=v, R=self.nh,
                    lines=[list(x) for x in f.vec], form={'num': [[(9 if i == j else 0) - 1 for j in range(f.h)] for i in range(f.h)], 'den': 9},
                    frames=fr, start=start, final=final, ret=list(self.ret), ret_frames=[fid(F) for F in ret_frames],
                    scatter=[list(r) for r in scatter_rows], D=D, A=A, B=B, C=Cl)
