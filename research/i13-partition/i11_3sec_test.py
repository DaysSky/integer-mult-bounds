"""I11 rank-7 3-section test: is R(t) in the GF(2) span of {t,e1,e2}-perps through t?
Two-sided check for I11: threshold u >= ~3.0 (mean |R(t)|=118.5, capacity 11 x 840 = 9,240);
3-sections: s = 56, u = 3-9 (>= threshold always).  If R(t) = XOR of 2-3 3-sections +
small correction, the architecture prices at R ~ 440 + dead ~ 2.5-3.4v < break-even
3.8-4.1v — a potential frontier word.  Test: span membership + greedy min-weight."""
import sys, time, collections
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; HYP = g.HYP; G = g.G
full = (1 << V) - 1
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def perp(mask):
    r = full
    for s in [x for x in range(V) if mask >> x & 1]: r &= HYP[s]
    return r
for t in (g.P(0,1), g.T(0,1,2)):
    R_t = HYP[t] & ~(1 << t)
    log('%s |R(t)| %d' % (g.kind[t] + str(g.supp[t]), bin(R_t).count('1')))
    # enumerate 3-sections through t: pairs (e1,e2) orthogonal to t and to each other
    mates = [e for e in range(V) if e != t and G[t, e] == 0]
    log('  orthogonal mates:', len(mates))
    secs = []
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            e1, e2 = mates[i], mates[j]
            if G[e1, e2] == 0:
                S = HYP[e1] & HYP[e2]  # section {t,e1,e2}-perp (t's perp implicit: mates already \perp t)
                secs.append(S)
    log('  3-sections through t:', len(secs), 'sizes', dict(sorted(collections.Counter(bin(s).count('1') for s in secs).items())))
    # span test
    basis = {}
    for c in secs:
        v = c
        while v:
            b = v & -v
            if b in basis: v ^= basis[b][0]
            else: basis[b] = (v, c); break
    def reduce_vec(v):
        while v:
            b = v & -v
            if b not in basis: return v
            v ^= basis[b][0]
        return 0
    res = reduce_vec(R_t)
    log('  R(t) in span of 3-sections?', res == 0, '(residual %d lines)' % bin(res).count('1'))
    if res:
        # how many sections to close?  greedy
        used = 0
        while res and used < 20:
            best, gain = None, -1
            for s in secs:
                rs = reduce_vec(s)
                if not rs: continue
                c = bin(res & rs).count('1') - bin(rs & ~res).count('1')
                if c > gain: gain, best = c, rs
            if best is None or gain <= 0: break
            res ^= best; used += 1
        log('  greedy: %d more sections -> residual %d' % (used, bin(res).count('1')))
    else:
        # min-weight: try weight 2, 3 via elimination combo (greedy first)
        # greedy XOR from reduced forms
        res = R_t; used = 0
        while res:
            best, gain = None, -1
            for s in secs:
                rs = reduce_vec(s)
                if not rs: continue
                c = bin(res & rs).count('1') - bin(rs & ~res).count('1')
                if c > gain: gain, best = c, rs
            if best is None or gain <= 0: break
            res ^= best; used += 1
        log('  greedy min-weight estimate: %d sections (residual %d)' % (used, bin(res).count('1')))