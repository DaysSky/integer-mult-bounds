"""THE P111-WORD v14 (ii19_p111w14.py) — THE FULL LEGAL BUILD (THE R = 527!!!)

THE MEASURED-DESIGN (the v9-v13!!!): the w8's-B-entanglement (the 92-down-climbs (the pinned
pool-registers!!!)) -> THE PIECE-DESIGN (THE FREE-SAME-FRAME-READS (the §1750!!!)):
  - THE PIECES (the 89 (the v13's-best-RM!!)): the per-(star, frame)-fresh-registers at the
    STAR-INTERNAL frames (the D6s (the ~30-bit-parts (the at-frame-helpers (the FREE!!))) /
    the lucky-cells (the 2-bits (the at-cell-sources (the FREE!!!)))) — the pieces'-chains:
    the frame (2/6!!) -> W_si (7!!) -> FULL (8!!) ✓✓✓ THE ZERO-PIN-VIOLATION!!!
  - THE RETS (the 9!!): [W_si, RET_si, [the si's-pieces (the FREE (the cur == W_si!!!))!!)]
    — the CST 63 (the 9x7 (the §1916's-floor!!!))
  - THE MIMICS (the 9!!): the dropped-sources'-B-scratch-roles (the w8's ✓!!)
  - THE COMPUTED-D (the exact-cancel (the w8's-(5) + the nat19's-D-extension-law!!!))
  - THE C (the H4-literal-reversal (the FULL-frames!!))

THE RM = [4, 19, 22, 26, 27, 70, 85, 112, 118] (the v13's-best (the 89-pieces!!!)) ->
THE R = 420 + 89 + 9 + 9 = 527 (the honest-record-class (the ~-5..-6%-expected (the +18-over
the word4!!!))).

THE VERIFICATION-LADDER: (a) the algebra (the stars'-solve ✓); (b) the FULL-VALS-REPLAY (the
749-finals!!); (c) THE CLIMB-CHECK (the gcheck-exact (the w9's-machinery (the EXPECTED: 0!!!)));
(d) THE GCHECK (the real!!!); (e) THE PRICE (the damped-pricer!!!).
"""
import gzip, json, time
from collections import Counter
from fractions import Fraction

