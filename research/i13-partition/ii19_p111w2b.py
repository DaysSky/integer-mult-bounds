"""THE STAR-SOLVE v2 (ii19_p111w2b.py) — THE FRAME-POOLS (the cur-span ⊆ W_i!!)
THE CORRECT CRITERION (the legality!!): the src's CUR-FRAME's span ⊆ W_i (NOT the content
⊆ the star!! the contents XOR-cancel!!).  THE R420's own B-gates read at the dim-7 perps
(the same one-climb law!!) -> THE POOLS: the helpers' A-END curs with the span ⊆ W_i!!
THE MEASURE: the A-replay WITH the frame-tracking -> the pools -> the one-use greedy!!
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

# (0) THE FRAMES' SPANS (the OLD indexing: the 120-line vectors!!) + the dims!!
def span_dim_list(idx_list):
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
    return len(bas), bas

FDIM = {}
for fi, f in enumerate(frames0):
    if f:
        d, _ = span_dim_list(f)
        FDIM[fi] = d
    else:
        FDIM[fi] = 0
log('(0) the frames: %d | the dims: %s' % (len(frames0),
    dict(sorted(Counter(FDIM.values()).items()))))

# (1) THE W_i-SPANS (the star-spans: the OLD-line-index sets -> the spans!!)
STARS_OLD = []
for L in RM:
    s = [u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]
    STARS_OLD.append(s)
WiBAS = []
for s in STARS_OLD:
    _, bas = span_dim_list(s)
    WiBAS.append(bas)
log('(1) the W_i-spans: %s' % [len(b) for b in WiBAS])

# the span-inclusion test: a frame's basis ⊆ W_i's span!!
def in_W(bas_frame, wbas):
    # is each vector of bas_frame in the span of wbas?!
    for y in bas_frame:
        z = y
        for b in wbas:
            p = next((c for c in range(8) if b[c] != 0), None)
            if p is not None and z[p] != 0:
                f = z[p] / b[p]
                z = [a2 - f * c for a2, c in zip(z, b)]
        if any(z[c] != 0 for c in range(8)):
            return False
    return True

# (2) THE A-REPLAY WITH THE FRAME-TRACKING (the cur-frames!!)
nreg0 = len(W['start'])
val = [1 << r for r in range(nreg0)]
cur = list(W['start'])
for F, d, srcs in W['D']:
    for s in srcs:
        val[d] ^= val[s]
log('(2) the D-phase done!!')
Aend_cur = {}
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs:
        x ^= val[s]
    val[d] ^= x
    cur[d] = F
log('    the A-phase done (%d!!)' % len(W['A']))
# the helpers' A-end curs (the frames!!)!!
helpers = range(2 * v0, nreg0)
curs = Counter(FDIM[cur[h]] for h in helpers)
log('    the A-end cur-dims (the helpers!!): %s' % dict(sorted(curs.items())))

# (3) THE POOLS: the helpers with cur-span ⊆ W_i!!
FRAME_SPAN = {}
for fi in range(len(frames0)):
    if frames0[fi]:
        _, bas = span_dim_list(frames0[fi])
        FRAME_SPAN[fi] = bas
log('(3) THE FRAME-POOLS (the cur-span ⊆ W_i!!):')
pools = []
for si in range(9):
    pool = []
    for h in helpers:
        c = cur[h]
        if c and FDIM[c] <= 7 and in_W(FRAME_SPAN[c], WiBAS[si]):
            pool.append(h)
        elif c == 0:
            pass  # the dim-0: usable anywhere?!
    pools.append(pool)
    log('    the W_%d: the pool %d (the cur-dims %s!!)' % (
        si, len(pool), dict(sorted(Counter(FDIM[cur[h]] for h in pool).items()))))
# the multi-pool (the conflict volume!!)
multi = Counter()
for h in helpers:
    k = sum(1 for si in range(9) if h in pools[si])
    if k >= 2: multi[k] += 1
log('    THE CONFLICT: the helpers in >=2 pools: %s' % dict(sorted(multi.items())))

# (4) THE ONE-USE GREEDY-SOLVE (the sequential: W_0 first!!)!!
log('(4) THE ONE-USE GREEDY (the star_0 -> the star_8!!):')
# the contents (the projected!!)!!
CONT = {}
for h in helpers:
    proj = 0
    for b in range(v0):
        if (val[h] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[h] = proj
used = set()
ok = True
for si in range(9):
    s = 0
    for u in STARS_OLD[si]:
        if u in old2new:
            s |= 1 << old2new[u]
    pool = [h for h in pools[si] if h not in used and CONT[h]]
    piv = {}
    for h in pool:
        x = CONT[h]
        chain = 1 << h
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
        sol = [h for h in pool if (chain >> h) & 1]
        used.update(sol)
        log('    the star %d: SOLVED (%d srcs; the new-used %d!!)' % (
            si, len(sol), len(sol)))
    else:
        ok = False
        log('    the star %d: THE RESIDUE %d (the pool %d!!) FAIL' % (
            si, bin(x).count('1'), len(pool)))
log('    THE ALL-SOLVED: %s' % ok)
log('DONE — THE STAR-SOLVE v2!!')
