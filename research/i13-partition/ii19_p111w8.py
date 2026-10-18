"""THE P111-CLASS WORD — THE FULL BUILD v2 (ii19_p111w8.py)!!!
THE COMPLETE-DESIGN (post the B-scratch-discovery!!!):
- THE FRAMES: THE FULL-R420 (the dropped-vectors INCLUDED: the whole climb-structure ✓!!)
- THE +9-MIMICRY-HELPERS (the dropped-sources' B-scratch-roles (the chains mapped!!!))
- THE +9-FRESH-RETS (the star-builds (the pollution-free!!)) + THE +17-MINIS
- THE COMPUTED-D + THE C (the H4!!) + THE FULL-REPLAY + THE EMISSION!!!
THE R = 420 + 17 + 9 + 9 = 455 | THE EXPECTED ~-3.3% (THE +20-POINT RECORD vs the word4!!)
"""
import gzip, json, time
from collections import Counter
from fractions import Fraction
W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
SOLJ = json.load(open('ii19_p111_sol.json'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = SOLJ['rm']
SOLS = {int(k): v for k, v in SOLJ['sols'].items()}
MINIS = [tuple(m) for m in SOLJ['minis']]
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']

# THE REGISTER-MAP: the sources 0..110 | the targets V..2V-1 | the helpers 222+!!
MINI_BASE = 222 + R0                    # 642
FRESH_BASE = MINI_BASE + len(MINIS)     # 659
MIMIC_BASE = FRESH_BASE + 9             # 668
R = R0 + len(MINIS) + 9 + 9
nreg = 2 * V + R
log('(0) the minis %d | THE R = %d (the minis %d + the fresh-rets 9 + the mimicry 9!!)' % (
    len(MINIS), R, len(MINIS)))

def nh(h): return h - 18
def map_reg(r):
    """the general-map: the kept-sources/targets/helpers; the DROPPED-sources -> the mimicry h_d!!"""
    if r < v0:
        if r in old2new:
            return old2new[r]
        return MIMIC_BASE + RM.index(r)      # the dropped-source -> the h_d!!!
    if r < 2 * v0:
        return V + old2new[r - v0] if (r - v0) in old2new else None
    return nh(r)
MIMIC = {r: MIMIC_BASE + RM.index(r) for r in RM}
MINI_ID = {(si, u): MINI_BASE + j for j, (si, u) in enumerate(MINIS)}
FRESHRET = {si: FRESH_BASE + si for si in range(9)}

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

# ============ (1) THE FRAMES: THE FULL-R420 (the vectors AS-IS!!!) ============
frames_vecs = [[[v for v in lines[i]] if isinstance(i, int) and i < v0 else list(i) for i in fl] for fl in frames0]
FDIM = [len(basis_of(f)) if f else 0 for f in frames0]
FULL_F = 1
WiF = [W['final'][v0 + L] for L in RM]
log('(1) the frames: %d (THE FULL-R420 (the dims: the full %d, the W_i %s!!))' % (
    len(frames_vecs), FDIM[FULL_F], [FDIM[f] for f in WiF]))
assert all(FDIM[f] == 7 for f in WiF)

# ============ (2) THE GATES' PROJECTION (the mimicry-included!!!) ============
# THE D: the kept-targets' (the srcs: the helpers-only (the H2 ✓!!)!
D = []
for F, d, srcs in W['D']:
    if (d - v0) in old2new:
        D.append([0, V + old2new[d - v0], [nh(s) for s in srcs]])
# THE A: the srcs: the KEPT-only (the dropped-src-pruning (the A-time-pure ✓!!))!
A = []
for F, d, srcs in W['A']:
    nd = map_reg(d)
    if nd is None or nd >= MIMIC_BASE:
        continue                       # the A: the dropped-srcs (the 27!!) pruned (the pure ✓)!!
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None and x < MIMIC_BASE]
    if not nsrcs:
        continue
    A.append([F, nd, nsrcs])
# THE B: the FULL-MIMICRY (the s_d-reads/writes -> the h_d!!)!!
B = []
for F, d, srcs in W['B']:
    nd = map_reg(d)
    if nd is None:
        continue                       # the dropped-TARGETS (no registers!!)!!
    nsrcs = [map_reg(s) for s in srcs]
    nsrcs = [x for x in nsrcs if x is not None]
    if not nsrcs:
        continue
    B.append([F, nd, nsrcs])
log('(2) the gates: D %d | A %d | B %d (the mimicry-writes/read included!!)' % (len(D), len(A), len(B)))

# ============ (3) THE STAR-BUILDS + THE MINIS (the A-tail!!) ============
# the pools' cur-tracking (the R420's own-A-replay: the w6's-pools ✓ (the SOLS ✓!!))!
val0 = [1 << r for r in range(nreg0)]
cur0 = list(W['start'])
FBAS0 = [basis_of(f) if f else [] for f in frames0]
FDIM0 = [len(b) for b in FBAS0]
def in_Wb(fbas, wbas):
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
    for s in srcs: val0[d] ^= val0[s]
for F, d, srcs in W['A']:
    x = 0
    for s in srcs: x ^= val0[s]
    val0[d] ^= x
    for s in srcs:
        if FDIM0[cur0[s]] < FDIM0[F] or not in_Wb(FBAS0[cur0[s]], FBAS0[F]):
            cur0[s] = F
    cur0[d] = F
log('(3) the base-replay done!!')
# THE MINIS: the fresh e_u-copies (the SOL-residues' bits!!)
for j, (si, u) in enumerate(MINIS):
    u_old = kept[u]
    A.append([cur0[u_old], MINI_ID[(si, u)], [u]])
# THE STAR-BUILDS: the fresh-rets (the full SOLs (the w6's algebra ✓!!))!!
for si in range(9):
    srcs = [x for r in SOLS[si] if (x := map_reg(r)) is not None and x < MIMIC_BASE]
    srcs += [MINI_ID[(si, u)] for (s2, u) in MINIS if s2 == si]
    A.append([WiF[si], FRESHRET[si], srcs])
    log('    the star %d -> the fresh-ret %d: %d srcs' % (si, FRESHRET[si], len(srcs)))

# ============ (4) THE SCATTER (the W-solve over the stars!!) ============
STARS = []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
BROWS = []
for t in kept:
    m = 1 << old2new[t]
    for u in kept:
        if u != t and iph(lines[t], lines[u]) == 0:
            m |= 1 << old2new[u]
    BROWS.append(m)
piv = {}
for si in range(9):
    x = STARS[si]
    chain = 1 << si
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]
            x ^= x2
            chain ^= m2
        else:
            piv[p] = (x, chain)
            break
