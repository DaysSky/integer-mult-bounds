"""Intermediate clique LP: all flat orbits of rank <= 9 (from flats_reps.pkl) + structured rank-10 flats + full frame.
Upper estimate of the final certified value (rank-10 flats incomplete)."""
import sys, pickle, numpy as np, collections
from scipy.optimize import linprog
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
orb = pickle.load(open(D + 'corbits2.pkl', 'rb'))
flist = [(r, cl) for r in sorted(reps) if r <= 9 for cl in reps[r].values()]
G = g.G
extra10 = [flats.closure([s for s in range(V) if s != t and G[s, t] == 0])[0] for t in (0, 55)]
extra10.append(flats.closure([x for x in range(V) if (0 in g.supp[x]) == (g.kind[x] == 'T')])[0])
extra10.append(flats.closure([x for x in range(V) if 0 not in g.supp[x]])[0])
flist += [(10, cl) for cl in extra10]
def mask(idx):
    m = np.zeros(4, dtype=np.uint64)
    for i in idx: m[i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    return m
FM = np.array([mask(cl) for r, cl in flist])
keys = list(orb)
A = np.zeros((len(flist) + 1, len(keys)))
for j, k in enumerate(keys):
    M = np.array([mask(c) for c in orb[k]])
    bs = max(1, int(1e7 // len(M)))
    for i0 in range(0, len(FM), bs):
        blk = FM[i0:i0 + bs]
        hit = ((M[:, None, :] & blk[None, :, :]) != 0).any(axis=2)
        A[i0:i0 + len(blk), j] = hit.sum(axis=0)
    A[-1, j] = len(orb[k])
    print('counted orbit', j, len(orb[k]), flush=True)
b = np.array([r for r, cl in flist] + [11], dtype=float)
cobj = -np.array([len(orb[k]) * len(orb[k][0]) for k in keys], dtype=float)
res = linprog(cobj, A_ub=A, b_ub=b, bounds=[(0, None)] * len(keys), method='highs')
print('flats', len(flist), 'LP value (upper estimate): %.6f' % -res.fun, flush=True)
sl = b - A @ res.x
for i in np.argsort(sl)[:12]:
    if i == len(flist): print('  tight full frame', sl[i]); continue
    r, cl = flist[i]
    print('  rank %d flat, %d lines (P %d, T %d), slack %.5f' % (r, len(cl), sum(g.kind[x] == 'P' for x in cl), sum(g.kind[x] == 'T' for x in cl), sl[i]))
for j, k in enumerate(keys):
    if res.x[j] > 1e-10: print('  weight %.6f on %s orbit %d |Q| %d' % (res.x[j], 'sub' if k[0] == 'sub' else 'max', len(orb[k]), len(orb[k][0])))
