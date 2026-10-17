"""Extended clique-hitting LP: Y-families = clique orbits (|Q| pieces forced) + sub-clique orbits (9) + orbits of
small line sets with SAT-proven minrank >= 11 (11 pieces forced; from mr11_*.pkl).  Exact per-flat meeting counts
(cliques: explicit orbits; minrank-11 sets: exhaustive S11 counter c/orbmeet).  Certified by exact rational rescaling.
usage: declp2.py MAXEXTRA"""
import sys, pickle, glob, numpy as np, collections
from fractions import Fraction as Fr
from scipy.optimize import linprog
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats, orbdrv
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
MAXX = int(sys.argv[1])
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
orb = pickle.load(open(D + 'corbits2.pkl', 'rb'))
flist = [(r, cl) for r in sorted(reps) for cl in reps[r].values()]
print('flat orbits', len(flist), {r: len(reps[r]) for r in reps}, flush=True)
def mask(idx):
    m = np.zeros(4, dtype=np.uint64)
    for i in idx: m[i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    return m
FM = np.array([mask(cl) for r, cl in flist])
cols = []   # (name, orbit size, forced pieces, per-flat counts)
for k, v in orb.items():
    M = np.array([mask(c) for c in v])
    cnt = [int(np.count_nonzero((M & fm).any(axis=1))) for fm in FM]
    cols.append(('clique%d' % len(v[0]) + ('sub' if k[0] == 'sub' else ''), len(v), len(v[0]), cnt))
print('clique columns', len(cols), flush=True)
extra = {}
for fn in sorted(glob.glob(D + 'mr11_*.pkl')):
    for Y, Q in pickle.load(open(fn, 'rb')):
        extra.setdefault(flats.canon(Y), Y)
ex = sorted(extra.values(), key=len)[:MAXX]
for Y in ex:
    size, cnt = orbdrv.orbit_meet(Y, [cl for r, cl in flist])
    cols.append(('mr11_%d' % len(Y), size, 11, cnt))
    print('  minrank-11 set |Y| = %d, orbit %d' % (len(Y), size), flush=True)
n = len(cols)
A = np.array([[c[3][i] for c in cols] for i in range(len(flist))] + [[c[1] for c in cols]], dtype=float)
b = np.array([r for r, cl in flist] + [11], dtype=float)
cobj = -np.array([c[1] * c[2] for c in cols], dtype=float)
res = linprog(cobj, A_ub=A, b_ub=b, bounds=[(0, None)] * n, method='highs')
print('LP status', res.status, 'value %.6f' % -res.fun, flush=True)
mu = [Fr(x).limit_denominator(10 ** 9) if x > 1e-13 else Fr(0) for x in res.x]
Ai = [[int(A[i, j]) for j in range(n)] for i in range(len(b))]
lhs = [sum(Ai[i][j] * mu[j] for j in range(n) if mu[j]) for i in range(len(b))]
scale = min([Fr(1)] + [Fr(int(b[i])) / lhs[i] for i in range(len(b)) if lhs[i] > 0])
mu = [m * scale for m in mu]
assert all(sum(Ai[i][j] * mu[j] for j in range(n) if mu[j]) <= int(b[i]) for i in range(len(b)))
cert = sum(mu[j] * cols[j][1] * cols[j][2] for j in range(n))
print('CERTIFIED lower bound on the cost of every I_{11,1} decoder: %.6f  (exact %s)' % (float(cert), cert), flush=True)
for j in range(n):
    if mu[j]: print('  %s orbit %d weight %.6g' % (cols[j][0], cols[j][1], float(mu[j])))
sl = sorted((float(int(b[i]) - lhs[i] * scale), i) for i in range(len(b)))[:10]
for s, i in sl:
    print('  tight:', 'full frame' if i == len(flist) else 'rank %d flat with %d lines (P %d, T %d)' % (flist[i][0], len(flist[i][1]),
          sum(g.kind[x] == 'P' for x in flist[i][1]), sum(g.kind[x] == 'T' for x in flist[i][1])), 'slack %.4f' % s)
pickle.dump(dict(cols=[(c[0], c[1], c[2]) for c in cols], mu=mu, cert=cert, ex=ex), open(D + 'declp2_result.pkl', 'wb'))
