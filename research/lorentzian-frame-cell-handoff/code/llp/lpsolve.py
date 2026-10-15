"""S11-symmetric LP lower bound on the number of registers of a STRICT ONE-LEVEL I_{11,1} frame-cell bit word.
Model (union coverage, valid relaxation; see lp_model.md):
  every register that reaches a target passes  [rank<=2 frame] -> (at most one middle frame F) -> sink;
  node N = pp(lines F) (closed line set, |pm N| >= 2); sinks = plane sections pm(pi), users = lines of pi;
  registers entering N carry <= 2 lines (branch registers, from cells) or <= 3 (extra registers from A2 planes);
  a target reads: one rank<=2 in-chain frame (<= 3 lines) + private registers (<= 3 lines each),
  ONE plane section in-chain (all arrivals' supports), and delivered registers (one arrival of a section each).
Variables are orbit values (an S11-invariant optimum exists).  Objective: total registers T,
  T >= sum Y + private,  T >= 660 + (# 3-line registers).
usage: lpsolve.py [nodeleread]"""
import pickle, glob, sys, time, collections
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from lgeo import *
t0_ = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0_), *a, flush=True)
planes = pickle.load(open('planes.pkl', 'rb'))
side = pickle.load(open('side.pkl', 'rb'))
secs = {}
for f in sorted(glob.glob('sec_*.pkl')):
    i = int(f.split('_')[1].split('.')[0]); secs[i] = pickle.load(open(f, 'rb'))
assert sorted(secs) == list(range(len(planes))), 'missing sections'
psize = side['psize']; nodes = side['nodes']; tgt = side['tgt']; users = side['users']
VAR = {}
lb, ub, cost = [], [], []
def var(name, lo=0.0, hi=None, c=0.0):
    if name not in VAR:
        VAR[name] = len(lb); lb.append(lo); ub.append(hi); cost.append(c)
    return VAR[name]
rows, cols, vals, rhs = [], [], [], []
nr = [0]
def le(terms, b):
    """sum coef*var <= b"""
    r = nr[0]; nr[0] += 1
    acc = collections.defaultdict(float)
    for v, c in terms: acc[v] += c
    for v, c in acc.items():
        if c != 0: rows.append(r); cols.append(v); vals.append(c)
    rhs.append(b)
T = var('T', c=1.0)
# ---------- Y, W, Z from sections
ytot = []      # (var, orbit size) for objective constraint
for i, s in secs.items():
    for yk, r in s['reps'].items():
        y = var(('Y', yk))
        if ('Ysz', yk) not in VAR:
            VAR[('Ysz', yk)] = None
            ytot.append((y, psize[i] * r['count']))
        for u, wk in r['wkeys'].items():
            w = var(('W', wk), 0.0, 1.0)
            z = var(('Z', r['zkeys'][u]), 0.0, 1.0)
            if ('Wdone', wk) not in VAR:
                VAR[('Wdone', wk)] = None
                le([(w, 1.0), (y, -1.0)], 0.0)
                le([(w, 1.0), (z, -1.0)], 0.0)
log('Y vars', len(ytot), 'W/Z constraints built; vars', len(lb))
# ---------- node capacity: sum_u Z <= 2 k + K3,  K3 <= k (if lam 3)
k3tot = []
for nk, d in nodes.items():
    ks = []
    for yk, c in d['ykeys'].items():
        assert ('Y', yk) in VAR, 'node-side plane key missing on section side'
        ks.append((VAR[('Y', yk)], c))
    zt = [(var(('Z', zk), 0.0, 1.0), c) for zk, c in d['zkeys'].items()]
    if d['lam'] == 3:
        k3 = var(('K3', nk))
        le(zt + [(v, -2.0 * c) for v, c in ks] + [(k3, -1.0)], 0.0)
        le([(k3, 1.0)] + [(v, -1.0 * c) for v, c in ks], 0.0)
        # orbit size of node: sum over its Y-orbits of #(N,pi) pairs / #planes per node
        npairs = 0
        for i, s in secs.items():
            for yk, r in s['reps'].items():
                if r['nkey'] == nk: npairs += psize[i] * r['count']
        k3tot.append((k3, npairs / d['nplanes']))
    else:
        le(zt + [(v, -2.0 * c) for v, c in ks], 0.0)
