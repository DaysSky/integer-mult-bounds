"""Exhaustive keeper-plan census for P111's punctured L3 word family (not run by verify.sh; about 15 minutes on 4 cores
for the shipped puncture set, about 15 minutes more for --all).

The helper bill of a P111-family word is 429 + (extra helpers) + (new junk wires), and the extras and junk wires are
block-local: the mini-node of block B (which writes the Q-parts of the pseudo-target totals tau_p, p in comp(B)) and
the phase-B block node of B depend only on
  - the free-keeper line of each of B's six non-dual cells (freeline, 2^6),
  - which of those six keepers becomes the third register of each of the six (z,z) D6s of comp(B) (thirds, 6!),
  - the receivers of the taus of comp(B) (3 choices each),
  - the punctured lines in B and comp(B).
This script enumerates all of them per block and reports the exact minimum of
  gen_p3 accounting (--old): extra carriers (single lines, added by gen_p3's closure loop) + new junk wires;
  gen_p4 accounting (default): max(|E|, junk directions), E a minimum set of extras each of which is a single line or a
      cell sum x_a + x_b of a cell {a, b} of B (both live) such that every tau's write is expressible.
The block evaluator is a separate re-implementation of gen_p3.build's mini-node and block-node accounting (it imports
only the geometry, the plan and derive/ex_part/eligible from gen_p3); `--calibrate` compares it with full gen_p3 builds
on random keeper plans.  --all runs the --old census over every subset of eligible lines of every complementary block
pair and combines the subsets into all affinely independent puncture sets.
usage: python -I census.py [--old] [--all] [--calibrate N]
Prepared by DaysSky with assistance from Claude; Apache-2.0."""
import itertools
import json
import os
import pickle
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
P111 = os.path.join(HERE, "..", "..", "e8-bit-p111")
sys.path.insert(0, os.path.join(HERE, "..", "..", "e8-bit-carrier-skeleton", "code", "skeleton"))
sys.path.insert(0, os.path.join(P111, "code"))
import e8  # noqa: E402
import gen_p3  # noqa: E402
from gen import span_add  # noqa: E402
from geom import Geom  # noqa: E402
from planio import load_plan  # noqa: E402

V = e8.V
bits = e8.bits
G = Geom()
SOL = load_plan(os.path.join(P111, "data", "plan-l3.json"))
DCELL, KL0, HOME, QHOST, ZZ = gen_p3.derive(G, SOL)
DUAL = set(HOME.values())
EXF = {H: gen_p3.ex_part(G, SOL, G.d6quads[H][0], H) ^ gen_p3.ex_part(G, SOL, G.d6quads[H][1], H) for H in G.cells}
NDC = {b: [c for c in G.cells if c not in DUAL and G.cblk[c] == b] for b in range(10)}   # six non-dual cells
ZZB = {b: sorted(H for H in ZZ if G.cblk[H] == b) for b in range(10)}                       # six (z,z) D6s
ELIG = [p for p in range(8, V) if gen_p3.eligible(G, SOL, DCELL, KL0, QHOST, ZZ, p)[0]]   # lines 0..7 stay live
SHIPPED = [10, 15, 51, 53, 56, 66, 72, 89, 111]


def reduce_(r, basis):
    for pb, bv in basis:
        if r >> pb & 1:
            r ^= bv
    return r


def addb(basis, v):
    v = reduce_(v, basis)
    if v:
        basis.append((v.bit_length() - 1, v))
        basis.sort(key=lambda z: -z[0])


