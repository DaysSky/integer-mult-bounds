"""Subset-minrank LP lower bound for Eisenstein decoder copy cost (generalizes #798's clique LP)."""
import pickle, itertools, time, threading, os, numpy as np
from scipy.optimize import linprog
from pysat.solvers import Cadical153
from pysat.formula import IDPool
d = pickle.load(open('eis.pkl','rb'))
n = 40; fl = d['flat_list']; C = d['cost'].astype(int); nonorth = d['nonorth']; orth = d['orth']
nf = len(fl); fidx = {f: i for i, f in enumerate(fl)}
elems = np.load('eis_elems.npy').astype(np.int64)
gens = pickle.load(open('eis_gens.pkl','rb'))
def img(mask, g):
    m = 0
    while mask:
        b = mask & -mask; t = b.bit_length() - 1; mask ^= b
        m |= 1 << int(g[t])
    return m
if os.path.exists('pair_reps.pkl'):
    pair_reps = pickle.load(open('pair_reps.pkl','rb'))
else:
    gf = [np.array([fidx[img(f, g)] for f in fl]) for g in gens]
    parent = list(range(nf * nf))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for g in gf:
        for a in range(nf):
            for b in range(nf):
                x, y = find(a * nf + b), find(int(g[a]) * nf + int(g[b]))
                if x != y: parent[x] = y
    reps = {}
    for a in range(nf):
        for b in range(nf):
            if fl[a] and fl[b]: reps.setdefault(find(a * nf + b), (a, b))
    pair_reps = list(reps.values()); pickle.dump(pair_reps, open('pair_reps.pkl','wb'))
print('pair orbits', len(pair_reps), flush=True)
def sat_rank_le(Q, r, tmax):
    k = len(Q); pool = IDPool(); cl = []
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
            if i == j or (nonorth[Q[i]] >> Q[j]) & 1:
                xor_eq([and_(a[i][t], b[j][t]) for t in range(r)], 1 if i == j else 0)
    S = Cadical153(bootstrap_with=cl)
    tm = threading.Timer(tmax, lambda: S.interrupt()); tm.start()
    ok = S.solve_limited(expect_interrupt=True); tm.cancel(); return ok
def is_clique(Q): return all((nonorth[a] >> b) & 1 for a, b in itertools.combinations(Q, 2))
def clique_number(Q):
    Q = list(Q); best = 1
    adj = {a: [b for b in Q if (nonorth[a] >> b) & 1] for a in Q}
    def ext(cl, cand):
        nonlocal best
        best = max(best, len(cl))
        for i, c in enumerate(cand):
            if len(cl) + len(cand) - i <= best: return
            ext(cl + [c], [x for x in cand[i+1:] if (nonorth[c] >> x) & 1])
    ext([], Q); return best
def greedy_clique(Q, trials=300):
    import random
    best = 1
    for tr in range(trials):
        rnd = random.Random(tr); order = list(Q); rnd.shuffle(order); c = []
        for v in order:
            if all((nonorth[v] >> u) & 1 for u in c): c.append(v)
        best = max(best, len(c))
    return best
def minrank_lb(Q, tmax=20):
    Q = list(Q)
    if is_clique(Q): return len(Q)
    lb = clique_number(Q) if len(Q) <= 16 else greedy_clique(Q)
    r = lb
    while r < len(Q):
        ok = sat_rank_le(Q, r, tmax)
        if ok: return r          # rank r achievable; and all < r refuted (or below clique bound)
        if ok is None: return r  # unknown at r: r is still a valid lower bound (r-1 refuted)
        r += 1
    return r
def orbit(mask): return sorted(set(img(mask, g) for g in elems))
def lines(m): return [t for t in range(n) if (m >> t) & 1]
types = {}
def add(name, mask): types[name] = mask
# clique orbit types up to size 7
adjm = [[(nonorth[t] >> s) & 1 for s in range(n)] for t in range(n)]
seen_orb = set()
def cliques_from(cl, cand, out):
    out.append(cl)
    if len(cl) == 7: return
    for i, c in enumerate(cand):
        cliques_from(cl + [c], [x for x in cand[i+1:] if adjm[c][x]], out)
allc = []; cliques_from([0], [x for x in range(1, n) if adjm[0][x]], allc)
for c in allc:
    m = sum(1 << t for t in c)
    key = min(orbit(m)) if len(c) <= 4 else None
    if key is None:
        # cheaper invariant for big cliques: size + sorted degree pattern
        key = (len(c), m)
    if len(c) >= 5:
        # keep a few reps per size
        cnt = sum(1 for k in seen_orb if isinstance(k, tuple) and k[0] == len(c))
        if cnt >= 3: continue
    if key in seen_orb: continue
    seen_orb.add(key); add('clique%d_%d' % (len(c), len(seen_orb)), m)
u = 0
add('perp', orth[u]); add('perp+u', orth[u] | 1); add('u+nonorth', nonorth[u] | 1); add('all', (1 << n) - 1)
for i, f in enumerate(fl):
    c = bin(f).count('1')
    if c == 5 and 'flat5' not in types: add('flat5', f)
    if c == 4 and 'tetrad' not in types: add('tetrad', f)
tet = types['tetrad']; T = lines(tet)
polar = [x for x in range(n) if all((orth[x] >> t) & 1 for t in T)]
add('tetrad+polar', tet | sum(1 << x for x in polar))
# GQ line
for t in range(n):
    nb = lines(orth[t])
    for a_, b_, c_ in itertools.combinations(nb, 3):
        if (orth[a_] >> b_) & 1 and (orth[a_] >> c_) & 1 and (orth[b_] >> c_) & 1:
            add('gqline', (1 << t) | (1 << a_) | (1 << b_) | (1 << c_)); break
    if 'gqline' in types: break
# point + one GQ line through it plus another
# random medium subsets (orbit reps) for variety
rng = np.random.default_rng(7)
for k in (6, 8, 10, 13, 16, 20):
    for rep in range(3):
        S_ = rng.choice(n, size=k, replace=False); add('rand%d_%d' % (k, rep), sum(1 << int(x) for x in S_))
tt = []
for name, m in types.items():
    t0 = time.time(); orb = orbit(m); Q = lines(m); mr = minrank_lb(Q)
    tt.append((name, m, orb, mr)); print(name, 'size', len(Q), 'orbit', len(orb), 'minrank>=', mr, '%.1fs' % (time.time() - t0), flush=True)
A_ub = np.zeros((len(pair_reps), len(tt))); b_ub = np.zeros(len(pair_reps))
for i, (a, b) in enumerate(pair_reps):
    F, G = fl[a], fl[b]; b_ub[i] = C[a, b]
    for j, (name, m, orb, mr) in enumerate(tt):
        A_ub[i, j] = sum(1 for q in orb if (q & F) and (q & G))
obj = -np.array([len(orb) * mr for (name, m, orb, mr) in tt], dtype=float)
res = linprog(obj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * len(tt), method='highs')
print('LP lower bound', -res.fun, flush=True)
for (name, m, orb, mr), w in zip(tt, res.x):
    if w > 1e-12: print('  ', name, 'w', w, 'contrib', w * len(orb) * mr)
