"""Stall-tail v2: 10x vocabulary (20,000 flats) + multi-restart + lookahead greedy.
Measures how much of the bulk weight gap (5 vs needed 4) is sample sparsity.
RAM-safe: ints only (~20 MB).  If bulk drops to 4 and tail to 2-3: c_t = 6-7 <= 7.2 budget
-> the architecture fits -> design + pricer next."""
import sys, time, random, resource
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
LA = np.array(g.LA, dtype=float)
rng = random.Random(9)

def sample_flats(R_lines, ntarget, maxw):
    """sample rank-maxw flats via closures of independent w-subsets"""
    tots, seen = [], set()
    tries = 0
    while len(tots) < ntarget and tries < ntarget * 60:
        tries += 1
        k = rng.choice((maxw, maxw - 1))
        pick = rng.sample(R_lines, k)
        if np.linalg.matrix_rank(LA[pick]) != k: continue
        m = HYP[pick[0]]
        for p in pick[1:]: m &= HYP[p]
        flat = (1 << V) - 1
        for kk in [x for x in range(V) if m >> x & 1]: flat &= HYP[kk]
        if not flat or flat in seen: continue
        u = (1 << V) - 1
        for x in range(V):
            if flat >> x & 1: u &= HYP[x]
        if bin(u).count('1') < 4: continue  # users >= 4 for sharing
        if bin(flat).count('1') > 70: continue  # economy band
        seen.add(flat)
        tot = 0
        for x in range(V):
            if flat >> x & 1: tot ^= (1 << x)
        tots.append(tot)
    return tots

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
        if best_w is None or rc < best_res:
            best_w, best_res = w, rc
        if best_res == 0: break
    return best_w, best_res

for t in (0, 55, 110, 200):
    R_t = HYP[t] & ~(1 << t)
    R_lines = [x for x in range(V) if R_t >> x & 1]
    log('t=%d: sampling 20k rank-6 flats...' % t)
    band = sample_flats(R_lines, 20000, 6)
    log('   %d flats sampled' % len(band))
    w1, r1 = greedy_w(R_t, band, 5, 4)
    log('   bulk: weight %d residual %d' % (w1, r1))
    # tail on the residual
    RL = [x for x in range(V) if (R_t ^ R_t) >> x & 1]  # placeholder fix below
    # recompute residual vector properly: rerun greedy deterministically to capture res
    res = R_t
    for _ in range(w1):
        best, bp = None, 1 << 30
        for tt in band:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        res ^= best
    RL = [x for x in range(V) if res >> x & 1]
    small = []
    sseen = set()
    for _ in range(8000):
        k = rng.choice((2, 3, 4))
        if len(RL) < k: break
        pick = rng.sample(RL, k)
        m = HYP[pick[0]]
        for p in pick[1:]: m &= HYP[p]
        flat = (1 << V) - 1
        for kk in [x for x in range(V) if m >> x & 1]: flat &= HYP[kk]
        if not flat or flat in sseen: continue
        sseen.add(flat)
        tot = 0
        for x in range(V):
            if flat >> x & 1: tot ^= (1 << x)
        small.append(tot)
    w2, r2 = greedy_w(res, small, 4, 4)
    log('   tail: weight %d leftover %d -> TOTAL c_t = %d' % (w2, r2, w1 + w2 + (1 if r2 else 0)))
log('DONE')