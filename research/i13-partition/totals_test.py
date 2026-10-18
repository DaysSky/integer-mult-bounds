"""E8-grammar test on I11 and II19: RANK-6 FLAT-TOTALS (never tested on Lorentzian systems).
Piece = XOR of all lines of a rank-6 flat F with F \\perp t (F inside R(t)); users = perp(F)
lines (rank-5 flat: 15-31 for I11).  E8's actual frontier mechanism (D6-totals) transplanted.
RAM-safe: sampled closures + greedy cover search; no big dicts."""
import sys, time, random, itertools, resource
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

from geom import Geom
g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
rng = random.Random(5)
log('I11 rank-6 flat-totals test')
for t in (0, 55, 110, 200):
    R_t = HYP[t] & ~(1 << t)
    R_lines = [x for x in range(V) if R_t >> x & 1]
    # sample rank-6 flats inside R(t): pick 6 lines spanning rank 6, take closure, keep rank-6 flats
    totals = []  # bitmask ints of flat totals
    users = []
    seen = set()
    tries = 0
    while len(totals) < 3000 and tries < 60000:
        tries += 1
        pick = rng.sample(R_lines, 6)
        # closure: lines orthogonal to the perp of the span: perp = lines \perp all 6
        m = HYP[pick[0]]
        for p in pick[1:]:
            m &= HYP[p]
        # flat = perp(perp): lines \perp every line of m... too slow; use: flat = lines \perp m (m's span's perp)
        # flat = set of lines orthogonal to all lines in perp(span(pick)):
        flat = (1 << V) - 1
        for k in range(V):
            if m >> k & 1:
                flat &= HYP[k]
        if bin(flat).count('1') == 0: continue
        if flat in seen: continue
        seen.add(flat)
        # total = XOR of flat's lines
        tot = 0
        for k in range(V):
            if flat >> k & 1:
                tot ^= (1 << k)
        totals.append(tot)
        # users = perp(flat's span): lines \perp all flat lines
        u = (1 << V) - 1
        for k in range(V):
            if flat >> k & 1:
                u &= HYP[k]
        users.append(bin(u).count('1'))
    log('t=%d |R|=%d: %d distinct flats sampled, sizes %s, users hist %s' % (
        t, bin(R_t).count('1'), len(totals),
        dict(sorted({bin(sum(1 << k for k in range(V) if (1 << k) & f)).count('1') for f in []} for _ in [0]) and
        {k: 1 for k in sorted(set(bin(f).count('1') for f in totals))}),
        dict(sorted({k: 1 for k in sorted(set(users))}.items()))))
    # greedy cover: minimize |R_t XOR totals|
    res = R_t
    w = 0
    hist = [bin(res).count('1')]
    while w < 6:
        best, bp = None, 1 << 30
        for tt in totals:
            p = bin(res ^ tt).count('1')
            if p < bp: bp, best = p, tt
        if best is None: break
        res ^= best
        w += 1
        hist.append(bin(res).count('1'))
        if hist[-1] == 0: break
    log('  greedy: residual %s (weight %d)' % (hist, w))
log('DONE I11')