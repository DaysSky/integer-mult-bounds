"""THE PUNCTURE-HUNT v2 (ii19_phunt2.py) — THE (CST-63 + MIN-MINIS)-PUNCTURE!!
THE DISCOVERY (ii19_p111w2e!!): the one-use tax is PUNCTURE-DEPENDENT (the multi-star
conflict bits!!): the best-found minis 33 (the R 453: 25 OVER the crossing!!).
THE HUNT: the random CST-63 punctures x the minis-solve -> THE (63, <=8)-PUNCTURE
(THE R <= 428: THE CROSSING!!!).
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

# the base-replay machinery (the puncture-independent parts: the R420's val/cur are
# puncture-independent (the OLD system!!) -> compute ONCE!!)
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
log('(0) the base-replay done (once!!)')

def evaluate(rm, restarts=60):
    """the puncture rm: the CST-check (the 9 independent span-7s!!) + the minis-solve!!"""
    kept = [i for i in range(120) if i not in rm]
    old2new = {o: n for n, o in enumerate(kept)}
    # the stars + the span-7-independence!!
    STARS, WiB = [], []
    for L in rm:
        s_new = 0
        star_old = [u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]
        for u in kept:
            if iph(lines[L], lines[u]) == 0:
                s_new |= 1 << old2new[u]
        STARS.append(s_new)
        WiB.append(basis_of(star_old))
    bx = {}
    for s in STARS:
        x = s
        while x:
            p = (x & -x).bit_length() - 1
            if p in bx: x ^= bx[p]
            else: bx[p] = x; break
    if len(bx) != 9:
        return None, None                    # NOT the CST-63!!
    # the pools!!
    CONT = {}
    for r in range(nreg0):
        proj = 0
        for b in range(v0):
            if (val[r] >> b) & 1 and b in old2new:
                proj |= 1 << old2new[b]
        CONT[r] = proj
    pools = []
    for si in range(9):
        pools.append([r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
                      and in_W(FBAS[cur[r]], WiB[si]) and CONT[r]])
    # the minis-solve (the randomized restarts!!)!
    rng = random.Random(hash(tuple(rm)) & 0xffff)
    best = 999
    for trial in range(restarts):
        order = list(range(9))
        rng.shuffle(order)
        used = set()
        minis = 0
        for si in order:
            s = STARS[si]
            pool = [r for r in pools[si] if r not in used]
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
                used.update(r for r in pool if (chain >> r) & 1)
            else:
                minis += bin(x).count('1')
                used.update(r for r in pool if (chain >> r) & 1)
        best = min(best, minis)
    return best, pools

# THE HUNT!!
rng = random.Random(111)
tried = set()
best = (999, None)
log('(1) THE HUNT (the CST-63 + the min-minis!!):')
n63 = 0
for trial in range(300):
    rm = tuple(sorted(rng.sample(range(120), 9)))
    if rm in tried: continue
    tried.add(rm)
    m, pools = evaluate(list(rm))
    if m is None: continue
    n63 += 1
    if m < best[0]:
        best = (m, rm)
        log('    the trial %d: rm=%s -> THE MINIS %d %s' % (
            trial, list(rm), m, 'THE TARGET (<=8)!!!' if m <= 8 else ''))
        if m <= 8:
            break
log('(2) THE HUNT-RESULT: the CST-63 punctures tried: %d | THE BEST: the minis %d (rm=%s!!) | the R = %d' % (
    n63, best[0], list(best[1]) if best[1] else None, 420 + best[0]))
log('DONE — THE PUNCTURE-HUNT v2!!')