W = json.load(gzip.open('/Users/dayssky/integer-mult-bounds/research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

RM = [4, 19, 22, 26, 27, 70, 85, 112, 118]        # THE V13's-BEST (the 89-pieces!!)
kept = [i for i in range(120) if i not in RM]
old2new = {o: n for n, o in enumerate(kept)}
V, H = 111, 8
lines = W['lines']
v0 = W['v']
frames0 = W['frames']
nreg0 = len(W['start'])
R0 = W['R']
FULL_F = 1

def iph(a, b): return sum(x * y for x, y in zip(a, b)) / 2
def basis_of(idx_list):
    rr = [[Fraction(z) for z in lines[i]] for i in idx_list]
    bas = []
    for row in rr:
        y = list(row)
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

# ============ (0) THE BASE-REPLAY (the R420's-own (the cur-map + the contents!!)) ============
val0 = [1 << r for r in range(nreg0)]
cur0 = list(W['start'])
for F, d, srcs in W['D']:
    for s in srcs: val0[d] ^= val0[s]
for gi, (F, d, srcs) in enumerate(W['A']):
    x = 0
    for s in srcs: x ^= val0[s]
    val0[d] ^= x
    for s in srcs:
        if FDIM[cur0[s]] < FDIM[F] or not in_W(FBAS[cur0[s]], FBAS[F]):
            cur0[s] = F
    cur0[d] = F
log('(0) the base-replay done!!')
def CONTp(r):
    c = 0
    for b in range(v0):
        if (val0[r] >> b) & 1 and b in old2new:
            c |= 1 << old2new[b]
    return c
STARS, WiB, WiF = [], [], []
for L in RM:
    s_new = 0
    for u in kept:
        if iph(lines[L], lines[u]) == 0:
            s_new |= 1 << old2new[u]
    STARS.append(s_new)
    WiB.append(basis_of([u for u in range(120) if u != L and iph(lines[L], lines[u]) == 0]))
    WiF.append(W['final'][v0 + L])
assert all(FDIM[f] == 7 for f in WiF)
log('    the stars: %s (the W-frames %s (the dims %s!!))' % (
    [bin(s).count('1') for s in STARS], WiF, [FDIM[f] for f in WiF]))

# ============ (1) THE REGISTERS ============
HELPS_AT_D6 = {}
for h in range(2 * v0, nreg0):
    if FDIM[cur0[h]] == 6 and CONTp(h):
        HELPS_AT_D6.setdefault(cur0[h], []).append(h)
SRC_CELL = {}
for u_old in range(v0):
    if FDIM[cur0[u_old]] == 2:
        SRC_CELL.setdefault(cur0[u_old], []).append(u_old)
PIECE_BASE = 222 + R0                                  # 642
RET_BASE = PIECE_BASE                                   # set after the selection!!
# the piece-selection (the v13's-greedy (the per-star (the D6-pieces + the cell-pieces!!!))!!)
PIECES = []            # (si, frame, [the mapped-srcs], the bits)
for si in range(9):
    rem = STARS[si]
    d6fr = [fi for fi in HELPS_AT_D6 if in_W(FBAS[fi], WiB[si])]
    used_fr = set()
    while rem:
        best = None
        for fi in d6fr:
            if fi in used_fr: continue
            hs = HELPS_AT_D6[fi]
            for m in range(1, 1 << len(hs)):
                bits = 0
                for j in range(len(hs)):
                    if (m >> j) & 1:
                        bits ^= CONTp(hs[j])
                g = bin(bits & rem).count('1')
                if g > 0 and (best is None or g > best[0] or
                              (g == best[0] and bin(bits).count('1') < bin(best[2]).count('1'))):
                    best = (g, fi, bits, [hs[j] for j in range(len(hs)) if (m >> j) & 1], 'd6')
        for c, us in SRC_CELL.items():
            if c in used_fr: continue
            if not in_W(FBAS[c], WiB[si]): continue
            bits = 0
            for u_old in us:
                if u_old in old2new and (STARS[si] >> old2new[u_old]) & 1:
                    bits |= 1 << old2new[u_old]
            g = bin(bits & rem).count('1')
            if g > 0 and (best is None or g > best[0]):
                best = (g, c, bits, [u_old for u_old in us if u_old in old2new
                                      and (STARS[si] >> old2new[u_old]) & 1], 'cell')
        if best is None:
            raise SystemExit('THE UNCOVERED-RESIDUE (the star %d: %d bits!!)!!' % (
                si, bin(rem).count('1')))
        g, fi, bits, srcs_old, kind = best
        used_fr.add(fi)
        PIECES.append((si, fi, srcs_old, bits, kind))
        rem &= ~bits
    log('    the star %d: the pieces so far %d (the residue %d!!)' % (si, len(PIECES), bin(rem).count('1')))
N_PIECES = len(PIECES)
PIECE_ID = {j: PIECE_BASE + j for j in range(N_PIECES)}
RET_BASE = PIECE_BASE + N_PIECES
MIMIC_BASE = RET_BASE + 9
R = R0 + N_PIECES + 9 + 9
nreg = 2 * V + R
log('(1) THE PIECES: %d (the D6 %d | the cells %d!!) | the R = %d (the nreg %d!!)' % (
    N_PIECES, sum(1 for p in PIECES if p[4] == 'd6'), sum(1 for p in PIECES if p[4] == 'cell'),
    R, nreg))
# the algebra-verification (the pieces per star XOR to the stars!!)
for si in range(9):
    acc = 0
    for j, (si2, fi, srcs_old, bits, kind) in enumerate(PIECES):
        if si2 == si: acc ^= bits
    assert acc == STARS[si], 'THE STAR-VERIFY at %d!!' % si
log('    the star-algebra: ALL 9 PASS ✓✓')

# ============ (2) THE GATES'-PROJECTION (the w8's-machinery!!) ============
def nh(h): return h - 18
def map_reg(r):
    if r < v0:
        if r in old2new: return old2new[r]
        return MIMIC_BASE + RM.index(r)
    if r < 2 * v0:
        return V + old2new[r - v0] if (r - v0) in old2new else None
    return nh(r)
# the A: the projected + the pieces + the rets!!
A = []
for F, d, srcs in W['A']:
    nd = map_reg(d)
    if nd is None or nd >= MIMIC_BASE:
        continue
    nsrcs = [x for s in srcs if (x := map_reg(s)) is not None and x < MIMIC_BASE]
    if not nsrcs:
        continue
    A.append([F, nd, nsrcs])
for j, (si, fi, srcs_old, bits, kind) in enumerate(PIECES):
    srcs = [nh(s) if s >= 2 * v0 else old2new[s] for s in srcs_old]
    A.append([fi, PIECE_ID[j], srcs])
RET = {si: RET_BASE + si for si in range(9)}
pieces_by_star = {}
for j, (si, fi, srcs_old, bits, kind) in enumerate(PIECES):
    pieces_by_star.setdefault(si, []).append(PIECE_ID[j])
for si in range(9):
    A.append([WiF[si], RET[si], pieces_by_star[si]])
# the B: the FULL-MIMICRY (the w8's!!)
B = []
for F, d, srcs in W['B']:
    nd = map_reg(d)
    if nd is None:
        continue
    nsrcs = [map_reg(s) for s in srcs]
    nsrcs = [x for x in nsrcs if x is not None]
    if not nsrcs:
        continue
    B.append([F, nd, nsrcs])
log('(2) the gates: the A %d (the projected %d + the pieces %d + the rets 9!!) | the B %d' % (
    len(A), len(A) - N_PIECES - 9, N_PIECES, len(B)))

# ============ (3) THE SCATTER (the W-solve-over-the-stars (the w7's-(4)!!)) ============
piv = {}
for si in range(9):
    x = STARS[si]; chain = 1 << si
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]; x ^= x2; chain ^= m2
        else:
            piv[p] = (x, chain); break
assert len(piv) == 9, 'the stars-independence!!'
BROWS = []
for t in kept:
    m = 1 << old2new[t]
    for u in kept:
        if u != t and iph(lines[t], lines[u]) == 0:
            m |= 1 << old2new[u]
    BROWS.append(m)
SCAT = []
for t in range(V):
    x = BROWS[t]; chain = 0
    while x:
        p = (x & -x).bit_length() - 1
        if p in piv:
            x2, m2 = piv[p]; x ^= x2; chain ^= m2
        else:
            raise SystemExit('THE W-SOLVE FAILS at t=%d!!' % t)
    SCAT.append([si for si in range(9) if (chain >> si) & 1])
log('(3) the scatter: the row-sizes %s' % dict(sorted(Counter(len(s) for s in SCAT).items())))

# ============ (4) THE COMPUTED-D (the exact-cancel!!) ============
val = [1 << r for r in range(nreg)]
for F, d, srcs in A:
    x = 0
    for s in srcs: x ^= val[s]
    val[d] ^= x
for t in range(V):
    for si in SCAT[t]:
        val[V + t] ^= val[RET[si]]
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
log('(4) THE COMPUTED-D: the line-residues %d/%d | the src-sizes %s' % (
    nline_resid, V, dict(sorted(Counter(len(g[2]) for g in DNEW).items()))))
assert nline_resid == 0, 'THE X-BALANCE FAILS!!'
D = DNEW

# ============ (5) THE C (the H4!!) ============
zg = [[F, d, srcs] for F, d, srcs in A + B if not (V <= d < 2 * V)]
C = [[FULL_F, d, list(srcs)] for F, d, srcs in reversed(zg)]
log('(5) THE C: %d (the z-gates %d!!)' % (len(C), len(zg)))

# ============ (6) THE STARTS + FINALS ============
start = [0] * nreg
for s_new in range(V):
    start[s_new] = 2 + kept[s_new]
final = [FULL_F] * nreg
for t in range(V):
    final[V + t] = W['final'][v0 + kept[t]]

# ============ (7) THE FULL-VALS-REPLAY + THE CLIMB-CHECK (the gcheck-exact!!) ============
def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]
frames_vecs = [[[v2 for v2 in lines[i]] if isinstance(i, int) and i < v0 else list(i)
                for i in fl] for fl in frames0]