log('node capacity rows done; nodes', len(nodes))
# ---------- deliveries per section orbit rep: sum_t DEL(t,pi0) <= sum_N count*Y
for i, s in secs.items():
    terms = [(var(('DEL', uk)), 1.0) for uk in users[i]]
    terms += [(VAR[('Y', yk)], -float(r['count'])) for yk, r in s['reps'].items()]
    le(terms, 0.0)
# ---------- targets
NODEREAD = len(sys.argv) > 1 and sys.argv[1] == 'noderead'
priv = []
for t0, d in tgt.items():
    tsz = 55 if t0 < 55 else 165
    pv = var(('PRIV', t0)); priv.append((pv, tsz))
    # in-chain: sum IN <= 1
    le([(var(('IN', p['inkey'])), 1.0) for p in d['planes']], 1.0)
    # >= 2 deliveries (l2cover.py: two plane sections leave >= 15 lines of rank 9 uncovered, beyond a rank<=2 read)
    if 'del2' in sys.argv:
        le([(var(('DEL', p['inkey'])), -1.0) for p in d['planes']], -2.0)
    # cell/rank<=2 reads + private: sum C <= 3 + 3 PRIV
    le([(var(('C', ck), 0.0, 1.0), 1.0) for ck in d['ckeys'].values()] + [(pv, -3.0)], 3.0)
    # coverage per (t0,u) orbit rep
    done = set()
    for u, ck in d['ckeys'].items():
        if ck in done: continue
        done.add(ck)
        terms = [(VAR[('C', ck)], 1.0)]
        for p in d['planes']:
            if u in p['covs']:
                terms.append((var(('COV', p['covs'][u][0]), 0.0, 1.0), 1.0))
        le([(v, -c) for v, c in terms], -1.0)
    # COV <= IN + DEL ; COV <= sum mult W
    cdone = set()
    for p in d['planes']:
        inv_ = var(('IN', p['inkey'])); dv = var(('DEL', p['inkey']))
        s = secs[p['sec']]
        for u, (covk, u0) in p['covs'].items():
            if covk in cdone: continue
            cdone.add(covk)
            cv = var(('COV', covk), 0.0, 1.0)
            le([(cv, 1.0), (inv_, -1.0), (dv, -1.0)], 0.0)
            m = s['mult'].get(u0, {})
            le([(cv, 1.0)] + [(VAR[('W', wk)], -float(c)) for wk, c in m.items()], 0.0)
log('target rows done')
# ---------- T >= sum Y*size + priv ; T >= 660 + sum K3*size
PRICE = 'price' in sys.argv
if PRICE:
    # price-weighted objective (linearised break-even weights): middle registers 1/897 (best middle rank 3/8),
    # registers whose node has rank <= 2 (no middle frame needed) 1/975 (zero-level).  T is then a 'budget' (<1 wins).
    rk = {}
    for i, s in secs.items():
        for yk, r in s['reps'].items(): rk[VAR[('Y', yk)]] = r['rank']
    le([(T, -1.0)] + [(v, float(c) / (975.0 if rk[v] <= 2 else 897.0)) for v, c in ytot] +
       [(v, float(c) / 975.0) for v, c in priv], 0.0)
else:
    le([(T, -1.0)] + [(v, float(c)) for v, c in ytot] + [(v, float(c)) for v, c in priv], 0.0)
    le([(T, -1.0)] + [(v, float(c)) for v, c in k3tot], -660.0)
A = coo_matrix((vals, (rows, cols)), shape=(nr[0], len(lb))).tocsr()
log('LP size', A.shape, 'nnz', A.nnz)
res = linprog(np.array(cost), A_ub=A, b_ub=np.array(rhs), bounds=list(zip(lb, ub)), method='highs',
              options=dict(presolve=True, disp=False, time_limit=3000))
log('status', res.status, res.message)
if res.status == 0:
    x = res.x
    tot_y = sum(x[v] * c for v, c in ytot); tot_p = sum(x[v] * c for v, c in priv); tot_k3 = sum(x[v] * c for v, c in k3tot)
    log('LP OPT registers T = %.3f  (sum Y %.2f, private %.2f, 3-line regs %.2f)  => R >= %.2f' % (res.fun, tot_y, tot_p, tot_k3, res.fun - 220))
    pickle.dump(dict(x=x, VAR={k: v for k, v in VAR.items() if v is not None}, fun=res.fun), open('lp_sol.pkl', 'wb'))
