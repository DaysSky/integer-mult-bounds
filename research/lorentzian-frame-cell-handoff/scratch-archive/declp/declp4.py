"""Iterative certified clique + minrank-11 LP (see declp3.py).  Exact orbit counts (c/orbmeet) are cached per family
and per flat; union bounds (integer ceilings) elsewhere.  Each round converts every union-bound flat that is (near)
tight into an exact count, until no union-bound constraint is tight.  usage: declp4.py NEXTRA SLACK ROUNDS"""
import sys, os, pickle, glob, numpy as np
from fractions import Fraction as Fr
from scipy.optimize import linprog
from concurrent.futures import ProcessPoolExecutor
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
sys.path.insert(0, D); sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats, orbdrv
NX, SL, ROUNDS = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
flist = [(r, cl) for r in sorted(reps) for cl in reps[r].values()]; nF = len(flist)
orb = pickle.load(open(D + 'corbits2.pkl', 'rb')); okeys = list(orb)
Ac = np.load(D + 'clique_counts.npz')['A']
csz = np.array([len(orb[k]) for k in okeys], dtype=float); cq = np.array([len(orb[k][0]) for k in okeys], dtype=float)
b = np.array([r for r, cl in flist] + [11], dtype=float)
A0 = np.vstack([Ac, csz])
r0 = linprog(-csz * cq, A_ub=A0, b_ub=b, bounds=[(0, None)] * len(okeys), method='highs')
W = set(i for i in range(nF) if (b - A0 @ r0.x)[i] < SL)
extra = {}; guided = set()
for fn in sorted(f for f in glob.glob(D + 'mr11_*.pkl') if 'counts' not in f):
    for Y, Q in pickle.load(open(fn, 'rb')):
        k = flats.canon(Y); extra.setdefault(k, Y)
        if 'mr11_cg_' in fn: guided.add(k)
ex = sorted((extra[k] for k in guided), key=len) + sorted((extra[k] for k in extra if k not in guided), key=len)
ex = ex[:NX]
print('clique LP %.6f; %d minrank-11 families (of %d found); initial |W| = %d' % (-r0.fun, len(ex), len(extra), len(W)), flush=True)
cachef = D + 'mr11_counts.pkl'
cache = pickle.load(open(cachef, 'rb')) if os.path.exists(cachef) else {}
nP = lambda S: sum(g.kind[x] == 'P' for x in S); nT = lambda S: sum(g.kind[x] == 'T' for x in S)
def job(args):
    Y, idx = args; return orbdrv.orbit_meet(Y, [flist[i][1] for i in idx])
for rnd in range(ROUNDS):
    todo = []
    for Y in ex:
        c = cache.setdefault(Y, {'size': None, 'cnt': {}})
        miss = sorted(i for i in W if i not in c['cnt'])
        if miss: todo.append((Y, miss))
    if todo:
        with ProcessPoolExecutor(4) as pool:
            for (Y, miss), (osize, cnts) in zip(todo, pool.map(job, todo)):
                cache[Y]['size'] = osize
                for i, cval in zip(miss, cnts): cache[Y]['cnt'][i] = cval
        pickle.dump(cache, open(cachef, 'wb'))
    cols = []
    for Y in ex:
        osize = cache[Y]['size']; col = np.zeros(nF + 1)
        for i, (r, cl) in enumerate(flist):
            if i in cache[Y]['cnt']: col[i] = cache[Y]['cnt'][i]
            else:
                num = osize * (3 * nP(cl) * nP(Y) + nT(cl) * nT(Y)); col[i] = min(osize, -(-num // 165))
        col[-1] = osize; cols.append(col)
    A = np.hstack([A0, np.array(cols).T]); obj = np.concatenate([csz * cq, [11.0 * cache[Y]['size'] for Y in ex]])
    res = linprog(-obj, A_ub=A, b_ub=b, bounds=[(0, None)] * A.shape[1], method='highs')
    n = A.shape[1]
    mu = [Fr(x).limit_denominator(10 ** 9) if x > 1e-13 else Fr(0) for x in res.x]; nz = [j for j in range(n) if mu[j]]
    lhs = [sum(Fr(int(round(A[i, j]))) * mu[j] for j in nz) for i in range(len(b))]
    scale = min([Fr(1)] + [Fr(int(b[i])) / lhs[i] for i in range(len(b)) if lhs[i] > 0])
    assert all(lhs[i] * scale <= int(b[i]) for i in range(len(b)))
    cert = sum(mu[j] * Fr(int(round(obj[j]))) for j in nz) * scale
    slack = [float(int(b[i]) - lhs[i] * scale) for i in range(len(b))]
    ub_tight = [i for i in range(nF) if i not in W and slack[i] < 0.05]
    print('round %d: LP %.6f, CERTIFIED %.6f, |W| %d, union-bound flats with slack < 0.05: %d' % (rnd, -res.fun, float(cert), len(W), len(ub_tight)), flush=True)
    for j in nz:
        print('   weight %.4g on %s' % (float(mu[j] * scale), ('clique orbit %d' % csz[j]) if j < len(okeys) else 'minrank-11 |Y| %d orbit %d' % (len(ex[j - len(okeys)]), cache[ex[j - len(okeys)]]['size'])), flush=True)
    if not ub_tight: break
    W |= set(ub_tight) | set(i for i in range(nF) if slack[i] < SL)
pickle.dump(dict(cert=cert, mu=mu, ex=ex, W=sorted(W)), open(D + 'declp4_result.pkl', 'wb'))
yv = -np.asarray(res.ineqlin.marginals)
duals = [(float(yv[i]), tuple(flist[i][1]) if i < nF else tuple(range(V))) for i in range(len(b)) if yv[i] > 1e-9]
pickle.dump(duals, open(D + 'duals.pkl', 'wb')); print('saved', len(duals), 'dual weights', flush=True)
