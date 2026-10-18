"""THE P111-CLASS WORD — THE FULL BUILD (ii19_p111w7.py)!!!
THE CONSTRUCTION: the R420 projection + the star-builds (the solve-JSON!!) + the minis +
the scatter (the W-solve over the stars!!) + THE COMPUTED-D (the exact one-shot cancel!!) +
the C (the H4!!) + the full replay + the emission (the gcheck-format!!!).
THE REGISTERS: the sources 0..110 | the targets 111..221 | the helpers 222..(222+R-1!!)
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
OLDRETS = W['ret']

def nh(h): return h - 18
NEWRET = {si: nh(OLDRETS[si]) for si in range(9)}
MINI_BASE = 222 + R0
MINI_ID = {}
for j, (si, u) in enumerate(MINIS):
    MINI_ID[(si, u)] = MINI_BASE + j
R = R0 + len(MINIS)
nreg = 2 * V + R
log('(0) the puncture %s | the minis %d | THE R = %d (the crossing at 428!!!)' % (RM, len(MINIS), R))

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

# ============ (1) THE FRAMES (the OLD-index kept-lists -> the VECTOR-lists!!) ============
frames_old = [[o for o in fl if o in old2new] for fl in frames0]
frames_vecs = [[list(lines[o]) for o in nl] if nl else [] for nl in frames_old]
FDIM = [len(basis_of(nl)) if nl else 0 for nl in frames_old]
FULL_F = 1
log('(1) the frames: %d | the full-frame dim %d' % (len(frames_vecs), FDIM[FULL_F]))
WiF = [W['final'][v0 + L] for L in RM]
log('    the W_i-frames: %s (the dims %s!!)' % (WiF, [FDIM[f] for f in WiF]))
assert all(FDIM[f] == 7 for f in WiF), 'THE W_i DIMS MUST BE 7 (the CST-63!!!)'

# ============ (2) THE GATES PROJECTION ============
def map_reg(r):
    if r < v0:
        return old2new.get(r)
    if r < 2 * v0:
        return V + old2new[r - v0] if (r - v0) in old2new else None
    return nh(r)

D = []
for F, d, srcs in W['D']:
    if (d - v0) in old2new:
        D.append([0, V + old2new[d - v0], [nh(s) for s in srcs]])
A = []
for F, d, srcs in W['A']:
    nd = map_reg(d)
    if nd is None:
        continue                      # the dropped-source-dests (none!!) / the dropped!!
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None]
    if not nsrcs:
        continue
    A.append([F, nd, nsrcs])
B = []
for F, d, srcs in W['B']:
    nd = map_reg(d)
    if nd is None:
        continue                      # the dropped-target dests only!!
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None]
    if nsrcs:
        B.append([F, nd, nsrcs])
log('(2) the projected gates: D %d | A %d | B %d' % (len(D), len(A), len(B)))

# ============ (2b) THE STARS (before the star-builds!!) ============
STARS = []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
assert len(STARS) == 9

# ============ (3) THE STAR-BUILDS + THE MINI-BUILDS ============
# THE SOURCE-RET DESIGN: the rets = the SOLs' SOURCE-members (the self-bit-cancellation!!)
# — the star-build writes the u_j: val = 1<<u_j XOR (the SOL-minus-u_j) = the star!!
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
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs: x ^= val0[s]
    val0[d] ^= x
    for s in srcs:
        if FDIM0[cur0[s]] < FDIM0[F] or not in_Wb(FBAS0[cur0[s]], FBAS0[F]):
            cur0[s] = F
    cur0[d] = F
log('(3) the base-replay done!!')
for j, (si, u) in enumerate(MINIS):
    u_old = kept[u]
    A.append([cur0[u_old], MINI_ID[(si, u)], [u]])
log('    the mini-builds: %d (the ids %d..%d!!)' % (len(MINIS), MINI_BASE, MINI_BASE + len(MINIS) - 1))
# THE B-SRC-SOURCES (the u_j's must avoid them (the pollution!!))!!
BSRC = set()
for F, d, srcs in W['B']:
    for s in srcs:
        if s < v0:
            BSRC.add(s)
log('(3b) the B-src-sources: %d (the u_j-avoidance-set!!)' % len(BSRC))
# (3c) THE FRESH-HELPER-RETS (the pollution-free!!!): the ids 642+17+0..8 = 659..667!!
FRESH_BASE = MINI_BASE + len(MINIS)
R = R0 + len(MINIS) + 9
nreg = 2 * V + R
log('(3c) THE FRESH-RETS: the ids %d..%d | THE R = %d (the +9!!!)' % (
    FRESH_BASE, FRESH_BASE + 8, R))
NEWRET = {si: FRESH_BASE + si for si in range(9)}
for si in range(9):
    srcs = [map_reg(r) for r in SOLS[si]]
    srcs = [x for x in srcs if x is not None]
    srcs += [MINI_ID[(si, u)] for (s2, u) in MINIS if s2 == si]
    A.append([WiF[si], NEWRET[si], srcs])
    log('    the star %d -> THE FRESH-RET %d: %d srcs (the frame %d!!)' % (
        si, NEWRET[si], len(srcs), WiF[si]))

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
            chain |= m2
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
            chain |= m2
        else:
            raise SystemExit('THE W-SOLVE FAILS at t=%d!!' % t)
    SCAT.append([si for si in range(9) if (chain >> si) & 1])
log('(4) the scatter: the row-sizes %s' % dict(sorted(Counter(len(s) for s in SCAT).items())))

# ============ (5) THE COMPUTED-D (the exact one-shot cancel!!) ============
val = [1 << r for r in range(nreg)]
for F, d, srcs in A:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
for t in range(V):
    for si in SCAT[t]:
        val[V + t] ^= val[NEWRET[si]]
for F, d, srcs in B:
    for s in srcs: val[d] ^= val[s]
DNEW = []
nline_resid = 0
for t in range(V):
    resid = val[V + t] ^ (1 << (V + t)) ^ (1 << t)
    line_resid = [b for b in range(V) if (resid >> b) & 1]
    reg_resid = [b for b in range(2 * V, nreg) if (resid >> b) & 1]
    if line_resid:
        nline_resid += 1
        if nline_resid <= 3:
            log('    !!! THE LINE-RESIDUE at t=%d: %s (THE BALANCE-ERROR!!)' % (t, line_resid[:8]))
    DNEW.append([0, V + t, reg_resid])
log('(5) THE COMPUTED-D: the src-sizes %s (the max %d!!) | the line-residues %d' % (
    dict(sorted(Counter(len(g[2]) for g in DNEW).items())),
    max(len(g[2]) for g in DNEW) if DNEW else 0, nline_resid))
D = DNEW

# ============ (6) THE C (the H4-reversal!!) ============
zg = [[F, d, srcs] for F, d, srcs in A + B if not (V <= d < 2 * V)]
C = [[FULL_F, d, list(srcs)] for F, d, srcs in reversed(zg)]
log('(6) THE C: %d (the z-gates %d!!)' % (len(C), len(zg)))

# ============ (7) THE STARTS + THE FINALS!! ============
start = [0] * nreg
for s_new in range(V):
    start[s_new] = 2 + kept[s_new]
final = [FULL_F] * nreg
for t in range(V):
    final[V + t] = W['final'][v0 + kept[t]]

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
        val[V + t] ^= val[NEWRET[si]]
for F, d, srcs in B:
    for s in srcs: val[d] ^= val[s]
# THE C-PHASE (the full semantics: the z-reversals restore everything!!)
for F, d, srcs in C:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
bad = []
for r in range(nreg):
    if r < V:
        want = 1 << r
    elif r < 2 * V:
        want = (1 << r) ^ (1 << (r - V))
    else:
        want = 1 << r
    if val[r] != want:
        bad.append(r)
log('(7) THE FULL REPLAY: the bad registers %d/%d %s' % (
    len(bad), nreg, 'THE FINALS PASS!!!!' if not bad else '!!'))
for r in bad[:6]:
    diff = val[r] ^ ((1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r)
    log('    r=%d: the line-res %s | the reg-res %s' % (
        r, [b for b in range(V) if (diff >> b) & 1][:8],
        [b for b in range(V, nreg) if (diff >> b) & 1][:8]))

# ============ (9) THE EMISSION (the gcheck-format!!) ============
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
    ret=[NEWRET[si] for si in range(9)],
    ret_frames=[WiF[si] for si in range(9)],
    scatter=SCAT,
)
json.dump(word, open('ii19_p111_word.json', 'wt'))
log('(8) THE WORD EMITTED (ii19_p111_word.json!!): R=%d v=%d h=%d' % (R, V, H))
log('    the gates: D %d | A %d | B %d | C %d' % (len(D), len(A), len(B), len(C)))
log('DONE — THE P111-CLASS WORD BUILD!!')