class Block:
    """block B under puncture set P: the supplier of the taus of comp(B) and the node of comp(B)'s targets"""

    def __init__(self, B, P):
        self.B, self.P = B, sorted(P)
        self.Pset = Pset = set(P)
        self.live = live = ((1 << V) - 1) & ~sum(1 << q for q in Pset)
        cb = G.comp[B]
        self.Hs, self.cells = ZZB[cb], NDC[B]
        self.taus = [p for p in self.P if G.blk[p] == cb]
        Ex = {H: EXF[H] & live for H in G.cells}
        self.freed = [KL0[DCELL[q]] for q in self.P if G.blk[q] == B and KL0[DCELL[q]] not in Pset]
        self.zzp = {p: sorted(H for H in ZZ if G.phi[H[0]] == G.phi[p]) for p in self.taus}
        self.Np0 = {}
        for p in self.taus:
            Np = (e8.HYP[p] & live) ^ (1 << KL0[DCELL[p]]) ^ Ex[QHOST[p]]
            for H in self.zzp[p]:
                Np ^= Ex[H]
            self.Np0[p] = Np
        self.srcl = [KL0[c] for c in G.cells if c in DUAL and G.cblk[c] == B and KL0[c] not in Pset]
        self.pos = {l: k for k, l in enumerate(self.srcl)}
        self.us = [t for t in bits(live) if G.blk[t] == cb]
        self.base, self.uzz = {}, {}
        for u in self.us:
            acc = e8.HYP[u] & live
            if KL0[DCELL[u]] not in Pset:
                acc ^= 1 << KL0[DCELL[u]]
            zl = []
            for x in G.phi[u]:
                if x != u:
                    H = tuple(sorted((u, x)))
                    acc ^= Ex[H]
                    if H in self.Hs:
                        zl.append(H)
            self.base[u], self.uzz[u] = acc, zl
        self.rcv0 = {H: SOL["rcv"][H] for H in self.Hs}
        self.cellsB = [c for c in G.cells if G.cblk[c] == B and c[0] not in Pset and c[1] not in Pset]

    def setup(self, flb, perm, rs):
        fkc = {}
        for H, c in zip(self.Hs, perm):
            line = c[(flb >> self.cells.index(c)) & 1]
            fkc[H] = 0 if line in self.Pset else 1 << line
        rcv = dict(self.rcv0)
        for p, r in zip(self.taus, rs):
            for i, H in enumerate(self.zzp[p]):
                rcv[H] = p if (r >> i) & 1 else (H[0] if H[1] == p else H[1])
        for p in self.taus:
            if not any(rcv[H] == p for H in self.zzp[p]):
                rcv[self.zzp[p][0]] = p
        return fkc, rcv

    def mininode(self, fkc, rcv, E):
        """gen_p3's mini-node in order: each tau's designated keeper must reach Np from the other wires (other free
        keepers, the extras E, the freed sources).  Returns (missing lines mask, final keeper contents)."""
        cont = dict(fkc)
        others = list(E) + [1 << x for x in self.freed]
        plan = []
        for p in self.taus:
            mine = [H for H in self.zzp[p] if rcv[H] == p]
            Np = self.Np0[p]
            for H in mine[1:]:
                Np ^= cont[H]
            plan.append((mine[0], Np))
        missing = 0
        for des, Np in plan:
            need = Np ^ cont[des]
            basis = []
            for H in self.Hs:
                if H != des:
                    addb(basis, cont[H])
            for o in others:
                addb(basis, o)
            r = reduce_(need, basis)
            if r:
                missing |= r
                continue
            cont[des] ^= need
        return missing, cont

    def junk(self, cont, rcv):
        """dependent rows of the phase-B block node (each needs a junk direction)"""
        rows = []
        for u in self.us:
            acc = self.base[u]
            for H in self.uzz[u]:
                if rcv[H] == u:
                    acc ^= cont[H]
            assert acc & ~(G.blocks[self.B] & self.live) == 0
            rows.append(sum(1 << self.pos[l] for l in bits(acc)))
        bs, nj = [], 0
        for r in rows:
            if not span_add(bs, r):
                nj += 1
                assert span_add(bs, r | (1 << (len(self.srcl) + nj - 1)))
        return nj

    def single(self, fkc, rcv):
        """gen_p3's closure loop: add every missing line as an extra carrier until the mini-node closes"""
        ext = []
        for _ in range(20):
            m, cont = self.mininode(fkc, rcv, [1 << x for x in ext])
            if not m:
                return ext, cont
            ext = sorted(set(ext) | set(bits(m)))
        raise AssertionError("closure loop did not converge")

    def cost_old(self, flb, perm, rs):
        fkc, rcv = self.setup(flb, perm, rs)
        ext, cont = self.single(fkc, rcv)
        nj = self.junk(cont, rcv)
        return len(ext) + max(0, nj - len(ext)), [(x,) for x in ext], nj

    def cost_new(self, flb, perm, rs, bound=None):
        fkc, rcv = self.setup(flb, perm, rs)
        ext, cont = self.single(fkc, rcv)
        nj = self.junk(cont, rcv)
        M = set(ext)
        if bound is not None and max(nj, (len(M) + 1) // 2) >= bound:      # every line of M lies in some extra
            return None
        best = (max(len(M), nj), [(x,) for x in sorted(M)])
        cands = [(x,) for x in sorted(M)] + [c for c in self.cellsB if c[0] in M or c[1] in M]
        for k in range((len(M) + 1) // 2, len(M)):
            if max(k, nj) >= best[0]:
                break
            hit = None
            for comb in itertools.combinations(cands, k):
                if not M <= {l for c in comb for l in c}:
                    continue
                if not self.mininode(fkc, rcv, [sum(1 << l for l in c) for c in comb])[0]:
                    hit = list(comb)
                    break
            if hit is not None:
                best = (max(k, nj), hit)
                break
        if bound is not None and best[0] >= bound:
            return None
        return best[0], best[1], nj


def solve(job):
    B, S, mode = job
    bk = Block(B, list(S))
    best, opt = None, []
    for flb in range(64):
        for perm in itertools.permutations(bk.cells):
            for rs in itertools.product((1, 2, 3), repeat=len(bk.taus)):
                if mode == "old":
                    r = bk.cost_old(flb, perm, rs)
                else:
                    r = bk.cost_new(flb, perm, rs, bound=None if best is None else best + 1)
                    if r is None:
                        continue
                if best is None or r[0] < best:
                    best, opt = r[0], []
                if r[0] == best:
                    opt.append((flb, perm, rs, r[1], r[2]))
                if best == 0 and not bk.taus:
                    return job, best, opt
    return job, best, opt


def calibrate(n):
    """the block evaluator against full gen_p3 builds (random keeper plans and receivers, shipped P)"""
    gen_p3.NODEOPT[0] = 1
    rng = random.Random(1)
    ok = 0
    for i in range(n):
        fl, thirds = gen_p3.plan_thirds(G, SOL, random.Random(i))
        sel = {p: rng.choice((1, 2, 3)) for p in SHIPPED}
        extras = {}
        for _ in range(20):
            res = gen_p3.build(G, SOL, SHIPPED, fl, thirds, extras=extras, verbose=False, rcvsel=sel)
            if res[0] != "missing":
                break
            for B, ls in res[1].items():
                extras[B] = sorted(set(extras.get(B, [])) | set(ls))
        tot = 0
        for B in range(10):
            bk = Block(B, SHIPPED)
            flb = sum(fl.get(c, 0) << k for k, c in enumerate(bk.cells))
            tot += bk.cost_old(flb, [thirds[H] for H in bk.Hs], [sel[p] for p in bk.taus])[0]
        ok += (429 + tot == res[1]["R"])
    print("calibration: block evaluator == gen_p3 build helper count on %d of %d random keeper plans" % (ok, n))
    assert ok == n
    sys.path.insert(0, HERE)
    import gen_p4
    gen_p4.NODEOPT[0] = 1
    ok = 0
    for i in range(n):
        fl, thirds = gen_p3.plan_thirds(G, SOL, random.Random(i))
        sel = {p: rng.choice((1, 2, 3)) for p in SHIPPED}
        tot, extras = 0, {}
        for B in range(10):
            bk = Block(B, SHIPPED)
            flb = sum(fl.get(c, 0) << k for k, c in enumerate(bk.cells))
            c, E, nj = bk.cost_new(flb, [thirds[H] for H in bk.Hs], [sel[p] for p in bk.taus])
            tot += c
            if E:
                extras[B] = [x[0] if len(x) == 1 else list(x) for x in E]
        res = gen_p4.build(G, SOL, SHIPPED, fl, thirds, extras=extras, verbose=False, rcvsel=sel)
        ok += (res[0] != "missing" and 429 + tot == res[1]["R"])
    print("calibration: gen_p4 accounting == gen_p4 build helper count (with the extras it names) on %d of %d" % (ok, n))
    assert ok == n


def affine_ok(P):
    brow = [sum((int(e8.GI[t, b]) & 1) << b for b in range(V)) for t in range(V)]
    basis = []
    for v in [(1 << V) | brow[p] for p in P]:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis) == 9


if __name__ == "__main__":
    if "--calibrate" in sys.argv:
        calibrate(int(sys.argv[sys.argv.index("--calibrate") + 1]))
        sys.exit(0)
    mode = "old" if "--old" in sys.argv else "new"
    if "--all" in sys.argv:
        pairs = [(0, 1), (2, 4), (3, 5), (6, 9), (7, 8)]
        jobs = []
        for X, Y in pairs:
            el = [p for p in ELIG if G.blk[p] in (X, Y)]
            for k in range(len(el) + 1):
                for S in itertools.combinations(el, k):
                    jobs += [(X, S, mode), (Y, S, mode)]
    else:
        jobs = [(B, tuple(SHIPPED), mode) for B in range(10)]
    out = {}
    with Pool(4) as pool:
        for job, best, opt in pool.imap_unordered(solve, jobs):
            out[job[:2]] = (best, len(opt), opt[0] if opt else None)
            print(job[:2], "min", best, "attained by", len(opt), "configurations; e.g.", opt[0] if opt else None, flush=True)
    if "--all" in sys.argv:
        best = []
        for P in itertools.combinations(ELIG, 9):
            if affine_ok(P):
                tot = sum(out[(X, tuple(p for p in P if G.blk[p] in (X, Y)))][0] + out[(Y, tuple(p for p in P if G.blk[p] in (X, Y)))][0]
                          for X, Y in pairs)
                best.append((tot, P))
        best.sort()
        print("affinely independent puncture sets:", len(best), "; minimum extra helpers", best[0][0], "-> R", 429 + best[0][0],
              "at", [P for t, P in best if t == best[0][0]], "; next", sorted({t for t, _ in best})[1])
    else:
        tot = sum(out[(B, tuple(SHIPPED))][0] for B in range(10))
        print("shipped puncture set, %s accounting: minimum extra helpers %d -> R = %d" % (mode, tot, 429 + tot))
    if "--save" in sys.argv:
        pickle.dump(out, open(sys.argv[sys.argv.index("--save") + 1], "wb"))
