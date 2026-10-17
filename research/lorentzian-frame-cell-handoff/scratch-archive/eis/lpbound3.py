"""Generalized subset-minrank LP lower bound for the Eisenstein decoder cost."""
import pickle, numpy as np, itertools, sys, time
from scipy.optimize import linprog
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('eis.pkl','rb'))
n = 40; fl = d['flat_list']; C = d['cost'].astype(int); nonorth = d['nonorth']; orth = d['orth']
nf = len(fl); fidx = {f: i for i, f in enumerate(fl)}
gens = pickle.load(open('eis_gens.pkl','rb'))
elems = np.load('eis_elems.npy').astype(np.int64)
def img_mask(mask, g):
    m = 0
    while mask:
        b = mask & -mask; t = b.bit_length() - 1; mask ^= b
        m |= 1 << int(g[t])
    return m
# flat images under generators -> orbits of flat pairs via union-find
gf = [np.array([fidx[img_mask(f, g)] for f in fl]) for g in gens]
parent = np.arange(nf * nf)
def find(x):
    r = x
    while parent[r] != r: r = parent[r]
    while parent[x] != r: parent[x], x = r, parent[x]
    return r
for g in gf:
    for a in range(nf):
        ga = g[a]
        for b in range(nf):
            x = find(a * nf + b); y = find(ga * nf + g[b])
            if x != y: parent[x] = y
reps = {}
for a in range(nf):
    for b in range(nf):
        if fl[a] and fl[b]:
            r = find(a * nf + b); reps.setdefault(r, (a, b))
pair_reps = list(reps.values())
print('flat-pair orbits', len(pair_reps), flush=True)
def minrank_sat(Q, tmax=60):
    Q = list(Q); k = len(Q)
    for r in range(1, k + 1):
        pool = IDPool(); cl = []
        a = [[pool.id(('a', i, j)) for j in range(r)] for i in range(k)]
        b = [[pool.id(('b', i, j)) for j in range(r)] for i in range(k)]
        def xor_eq(lits, val):
            acc = lits[0]
            for x in lits[1:]:
                y = pool.id(); cl.extend([[-y, acc, x], [-y, -acc, -x], [y, -acc, x], [y, acc, -x]]); acc = y
            cl.append([acc] if val else [-acc])
        def and_(x, y):
            z = pool.id(); cl.extend([[-z, x], [-z, y], [z, -x, -y]]); return z
        for i in range(k):
            for j in range(k):
                if i == j: xor_eq([and_(a[i][t], b[j][t]) for t in range(r)], 1)
                elif (nonorth[Q[i]] >> Q[j]) & 1: xor_eq([and_(a[i][t], b[j][t]) for t in range(r)], 0)
        S = Cadical153(bootstrap_with=cl)
        import threading
        tm = threading.Timer(tmax, lambda: S.interrupt()); tm.start()
        ok = S.solve_limited(expect_interrupt=True); tm.cancel()
        if ok: return r
        if ok is None: return None  # unknown -> caller uses lower bound
    return k
def is_clique(Q):
    return all((nonorth[a] >> b) & 1 for a, b in itertools.combinations(Q, 2))
def max_clique_in(Q):
    best = 1
    for k in range(len(Q), 1, -1):
        for c in itertools.combinations(Q, k):
            if is_clique(c): return k
        if k <= best: break
    return best
def minrank(Q):
    Q = list(Q)
    if is_clique(Q): return len(Q)
    lb = max_clique_in(Q) if len(Q) <= 14 else 1
    # search upward from lb
    k = len(Q)
    for r in range(lb, k + 1):
        res = minrank_sat_r(Q, r)
        if res: return r
        if res is None: return r  # unknown: conservative use r (lower bound valid only if all smaller UNSAT)
    return k
def orbit_of(mask):
    return sorted(set(img_mask(mask, g) for g in elems))
# candidate subset types
cands = {}
def add(name, mask):
    cands[name] = mask
add('point', 1)
# one 7-clique, one 4-clique, one 5-clique and one 6-clique representative (greedy)
adj = [[(nonorth[t] >> s) & 1 for s in range(n)] for t in range(n)]
def find_clique(k):
    def ext(cl, cand):
        if len(cl) == k: return cl
        for c in cand:
            r = ext(cl + [c], [x for x in cand if x > c and adj[c][x]])
            if r: return r
        return None
    return ext([], list(range(n)))
for k in (2, 3, 4, 5, 6, 7):
    q = find_clique(k); add('clique%d' % k, sum(1 << t for t in q))
u = 0
add('perp', orth[u]); add('perp+u', orth[u] | 1)
for i, f in enumerate(fl):
    c = bin(f).count('1')
    if c in (4, 5) and 'flat%d' % c not in cands: add('flat%d' % c, f)
# GQ lines (4 mutually orthogonal)
for t in range(n):
    nb = [s for s in range(n) if (orth[t] >> s) & 1]
    for a_, b_, c_ in itertools.combinations(nb, 3):
        if (orth[a_] >> b_) & 1 and (orth[a_] >> c_) & 1 and (orth[b_] >> c_) & 1:
            add('gqline', (1 << t) | (1 << a_) | (1 << b_) | (1 << c_)); break
    if 'gqline' in cands: break
add('all', (1 << n) - 1)
# unions: point u + nonorth(u) (28), complement of perp+u
add('u+nonorth', nonorth[u] | 1)
types = []
for name, m in cands.items():
    t0 = time.time(); orb = orbit_of(m); mr = minrank([t for t in range(n) if (m >> t) & 1])
    types.append((name, m, orb, mr)); print(name, 'size', bin(m).count('1'), 'orbit', len(orb), 'minrank', mr, '%.1fs' % (time.time() - t0), flush=True)
mem = [fl[a] for a in range(nf)]
A_ub = np.zeros((len(pair_reps), len(types))); b_ub = np.zeros(len(pair_reps))
for i, (a, b) in enumerate(pair_reps):
    F, G = fl[a], fl[b]
    b_ub[i] = C[a, b]
    for j, (name, m, orb, mr) in enumerate(types):
        A_ub[i, j] = sum(1 for q in orb if (q & F) and (q & G))
obj = -np.array([len(orb) * mr for (name, m, orb, mr) in types], dtype=float)
res = linprog(obj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * len(types), method='highs')
print('LP bound', -res.fun)
for (name, m, orb, mr), w in zip(types, res.x):
    if w > 1e-12: print('  ', name, 'weight', w, 'contrib', w * len(orb) * mr)
