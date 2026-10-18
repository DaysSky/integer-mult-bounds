"""Level-2 II19 probe (v=929, ceiling 4.74x E8): flat-totals greedy on (1,0) and (1,-1)
targets (demands ~330 and ~209).  If covers close at weight 6-8, the richer system prices
at the same R/v multiple as II19-0-1 but a 2.6x higher ceiling."""
import sys, itertools, random, time, collections
import numpy as np
t0 = time.time()
E8 = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                E8.append(v)
for s in itertools.product([1, -1], repeat=8):
    if s.count(-1) % 2 == 0:
        E8.append(np.array(s) / 2)
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
r8 = {}
for v in E8: r8[canon(v)] = np.array(v)
norm4 = []
for i in range(8):
    for s in (2, -2):
        v = np.zeros(8); v[i] = s
        norm4.append(v)
for combo in itertools.combinations(range(8), 4):
    for signs in itertools.product([1, -1], repeat=4):
        v = np.zeros(8)
        for k, idx in enumerate(combo): v[idx] = signs[k]
        norm4.append(v)
n4 = {}
for v in norm4: n4[canon(v)] = np.array(v)
L = []
for al in r8.values():
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
for lm in n4.values():
    L.append((lm, 1, -1))
L.append((np.zeros(8), 1, 1))
n = len(L)
coords = np.array([list(al) + [a, b] for al, a, b in L])
def ipv(x, y):
    return float(np.dot(x[:8], y[:8])) + x[8] * y[9] + x[9] * y[8]
Gm = np.array([[ipv(coords[i], coords[j]) for j in range(n)] for i in range(n)])
norms = np.diag(Gm)
print('lines %d, norms %s' % (n, dict(collections.Counter(np.round(norms, 2).tolist()))))
Z = np.abs(Gm) < 1e-9
cls = [(a, b) for al, a, b in L]
rng = random.Random(7)
t10 = [i for i in range(n) if cls[i] == (1, 0)][0]
t1m1 = [i for i in range(n) if cls[i] == (1, -1)][5]
t00 = 0
for t in (t10, t1m1, t00):
    R_lines = [k for k in range(n) if Z[t, k]]
    R_t = sum(1 << k for k in R_lines)
    tots, seen = [], set()
    tries = 0
    while len(tots) < 8000 and tries < 400000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(coords[pick]) != 6: continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        idxs = [x for x in range(n) if m[x]]
        for kk in idxs: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        u = np.ones(n, dtype=bool)
        for k in range(n):
            if flat[k]: u = u & Z[k]
        if int(u.sum()) < 4: continue
        if int(flat.sum()) > 100: continue
        seen.add(fmask)
        tot = 0
        for k in range(n):
            if flat[k]: tot ^= (1 << k)
        tots.append(tot)
    res = R_t
    hist = [bin(res).count('1')]
    for _ in range(10):
        best, bp = None, 1 << 30
        for tt in tots:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None or bp >= hist[-1]: break
        res ^= best
        hist.append(bin(res).count('1'))
        if hist[-1] == 0: break
    print('t cls %s |R|=%d flats %d: greedy %s' % (cls[t], bin(R_t).count('1'), len(tots), hist))
print('%.0fs' % (time.time() - t0))