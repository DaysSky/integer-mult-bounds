"""Stall-tail v2 on II19 (the system with the 15v budget — the architecture only needs
tails to close; c_t 9-12 fits).  20k rank-6 flats + restarts + small-flat tails.
If tails close: full-361 design -> exact pricer -> frontier verdict on the highest-ceiling
system (1.84x E8, budget 2.5x I11's)."""
import sys, time, random, itertools, resource
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8, dtype=int); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
lines8 = {}
for r in list(roots) + half: lines8[canon(r)] = r
R8 = list(lines8.values())
L = []
for al in R8:
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
L.append((None, 1, 1))
n = len(L)
coords = [list(al) + [a, b] if al is not None else [0.0] * 8 + [a, b] for al, a, b in L]
LA = np.array(coords)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    gg = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return gg + a1 * b2 + b1 * a2
Gm = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
Zint = [sum(1 << k for k in range(n) if Z[i, k]) for i in range(n)]
rng = random.Random(9)

def greedy_w(R_t, band, maxw, restarts):
    best_w, best_res = None, None
    for _ in range(restarts):
        res = R_t; w = 0
        order = list(band)
        while w < maxw:
            rng.shuffle(order)
            best, bp = None, 1 << 30
            for tt in order:
                p = bin(res ^ tt).count('1')
                if p < bp: bp, best = p, tt
                if bp <= 2: break
            if bp >= bin(res).count('1'): break
            res ^= best; w += 1
            if bin(res).count('1') == 0: break
        rc = bin(res).count('1')
        if best_w is None or rc < best_res: best_w, best_res = w, rc
        if best_res == 0: break
    return best_w, best_res

for t in (0, 60, 200, 360, 121, 241):
    R_t = Zint[t]
    R_lines = [k for k in range(n) if R_t >> k & 1]
    tots, seen = [], set()
    tries = 0
    while len(tots) < 20000 and tries < 1200000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(LA[pick]) != 6: continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        u = np.ones(n, dtype=bool)
        for k in range(n):
            if flat[k]: u = u & Z[k]
        if int(u.sum()) < 4: continue
        if int(flat.sum()) > 80: continue
        seen.add(fmask)
        tot = 0
        for k in range(n):
            if flat[k]: tot ^= (1 << k)
        tots.append(tot)
    log('t=%d |R|=%d: %d flats sampled' % (t, bin(R_t).count('1'), len(tots)))
    w1, r1 = greedy_w(R_t, tots, 6, 4)
    log('   bulk: weight %d residual %d' % (w1, r1))
    res = R_t
    for _ in range(w1):
        best, bp = None, 1 << 30
        for tt in tots:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        res ^= best
    RL = [k for k in range(n) if res >> k & 1]
    small, sseen = [], set()
    for _ in range(8000):
        k = rng.choice((2, 3, 4))
        if len(RL) < k: break
        pick = rng.sample(RL, k)
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in sseen: continue
        sseen.add(fmask)
        tot = 0
        for x in range(n):
            if flat[x]: tot ^= (1 << x)
        small.append(tot)
    w2, r2 = greedy_w(res, small, 5, 4)
    log('   tail: weight %d leftover %d -> TOTAL c_t = %d' % (w2, r2, w1 + w2 + (1 if r2 else 0)))
log('DONE')