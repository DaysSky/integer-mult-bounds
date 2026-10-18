"""THE MIN-MINIS SEARCH (ii19_p111w2e.py) — THE RANDOMIZED-RESTART!!
THE ONE-USE STAR-ASSIGNMENT: the 9 stars x the tail-pools (~38/star: the sources + the
helpers!!): the sequential greedy is FRAGILE (the chain-tie-breaks + the orderings!!).
THE SEARCH: the randomized restarts (the orders + the pool-shuffles!!) -> THE MIN-MINIS
(the target <= 8 (the R <= 428: THE CROSSING!!!)!!!
"""
import gzip, json, random, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
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
STARS_NEW, WiBAS = [], []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS_NEW.append(s_new)
    WiBAS.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))

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

val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
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
CONT = {}
for r in range(nreg0):
    proj = 0
    for b in range(v0):
        if (val[r] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[r] = proj
POOLS = [[r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
          and in_W(FBAS[cur[r]], WiBAS[si])] for si in range(9)]
log('(0) the pools: %s' % [len(p) for p in POOLS])

def attempt(rng):
    """one randomized attempt: the order + the pool-shuffles -> (the minis, the sols!!)"""
    order = list(range(9))
    rng.shuffle(order)
    used = set()
    sols = {}
    minis = []
    for si in order:
        s = STARS_NEW[si]
        pool = [r for r in POOLS[si] if r not in used and CONT[r]]
        rng.shuffle(pool)
        piv = {}
        for r in pool:
            x = CONT[r]
            chain = 1 << r
            while x:
                p = (x & -x).bit_length() - 1
                if p in piv:
                    x2, m2 = piv[p]
                    x ^= x2
                    chain |= m2
                else:
                    piv[p] = (x, chain)
                    break
        x = s
        chain = 0
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2
                chain |= m2
            else:
                break
        if x == 0:
            sol = [r for r in pool if (chain >> r) & 1]
            used.update(sol)
            sols[si] = sol
        else:
            # THE RESIDUE: try the MINI-ROUTE (the fresh e_u-copies!!) — count only!!
            res_bits = [i for i in range(111) if (x >> i) & 1]
            minis.extend((si, u) for u in res_bits)
            sols[si] = [r for r in pool if (chain >> r) & 1]
            used.update(sols[si])
    return len(minis), sols, minis

rng = random.Random(111)
best = (999, None, None)
for trial in range(4000):
    m, sols, minis = attempt(rng)
    if m < best[0]:
        best = (m, sols, minis)
        log('    the trial %d: THE MINIS %d %s' % (trial, m, 'THE TARGET!!!' if m <= 8 else ''))
        if m <= 8:
            break
log('(1) THE BEST: the minis %d (the R = %d!!) %s' % (
    best[0], 420 + best[0], 'UNDER THE CROSSING (428)!!!' if best[0] <= 8 else 'OVER — keep searching!!'))
if best[2] is not None:
    log('    the minis: %s' % best[2][:20])
log('DONE — THE MIN-MINIS SEARCH!!')
