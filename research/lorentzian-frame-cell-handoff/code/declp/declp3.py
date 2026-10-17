"""Clique-hitting LP + minrank-11 families, certified.  Minrank-11 orbit counts are exact (c/orbmeet, all 11! perms)
on a working set W of flats (near-tight in the clique LP); elsewhere the union bound
  #{Y' in orbit : Y' meets L} <= |orbit| * (n_P(L) n_P(Y)/55 + n_T(L) n_T(Y)/165)   (S11 transitive on P and on T lines)
is used, capped by |orbit|.  Every constraint coefficient is therefore >= the true count: the certificate is valid.
usage: declp3.py NEXTRA SLACK"""
import sys, os, pickle, glob, numpy as np, collections
from fractions import Fraction as Fr
from scipy.optimize import linprog
from concurrent.futures import ProcessPoolExecutor
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
sys.path.insert(0, D); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats, orbdrv
NX, SL = int(sys.argv[1]), float(sys.argv[2])
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
flist = [(r, cl) for r in sorted(reps) for cl in reps[r].values()]
nF = len(flist)
def mask(idx):
    m = np.zeros(4, dtype=np.uint64)
    for i in idx: m[i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    return m
cache = D + 'clique_counts.npz'
orb = pickle.load(open(D + 'corbits2.pkl', 'rb')); okeys = list(orb)
if os.path.exists(cache):
    Ac = np.load(cache)['A']
else:
    FM = np.array([mask(cl) for r, cl in flist]); Ac = np.zeros((nF, len(okeys)))
    for j, k in enumerate(okeys):
        M = np.array([mask(c) for c in orb[k]]); bs = max(1, int(1e7 // len(M)))
        for i0 in range(0, nF, bs):
            blk = FM[i0:i0 + bs]; Ac[i0:i0 + len(blk), j] = ((M[:, None, :] & blk[None, :, :]) != 0).any(axis=2).sum(axis=0)
    np.savez(cache, A=Ac)
csz = np.array([len(orb[k]) for k in okeys], dtype=float); cq = np.array([len(orb[k][0]) for k in okeys], dtype=float)
b = np.array([r for r, cl in flist] + [11], dtype=float)
A0 = np.vstack([Ac, csz])
r0 = linprog(-csz * cq, A_ub=A0, b_ub=b, bounds=[(0, None)] * len(okeys), method='highs')
slack0 = b - A0 @ r0.x
W = [i for i in range(nF) if slack0[i] < SL]
print('clique-only LP %.6f; working set |W| = %d flats with slack < %.2f' % (-r0.fun, len(W), SL), flush=True)
extra = {}
for fn in sorted(glob.glob(D + 'mr11_*.pkl')):
    for Y, Q in pickle.load(open(fn, 'rb')): extra.setdefault(flats.canon(Y), Y)
ex = sorted(extra.values(), key=len)[:NX]
def job(Y): return orbdrv.orbit_meet(Y, [flist[i][1] for i in W])
with ProcessPoolExecutor(4) as pool: outs = list(pool.map(job, ex))
nP = lambda S: sum(g.kind[x] == 'P' for x in S); nT = lambda S: sum(g.kind[x] == 'T' for x in S)
cols = []
for Y, (osize, cntW) in zip(ex, outs):
    col = np.zeros(nF + 1)
    for i, (r, cl) in enumerate(flist):
        num = osize * (3 * nP(cl) * nP(Y) + nT(cl) * nT(Y)); col[i] = min(osize, -(-num // 165))   # exact integer ceiling
    for i, c in zip(W, cntW): col[i] = c
    col[-1] = osize; cols.append((Y, osize, col))
    print('  minrank-11 set |Y| = %d (P %d, T %d), orbit %d' % (len(Y), nP(Y), nT(Y), osize), flush=True)
A = np.hstack([A0, np.array([c[2] for c in cols]).T]); obj = np.concatenate([csz * cq, [11.0 * c[1] for c in cols]])
res = linprog(-obj, A_ub=A, b_ub=b, bounds=[(0, None)] * A.shape[1], method='highs')
print('LP value with minrank-11 families: %.6f' % -res.fun, flush=True)
n = A.shape[1]
mu = [Fr(x).limit_denominator(10 ** 9) if x > 1e-13 else Fr(0) for x in res.x]
nz = [j for j in range(n) if mu[j]]
def coef(i, j):
    v = A[i, j]; assert abs(v - round(v)) < 1e-9; return Fr(int(round(v)))   # every coefficient is an integer
lhs = [sum(coef(i, j) * mu[j] for j in nz) for i in range(len(b))]
scale = min([Fr(1)] + [Fr(int(b[i])) / lhs[i] for i in range(len(b)) if lhs[i] > 0])
cert = sum(mu[j] * Fr(int(round(obj[j]))) for j in nz) * scale
assert all(lhs[i] * scale <= int(b[i]) for i in range(len(b)))
print('CERTIFIED lower bound on every I_{11,1} decoder: %.6f' % float(cert), flush=True)
sl = sorted((float(int(b[i]) - lhs[i] * scale), i) for i in range(len(b)))[:12]
for s, i in sl:
    tag = 'full' if i == nF else ('rank %d, %d lines, %s' % (flist[i][0], len(flist[i][1]), 'in W' if i in set(W) else 'UNION BOUND'))
    print('  tight: %s slack %.4f' % (tag, s))
for j in nz:
    print('  weight %.6g on %s' % (float(mu[j] * scale), ('clique orbit %d' % csz[j]) if j < len(okeys) else 'minrank-11 orbit %d' % cols[j - len(okeys)][1]))
