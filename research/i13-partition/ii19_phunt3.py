"""THE SMART PUNCTURE-HUNT (ii19_phunt3.py) — THE NON-⊥-CLIQUES!!
THE THEORY: the minis ~ the multi-star conflict ~ Sum |star_i ∩ star_j| ~ controlled by
the REMOVED LINES' pairwise structure: the NON-⊥-cliques (the 9 removed lines pairwise
ip != 0!!) -> the minimal star-overlaps!!!  + THE DEEPER SOLVE (the 200 restarts!!)
THE TARGET: the minis <= 8 (the R <= 428: THE CROSSING!!!)
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

# (1) THE NON-⊥-GRAPH + THE CLIQUE-SAMPLING!!
NON = [[j for j in range(120) if j != i and iph(lines[i], lines[j]) != 0] for i in range(120)]
log('(1) the non-perp graph: the degrees %s' % dict(sorted(Counter(len(n) for n in NON).items())))

def evaluate(rm, restarts=200):
    kept = [i for i in range(120) if i not in rm]
    old2new = {o: n for n, o in enumerate(kept)}
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
        return None, None, None
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
    # the star-overlap metric!!
    ov = sum(bin(STARS[i] & STARS[j]).count('1') for i in range(9) for j in range(i + 1, 9))
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
    return best, ov, pools

# (2) THE CLIQUE-HUNT (the random cliques + the greedy-growth!!!)!
rng = random.Random(111)
log('(2) THE CLIQUE-HUNT (the 9-cliques in the non-perp graph!!):')
best = (999, None, None)
tried = set()
def grow_clique(rng):
    c = [rng.randrange(120)]
    while len(c) < 9:
        cands = set(NON[c[0]])
        for x in c[1:]:
            cands &= set(NON[x])
        cands = [x for x in cands if x not in c]
        if not cands: return None
        c.append(rng.choice(sorted(cands)))
    return sorted(c)

n_ok = 0
for trial in range(400):
    rm = grow_clique(rng)
    if rm is None or tuple(rm) in tried: continue
    tried.add(tuple(rm))
    m, ov, pools = evaluate(rm)
    if m is None: continue
    n_ok += 1
    if m < best[0]:
        best = (m, rm, ov)
        log('    the trial %d: rm=%s -> THE MINIS %d (the overlap %d!!) %s' % (
            trial, rm, m, ov, 'THE TARGET!!!' if m <= 8 else ''))
        if m <= 8: break
# (2b) THE DEEP RANDOM HUNT (the 200-restart solve + the long run!!)
rng2 = random.Random(4242)
log('(2b) THE DEEP RANDOM HUNT (the 200-restart solve!!):')
best = (999, None, None)
tried = set()
n63 = 0
for trial in range(500):
    rm = tuple(sorted(rng2.sample(range(120), 9)))
    if rm in tried: continue
    tried.add(rm)
    m, ov, pools = evaluate(list(rm))
    if m is None: continue
    n63 += 1
    if m < best[0]:
        best = (m, list(rm), ov)
        log('    the trial %d: rm=%s -> THE MINIS %d (the overlap %d!!) %s' % (
            trial, list(rm), m, ov, 'THE TARGET!!!' if m <= 8 else ''))
        if m <= 8: break
log('(3) THE RESULT: the CST-63 punctures: %d | THE BEST: %s' % (
    n63, 'the minis %d (rm=%s, the overlap %d!!) | the R = %d' % (best[0], best[1], best[2], 420 + best[0]) if best[1] else 'NONE!!'))
log('DONE — THE SMART HUNT!!')
