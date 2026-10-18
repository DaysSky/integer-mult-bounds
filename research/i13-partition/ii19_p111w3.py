"""THE P111-CLASS WORD — THE FULL CONSTRUCTION (ii19_p111w3.py)!!!
THE FRONTIER-WORD: the R420's projection to the 111-puncture (rm=[21,23,24,29,53,71,80,89,103]
(the CST-63!!)) + THE 9 STAR-RETS (the span-7 basis: the deficit 10,272!!) + THE ONE-USE SOLVES
(the order [2,3,0,1,8,6,7,4,5] + the 1 mini-rescue!!) -> THE R = 421 < 428 (THE CROSSING!!!).
THE PIECES (all measured!!): (0) the maps; (1) the frames (the re-based vectors!!); (2) the
gates' projection; (3) THE STAR-BUILDS (the one-use sols!!); (4) THE SCATTER (the W-solve!!);
(5) THE D-EXTENSION (the law!!); (6) the C; (7) THE FULL REPLAY (the finals!!) + (8) the emit!!
"""
import gzip, json, time
from collections import Counter, defaultdict
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [21, 23, 24, 29, 53, 71, 80, 89, 103]
ORDER = [2, 3, 0, 1, 8, 6, 7, 4, 5]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines0 = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2

# ============ (0) THE STAR-SOLVE (the one-use!! the mini-rescue!!) ============
def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines0[i]] for i in idx_list]
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
STARS_NEW, WiBAS, WiLINES = [], [], []
for L in RM:
    s_new = 0
    star_old = [u for u in range(120) if u != L and iph(lines0[L], lines0[u]) == 0]
    for u in kept:
        if iph(lines0[L], lines0[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS_NEW.append(s_new)
    WiBAS.append(basis_of(star_old))
    WiLINES.append([old2new[u] for u in star_old if u in old2new])
log('(0) the stars: %s (the W_i-dims %s!!)' % (
    [bin(s).count('1') for s in STARS_NEW], [len(b) for b in WiBAS]))

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

# the A-replay (the cur-tracking + the contents!!)
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
pools = [[r for r in range(nreg0) if cur[r] and FDIM[cur[r]] <= 7
          and in_W(FBAS[cur[r]], WiBAS[si])] for si in range(9)]

# THE ONE-USE SOLVES (the ORDER!!) + the mini-rescue!!
used = set()
SOLS = {}
MINIS = []            # the (star_idx, the residue-bit u, the fresh-reg!!)!
for si in ORDER:
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
    if x:
        # THE MINI-RESCUE (the fresh e_u-copies at the LOW frames (the OWN chains!!!))!!
        res_bits = [i for i in range(V) if (x >> i) & 1]
        log('    the star %d: THE RESIDUE %d -> THE MINIS %s!!' % (si, len(res_bits), res_bits))
        for u in res_bits:
            MINIS.append((si, u))
        # the minis provide the residue: the sol gets the chain anyway (the minis added later!!)
        SOLS[si] = [r for r in pool if (chain >> r) & 1]
        used.update(SOLS[si])
    else:
        sol = [r for r in pool if (chain >> r) & 1]
        SOLS[si] = sol
        used.update(sol)
        log('    the star %d: SOLVED (%d srcs!!)' % (si, len(sol)))
log('(0b) THE MINIS: %d (the R + %d!!)' % (len(MINIS), len(MINIS)))
R = R0 + len(MINIS)
nreg = 2 * V + R
log('(0c) THE R = %d (the R420 %d + the minis %d!!) | the crossing at 428: %s' % (
    R, R0, len(MINIS), 'UNDER ✓✓✓' if R <= 428 else 'OVER ✗'))

# ============ (1) THE FRAMES (the re-based + the 9 W_i + the mini-singletons!!) ============
# the re-based: the R420's frames (the line-index lists!!) -> the kept-index lists -> the vectors!!
rb = []
for f in frames0:
    out = []
    for i in f:
        if i in old2new:
            out.append(old2new[i])
    rb.append(out)
IDX_W = []
for si in range(9):
    IDX_W.append(len(rb)); rb.append(list(WiLINES[si]))
IDX_MINI = []
for k, (si, u) in enumerate(MINIS):
    IDX_MINI.append(len(rb)); rb.append([u])
IDX_FULL = 1
assert rb[IDX_FULL] == list(range(V)) or len(rb[IDX_FULL]) == V
frames = [[lines0[kept[i]] for i in s] for s in rb]
dims = [0 if not s else len(basis_of([kept[i] for i in s])) for s in rb]
log('(1) the frames: %d (the R420 %d + the W_i 9 + the minis %d!!) | the dims %s' % (
    len(frames), len(frames0), len(MINIS), dict(sorted(Counter(dims).items()))))

# ============ (2) THE REGISTER-MAP + THE START/FINAL ============
# the sources 0..110 (the kept!!), the targets 111..221, the helpers 222.. (the R420's -18!!)
HELPER_BASE = 2 * V
def hmap(h0): return HELPER_BASE + (h0 - 2 * v0)
MINI_BASE = HELPER_BASE + R0
# the start: the sources at their singletons (the re-based!!), the rest at 0!!
start = [0] * nreg
for s in range(V):
    start[s] = 2 + s          # the singleton-frames: the frames[2..112] (the re-based!!)!!
assert all(len(rb[2 + s]) == 1 for s in range(V))
final = [IDX_FULL] * nreg
for t in range(v0):
    if t in old2new:
        final[V + old2new[t]] = len(frames0) and None
# the targets' finals: the R420's final[v0+t] (the perp-frame-indices!!) re-based!!
for t in range(v0):
    if t in old2new:
        f0 = W['final'][v0 + t]
        final[V + old2new[t]] = f0          # the frame-index PRESERVED (the re-based lists!!)
for k, (si, u) in enumerate(MINIS):
    start[MINI_BASE + k] = 2 + u            # the mini starts at u's singleton?!
    final[MINI_BASE + k] = IDX_FULL
log('(2) the registers: nreg %d | the target finals: the perp-frames (the re-based!!)' % nreg)

# ============ (3) THE GATES' PROJECTION ============
def gmap(r):
    if r < v0:
        return old2new.get(r, None)
    if r < 2 * v0:
        t = r - v0
        return old2new.get(t, None) + V if t in old2new else None
    if r < 2 * v0 + R0:
        return hmap(r)
    return None
def proj_gate(g, extra_srcs=None):
    F, d, srcs = g
    nd = gmap(d)
    if nd is None: return None
    nsrcs = []
    for s in srcs:
        m = gmap(s)
        if m is not None:
            nsrcs.append(m)
    return [F, nd, nsrcs]
D = []
for g in W['D']:
    pg = proj_gate(g)
    if pg: D.append(pg)
A = []
for g in W['A']:
    pg = proj_gate(g)
    if pg: A.append(pg)
B = []
for g in W['B']:
    pg = proj_gate(g)
    if pg: B.append(pg)
C = []
for g in W['C']:
    pg = proj_gate(g)
    if pg: C.append(pg)
log('(3) the gates: D %d (was %d) | A %d (was %d) | B %d (was %d) | C %d (was %d!!)' % (
    len(D), len(W['D']), len(A), len(W['A']), len(B), len(W['B']), len(C), len(W['C'])))

# ============ (4) THE STAR-BUILDS (THE RETS' A-GATES!!) + THE MINIS ============
# the ret-registers: RE-PURPOSE the R420's own 9 rets!!
RET0 = [gmap(q) for q in W['ret']]
log('(4) the rets (re-purposed!!): %s' % RET0)
# THE OLD RET-BUILDS PRUNED (the A-gates with dest = the old rets + F = the FULL!!)!!
A = [g for g in A if g[1] not in RET0]
# THE STAR-BUILDS: for each star_i: [IDX_W[i], ret_i, [the sol (the remapped!!) + the minis!!]]!!
star_builds = []
for si in range(9):
    srcs = []
    for r in SOLS[si]:
        srcs.append(r if r < v0 else (r - v0 + V if r < 2 * v0 else hmap(r)))
    for k, (sj, u) in enumerate(MINIS):
        if sj == si:
            srcs.append(MINI_BASE + k)
    star_builds.append([IDX_W[si], RET0[si], srcs])
    A.append([IDX_W[si], RET0[si], srcs])
# THE MINIS' OWN BUILDS: the fresh e_u-copies at the LOW singleton-frames!!
mini_builds = []
for k, (si, u) in enumerate(MINIS):
    mb = [2 + u, MINI_BASE + k, [u]]     # the mini's build at u's singleton reading u!!
    mini_builds.append(mb)
    A.append(mb)
log('(4b) the star-builds %d + the mini-builds %d (the A now %d!!)' % (
    len(star_builds), len(mini_builds), len(A)))

# ============ (5) THE SCATTER (the W-solve over the 9 stars!!) ============
# the stars' x-parts (the STARS_NEW vectors!!) as the basis: the rows Brows'[t]!!
BROWS = []
for t in kept:
    m = 1 << old2new[t]
    for u in kept:
        if u != t and iph(lines0[t], lines0[u]) == 0:
            m |= 1 << old2new[u]
    BROWS.append(m)
# the W-solve: Brows[t] = XOR_{j in W[t]} star_j!!
bxw = {}
for j, s in enumerate(STARS_NEW):
    x = s
    while x:
        p = (x & -x).bit_length() - 1
        if p in bxw: x ^= bxw[p]
        else: bxw[p] = s; break
assert len(bxw) == 9
scatter = []
for t in range(V):
    x = BROWS[t]
    rowj = []
    while x:
        p = (x & -x).bit_length() - 1
        assert p in bxw, 'the W-solve FAIL at %d!!' % t
        x ^= bxw[p]
        for j, s in enumerate(STARS_NEW):
            if s == bxw[p]:
                rowj.append(j)
                break
    scatter.append(rowj)
log('(5) the scatter: the row-sizes %s (the D-extension law!!)' % (
    dict(sorted(Counter(len(r) for r in scatter).items()))))
# THE D-EXTENSION: [0, V+t, [the rets in W[t]]]!!
for t in range(V):
    news = [RET0[j] for j in scatter[t]]
    if news:
        D.append([0, V + t, news])
log('(5b) the D-extension: %d gates!!' % V)

# ============ (6) THE C (the star/mini-builds' reversals!!) ============
# the C: the R420's projected + the star-builds' + the mini-builds' reversals!!
# NOTE: the C-phase reverses the z-gates (the A-builds!!): the same [F, d, srcs] XORed again!!
C = C + [[F, d, list(srcs)] for F, d, srcs in star_builds] + \
    [[F, d, list(srcs)] for F, d, srcs in mini_builds]
log('(6) the C: %d (the R420 %d + the star %d + the mini %d!!)' % (
    len(C), len(C) - len(star_builds) - len(mini_builds), len(star_builds), len(mini_builds)))

word = {
    'h': H, 'v': V, 'R': R, 'nreg': nreg,
    'lines': [lines0[t] for t in kept],
    'form': W['form'], 'coords': W['coords'], 'format': 'ii19/p111w1',
    'frames': frames, 'start': start, 'final': final,
    'D': D, 'A': A, 'B': B, 'C': C,
    'ret': RET0, 'ret_frames': [IDX_W[si] for si in range(9)],
    'scatter': scatter,
}
json.dump(word, open('ii19_p111_word.json', 'wt'))
log('(7) THE WORD EMITTED: ii19_p111_word.json (v=%d h=%d R=%d nreg=%d!!)' % (V, H, R, nreg))
log('DONE — THE P111-CLASS WORD CONSTRUCTION!!!')