fr = [rref(F, H) for F in frames_vecs]
dims = [len(F) for F in fr]
_sub = {}
def sub(a, b):
    k = (a, b)
    if k not in _sub:
        _sub[k] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
    return _sub[k]
cur = list(start)
val = [1 << r for r in range(nreg)]
bad_climbs = []
def climb(r, F, phase, gi):
    if cur[r] == F: return
    if not (sub(cur[r], F) and dims[F] > dims[cur[r]]):
        bad_climbs.append((phase, gi, r, cur[r], F, dims[cur[r]], dims[F]))
    cur[r] = F
def run(gates, phase):
    for gi, (F, d, srcs) in enumerate(gates):
        for r in [d] + srcs: climb(r, F, phase, gi)
        for s in srcs: val[d] ^= val[s]
run(D, 'D')
run(A, 'A')
for t in range(V):
    for si in SCAT[t]: val[V + t] ^= val[RET[si]]
run(B, 'B')
run(C, 'C')
for r in range(nreg): climb(r, final[r], 'FINAL', -1)
bad = []
for r in range(nreg):
    want = (1 << r) ^ (1 << (r - V)) if V <= r < 2 * V else 1 << r
    if val[r] != want:
        bad.append(r)
log('(7) THE FULL-REPLAY: the bad-vals %d/%d %s' % (len(bad), nreg, 'THE FINALS PASS!!!!' if not bad else '!!'))
log('    THE CLIMB-CHECK (the gcheck-exact!!): the illegal-climbs %d (the EXPECTED: 0!!!)' % len(bad_climbs))
for b in bad_climbs[:8]:
    log('    !!! [%s] gate %d reg %d: %d(d%d) -> %d(d%d)' % (b[0], b[1], b[2], b[3], b[5], b[4], b[6]))

# ============ (8) THE EMISSION ============
word = dict(
    convention='bitE8/1+mut', label='II19-P111-native-legal',
    form=dict(num=[[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1]], den=2),
    h=H, v=V, R=R,
    lines=[list(lines[o]) for o in kept],
    frames=frames_vecs,
    start=start, final=final,
    D=D, A=A, B=B, C=C,
    ret=[RET[si] for si in range(9)],
    ret_frames=[WiF[si] for si in range(9)],
    scatter=SCAT,
)
json.dump(word, open('ii19_p111_word2.json', 'wt'))
log('(8) THE WORD EMITTED (ii19_p111_word2.json!!): R=%d v=%d h=%d (the CST %d!!)' % (
    R, V, H, 9 * 7))
log('    the gates: the D %d | the A %d | the B %d | the C %d' % (len(D), len(A), len(B), len(C)))
log('    THE GCHECK: /Users/dayssky/.venv/bin/python '
    'research/lorentzian-frame-cell-handoff/code/tword/gcheck.py '
    'research/i13-partition/ii19_p111_word2.json --price')
log('DONE — THE v14-FULL-LEGAL-BUILD (THE R = %d!!!)!!' % R)
