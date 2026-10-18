"""I11 3-section design, step 2: structure of the residual.
For T targets the 3-section span misses 25 lines; for P, exactly 1.  What ARE the residual
lines?  If they are the frame-mate x_e lines (the classical corrections), they ride in-chain
free (E8's mate-correction mechanism).  Also: exact weight of representations for P targets
(the greedy stalled at 1 -- find a true weight-2/3 representation + identify the 1 line)."""
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
for t in (g.P(0,1), g.T(0,1,2), g.T(3,4,5), g.P(5,6)):
    R_t = HYP[t] & ~(1 << t)
    mates = [e for e in range(V) if e != t and G[t, e] == 0]
    secs = []
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            if G[mates[i], mates[j]] == 0:
                secs.append(HYP[mates[i]] & HYP[mates[j]])
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
    res_lines = [x for x in range(V) if res >> x & 1]
    kinds = collections.Counter(g.kind[x] for x in res_lines)
    log('%s residual %d lines: kinds %s' % (g.kind[t] + str(g.supp[t]), len(res_lines), dict(kinds)))
    # are the residual lines orthogonal to t? (they must be, being inside R(t))
    log('   all residual in R(t)? %s' % ((res & ~R_t) == 0))
    # do the residual lines share a structure? e.g. all in a common flat/perp?
    if res_lines:
        common = perp(sum(1 << x for x in res_lines))
        log('   perp(residual) has %d lines; is t in it? %s' % (bin(common).count('1'), bool(common >> t & 1)))
        # rank of the residual
        import numpy as np
        A = np.array([g.LA[x] for x in res_lines], dtype=float)
        log('   residual rank %d of %d lines' % (np.linalg.matrix_rank(A), len(res_lines)))