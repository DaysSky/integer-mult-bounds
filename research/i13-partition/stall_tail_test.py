"""Stall-acceptance test: after greedy rank-6 totals stall, do the 20-25-line residuals close
under SMALL flat-totals (rank 2-4: sizes 3-12, users 15-56) at weight 2-4?
If yes: the mixed grammar (totals bulk + small-flat tail) prices at R ~ 5.8v vs the 7.51v
budget -> ~+20% over the frontier.  RAM-safe: closures only, no big dicts."""
import sys, time, random, resource
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
LA = np.array(g.LA, dtype=float)
rng = random.Random(5)
for t in (0, 55, 110, 200):
    R_t = HYP[t] & ~(1 << t)
    R_lines = [x for x in range(V) if R_t >> x & 1]
    # phase 1: rank-6 totals greedy (economy band) -- as totals_test2
    totals, uszs, users = [], [], []
    seen = set(); tries = 0
    while len(totals) < 2000 and tries < 80000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(LA[pick]) != 6: continue
        m = HYP[pick[0]]
        for p in pick[1:]: m &= HYP[p]
        flat = (1 << V) - 1
        for k in [k for k in range(V) if m >> k & 1]: flat &= HYP[k]
        if not flat or flat in seen: continue
        u = (1 << V) - 1
        for k in range(V):
            if flat >> k & 1: u &= HYP[k]
        seen.add(flat)
        tot = 0
        for k in range(V):
            if flat >> k & 1: tot ^= (1 << k)
        totals.append(tot); uszs.append(bin(flat).count('1')); users.append(bin(u).count('1'))
    band = [tt for tt, u, s in zip(totals, users, uszs) if u >= 5 and s <= 60]
    res = R_t; w1 = 0
    while w1 < 5:
        best, bp = None, 1 << 30
        for tt in band:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None: break
        res ^= best; w1 += 1
        if bin(res).count('1') == 0: break
    resid = bin(res).count('1')
    log('t=%d: bulk weight %d, residual %d lines' % (t, w1, resid))
    # phase 2: small flats of the residual's lines (closures of pairs/triples/quads)
    RL = [x for x in range(V) if res >> x & 1]
    small = []; sseen = set()
    for _ in range(4000):
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
    # greedy on residual with small totals
    r2 = res; w2 = 0
    traj = [bin(r2).count('1')]
    while w2 < 5:
        best, bp = None, 1 << 30
        for tt in small:
            p = bin(r2 ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None or bp >= bin(r2).count('1'): break
        r2 ^= best; w2 += 1; traj.append(bin(r2).count('1'))
        if traj[-1] == 0: break
    log('   tail: small-flats %d, greedy %s (tail weight %d, leftover %d)' %
        (len(small), traj, w2, bin(r2).count('1')))
log('DONE')