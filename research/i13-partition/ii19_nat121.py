"""nat121: THE SPLIT-REACH CENSUS on the tuned r434 (no word modification - pure measurement).

For every climb (register, gate): the rank paid and the deepest legal split
(the intermediate frames bounded by the src-contents' spans). The reachable hist
redistribution + the price at the reachable hist (mass-neutral by construction).
"""
import json, gzip, os, sys
import numpy as np
import mpmath as mp
from collections import Counter

mp.mp.dps = 50
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
lines = W['lines']
v = W['v']; R = W['R']; nreg = 2 * v + R
start = W['start']; final = W['final']


def rref(rows):
    m = [list(map(mp.mpf, r)) for r in rows]
    ncols = len(m[0]) if m else 0
    r = 0; piv = []
    for c in range(ncols):
        p = None
        for i in range(r, len(m)):
            if m[i][c]:
                p = i; break
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c] / m[r][c]
                m[i] = [(a - f * b) for a, b in zip(m[i], m[r])]
        piv.append(c); r += 1
    return m[:r], piv


fr_cache = {}


def fdim(F):
    if F not in fr_cache:
        fr_cache[F] = len(rref([lines[i] for i in W['frames'][F]])[0])
    return fr_cache[F]


dims = [fdim(F) for F in range(len(W['frames']))]
print('the frame dims census:', dict(sorted(Counter(dims).items())))

# the content of each register at each gate (the replay-lite: just the x-bits)
# src-content: the src's delivered line-set (its val's x-part) - computed by full replay
val = [0] * nreg
for r in range(v):
    val[r] = 1 << r
cur = list(start)

hist_paid = Counter()
split_hist = Counter()   # the reachable (all splits applied greedily, mass-neutral)
curdim = list(dims[F] for F in start)


def content_dim(mask):
    ls = [i for i in range(v) if (mask >> i) & 1]
    if not ls:
        return 0
    return len(rref([lines[i] for i in ls])[0])


for F, d, ss in W['D']:
    fd = dims[F]
    parts = [d] + list(ss)
    cmax = max(content_dim(val[p]) for p in parts)
    for p in parts:
        r0 = fd - dims[cur[p]]
        if r0 <= 0:
            continue
        hist_paid[r0] += 1
        lo = max(cmax, dims[cur[p]] + 1)
        if lo >= fd:
            split_hist[r0] += 1
        else:
            k = fd - lo
            split_hist[1] += k
            split_hist[lo - dims[cur[p]]] += 1
    for p in parts:
        cur[p] = F
    for s in ss:
        val[d] ^= val[s]
for phase, gates in (('A', W['A']), ('B', W['B'])):
    for F, d, ss in gates:
        fd = dims[F]
        parts = [d] + list(ss)
        cmax = max(content_dim(val[p]) for p in parts)
        for p in parts:
            r0 = fd - dims[cur[p]]
            if r0 <= 0:
                continue
            hist_paid[r0] += 1
            lo = max(cmax, dims[cur[p]] + 1)
            if lo >= fd:
                split_hist[r0] += 1
            else:
                k = fd - lo
                split_hist[1] += k
                split_hist[lo - dims[cur[p]]] += 1
        for p in parts:
            cur[p] = F
        for s in ss:
            val[d] ^= val[s]
        if phase == 'A' and False:
            pass
    if phase == 'A':
        # the scatter point: the ret-frames (the totals' cur after D+A, BEFORE B!!)
        rf = [cur[q] for q in W['ret']]
        cst = sum(dims[f] for f in rf)
        print('the ret_frames:', rf, 'the cst:', cst)
# the C-phase: all gates at dim-8 - the climbs as-is
hist_c = Counter()
for F, d, ss in W['C']:
    fd = dims[F]
    for p in [d] + list(ss):
        r0 = fd - dims[cur[p]]
        hist_c[r0] += 1
        cur[p] = F
    # C is the literal reversal: un-build the vals
# the finals
hist_f = Counter()
for r in range(nreg):
    fd = dims[final[r]]
    r0 = fd - dims[cur[r]]
    hist_f[r0] += 1
print('the paid hist (D+A+B):', dict(sorted(hist_paid.items())))
print('the reachable split hist (D+A+B):', dict(sorted(split_hist.items())))
print('the C hist:', dict(sorted(hist_c.items())))
print('the finals hist:', dict(sorted(hist_f.items())))

# the scatter's copy_ranks (rf computed at the A-end above)
print('the ret copy_ranks:', [dims[f] for f in rf])

# the reachable total hist: the split D+A+B + the C + the finals + the copy_ranks
reach = Counter(split_hist) + Counter({k: c for k, c in hist_c.items() if k > 0}) + Counter({k: c for k, c in hist_f.items() if k > 0})
for c0 in [dims[f] for f in rf]:
    reach[c0] += 1
mass = sum(k * c for k, c in reach.items())
ident = 8 * R + cst + 2 * v * 7
print('the reachable total hist:', dict(sorted(reach.items())))
print('the mass check: %d vs the identity %d' % (mass, ident))

# the price at the reachable hist (mass-corrected: pad rank-1)
tot = dict(reach)
m2 = sum(r * c for r, c in tot.items())
tot[1] = tot.get(1, 0) + (mass - m2)
print('the priced hist:', dict(sorted(tot.items())))
P111 = mp.mpf('0.001733052823330162099157')
c, prof, d = price(tot, v, 8, R)
print('THE REACHABLE PRICE: c = %s (%+.4f%%)' % (mp.nstr(c, 22), float((c - P111) / P111) * 100))
