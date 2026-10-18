"""E8-grammar test v2: rank-6 flat-totals with RANK ENFORCED (v1 bug: dependent 6-subsets
gave degenerate closures up to R(t) itself, 'weight 1' = trivial cover).
Proper: 6 lines spanning rank exactly 6 (numpy rank check on LA coords), closure stays rank 6,
greedy restricted to the economical band (users >= 5, size <= 60)."""
import sys, time, random, itertools, resource
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
LA = np.array(g.LA, dtype=float)
rng = random.Random(5)
log('I11 rank-6 flat-totals test v2 (rank enforced)')
for t in (0, 55, 110, 200):
    R_t = HYP[t] & ~(1 << t)
    R_lines = [x for x in range(V) if R_t >> x & 1]
    totals, uszs, users = [], [], []
    seen = set()
    tries = 0
    while len(totals) < 2500 and tries < 120000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        if np.linalg.matrix_rank(LA[pick]) != 6: continue
        m = HYP[pick[0]]
        for p in pick[1:]:
            m &= HYP[p]
        # closure = lines orthogonal to every line of m (double perp)
        flat = (1 << V) - 1
        mk = [k for k in range(V) if m >> k & 1]
        for k in mk:
            flat &= HYP[k]
        if not flat or flat in seen: continue
        # flat should be within R(t)?  flat = closure of span(pick) \subseteq... not nec. inside R(t);
        # users = lines \perp flat
        u = (1 << V) - 1
        for k in range(V):
            if flat >> k & 1:
                u &= HYP[k]
        nu = bin(u).count('1')
        # sanity: the flat's lines should be \perp t?  closure of lines in R(t): orthogonal to t? not guaranteed
        seen.add(flat)
        tot = 0
        for k in range(V):
            if flat >> k & 1:
                tot ^= (1 << k)
        totals.append(tot); uszs.append(bin(flat).count('1')); users.append(nu)
    sizes_hist = {}
    for s in uszs: sizes_hist[s] = sizes_hist.get(s, 0) + 1
    users_hist = {}
    for u in users: users_hist[u] = users_hist.get(u, 0) + 1
    # totals inside R(t)? check overlap
    inR = sum(1 for tt in totals if (tt & ~R_t) == 0)
    log('t=%d |R|=%d: %d flats (rank-6 enforced), size hist %s' %
        (t, bin(R_t).count('1'), len(totals), dict(sorted(sizes_hist.items()))))
    log('   users hist %s ; totals fully inside R(t): %d/%d' % (dict(sorted(users_hist.items())), inR, len(totals)))
    # greedy with the economical band
    band = [(tt, u, s) for tt, u, s in zip(totals, users, uszs) if u >= 5 and s <= 60]
    log('   economical band (u>=5, s<=60): %d pieces' % len(band))
    res = R_t
    hist = [bin(res).count('1')]
    for _ in range(8):
        best, bp = None, 1 << 30
        for tt, u, s in band:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None: break
        res ^= best
        hist.append(bin(res).count('1'))
        if hist[-1] == 0: break
    log('   greedy residual trajectory: %s' % hist)
log('DONE')