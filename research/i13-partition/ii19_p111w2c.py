"""THE STAR-SOLVE v3 (ii19_p111w2c.py) — THE COMPLETE TAIL-POOLS + THE PRUNE-CENSUS!!
THE INSERT-POINT (the A-TAIL!!): the star-builds [W_i, ret_i, srcs] inserted at the A's end:
the legal srcs = THE REGISTERS WHOSE CUR-SPAN ⊆ W_i (the sources at their last-ladder-cell
+ the helpers at their last-build-frame!!) — THE COMPLETE POOL!!!  + THE PRUNE-CENSUS (the
dead-helpers: the dropped-targets-only servants -> THE R-SHAVE!!)!
"""
import gzip, json, time
from collections import Counter, defaultdict
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
n = 111
lines = W['lines']
v0, h0 = W['v'], W['h']
frames0 = W['frames']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2

# the frames' bases (the span-tracking!!)
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
log('(0) the frames: %d | the dims: %s' % (len(frames0),
    dict(sorted(Counter(FDIM).items()))))

# the W_i (the star-spans!!)
WiBAS = []
STARS_NEW = []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS_NEW.append(s_new)
    WiBAS.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))
log('(1) the W_i-dims: %s | the star-weights %s' % (
    [len(b) for b in WiBAS], [bin(s).count('1') for s in STARS_NEW]))

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

# (2) THE FULL REPLAY: the D + the A WITH the cur-tracking (the A-END positions!!)!!
nreg0 = len(W['start'])
val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
for F, d, srcs in W['D']:
    for s in srcs:
        val[d] ^= val[s]
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs:
        x ^= val[s]
    val[d] ^= x
    for s in srcs:
        if FDIM[cur[s]] < FDIM[F] or not in_W(FBAS[cur[s]], FBAS[F]):
            cur[s] = F          # the srcs climb to F (the legal nested!!)
    cur[d] = F
log('(2) the A-replay done | the cur-dims at the A-END: the sources %s | the helpers %s' % (
    dict(sorted(Counter(FDIM[cur[s]] for s in range(v0)).items())),
    dict(sorted(Counter(FDIM[cur[h]] for h in range(2 * v0, nreg0)).items()))))

# (3) THE COMPLETE TAIL-POOLS: the registers with cur-span ⊆ W_i!!
pools = []
for si in range(9):
    pool = [r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
            and in_W(FBAS[cur[r]], WiBAS[si])]
    pools.append(pool)
    psrc = [r for r in pool if r < v0]
    phel = [r for r in pool if r >= 2 * v0]
    log('(3) the W_%d: the pool %d (the sources %d + the helpers %d!!)' % (
        si, len(pool), len(psrc), len(phel)))
multi = Counter()
for r in range(nreg0):
    k = sum(1 for si in range(9) if r in pools[si])
    if k >= 2: multi[k] += 1
log('    THE CONFLICT: %s' % dict(sorted(multi.items())))

# (4) THE ONE-USE GREEDY-SOLVE (the sequential!!) — the srcs' VALUES: the sources = their
#     own e_s (the self-bit!!) + the helpers' contents (the projected!!)!!
CONT = {}
for r in range(nreg0):
    proj = 0
    for b in range(v0):
        if (val[r] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[r] = proj
used = set()
ok = True
solall = []
for si in range(9):
    s = STARS_NEW[si]
    pool = [r for r in pools[si] if r not in used and CONT[r]]
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
        solall.append(sol)
        log('(4) the star %d: SOLVED (%d srcs: %d sources + %d helpers!!)' % (
            si, len(sol), len([r for r in sol if r < v0]),
            len([r for r in sol if r >= 2 * v0])))
    else:
        ok = False
        solall.append(None)
        log('(4) the star %d: THE RESIDUE %d (the pool %d!!) FAIL' % (
            si, bin(x).count('1'), len(pool)))
log('    THE ALL-SOLVED: %s' % ok)

# (5) THE PRUNE-CENSUS: the dead-helpers (the dropped-targets-only servants!!)
#     the usage: which helpers are READ (as srcs!!) by the kept targets' B-gates + the kept
#     helpers' A-builds + the D-gates + the C!!
readers = defaultdict(set)
for F, d, srcs in W['D']:
    for s in srcs:
        if s >= 2 * v0: readers[s].add(('D', d))
for F, d, srcs in W['A']:
    for s in srcs:
        readers[s].add(('A', d))
for F, d, srcs in W['B']:
    for s in srcs:
        readers[s].add(('B', d))
for F, d, srcs in W['C']:
    for s in srcs:
        readers[s].add(('C', d))
# the usage-classification: the helper's readers: the kept-targets vs the dropped!!
dead = []
alive = []
for h in range(2 * v0, nreg0):
    rs = readers.get(h, set())
    if not rs:
        dead.append(h)  # unread (the rets?! check!!)
        continue
    # the readers' dest-classes!!
    any_kept = False
    any_dropped = False
    for ph, d in rs:
        if ph in ('B', 'D') and v0 <= d < 2 * v0:
            if (d - v0) in old2new: any_kept = True
            else: any_dropped = True
        else:
            any_kept = True   # the A/C-reads: the kept helpers!!
    if any_kept: alive.append(h)
    else: dead.append(h)
log('(5) THE PRUNE-CENSUS: the helpers %d | the alive %d | THE DEAD (the prunable!!) %d' % (
    nreg0 - 2 * v0, len(alive), len(dead)))
log('    the dead-list (the first 30!!): %s' % dead[:30])
log('DONE — THE STAR-SOLVE v3 (the tail-pools + the prune!!)')
