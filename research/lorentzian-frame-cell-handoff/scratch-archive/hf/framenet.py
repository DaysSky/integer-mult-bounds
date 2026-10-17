"""Level-synchronous frame network + masked ALS.

A design is a list of registers, each with a type ('X','Y','H'), an optional port, and a
chain: list of (dim, frame_basis) with strictly increasing dims and nested frames.
At each dim d, registers whose chain has a frame of dim d are grouped by that frame;
each group applies a free linear map (non-target rows may not read target columns).
Drop-free values: X_s starts as e_s (at its first frame), everything else 0.
Goal: final values of Y_t equal N[t] (row over sources).

Level-synchronous ordering is WLOG: two gates sharing a register are ordered by the dims
of their frames because frames are monotone per register.
"""
import numpy as np
from geo import basis, contained


class FrameNet:
    def __init__(self, regs, target, nsrc):
        self.regs = regs
        self.n = len(regs)
        self.N = np.asarray(target, dtype=float)
        self.nsrc = nsrc
        self.is_t = np.array([r['type'] == 'Y' for r in regs])
        for i, r in enumerate(regs):
            ch = r['chain']
            for (d0, f0), (d1, f1) in zip(ch, ch[1:]):
                assert d1 > d0 and contained(f0, f1), ('chain not monotone', i, ch)
            for d, f in ch:
                assert len(basis(f)) == d, ('dim mismatch', i, d, f)
        self.stages = []
        for d in range(0, 10):
            groups = {}
            if d == 0:
                self.stages.append([]); continue
            for i, r in enumerate(regs):
                for dd, f in r['chain']:
                    if dd == d:
                        groups.setdefault(tuple(basis(f)), []).append(i)
            gl = [(f, g) for f, g in groups.items() if len(g) >= 2]
            self.stages.append(gl)
        # parameter blocks
        self.M = []
        self.masks = []
        for gl in self.stages:
            ms, mk = [], []
            for f, g in gl:
                k = len(g)
                mask = np.ones((k, k), bool)
                for a, i in enumerate(g):
                    if not self.is_t[i]:
                        for b, j in enumerate(g):
                            if self.is_t[j] and a != b:
                                mask[a, b] = False
                ms.append(np.eye(k))
                mk.append(mask)
            self.M.append(ms)
            self.masks.append(mk)
        self.src_reg = {r['port']: i for i, r in enumerate(regs) if r['type'] == 'X'}
        self.tgt_reg = {r['port']: i for i, r in enumerate(regs) if r['type'] == 'Y'}
        self.tgt_idx = np.array([self.tgt_reg[t] for t in range(self.N.shape[0])])

    def init_values(self):
        V = np.zeros((self.n, self.nsrc))
        for s, i in self.src_reg.items():
            V[i, s] = 1.0
        return V

    def apply_stage(self, k, V):
        for (f, g), M in zip(self.stages[k], self.M[k]):
            V[g] = M @ V[g]
        return V

    def forward(self, upto=10):
        V = self.init_values()
        hist = [V.copy()]
        for k in range(upto):
            V = self.apply_stage(k, V)
            hist.append(V.copy())
        return hist

    def backward(self):
        """L[k] : (ntgt x n) map from values after stage k-1 (before stage k) ... we store
        after-stage maps: Lafter[k] maps values after stage k to final target outputs."""
        L = np.zeros((len(self.tgt_idx), self.n))
        L[np.arange(len(self.tgt_idx)), self.tgt_idx] = 1.0
        Lafter = [None] * 10
        for k in range(9, -1, -1):
            Lafter[k] = L.copy()
            # L_before = L_after @ blockdiag(M_k)
            Lb = L.copy()
            for (f, g), M in zip(self.stages[k], self.M[k]):
                Lb[:, g] = L[:, g] @ M
            L = Lb
        return Lafter

    def residual(self):
        V = self.forward()[-1]
        return np.linalg.norm(V[self.tgt_idx] - self.N)

    def als_stage(self, k, hist, Lafter, lam=1e-6, cg_iters=200):
        """Matrix-free CG on the masked block-diagonal unknown X of stage k."""
        R = hist[k]                      # n x nsrc, values before stage k
        L = Lafter[k]                    # ntgt x n, after stage k -> outputs
        gl = self.stages[k]
        if not gl:
            return
        ing = np.zeros(self.n, bool)
        for f, g in gl:
            ing[g] = True
        # pass-through part (registers not in any group keep their value)
        T = self.N - L[:, ~ing] @ R[~ing]
        GL = L.T @ L                     # n x n
        GR = R @ R.T                     # n x n
        RHS = L.T @ T @ R.T              # n x n
        blocks = [(np.array(g), mask) for (f, g), mask in zip(gl, self.masks[k])]
        def pack(Xfull):
            return [Xfull[np.ix_(g, g)] * mask for g, mask in blocks]
        def unpack(bl):
            X = np.zeros((self.n, self.n))
            for (g, mask), B in zip(blocks, bl):
                X[np.ix_(g, g)] = B
            return X
        x0 = [M.copy() for M in self.M[k]]
        def H(bl):
            X = unpack(bl)
            Y = pack(GL @ X @ GR)
            return [y + lam * b for y, b in zip(Y, bl)]
        b = [r + lam * x for r, x in zip(pack(RHS), x0)]
        x = [m.copy() for m in x0]
        Hx = H(x)
        r = [bi - hi for bi, hi in zip(b, Hx)]
        p = [ri.copy() for ri in r]
        rs = sum((ri * ri).sum() for ri in r)
        for it in range(cg_iters):
            Hp = H(p)
            alpha = rs / max(sum((pi * hi).sum() for pi, hi in zip(p, Hp)), 1e-300)
            x = [xi + alpha * pi for xi, pi in zip(x, p)]
            r = [ri - alpha * hi for ri, hi in zip(r, Hp)]
            rs2 = sum((ri * ri).sum() for ri in r)
            if rs2 < 1e-26:
                break
            p = [ri + (rs2 / rs) * pi for ri, pi in zip(r, p)]
            rs = rs2
        self.M[k] = x

    def solve(self, sweeps=50, lam=1e-6, tol=1e-10, verbose=False, seed=0):
        rng = np.random.default_rng(seed)
        for k in range(10):
            for gi, (M, mask) in enumerate(zip(self.M[k], self.masks[k])):
                self.M[k][gi] = (np.eye(len(M)) + 0.3 * rng.standard_normal(M.shape)) * mask
        best = None
        for it in range(sweeps):
            for k in list(range(10)) + list(range(8, -1, -1)):
                if not self.stages[k]:
                    continue
                hist = self.forward(upto=k)
                Lafter = self.backward()
                self.als_stage(k, hist, Lafter, lam)
            r = self.residual()
            if verbose:
                print('sweep', it, 'residual', r, flush=True)
            best = r if best is None else min(best, r)
            if r < tol:
                break
        return self.residual()

    def min_abs_det(self):
        m = np.inf
        for ms in self.M:
            for M in ms:
                s = np.linalg.svd(M, compute_uv=False)
                m = min(m, s[-1])
        return m
