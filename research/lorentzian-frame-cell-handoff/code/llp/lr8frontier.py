"""Annealing over Z11 cover choices with a COMBINED rigorous-per-design objective:
  node extra registers (lr8nodecost model, RHO = 7) + isolated rank-7 closures (lr8midlb bound),
both computed from the exact Z11 parts layer (lr8z11.solve, FAITH=1).  Maps the sharing / node-rank trade-off.
usage: lr8frontier.py init_sel.json seed minutes   (env POOL as lr8z11)"""
import sys, json, random, math, time, collections
import numpy as np
sys_argv = sys.argv[:]; sys.argv = ['x']
import lr8z11 as Z
from lgeo import *
sys.argv = sys_argv
init, seed, MIN = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); random.seed(seed); t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
LA = np.array(g.LA, dtype=float); ALL = list(range(V))
def span_closure(v):
    B = LA[bits(v)]; q, r = np.linalg.qr(B.T); keep = np.abs(np.diag(r)) > 1e-9; Q = q[:, keep]
    res = LA - (LA @ Q) @ Q.T; ins = np.linalg.norm(res, axis=1) < 1e-7
    m = 0
    for i in np.nonzero(ins)[0]: m |= 1 << int(i)
    return m
def gf2_basis(vs):
    basis = []
    for v in vs:
        for b in basis:
            if v ^ b < v: v ^= b
        if v: basis.append(v); basis.sort(reverse=True)
    return basis
RK = {}
def srank(v):
    if v not in RK: RK[v] = rank(v)
    return RK[v]
def evaluate(sel):
    val, det = Z.solve(sel, TL=3.0, want=True)
    if det is None: return 10 ** 6, None
    asg = collections.defaultdict(int)
    for key, v in det['assign'].items():
        ri, i, u = map(int, key.split(','))
        if v: asg[(ri, i)] |= 1 << u
    users = collections.defaultdict(list)
    for t in range(V):
        o, k = Z.orb[t]; ci = det['cin'][o].index(1)
        for j, F in enumerate(Z.cov[Z.reps[o]][sel[o]]):
            users[Z.rotm(F, k)].append((Z.rotm(asg[(o, j)], k), j == ci))
    node_extra = 0; forced = collections.Counter(); fnode = {}; regs = {}
    for F, us in users.items():
        dl = [p for p, ic in us if not ic]; allp = [p for p, ic in us]
        Bd = gf2_basis(dl); B = gf2_basis(allp); s = len(B)
        vecs = [0]
        for b in B: vecs = vecs + [v ^ b for v in vecs]
        gd = len(gf2_basis([v for v in vecs if v and srank(v) <= 7]))
        m = s if gd == s else s + 1
        node_extra += m - len(Bd)
        k = len(dl)
        if s == 1 and srank(B[0]) == 7 and k <= 1:
            M = span_closure(B[0]); forced[M] += 1; fnode[M] = F; regs[F] = 0
        else: regs[F] = max(k, 2 * s)
    iso = 0
    for M, c in forced.items():
        if c != 1: continue
        P = 0
        for x in bits(M): pass
        PM = (1 << V) - 1
        for x in bits(M): PM &= HYP[x]
        if not any(F2 != fnode[M] and r and F2 & ~PM == 0 for F2, r in regs.items()): iso += 1
    return node_extra + iso, (node_extra, iso)
d = json.load(open(init)); sel = [d[str(r)][0] if isinstance(d[str(r)], list) else d[str(r)] for r in Z.reps]
cur, parts = evaluate(sel); best = cur; bests = list(sel)
log('init combined %d (node %d + isolated closures %d)' % ((cur,) + parts))
it = 0
while time.time() - t0 < MIN * 60:
    it += 1
    ri = random.randrange(Z.NR); old = sel[ri]; sel[ri] = random.randrange(len(Z.cov[Z.reps[ri]]))
    val, pr = evaluate(sel)
    T = 8.0 * (0.05) ** ((time.time() - t0) / (MIN * 60))
    if val <= cur or random.random() < math.exp((cur - val) / T):
        cur = val
        if cur < best:
            best = cur; bests = list(sel); log('it %d combined %d (node %d + isolated %d)' % (it, best, pr[0], pr[1]))
            json.dump({str(r): bests[i] for i, r in enumerate(Z.reps)}, open('lr8frontier_%d.json' % seed, 'w'))
    else: sel[ri] = old
log('done; best combined', best, 'iterations', it)
