"""Grassmann relaxation of the Braverman-He frame embedding (necessary condition for the flag model).
Each vertex -> 5-dim subspace of F_2^10 (5 rows as 10-bit ints).  d(V,W) = rank(V+W) - 5 (Grassmann distance).
Minimise  sum_edges d + P * sum_sessions (5 - d)   (target: all sessions at 5 and edge sum < 785 = routing bill).
usage: grass.py m steps seed   (m=5: F_2^{2m})"""
import pickle, random, sys, time, math
b = pickle.load(open('../bh/bh.pkl', 'rb')); E = b['phys']; S = b['sessions']
m = int(sys.argv[1]); steps = int(float(sys.argv[2])); rng = random.Random(int(sys.argv[3])); n = 2 * m; V = 182
nb = [[] for _ in range(V)]; sv = [[] for _ in range(V)]
for u, v in E: nb[u].append(v); nb[v].append(u)
for s, t in S: sv[s].append(t); sv[t].append(s)
def rank(rows):
    rows = list(rows); r = 0
    for bit in range(n - 1, -1, -1):
        piv = None
        for i in range(r, len(rows)):
            if rows[i] >> bit & 1: piv = i; break
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
def dist(A, B): return rank(A + B) - m
def rand_sub():
    while True:
        rows = [rng.randrange(1, 1 << n) for _ in range(m)]
        if rank(rows) == m: return rows
P = 3.0
sub = [rand_sub() for _ in range(V)]
def local(v, A):
    return sum(dist(A, sub[u]) for u in nb[v]) + P * sum(m - dist(A, sub[w]) for w in sv[v])
ecost = sum(dist(sub[u], sub[v]) for u, v in E); viol = sum(m - dist(sub[s], sub[t]) for s, t in S)
cur = ecost + P * viol; best = None; t0 = time.time(); T0 = 2.0
for it in range(steps):
    Temp = T0 * (1 - it / steps) + 0.02
    v = rng.randrange(V); A = list(sub[v])
    if rng.random() < 0.8:
        i = rng.randrange(m); A[i] = rng.randrange(1, 1 << n)          # change one basis vector
    else:
        i = rng.randrange(m); j = rng.randrange(m)
        if i != j: A[i] ^= A[j] ^ (1 << rng.randrange(n))
    if rank(A) != m: continue
    d = local(v, A) - local(v, sub[v])
    if d <= 0 or rng.random() < math.exp(-d / Temp):
        sub[v] = A; cur += d
    if it % 200000 == 0 or it == steps - 1:
        ecost = sum(dist(sub[u], sub[v2]) for u, v2 in E); viol = sum(m - dist(sub[s], sub[t]) for s, t in S)
        print('it %d T %.2f edges %d session-deficit %d (sessions ok %d/157) %.0fs' % (it, Temp, ecost, viol,
              sum(1 for s, t in S if dist(sub[s], sub[t]) == m), time.time() - t0), flush=True)
        if viol == 0 and (best is None or ecost < best): best = ecost; pickle.dump(sub, open('grass_m%d_s%s.pkl' % (m, sys.argv[3]), 'wb'))
print('best edge sum with all sessions at distance %d: %s (routing bill %d)' % (m, best, 157 * m))
