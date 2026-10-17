"""Clique-hitting LP lower bound on the decoder cost of I_{11,1} (any pieces, any nondegenerate frames).
Fact: for a pairwise non-orthogonal clique Q, the rows r_q (q in Q) restrict to the unit vectors on Q, so at least
|Q| pieces meet Q, hence at least |Q| piece frames F_k have L(F_k) meeting Q.  For weights mu_Q >= 0 with
sum_{Q meets L(F)} mu_Q <= rank(F) for every flat, cost = sum_k rank F_k >= sum_Q mu_Q |Q|.
Variables: one weight per S11 clique orbit (S11-invariant weights lose nothing).  Constraints: every flat orbit
(rank of span, which is <= the rank of any frame containing it) plus the full frame (rank 11).  The solver weights are
rescaled in exact rationals until every constraint holds, so the printed certified bound is rigorous."""
import sys, pickle, numpy as np, collections
from fractions import Fraction as Fr
from scipy.optimize import linprog
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
orb = pickle.load(open(D + (sys.argv[1] if len(sys.argv) > 1 else 'corbits.pkl'), 'rb'))
okeys = list(orb)
def mask(idx):
    m = np.zeros(4, dtype=np.uint64)
    for i in idx: m[i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    return m
OM = [np.array([mask(c) for c in orb[k]]) for k in okeys]
osz = [len(orb[k]) for k in okeys]; qsz = [len(orb[k][0]) for k in okeys]
flist = [(r, cl) for r in sorted(reps) for cl in reps[r].values()]
A = np.zeros((len(flist) + 1, len(okeys))); b = np.zeros(len(flist) + 1)
for i, (r, cl) in enumerate(flist):
    fm = mask(cl)
    for j, M in enumerate(OM):
        A[i, j] = int(np.count_nonzero((M & fm).any(axis=1)))
    b[i] = r
A[-1] = osz; b[-1] = 11
cobj = -np.array([s * q for s, q in zip(osz, qsz)], dtype=float)
res = linprog(cobj, A_ub=A, b_ub=b, bounds=[(0, None)] * len(okeys), method='highs')
print('flat orbits', len(flist), 'clique orbits used', len(okeys), 'LP status', res.status, 'LP value %.6f' % (-res.fun), flush=True)
mu = [Fr(x).limit_denominator(10 ** 9) if x > 1e-12 else Fr(0) for x in res.x]
lhs = [sum(Fr(int(A[i, j])) * mu[j] for j in range(len(okeys))) for i in range(len(b))]
scale = min([Fr(1)] + [Fr(int(b[i])) / lhs[i] for i in range(len(b)) if lhs[i] > 0])
mu = [m * scale for m in mu]
cert = sum(mu[j] * osz[j] * qsz[j] for j in range(len(okeys)))
assert all(sum(Fr(int(A[i, j])) * mu[j] for j in range(len(okeys))) <= int(b[i]) for i in range(len(b)))
print('certified lower bound on decoder cost: %s = %.6f' % (cert, float(cert)), flush=True)
slack = [(float(int(b[i]) - lhs[i] * scale), i) for i in range(len(b))]
tight = sorted(slack)[:12]
for s, i in tight:
    if i == len(flist): print('  tight: full frame', s); continue
    r, cl = flist[i]
    print('  tight: rank %d flat, %d lines (P %d, T %d), slack %.4f' % (r, len(cl), sum(g.kind[x] == 'P' for x in cl), sum(g.kind[x] == 'T' for x in cl), s))
for j in range(len(okeys)):
    if mu[j] > 0: print('  weight %.6f on orbit of size %d (|Q| = %d, types %s)' % (float(mu[j]), osz[j], qsz[j], sorted(collections.Counter(g.kind[x] for x in orb[okeys[j]][0]).items())))
