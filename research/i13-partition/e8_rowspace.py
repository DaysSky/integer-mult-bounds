"""E8 ROW-SPACE CENSUS — the low-rank sparse-decoder search, phase 1.
The sparse-decoder freedom is restored (the completeness argument was retracted; the
products are the outer pipeline's business).  The target: a decoder B with rank <= 25,
rows ~12-25 (above the counting bound v/c - 1), support inside {t} u perp(t), diagonal 1.
THE ROW-SPACE CONSTRUCTION (unexplored — stronger than the masked-B0 families which
gave rank 75-117): the rows of B can be ANY codewords of a low-dimensional span.
PHASE 1 (this script): the census of B0's OWN row space (rank 9, 512 codewords):
  - the weight distribution of all 512 codewords;
  - for each target t: the legal codewords (support inside {t} u perp(t), bit t set):
    the count and the min weight.
IF every target has a legal codeword of weight ~13-25: THE SPARSE DECODER EXISTS AT
RANK 9 (cst ~ 72) — the jackpot: R = 240 + small middle + 9, mass/v ~ 32-36, c +10%?.
ELSE: the enrichment hunt (B0's space + k structured extras) is phase 2."""
import sys, time, itertools, resource
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
L = np.array(list(d8.values()))
V = len(L)
G = L @ L.T
log('E8 system: %d lines' % V)

B0 = (np.rint(1 + G).astype(int)) % 2
assert (np.diag(B0) == 1).all()

def pack(M):
    return [int(''.join(str(int(x)) for x in row[::-1]), 2) for row in M]
def rank_packed(rows):
    rows = list(rows); r = 0
    for col in range(V - 1, -1, -1):
        piv = None
        for i in range(r, len(rows)):
            if (rows[i] >> col) & 1: piv = i; break
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> col) & 1): rows[i] ^= rows[r]
        r += 1
    return r

# a basis of B0's row space (dict-pivot Gaussian elimination).  NOTE: the earlier
# single-pass lowest-bit match was broken — it produced 48 pseudo-basis vectors and the
# 2^48 enumeration RAM explosion (the process was killed at 22 GB).  This is the
# standard bit-parallel elimination: reduce against the pivot at the same lowest bit
# until no pivot matches (add) or the row vanishes.
rows0 = pack(B0)
piv = {}
for row in rows0:
    red = row
    while red:
        p = (red & -red).bit_length() - 1
        if p in piv:
            red ^= piv[p]
        else:
            piv[p] = red
            break
basis = list(piv.values())
log('B0 row-space basis: %d vectors (expected 9)' % len(basis))
if len(basis) > 16:
    log('ABORT: basis %d vectors is far above the expected 9 — refusing to enumerate 2^%d codewords' % (len(basis), len(basis)))
    sys.exit(1)

# all 512 codewords
codes = [0]
for b in basis:
    codes += [c ^ b for c in codes]
log('codewords enumerated: %d' % len(codes))

wts = [bin(c).count('1') for c in codes]
from collections import Counter
wd = Counter(wts)
log('WEIGHT DISTRIBUTION (weight: count): %s' % dict(sorted(wd.items())))
log('min nonzero weight: %d (of %d nonzero codewords)' % (min(w for w in wts if w), sum(1 for w in wts if w)))

# per-target legality: supp(r) inside {t} u perp(t) and r[t] = 1
NONPERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) > 1e-9:
            m |= (1 << s)
    NONPERP.append(m)
log('non-perp sizes: mean %.1f' % (sum(bin(m).count('1') for m in NONPERP) / V))

# precompute: the legal codewords for each target
best_at = []
t0c = time.time()
for t in range(V):
    np_, bit = NONPERP[t], (1 << t)
    best = None; cnt = 0; weights = []
    for c in codes:
        if (c & np_) == 0 and (c & bit):
            w = bin(c).count('1')
            weights.append(w)
            cnt += 1
            if best is None or w < best: best = w
    best_at.append((best, cnt))
log('per-target legal codeword census done in %.0fs' % (time.time() - t0c))

allsame = len(set(best_at))
mins = [b for b, c_ in best_at if b is not None]
log('targets with ANY legal codeword: %d / %d' % (len(mins), V))
if mins:
    log('legal min weights: min %d mean %.1f max %d' % (min(mins), sum(mins) / len(mins), max(mins)))
    cnts = [c_ for b, c_ in best_at]
    log('legal counts: min %d mean %.1f max %d' % (min(cnts), sum(cnts) / len(cnts), max(cnts)))
# the census verdict
if mins and max(mins) <= 30:
    log('VERDICT: every target admits a legal codeword of weight <= 30 INSIDE the rank-9 space:')
    log('THE SPARSE DECODER EXISTS AT RANK 9 — build B from the per-target best rows!')
elif mins:
    log('VERDICT: the rank-9 space is insufficient (max legal min-weight %d) — phase 2: enrichment' % max(mins))
log('DONE')