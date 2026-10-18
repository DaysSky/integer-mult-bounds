"""RAM-SAFE exact-cover search: greedy + random-restart local search (no pair dicts).
Targets: I11 weight-4/5 covers (never measured; <=3 was the wrong test) and II19
weight-3/4 covers incl. level-1 targets (level-0 failed at <=3).
Memory: sections stored as ints (~KB); searches are popcount scans (CPU-bound)."""
import sys, time, collections, random, itertools, resource
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

def greedy_cover(R_t, secs, maxw, restarts, rng):
    """find XOR of <= maxw sections equal to R_t or R_t ^ (1 line); return (weight, used, corr) or None"""
    best = None
    for attempt in range(restarts):
        res = R_t
        used = []
        while len(used) < maxw:
            # pick section minimizing residual popcount (with tiny noise on restarts > 0)
            bs, bp = None, 1 << 30
            for idx in rng.sample(range(len(secs)), len(secs)) if attempt else range(len(secs)):
                p = bin(res ^ secs[idx]).count('1')
                if p < bp:
                    bp, bs = p, idx
                    if p <= 1: break
            if bs is None: break
            res ^= secs[bs]
            used.append(bs)
            if bin(res).count('1') <= 1:
                corr = res.bit_length() - 1 if res else -1
                w = len(used)
                if best is None or w < best[0]:
                    best = (w, used, corr)
                break
        if best and best[0] <= 3:
            break
    return best

# ---- I11 ----
from geom import Geom
g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
def sections_of(t, V, HYP, G):
    mates = [e for e in range(V) if e != t and G[t, e] == 0]
    secs = []
    for i in range(len(mates)):
        zi = HYP[mates[i]]
        for j in range(i + 1, len(mates)):
            if G[mates[i], mates[j]] == 0:
                m = zi & HYP[mates[j]]
                secs.append(sum(1 << k for k in range(V) if m >> k & 1))
    return secs
log('I11 greedy weight-4/5 cover search (20 targets probe)')
rng = random.Random(7)
for t in list(range(0, V, max(1, V // 20)))[:20]:
    R_t = HYP[t] & ~(1 << t)
    secs = sections_of(t, V, HYP, G)
    best = greedy_cover(R_t, secs, 5, 3, rng)
    if best:
        log('I11 t=%d |R|=%d: WEIGHT %d (corr %s)' % (t, bin(R_t).count('1'), best[0], best[2]))
    else:
        log('I11 t=%d |R|=%d: no cover at weight<=5' % (t, bin(R_t).count('1')))

# ---- II19 ----
import numpy as np
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
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    gg = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return gg + a1 * b2 + b1 * a2
Gm = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
log('II19 greedy weight-3/4 cover search (12 targets: level-0 and level-1)')
rng = random.Random(11)
Zint = [sum(1 << k for k in range(n) if Z[i, k]) for i in range(n)]
Zmask = [Z[i] for i in range(n)]
for t in [0, 9, 60, 150, 200, 250, 300, 340, 355, 360, 121, 241]:
    R_t = Zint[t]
    mates = [e for e in range(n) if e != t and Z[t, e]]
    secs = []
    for i in range(len(mates)):
        zi = Zmask[mates[i]]
        for j in range(i + 1, len(mates)):
            if Z[mates[i], mates[j]]:
                m = zi & Zmask[mates[j]]
                secs.append(sum(1 << k for k in range(n) if m[k]))
    best = greedy_cover(R_t, secs, 4, 3, rng)
    if best:
        log('II19 t=%d |R|=%d: WEIGHT %d (corr %s)' % (t, bin(R_t).count('1'), best[0], best[2]))
    else:
        log('II19 t=%d |R|=%d: no cover at weight<=4' % (t, bin(R_t).count('1')))
log('DONE')