"""LP lower bounds for defect-1-triple (A3 / TT*) designs of I_{11,1}: NO symmetry, NO consistency.
Every line s picks a defect-1 triple of planes through it (fractional x_{s,k}); a plane p is a used section
(z_p) if any line uses it.  Register count of a section with u users and kappa pieces = kappa + u - 1 (independence
lemma), so total = sum_s 3 (=660, the 'u' terms) + sum_p (kappa_p - 1) z_p.
  model A (rigorous kappa): kappa_p = 2 for every section (kappa_ex = 2 exactly, proven for all 3-section tops)
  model B (shareability):   kappa_p = min over (line, triple) using p of 2/min(1, ratio(signature))  (lkex2 table)
  model C: as B but consistency enforced (used plane used by all its lines), no symmetry.
Output: LP optimum (registers) and R = registers - 220 for each model.  usage: e11lpdesign.py"""
import sys, itertools, collections, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from lgeo import *
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def third(a, b):
    out = []
    if G[a][b] == 0: return out
    for sg in (1, -1):
        c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
        if c is not None and c not in (a, b): out.append(c)
    return out
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    for c in third(a, b): m |= 1 << c
    return m
RATIO = {(3, 85, 29): 0.78, (2, 70, 14): 21.5, (3, 85, 43): 0.54, (2, 56, 14): 6.8, (3, 71, 29): 0.78,
         (3, 85, 38): 0.54, (3, 71, 24): 1.17, (2, 66, 19): 4.25, (2, 70, 28): 0.78, (2, 66, 29): 1.86,
         (2, 61, 24): 0.75, (2, 66, 30): 0.44, (3, 71, 34): 0.78, (2, 56, 19): 4.25}
def triples(t):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    Sm = [pm(p) for p in pl]; out = []
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        if pc(Sm[i] ^ Sm[j] ^ Sm[k] ^ R) == 1: out.append((pl[i], pl[j], pl[k]))
    return out
REPT = {}
for t in range(V):
    if KIND[t] not in REPT: REPT[KIND[t]] = (t, triples(t))
opts = []           # (s, (p1,p2,p3), (keff1,keff2,keff3))
for s in range(V):
    r, TR = REPT[KIND[s]]
    a_ = list(SUPP[r]); b_ = list(SUPP[s]); perm_ = [0] * n
    for x, y in zip(a_ + [i for i in range(n) if i not in a_], b_ + [i for i in range(n) if i not in b_]): perm_[x] = y
    for tr in TR:
        pl = tuple(act(p, perm_) for p in tr)
        S = {p: pm(p) for p in pl}; ke = []
        for p in pl:
            o = [q for q in pl if q != p]
            E = S[p] & ~S[o[0]] & ~S[o[1]]
            ke.append(2.0 / min(1.0, RATIO[(pc(p), pc(S[p]), pc(E))]))
        opts.append((s, pl, tuple(ke)))
log('options', len(opts))
planes = sorted(set(p for o in opts for p in o[1])); pidx = {p: i for i, p in enumerate(planes)}
nx = len(opts); nz = len(planes)
kmin = np.full(nz, 99.0)
for s, pl, ke in opts:
    for p, k in zip(pl, ke): kmin[pidx[p]] = min(kmin[pidx[p]], k)
log('planes', nz)
# equality: each line one option
rows, cols, vals = [], [], []
for j, (s, pl, ke) in enumerate(opts): rows.append(s); cols.append(j); vals.append(1.0)
Aeq = coo_matrix((vals, (rows, cols)), shape=(V, nx + nz)).tocsr(); beq = np.ones(V)
# inequality: use(p, s) - z_p <= 0
key = {}
rows, cols, vals = [], [], []
for j, (s, pl, ke) in enumerate(opts):
    for p in pl:
        r = key.setdefault((p, s), len(key)); rows.append(r); cols.append(j); vals.append(1.0)
for (p, s), r in key.items(): rows.append(r); cols.append(nx + pidx[p]); vals.append(-1.0)
Aub = coo_matrix((vals, (rows, cols)), shape=(len(key), nx + nz)).tocsr(); bub = np.zeros(len(key))
log('rows', len(key))
def solve(cz, consistent=False):
    c = np.concatenate([np.zeros(nx), cz])
    if consistent:
        # use(p, s) == z_p for every line s of p (a used plane is used by all its lines); lines of p with no option
        # containing p force z_p = 0
        A2 = Aub.copy(); A2 = A2.tocoo()
        Ae = __import__('scipy.sparse', fromlist=['vstack']).vstack([Aeq, Aub]).tocsr()
        be = np.concatenate([beq, bub])
        extra_r, extra_c = [], []
        zero = [pidx[p] for p in planes if any((p, s) not in key for s in bits(p))]
        bounds = [(0, 1)] * nx + [(0, 0) if i in set(zero) else (0, 1) for i in range(nz)]
        res = linprog(c, A_eq=Ae, b_eq=be, bounds=bounds, method='highs')
    else:
        res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=(0, 1), method='highs')
    return res
for name, cz, cons in (('A kappa=2', np.ones(nz), False), ('B shareability', kmin - 1, False),
                       ('A kappa=2 consistent', np.ones(nz), True), ('C shareability consistent', kmin - 1, True)):
    res = solve(cz, cons)
    if res.status != 0: log(name, 'status', res.status, res.message); continue
    regs = 660 + res.fun
    zs = res.x[nx:]
    log('%-28s LP registers %.2f -> R >= %.2f ; sections (sum z) %.1f' % (name, regs, regs - 220, zs.sum()))
