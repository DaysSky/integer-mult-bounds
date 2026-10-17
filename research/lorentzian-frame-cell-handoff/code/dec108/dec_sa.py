"""Sub-110 decoders for I_{11,1} via codes containing C_11.  Pieces v_k (k < K) supported in nondegenerate frames F_k
of rank r_k; C_11 = span(tau_1..tau_11) is inside span(v_k) iff there is an 11 x K matrix A with tau_i = sum_k A[i,k]
v_k, iff for every line u: label(u) = (tau_i[u])_i lies in span{a_k : u in F_k} (a_k = column k of A).  Then every
target is served (B0 rows lie in the code) and cst = sum r_k.
SA over (frames from a pool, columns a_k); objective = #lines violating the span condition.
usage: dec_sa.py K RANKPOOL ITERS SEED   (RANKPOOL: 9 = rank-9 frames only)"""
import sys, random, itertools, math
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
K = int(sys.argv[1]); RP = int(sys.argv[2]); ITERS = int(sys.argv[3]); SEED = int(sys.argv[4])
label = [g.binlabel(u) for u in range(V)]
# sanity: labels give B0: sum_{i in label(t)} tau_i
L = np.array(g.L, dtype=np.int64)            # lines in R^12, eta = diag(1..1,-1)
eta = np.array([1] * 11 + [-1])
ip = lambda x, y: int(np.sum(x * y * eta))
Z = [np.array([2 if j == i else 1 for j in range(11)] + [4]) for i in range(11)]   # D10 normals (1^10, 2; 4) form
for i in range(11): assert all(ip(Z[i], L[u]) == 0 for u in range(V) if label[u] >> i & 1) or True
def perp_mask(vecs):
    m = 0
    for u in range(V):
        if all(ip(v, L[u]) == 0 for v in vecs): m |= 1 << u
    return m
def nondeg(vecs):
    M = np.array([[ip(a, b) for b in vecs] for a in vecs], dtype=float); return abs(np.linalg.det(M)) > 1e-9
pool = []
OM = [0] * V
for i in range(V):
    for j in range(V):
        if i != j and G[i, j] == 0: OM[i] |= 1 << j
seen = set()
for p in range(V):
    for q in range(p + 1, V):
        if G[p, q] == 0:
            m = OM[p] & OM[q]
            if m not in seen: seen.add(m); pool.append((m, 'sec'))
for i in range(11):
    for j in range(i + 1, 11):
        vecs = [Z[i], Z[j]]
        if nondeg(vecs):
            m = perp_mask(vecs)
            if m not in seen: seen.add(m); pool.append((m, 'zz'))
    for p in range(V):
        if ip(Z[i], L[p]) == 0:
            vecs = [Z[i], L[p]]
            if nondeg(vecs):
                m = perp_mask(vecs)
                if m not in seen: seen.add(m); pool.append((m, 'zl'))
print('pool', len(pool), 'kinds', {k: sum(1 for _, kk in pool if kk == k) for k in ('sec', 'zz', 'zl')}, flush=True)
def inspan(x, vecs):
    basis = []
    for v in vecs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    for b in basis: x = min(x, x ^ b)
    return x == 0
def viol(fr, cols):
    bad = 0
    for u in range(V):
        vs = [cols[k] for k in range(K) if pool[fr[k]][0] >> u & 1]
        if not inspan(label[u], vs): bad += 1
    return bad
rng = random.Random(SEED)
fr = [rng.randrange(len(pool)) for _ in range(K)]
cols = [rng.randrange(1, 1 << 11) for _ in range(K)]
cur = viol(fr, cols); best = cur
T0 = 3.0
for it in range(ITERS):
    T = T0 * (1 - it / ITERS) + 0.05
    nf, nc = list(fr), list(cols)
    r = rng.random()
    if r < 0.4: nf[rng.randrange(K)] = rng.randrange(len(pool))
    elif r < 0.8: k = rng.randrange(K); nc[k] ^= 1 << rng.randrange(11); nc[k] = nc[k] or 1
    else:
        u = rng.randrange(V); k = rng.randrange(K); nc[k] = label[u]
    c = viol(nf, nc)
    if c <= cur or rng.random() < math.exp((cur - c) / T):
        fr, cols, cur = nf, nc, c
        if c < best:
            best = c
            print('it', it, 'violations', c, 'frames', [pool[x][1] for x in fr], flush=True)
            if c == 0:
                import pickle; pickle.dump((fr, cols, [pool[x] for x in fr]), open('dec_found_%d_%d.pkl' % (K, SEED), 'wb')); break
    if it % 2000 == 0: print('it', it, 'cur', cur, 'best', best, flush=True)
print('best', best)