assert len(piv) == 9
SCAT = []
for t in range(V):
    x = BROWS[t]
    chain = 0
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]
            x ^= x2
            chain ^= m2
        else:
            raise SystemExit('THE W-SOLVE FAILS at t=%d!!' % t)
    SCAT.append([si for si in range(9) if (chain >> si) & 1])
log('(4) the scatter: the row-sizes %s' % dict(sorted(Counter(len(s) for s in SCAT).items())))

# ============ (5) THE COMPUTED-D (the exact-cancel!!) ============
val = [1 << r for r in range(nreg)]
for F, d, srcs in A:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
for t in range(V):
    for si in SCAT[t]:
        val[V + t] ^= val[FRESHRET[si]]
for F, d, srcs in B:
    for s in srcs: val[d] ^= val[s]
DNEW = []
nline_resid = 0
for t in range(V):
    resid = val[V + t] ^ (1 << (V + t)) ^ (1 << t)
    lr = [b for b in range(V) if (resid >> b) & 1]
    rr = [b for b in range(2 * V, nreg) if (resid >> b) & 1]
    if lr:
        nline_resid += 1
        if nline_resid <= 3:
            log('    !!! THE LINE-RESIDUE at t=%d: %s' % (t, lr[:8]))
    DNEW.append([0, V + t, rr])
log('(5) THE COMPUTED-D: the line-residues %d/%d | the src-sizes %s' % (
    nline_resid, V, dict(sorted(Counter(len(g[2]) for g in DNEW).items()))))
D = DNEW

# ============ (6) THE C (the H4!!) ============
zg = [[F, d, srcs] for F, d, srcs in A + B if not (V <= d < 2 * V)]
C = [[FULL_F, d, list(srcs)] for F, d, srcs in reversed(zg)]
log('(6) THE C: %d' % len(C))

# ============ (7) THE STARTS + FINALS!! ============
start = [0] * nreg
for s_new in range(V):
    start[s_new] = 2 + kept[s_new]     # the R420's singleton-frames (the FULL ✓!!)
final = [FULL_F] * nreg
for t in range(V):
    final[V + t] = W['final'][v0 + kept[t]]   # the R420's perp-frames (the FULL (dim-7!!))!

# ============ (8) THE FULL REPLAY (the verification!!) ============
val = [1 << r for r in range(nreg)]
for F, d, srcs in D:
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in A:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
for t in range(V):
    for si in SCAT[t]:
        val[V + t] ^= val[FRESHRET[si]]
for F, d, srcs in B:
    for s in srcs: val[d] ^= val[s]
for F, d, srcs in C:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
bad = []
for r in range(nreg):
    want = (1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r
    if val[r] != want:
        bad.append(r)
log('(7) THE FULL REPLAY: the bad %d/%d %s' % (len(bad), nreg, 'THE FINALS PASS!!!!' if not bad else '!!'))
for r in bad[:6]:
    diff = val[r] ^ ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r)
    log('    r=%d (%s): the line-res %s | the reg-res %s' % (
        r, 'target' if V <= r < 2 * V else ('source' if r < V else 'helper'),
        [b for b in range(V) if (diff >> b) & 1][:8],
        [b for b in range(V, nreg) if (diff >> b) & 1][:8]))

# ============ (9) THE EMISSION!! ============
word = dict(
    convention='bitE8/1+mut', label='II19-P111-native',
    form=dict(num=[[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1]], den=2),
    h=H, v=V, R=R,
    lines=[list(lines[o]) for o in kept],
    frames=frames_vecs,
    start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=[FRESHRET[si] for si in range(9)],
    ret_frames=[WiF[si] for si in range(9)],
    scatter=SCAT,
)
json.dump(word, open('ii19_p111_word.json', 'wt'))
log('(8) THE WORD EMITTED (ii19_p111_word.json!!): R=%d v=%d h=%d' % (R, V, H))
log('    the gates: D %d | A %d | B %d | C %d' % (len(D), len(A), len(B), len(C)))
log('DONE — THE P111-CLASS WORD BUILD v2!!')
