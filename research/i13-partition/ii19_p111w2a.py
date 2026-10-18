"""THE STAR-SOLVE FEASIBILITY (ii19_p111w2a.py) — THE ONE-USE CONFLICT MEASUREMENT!!
THE RETS' x-parts = THE 9 STARS FORCED (the only span-7 codewords!!) -> the builds at the
dim-7 W_i = span(perp'(L_i))!! -> THE ONE-CLIMB LAW: each piece (a cell/source) serves
ONE dim-7 frame only!!  THE MEASUREMENT: the R420's helpers' contents vs the stars:
the incidence + the one-use-greedy + the residues!!
"""
import gzip, json, time
from collections import Counter, defaultdict
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
n = 111
lines = W['lines']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2
# the punctured perps (the NEW indexing!!)
PERP = [0] * n
for ti, t in enumerate(kept):
    m = 1 << ti
    for ui, u in enumerate(kept):
        if ui != ti and iph(lines[t], lines[u]) == 0:
            m |= 1 << ui
    PERP[ti] = m
log('(0) the punctured perps: %s' % dict(sorted(Counter(bin(p).count('1') for p in PERP).items())))

# (1) THE 9 STARS (the punctured-star indicators in the NEW indexing!!)
STARS = []
for L in RM:
    # the star = perp'(L) = the lines (the kept!!) ⊥ L!!
    m = 0
    for ui, u in enumerate(kept):
        if iph(lines[L], lines[u]) == 0:
            m |= 1 << ui
    STARS.append(m)
log('(1) the 9 stars: the weights %s (the P111-class!!)' % [bin(s).count('1') for s in STARS])
# the star-independence check (the 9 span-7s!!)
bx = {}
for s in STARS:
    x = s
    while x:
        p = (x & -x).bit_length() - 1
        if p in bx: x ^= bx[p]
        else: bx[p] = x; break
log('    the star-independence: %d/9 (the CST-63 puncture ✓!!)' % len(bx))

# (2) THE R420's HELPER-CONTENTS: the replay-lite (the D -> A!!)!!
v0, h0 = W['v'], W['h']
nreg0 = len(W['start'])
val = [1 << r for r in range(nreg0)]
# the D-phase: the self-bits (the pre-A: the helpers at the self-bits!!)
for F, d, srcs in W['D']:
    for s in srcs:
        val[d] ^= val[s]
log('(2) the D-phase done (%d gates!!)' % len(W['D']))
# the A-phase: the builds (the x-parts accumulate: the MULTI-BUILT helpers!!)!!
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs:
        x ^= val[s]
    val[d] ^= x          # the ACCUMULATION (the correct multi-build semantics!!)
log('    the A-phase done (%d gates!!)' % len(W['A']))
# the helpers' contents (the x-parts!!): the helpers 240..659!!
CONT = {}
for h in range(2 * v0, nreg0):
    c = val[h] & ~((1 << v0) - 1)
    c = 0
    for b in range(v0):
        if (val[h] >> b) & 1:
            c |= 1 << b
    # the content's projection to the kept lines (the NEW indexing!!)
    proj = 0
    for b in range(v0):
        if (val[h] >> b) & 1 and b in old2new:
            proj |= 1 << old2new[b]
    CONT[h] = proj
log('    the helper-contents: %d | the content-weights: %s' % (
    len(CONT), dict(sorted(Counter(bin(c).count('1') for c in CONT.values()).items()))))

# (3) THE STAR-INCIDENCE: the helpers with the content ⊆ the star!!
log('(3) THE STAR-INCIDENCE (the content ⊆ the star!!):')
pools = []
for si, s in enumerate(STARS):
    pool = [h for h, c in CONT.items() if c and (c & ~s) == 0]
    pools.append(pool)
    log('    the star %d (the weight %d!!): the pool %d (the weights %s!!)' % (
        si, bin(s).count('1'), len(pool),
        dict(sorted(Counter(bin(CONT[h]).count('1') for h in pool).items()))))
# the multi-star helpers (the one-use conflict volume!!)
multi = Counter()
for h, c in CONT.items():
    if not c: continue
    k = sum(1 for s in STARS if (c & ~s) == 0)
    if k >= 2:
        multi[k] += 1
log('    THE CONFLICT: the helpers in >=2 pools: %s (the one-use volume!!)' % dict(sorted(multi.items())))

# (4) THE ONE-USE GREEDY-SOLVE (the sequential: the star_i uses the unused pool!!) + the residues!!
log('(4) THE SEQUENTIAL ONE-USE GREEDY (the star_1 -> the star_9!!):')
used = set()
ok_all = True
for si, s in enumerate(STARS):
    pool = [h for h in pools[si] if h not in used]
    # the GF(2)-solve: s = XOR of the pool-contents!!
    bx2 = {}
    src_of = {}
    for h in pool:
        x = CONT[h]
        chain = [h]
        while x:
            p = (x & -x).bit_length() - 1
            if p in bx2:
                x ^= bx2[p][0]
                chain = chain[1:] if False else chain
                # track: the XOR-chain!!
                x = CONT[h]
                for hh in src_of[p]:
                    pass
                # simpler: recompute below!!
                break
            else:
                bx2[p] = (CONT[h],)
                src_of[p] = (h,)
                break
    # the full elimination solve!!
    piv = {}
    for h in pool:
        x = CONT[h]
        chain = 1 << h   # the used-mask over the helper-ids (a set!!)
        while x:
            p = (x & -x).bit_length() - 1
            if p in piv:
                x2, m2 = piv[p]
                x ^= x2
                chain |= m2
            else:
                piv[p] = (x, chain)
                break
    # the star's solve: reduce the star over the pivots!!
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
        # the solution: the chain-bits!!
        sol = [h for h in pool if (chain >> h) & 1]
        for h in sol: used.add(h)
        log('    the star %d: SOLVED with %d helpers (the leftover-pool %d!!)' % (
            si, len(sol), len([h for h in pools[si] if h not in used])))
    else:
        ok_all = False
        log('    the star %d: THE RESIDUE (the weight %d!!) — THE ONE-USE FAILURE!!' % (
            si, bin(x).count('1')))
log('    THE ALL-SOLVED: %s' % ok_all)
log('DONE — THE STAR-SOLVE FEASIBILITY!!')
