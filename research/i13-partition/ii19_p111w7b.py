"""THE BASELINE-TEST (ii19_p111w7b.py) — THE PURE PROJECTION (no star-swaps!!):
the projected D/A/B + the R420's OWN rets (their builds KEPT!!) + the R420's own scatter-rows
+ the C (the zg-reversal!!) -> the (5)-check (the line-residues?!?!)
IF PASS: the projection is sound (the star-swap is the bug!!); IF FAIL: the projection's bug!!
"""
import gzip, json, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [1, 8, 20, 24, 45, 63, 82, 89, 102]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']

def nh(h): return h - 18
def map_reg(r):
    if r < v0:
        return old2new.get(r)
    if r < 2 * v0:
        return V + old2new[r - v0] if (r - v0) in old2new else None
    return nh(r)

# THE GATES: the projection (NO drops of the ret-builds!!!)
D = []
for F, d, srcs in W['D']:
    if (d - v0) in old2new:
        D.append([0, V + old2new[d - v0], [nh(s) for s in srcs]])
A = []
for F, d, srcs in W['A']:
    nd = map_reg(d)
    if nd is None:
        continue
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None]
    if not nsrcs:
        continue
    A.append([F, nd, nsrcs])
B = []
for F, d, srcs in W['B']:
    nd = map_reg(d)
    if nd is None:
        continue
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None]
    if nsrcs:
        B.append([F, nd, nsrcs])
log('(1) the projected gates: D %d | A %d | B %d (NO ret-drops!!)' % (len(D), len(A), len(B)))

# THE RETS: the R420's own (the re-mapped!!) + THEIR FRAMES (the R420's own (the re-based!!!))
# the ret-frames: the R420's ret_frames (the frame-INDICES!!): the re-based frames (the same indices!!)
RET = [nh(r) for r in W['ret']]
SCAT = [[k for k in W['scatter'][kept[t]]] for t in range(V)]
log('(2) the rets %s | the rows %s' % (RET, dict(sorted(Counter(len(s) for s in SCAT).items()))))

# THE REPLAY (the values only!!): D + A + scatter + B!!
nreg = 2 * V + R0
val = [1 << r for r in range(nreg)]
for F, d, srcs in D:
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in A:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
for t in range(V):
    for k in SCAT[t]:
        val[V + t] ^= val[RET[k]]
for F, d, srcs in B:
    for s in srcs: val[d] ^= val[s]
nbad = 0
nline = 0
for t in range(V):
    resid = val[V + t] ^ (1 << (V + t)) ^ (1 << t)
    if resid:
        nbad += 1
    lr = [b for b in range(V) if (resid >> b) & 1]
    if lr:
        nline += 1
        if nline <= 3:
            log('    t=%d: the line-residue %s | the reg-residue %s' % (
                t, lr[:8], [b for b in range(2 * V, nreg) if (resid >> b) & 1][:8]))
log('(3) THE BASELINE-CHECK: the bad targets %d/%d (the line-residues %d!!)' % (nbad, V, nline))
log('DONE — THE BASELINE-TEST!!')
