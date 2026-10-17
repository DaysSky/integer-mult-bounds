"""Word builder with z-groups (helpers starting at span(z_g), cancelled by group-D reads of targets at span(z_g)
at the start of phase B).  Emits bitGen/1+mut JSON for gcheck_z.py.  Registers: x 0..v-1, y v..2v-1, helpers 2v.."""
import json, gzip, math
from fractions import Fraction as Fr
from collections import Counter

class ZWord:
    def __init__(self, S, zvecs=(), name='zword'):
        self.S = S; v = S.v; self.v = v; self.name = name
        self.Z = [S.span(z) for z in zvecs]                # group entrance frames
        for Zg in self.Z: assert S.nondeg(Zg)
        self.HYP = [S.line_perp(t) for t in range(v)]
        self.cur, self.content, self.path, self.start, self.group, self.role = {}, {}, {}, {}, {}, {}
        for s in range(v):
            F = S.span(s); self.cur[s] = F; self.content[s] = 1 << s; self.path[s] = [F]; self.start[s] = F
        for t in range(v):
            r = v + t; self.cur[r] = (); self.content[r] = 0; self.path[r] = [()]; self.start[r] = ()
        self.nh = 0; self.A, self.B = [], []; self.ret, self.ret_frames = [], []; self.phase = 'A'
        self.tgroup = {}                                    # target -> group index (if it uses group helpers)
        self.groupD_done = False
    def helper(self, role='', group=None):
        r = 2 * self.v + self.nh; self.nh += 1
        F = () if group is None else self.Z[group]
        self.cur[r] = F; self.content[r] = 0; self.path[r] = [F]; self.start[r] = F
        self.group[r] = group; self.role[r] = role
        return r
    def is_target(self, r): return self.v <= r < 2 * self.v
    def climb(self, r, F):
        a = self.cur[r]
        if a == F: return
        S = self.S
        assert S.sub(a, F), ('climb not nested', r, self.role.get(r))
        assert len(F) > len(a), ('no rank increase', r)
        assert S.nondeg(F), ('degenerate frame', r, self.role.get(r))
        if self.is_target(r): assert S.sub(F, self.HYP[r - self.v]), ('target frame not in t-perp', r - self.v)
        self.cur[r] = F; self.path[r].append(F)
    def gate(self, F, dst, srcs):
        regs = [dst] + list(srcs); assert len(set(regs)) == len(regs)
        S = self.S
        if self.is_target(dst): assert self.phase == 'B'
        for r in srcs: assert not self.is_target(r), 'H1: z-gate/target reads a target'
        for r in regs:
            g = self.group.get(r)
            if g is not None: assert self.phase == 'B' and self.groupD_done, 'group helper touched before group-D'
        for r in regs: self.climb(r, F)
        lm = S.linemask(F)
        for s in srcs:
            if self.is_target(dst): assert self.content[s] & ~lm == 0, 'target reads content outside frame'
            self.content[dst] ^= self.content[s]
        if not self.is_target(dst): assert self.content[dst] & ~lm == 0, 'content outside frame'
        (self.A if self.phase == 'A' else self.B).append((F, dst, list(srcs)))
    def retain(self, r):
        assert self.phase == 'A' and not self.is_target(r)
        self.ret.append(r); self.ret_frames.append(self.cur[r])
    def begin_B(self, scatter_rows):
        self.phase = 'B'; self.scatter = scatter_rows
        for t in range(self.v):
            for k in scatter_rows[t]: self.content[self.v + t] ^= self.content[self.ret[k]]
        # group-D placeholders: targets in groups climb to span(z_g) now (the reads are inserted at emit)
        self.groupD_index = len(self.B)
        self.groupD_done = True
    def set_target_group(self, t, g):
        """target t passes span(z_g) right after the scatter (must be called before any other B gate on t)"""
        S = self.S; assert S.sub(self.Z[g], self.HYP[t])
        assert self.cur[self.v + t] == (), 'target already moved'
        self.tgroup[t] = g; self.climb(self.v + t, self.Z[g])
    def finish(self):
        for r in list(self.cur):
            if self.is_target(r): self.climb(r, self.HYP[r - self.v])
            else: self.climb(r, self.S.FULL)
        for t in range(self.v):
            assert self.content[self.v + t] == 1 << t, ('target value wrong', t, bin(self.content[self.v + t] ^ (1 << t)).count('1'))
        for r in range(self.v): assert self.content[r] == 1 << r
    # ---------------- pricing data ----------------
    def histogram(self):
        H = Counter()
        for r, p in self.path.items():
            ds = [len(F) for F in p]
            for a, b in zip(ds, ds[1:]): H[b - a] += 1
        for F in self.ret_frames: H[len(F)] += 1
        return H
    def widths(self):
        h = self.S.h
        return [h - len(self.start[r]) for r in range(2 * self.v, 2 * self.v + self.nh)]
    def cst(self): return sum(len(F) for F in self.ret_frames)
    # ---------------- emission ----------------
    def emit(self, path):
        S = self.S; v = self.v; nreg = 2 * v + self.nh
        frames = {}
        def fid(F):
            if F not in frames: frames[F] = len(frames)
            return frames[F]
        fid(()); fid(S.FULL)
        # dirt propagation (helper dirt as bitmask over helpers)
        dv = [0] * nreg
        for r in range(2 * v, nreg): dv[r] = 1 << (r - 2 * v)
        for _, d, srcs in self.A:
            for s in srcs: dv[d] ^= dv[s]
        cd = [dv[q] for q in self.ret]
        for t in range(v):
            for k in self.scatter[t]: dv[v + t] ^= cd[k]
        for _, d, srcs in self.B:
            for s in srcs: dv[d] ^= dv[s]
        f0 = 0; gmask = {}
        for r in range(2 * v, nreg):
            g = self.group[r]
            if g is None: f0 |= 1 << (r - 2 * v)
            else: gmask[g] = gmask.get(g, 0) | 1 << (r - 2 * v)
        D, GD = [], []
        def regs_of(m):
            out = []
            while m:
                b = m & -m; out.append(2 * v + b.bit_length() - 1); m ^= b
            return out
        for t in range(v):
            m = dv[v + t]
            if m & f0: D.append([fid(()), v + t, regs_of(m & f0)])
            rest = m & ~f0
            if rest:
                g = self.tgroup.get(t)
                assert g is not None and rest & ~gmask[g] == 0, ('group dirt leak', t)
                GD.append([self.Z[g], v + t, regs_of(rest)])
        # group-D gates: inserted at the start of B; target already climbed to span(z_g) at set_target_group
        Bl = [[fid(F), d, list(s)] for F, d, s in GD] + [[fid(F), d, list(s)] for F, d, s in self.B]
        A = [[fid(F), d, list(s)] for F, d, s in self.A]
        Cl = [[fid(S.FULL), d, s] for _, d, s in reversed(A + Bl) if not (v <= d < 2 * v)]
        for F in self.ret_frames: fid(F)
        for r in range(nreg): fid(self.start[r])
        for t in range(v): fid(self.HYP[t])
        fr = [None] * len(frames)
        for F, i in frames.items():
            rows = []
            for row in F:
                den = 1
                for x in row: den = den * x.denominator // math.gcd(den, x.denominator)
                rows.append([int(x * den) for x in row])
            fr[i] = rows
        start = [fid(self.start[r]) for r in range(nreg)]
        final = [fid(S.FULL)] * v + [fid(self.HYP[t]) for t in range(v)] + [fid(S.FULL)] * self.nh
        lines = []
        for l in S.lines:
            assert all(x.denominator == 1 for x in l); lines.append([int(x) for x in l])
        w = dict(format='bitGen/1+mut', family=self.name, h=S.h, v=v, R=self.nh, lines=lines,
                 form={'num': [[int(x) for x in row] for row in S.GRAM], 'den': 1}, frames=fr, start=start, final=final,
                 ret=list(self.ret), ret_frames=[fid(F) for F in self.ret_frames],
                 scatter=[list(r) for r in self.scatter], D=D, A=A, B=Bl, C=Cl)
        op = gzip.open if path.endswith('.gz') else open
        with op(path, 'wt') as fh: json.dump(w, fh)
        return w
