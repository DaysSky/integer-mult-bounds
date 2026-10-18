"""THE LB-METRIC HUNT (ii19_phunt4.py) — THE PROPER PUNCTURE-DESIGN!!
THE THEORY (think properly!!): the line u in k(u) stars' supports needs k(u) one-use
coverings; available: 1 (its source!!) + c(u) (its in-pool cell-carriers!!).
THE STRUCTURAL LB: Sum_u max(0, k(u) - 1 - c(u)) — THE FAST METRIC (ms/puncture!!)
(1) validate: the LB vs the known minis (the [21,23..]: 34 / the [40,47..]: 20!!);
(2) THE LB-HUNT: the CST-63 punctures sorted by the LB -> the deep-solve on the LB-best!!
"""
import gzip, json, random, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2

def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines[i]] for i in idx_list]
    bas = []
    for row in rr:
        y = row
        for b in bas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and y[p] != 0:
                f = y[p] / b[p]
                y = [a2 - f * c for a2, c in zip(y, b)]
        p = next((c for c in range(8) if y[c] != 0), None)
        if p is not None: bas.append(y)
    return bas
FBAS = [basis_of(f) if f else [] for f in frames0]
FDIM = [len(b) for b in FBAS]

val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
def in_W(fbas, wbas):
    for y in fbas:
        z = list(y)
        for b in wbas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and z[p] != 0:
                f = z[p] / b[p]
                z = [a2 - f * c for a2, c in zip(z, b)]
        if any(z[c] != 0 for c in range(8)):
            return False
    return True
for F, d, srcs in W['D']:
    for s in srcs: val[d] ^= val[s]
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
    for s in srcs:
        if FDIM[cur[s]] < FDIM[F] or not in_W(FBAS[cur[s]], FBAS[F]):
            cur[s] = F
    cur[d] = F
log('(0) the base-replay done!!')
# the helpers' A-end frame-pools (the puncture-INDEPENDENT parts: the cur ⊆ W checks need
# the W's!!) — the helper pool-membership per W: precompute the helpers' cur-frame BASIS!!
HBAS = {h: FBAS[cur[h]] for h in range(2 * v0, nreg0) if cur[h] and FDIM[cur[h]] <= 7}
HCONT = {}
for h in HBAS:
    c = 0
    for b in range(v0):
        if (val[h] >> b) & 1:
            c |= 1 << b
    HCONT[h] = c
log('    the usable helpers (the cur <= dim-7!!): %d' % len(HBAS))

def puncture_LB(rm):
    """the LB: Sum_u max(0, k(u) - 1 - c(u))!! (the OLD-indexing!!)"""
    STARS_OLD = [[u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0] for L in rm]
    # the CST-63-check (the star-independence!!)!
    kept = [i for i in range(120) if i not in rm]
    old2new = {o: n for n, o in enumerate(kept)}
    STARS_NEW = []
    for L in rm:
        s_new = 0
        for u in kept:
            if iph(lines[L], lines[u]) == 0:
                s_new |= 1 << old2new[u]
        STARS_NEW.append(s_new)
    bx = {}
    for s in STARS_NEW:
        x = s
        while x:
            p = (x & -x).bit_length() - 1
            if p in bx: x ^= bx[p]
            else: bx[p] = x; break
    if len(bx) != 9:
        return None, None
    # the pools (the W_i!!)!
    WiB = [basis_of(s) for s in STARS_OLD]
    cellers = {}                  # the line -> the #in-pool cells!!
    for si in range(9):
        for h, hb in HBAS.items():
            if in_W(hb, WiB[si]):
                for b in range(v0):
                    if (HCONT[h] >> b) & 1:
                        cellers[b] = cellers.get(b, 0) + 1
    # hmm: c(u) should count the DISTINCT cells usable for the SPECIFIC star!! use the max!!
    # (the optimistic LB: the per-star availability: recompute properly below!!)
    # PROPER: for each line u: for each star si ∋ u: the available coverings EXCLUDING the
    # source: the cells C with u in C's content AND C in si's pool: count per (u, si)!!
    cov = {}
    for si in range(9):
        Wb = WiB[si]
        star = STARS_OLD[si]
        for h, hb in HBAS.items():
            if in_W(hb, Wb):
                for b in range(v0):
                    if (HCONT[h] >> b) & 1 and b in [x for x in star]:
                        cov[(b, si)] = cov.get((b, si), 0) + 1
    # the per-line star-membership!!
    k = {}
    for si in range(9):
        for u in STARS_OLD[si]:
            k[u] = k.get(u, 0) + 1
    lb = 0
    for u, kk in k.items():
        # the line u: kk stars; the source: 1; the cells: per-star cov[(u, si)] (the distinct
        # cells!!): the optimistic: the total distinct cells ∋ u across the pools!!
        c_tot = len(set(h for h in HBAS if (HCONT[h] >> u) & 1))
        # the usable-per-star: the min over its stars of cov[(u, si)]!!
        cs = [cov.get((u, si), 0) for si in range(9) if u in STARS_OLD[si]]
        cmin = min(cs) if cs else 0
        need = kk - 1 - cmin      # the optimistic: each star can use a DIFFERENT cell!!
        if need > 0:
            lb += need
    return lb, STARS_OLD

# (1) THE VALIDATION: the known punctures!!
for rm, known in ([[21, 23, 24, 29, 53, 71, 80, 89, 103], 34],
                  [[40, 47, 50, 75, 77, 89, 91, 96, 105], 20]):
    lb, _ = puncture_LB(rm)
    log('(1) rm=%s: the LB %s (the known minis %d!!)' % (rm, lb, known))

# (2) THE LB-HUNT: the random CST-63 punctures -> the LB-sorted!!
rng = random.Random(999)
cands = []
tried = set()
for trial in range(2000):
    rm = tuple(sorted(rng.sample(range(120), 9)))
    if rm in tried: continue
    tried.add(rm)
    lb, _ = puncture_LB(list(rm))
    if lb is not None:
        cands.append((lb, list(rm)))
cands.sort()
log('(2) THE LB-HUNT: the CST-63s found %d | the LB-distribution: %s' % (
    len(cands), dict(sorted(Counter(lb for lb, _ in cands).items()))))
log('    THE LB-BEST: %s' % cands[:5])
json.dump(cands[:40], open('ii19_phunt4_cands.json', 'wt'))
log('DONE — THE LB-METRIC HUNT!!')
