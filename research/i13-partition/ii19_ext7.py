"""THE SPECIAL's COMPLETENESS FIX — THE 120 (root, special) PRODUCTS DELIVERED (ii19_ext7.py).

THE HANDOFF §4.2's OWED CORRECTION: the ext4/word2's committed claim "COMPLETENESS HOLDS:
junk(t) >= perp_121(t) for all 121 targets" is WRONG for the special's column: the special's
delivered = e120 ONLY (the COPY — the SS1150 identity-word flaw!); the 120 (root, special)
orthogonal products are NOT realized. The roots' columns ARE complete (re-verified here!).

THE FIX v3 — THE RET-READS (the v1 source-reads are DEAD: the 477 B-reads climb the sources
to the PERP frames (dim 8, containing the special's line: NOT-subset IDX_R8, and dim-equal:
the climb ILLEGAL) — the one-climb-per-source law: THE SOURCES ARE UNTOUCHABLE!!):

THE LINEAR ALGEBRA (the census's uniqueness!!): the 10 registers' x-parts are GF(2)-
INDEPENDENT (rank 10: exactly ONE subset [1, 9] XORs to the all-ones = B121[120]!!), so
the NET delivery (the scatter row S XOR the reads R) has a UNIQUE representation — and
e120's is {0, 1, 9} (v0 ^ (v0 ^ e120) — THE EXT6's OWN ROW'S NET!!). THE DESIGN:
(a) THE SCATTER ROW: S = {0, 1, 9} U R — delivering e120 XOR X (X = the R-rets' XOR!):
    the FULL INCIDENCE FLOWS IN (the junk = the union of the x-parts!!).
(b) THE READS: R = the 7 rets at IDX_R8 (k = 2..8 — the row0-rets 0,1 + the odd 9 sit at
    the FULL (dim 9): UNREADABLE on the E8-internal chain!) — the read-gate
    [IDX_R8, V+SP, RET_IDX[2..8]]: the FREE SAME-FRAME RE-READS (cur == F: NO MOVEMENT,
    NO MASS!!) — the junk-cancel: the net = e120 exactly (the finals balance!).
(c) THE DIRT: the net = the {0,1,9}-dirt XOR = ODD ^ dirt0 ^ dirt1 ^ dirt(0) ^ dirt(1)
    = the ODD-bit — THE EXT6's D-GATE [0, V+SP, [ODD]] STAYS UNCHANGED!!
(d) THE JUNK = the union of the R-rets' x-parts' setbits (>= the 120 roots = perp(special)
    = THE COMPLETENESS — the census measures the coverage!!).

THE COST: +1 B-GATE + the special's scatter row ONLY!! R 463 UNCHANGED (the wall 484:
the 95.7%!!); THE HIST UNCHANGED (the special's target's +8 moves from the final climb to
the read-gate: the same bucket!!); THE MASS 6186; THE PRICE c IDENTICAL!!

THE VERIFICATION: MY OWN REPLAY (the finals fails 0!) + THE COMPLETENESS CHECK (junk(t) >=
perp_121(t) for ALL 121: the BEFORE (the special EMPTY — the honest §4.2!) and the AFTER!)
+ THE GCHECK + THE TRUE c.
"""
import gzip, json, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE LOAD + THE 121-LINE SYSTEM (the ext6 verbatim!) ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0, h0, R0 = W['v'], W['h'], W['R']            # 120, 8, 420
frames0, lines0 = W['frames'], W['lines']

V9 = [list(L) + [0] for L in lines0] + [[0] * 8 + [1]]
V, H, SP = 121, 9, 120
R = 463                                        # the 420 + the odd + the 42 SHARED carriers!
nreg = 2 * V + R                               # 705!
log('(0) the system: v0=%d h0=%d R0=%d -> V=%d H=%d R=%d nreg=%d' % (v0, h0, R0, V, H, R, nreg))

# ============ (C1) THE CENSUS CORE (the ext6 verbatim!) ============
def dot(a, b): return sum(x * y for x, y in zip(a, b))
G0 = [[dot(lines0[i], lines0[j]) for j in range(v0)] for i in range(v0)]
PU = [sum(1 << j for j in range(v0) if G0[j][t] == 0) for t in range(v0)]
CNT2DIM0 = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims0 = [CNT2DIM0[len(fr)] for fr in frames0]

chains = defaultdict(list)
for F, d, srcs in W['B']:
    if v0 <= d < 2 * v0:
        chains[d - v0].append((F, list(srcs)))
prior_span = {}
for t, gl in chains.items():
    last = None
    for (F, srcs) in gl:
        if F == W['final'][v0 + t]:
            break
        last = F
    prior_span[t] = frozenset(frames0[last]) if last is not None else frozenset()

def served(X):
    if not X:
        return set()
    xm = 0
    for r in X:
        xm |= 1 << r
    out = []
    for u in prior_span:
        if not (set(prior_span[u]) <= X):
            continue
        if xm & ~PU[u]:
            continue
        out.append(u)
    return set(out)

big_cands = []
for fi in range(len(frames0)):
    if dims0[fi] not in (4, 6):
        continue
    X = set(frames0[fi])
    S = served(X)
    if S:
        big_cands.append((frozenset(X), S))
big_cands.sort(key=lambda z: -len(z[1]))
covered = set()
carrier_groups = []
for (X, S) in big_cands:
    if S - covered:
        carrier_groups.append((X, sorted(S - covered)))
        covered |= S
for t in prior_span:                           # the fallback: the per-target cells!
    if t not in covered:
        carrier_groups.append((prior_span[t], [t]))
m = len(carrier_groups)
gsz = Counter(len(S) for (X, S) in carrier_groups)
log('(C1) THE CENSUS: the m = %d shared carriers | the group sizes %s' % (
    m, dict(sorted(gsz.items()))))

# ============ (1) THE FRAMES (+ the m shared F_j's!) (the ext6 verbatim!) ============
rb_sets = []
for f in frames0:
    fl = list(f)
    if len(fl) == 120 or len(fl) == 63:        # the FULL + the perps: +special!
        fl = fl + [SP]
    rb_sets.append(fl)
IDX_SPS = len(rb_sets); rb_sets.append([SP])               # the {120}-singleton!
IDX_R8 = len(rb_sets); rb_sets.append(list(range(120)))     # the 120-roots (the E8-span!)!
F_IDX = []                                     # the shared carriers' frames!
for (X, S) in carrier_groups:
    F_IDX.append(len(rb_sets))
    rb_sets.append(sorted(set(X) | {SP}))      # the F_j = the D4 U {120} (the 13-line!)!
IDX_FULL = 1                                               # the frame-1: the FULL (121-line!)!
frames = [[V9[i] for i in s] for s in rb_sets]
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(s)] for s in rb_sets]
log('(1) the frames: %d (+%d shared!) | the dims %s' % (
    len(frames), m, dict(sorted(Counter(dims).items()))))

# ============ (2) THE REGISTERS' MAP (the ext6 verbatim!) ============
def remap(r):
    if r < v0:
        return r                              # the sources: SAME!
    if r < 2 * v0:
        return r + 1                          # the targets: +1!
    return r + 2                               # the helpers: +2!

ODD = 2 * V + 421 - 1                          # the 662: the odd-gather (the fixed index!)
CARR = [2 * V + 421 + j for j in range(m)]     # the 663..663+m-1: the m SHARED carriers!
log('(2) the remap: the sources +0, the targets +1, the helpers +2; ODD=%d; the carriers %d..%d' % (
    ODD, CARR[0], CARR[-1]))

# ============ (3) THE START / FINAL (the ext6 verbatim!) ============
start = [0] * nreg
for s in range(v0):
    start[s] = 2 + s                           # the singletons: the frames[2..121]!
start[SP] = IDX_SPS
final = [IDX_FULL] * nreg
for t in range(v0):
    final[V + t] = W['final'][v0 + t]           # the t-perp frames (the re-based 64-line!)!
final[V + SP] = IDX_R8                          # the special's: the 120-roots!
log('(3) the start/final: the special start %d; the special final %d' % (IDX_SPS, IDX_R8))

# ============ (4) THE GATES + THE ORDER-AWARE CARRIER-INSERTION (the ext6 verbatim!) ============
def remap_gate(g):
    F, d, srcs = g
    return [F, remap(d), [remap(s) for s in srcs]]

D = [remap_gate(g) for g in W['D']]
A = [remap_gate(g) for g in W['A']]
RET_IDX = [remap(q) for q in W['ret']]
ret_set = set(RET_IDX)
n_retarget = 0
for g in A:
    if g[1] in ret_set and g[0] == 1:           # the rets' FULL-dest gates -> the 120-roots!
        g[0] = IDX_R8
        n_retarget += 1
log('(4) the gates: D %d | A %d (the %d ret-gates re-targeted!)' % (
    len(D), len(A), n_retarget))

# THE CARRIERS' A-BUILDS (the m shared!): the val = own-dirt ^ {120}!
for j in range(m):
    A.append([IDX_SPS, CARR[j], [SP]])
# THEN THE ODD'S A-BUILD (the SP: the {120} -> the FULL — AFTER the carriers!)
odd_srcs = [RET_IDX[k] for k in W['scatter'][0]] + [SP]
A.append([IDX_FULL, ODD, odd_srcs])
log('    the A-builds: %d shared carriers THEN the odd' % m)

# THE D-GATES: the +ODD (all!) + the special's NEW gate + the per-target +CARR[j_t]!
for g in D:
    g[2].append(ODD)
D.append([0, V + SP, [ODD]])
t_carrier = {}
for j, (X, S) in enumerate(carrier_groups):
    for t in S:
        t_carrier[t] = j
for t in range(v0):
    D[t][2].append(CARR[t_carrier[t]])
log('    the D: the +ODD to all %d + the special gate + the %d per-target carriers' % (
    len(D) - 1, len(t_carrier)))

# THE B-PHASE: the R420's gates + THE ORDER-AWARE INSERTION (the cell -> CARRIER -> perp!!)
B = []
n_ins = 0
for g in W['B']:
    F, d, srcs = g
    if v0 <= d < 2 * v0:
        t = d - v0
        B.append([F, remap(d), [remap(s) for s in srcs]])
        if F != W['final'][v0 + t] and t in t_carrier:
            j = t_carrier[t]
            B.append([F_IDX[j], V + t, [CARR[j]]])   # BETWEEN the cell and the perp!!
            n_ins += 1
    else:
        B.append([F, remap(d), [remap(s) for s in srcs]])
log('    the B: %d gates (the %d carrier-insertions!)' % (len(B), n_ins))

# ============ (5) THE SCATTER (the ext6 verbatim — the BEFORE-baseline!) ============
ret_list = RET_IDX + [ODD]
row0_rets = set(W['scatter'][0])               # the fix-7's truth: the CST 83!
ret_frames = [(IDX_FULL if (k in row0_rets or k == 9) else IDX_R8) for k in range(10)]
scatter = []
row0 = list(W['scatter'][0])
for t in range(V):
    if t < v0:
        sel = list(W['scatter'][t]) + row0 + [9]     # the roots: the row + the ROW-0 + the ODD!
        cnt = Counter(sel)
        scatter.append(sorted(k for k in cnt if cnt[k] % 2))
    else:
        sel = [9] + row0                             # the special: the ODD + the ROW-0!
        cnt = Counter(sel)
        scatter.append(sorted(k for k in cnt if cnt[k] % 2))
log('(5) the scatter: the 121 rows (the special row BEFORE: %s)' % scatter[SP])

# ============ (6) THE C (the ext6 verbatim — the replay #1's baseline!) ============
zg = [[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)]
C = [[IDX_FULL, d, s] for F, d, s in reversed(zg)]
log('(6) the C: %d gates (the H4 reverse of the %d z-gates!)' % (len(C), len(zg)))

# ============ (7) THE REPLAY MACHINERY (the ext6's semantics + THE INSTRUMENTATION!) ============
XMASK = (1 << V) - 1

def replay(D_g, A_g, B_g, C_g, rows, snap=False):
    """THE FULL REPLAY (the gcheck's exact semantics) + the instrumentation:
    the junk-sets (the scatter's delivered-x setbits U the reads' srcs' x-contents!),
    the A-end snapshot (the rets' values: the census's input!), the sources' B-end frames,
    the B-reads-of-sources count, the per-target dirt/scatter/reads."""
    val = [1 << i for i in range(nreg)]
    cur = list(start)
    hist = Counter()
    moves = 0
    junk = [set() for _ in range(V)]
    tgt_dirt = [0] * V
    tgt_scatter = [0] * V
    tgt_reads = [0] * V

    def climb(r, F):
        nonlocal moves
        if cur[r] == F:
            return
        assert dims[F] >= dims[cur[r]], 'DECREASING climb (reg %d): %d -> %d' % (
            r, dims[cur[r]], dims[F])
        hist[dims[F] - dims[cur[r]]] += 1
        moves += 1
        cur[r] = F

    def run(gates):
        for F, d, srcs in gates:
            for r in [d] + srcs:
                climb(r, F)
            for s in srcs:
                val[d] ^= val[s]

    for F, d, srcs in D_g:                       # THE D-PHASE!
        acc = 0
        for s in srcs:
            acc ^= val[s]
        tgt_dirt[d - V] = acc
        for r in [d] + srcs:
            climb(r, F)
        for s in srcs:
            val[d] ^= val[s]

    run(A_g)                                     # THE A-PHASE!
    vals_ret = [val[q] for q in ret_list] if snap else None
    vals_aend = list(val) if snap else None      # THE A-END SNAPSHOT (the pool's values!!)
    cur_aend = list(cur) if snap else None       # THE A-END FRAMES (the B-start sitters!!)

    for t in range(V):                           # THE SCATTER!
        acc = 0
        for k in rows[t]:
            acc ^= val[ret_list[k]]
        tgt_scatter[t] = acc
        xj = acc & XMASK                         # the delivered x-pattern (the XOR's bits!)
        while xj:
            b = xj & -xj
            junk[t].add(b.bit_length() - 1)
            xj ^= b
        val[V + t] ^= acc

    src_b_reads = 0
    for F, d, srcs in B_g:                       # THE B-PHASE!
        for r in [d] + srcs:
            climb(r, F)
        if V <= d < 2 * V:
            acc = 0
            for s in srcs:
                acc ^= val[s]
                xs = val[s] & XMASK             # the reads' x-contents (the UNION!)
                while xs:
                    b = xs & -xs
                    junk[d - V].add(b.bit_length() - 1)
                    xs ^= b
            tgt_reads[d - V] ^= acc
        else:
            for s in srcs:
                if s < v0:
                    src_b_reads += 1
        for s in srcs:
            val[d] ^= val[s]
    src_bend = [cur[s] for s in range(v0)]
    vals_bend = list(val)                       # THE B-END SNAPSHOT (the pool's values!!)

    run(C_g)                                     # THE C-PHASE!
    for r in range(nreg):                        # THE FINAL CLIMBS!
        climb(r, final[r])

    bad = []
    for r in range(nreg):
        want = (1 << r) ^ ((1 << (r - V)) if V <= r < 2 * V else 0)
        if val[r] != want:
            bad.append(r)
    return dict(bad=bad, hist=hist, moves=moves, vals_ret=vals_ret, src_bend=src_bend,
                src_b_reads=src_b_reads, junk=junk, tgt_dirt=tgt_dirt,
                tgt_scatter=tgt_scatter, tgt_reads=tgt_reads, cur=cur, vals_bend=vals_bend,
                vals_aend=vals_aend, cur_aend=cur_aend)

# ============ (7b) THE PERP-SETS (the 121-line form: the diag(1^8, 2)!) ============
def ip121(a, b):
    return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]

PERP = [set() for _ in range(V)]
for t in range(V):
    for u in range(V):
        if u != t and ip121(V9[t], V9[u]) == 0:
            PERP[t].add(u)
log('(7b) the perp sizes: %s (the roots 64, the special 120!)' % (
    dict(sorted(Counter(len(p) for p in PERP).items()))))

def completeness(junk, tag):
    inc = [t for t in range(V) if not (PERP[t] <= (junk[t] - {t}))]
    log('    THE COMPLETENESS (%s): the incomplete %d/121 | the junk-minus-self sizes %s' % (
        tag, len(inc), dict(sorted(Counter(len(junk[t] - {t}) for t in range(V)).items()))))
    return inc

# ============ (7c) THE REPLAY #1: THE BASELINE (the ext6's word!) + THE SNAPSHOT ============
rep1 = replay(D, A, B, C, scatter, snap=True)
log('(7c) THE BASELINE: the finals fails %d | the moves %d' % (len(rep1['bad']), rep1['moves']))
completeness(rep1['junk'], 'the BEFORE: the ext6')
log('    THE SPECIAL (the BEFORE): the junk %d bits vs the perp %d — %s' % (
    len(rep1['junk'][SP] - {SP}), len(PERP[SP]),
    'THE COPY: the §4.2 flaw CONFIRMED!!' if not (PERP[SP] <= rep1['junk'][SP] - {SP})
    else 'complete'))
for c in [dims[f] for f in ret_frames]:
    rep1['hist'][c] += 1
mass1 = sum(k * n for k, n in rep1['hist'].items())

# ============ (8) THE CENSUS v2: the x-parts' spans + THE RET-UNION COVERAGE! ============
xp = [rep1['vals_ret'][k] & XMASK for k in range(10)]
ALLONES = (1 << V) - 1
sols = []
for mask in range(1 << 10):
    x = 0
    for k in range(10):
        if (mask >> k) & 1:
            x ^= xp[k]
    if x == ALLONES:
        sols.append(mask)
if not sols:
    log('(8) THE CENSUS: NO SUBSET XORs to the ALL-ONES — the redesign needed!!')
    sys.exit(1)
log('(8) THE CENSUS: %d/%d subsets XOR to the ALL-ONES (B121[120]!) -> the rank %d/10' % (
    len(sols), 1 << 10, 10 - (len(sols) - 1).bit_length()))
for z in sorted(sols, key=lambda z: bin(z).count('1'))[:6]:
    log('    the ALL-ONES subset: %s' % sorted(k for k in range(10) if (z >> k) & 1))
e120_mask = 1 << SP
# e120's own representation (must be {0,1,9}: v0 ^ (v0 ^ e120)!!)
e120_reps = []
for mask in range(1 << 10):
    x = 0
    for k in range(10):
        if (mask >> k) & 1:
            x ^= xp[k]
    if x == e120_mask:
        e120_reps.append(sorted(k for k in range(10) if (mask >> k) & 1))
log('    e120 representation: %s (the ext6 net: {0, 1, 9}!!)' % e120_reps)
log('    the x-part sizes: %s' % [bin(xp[k]).count('1') for k in range(10)])

# THE RET-UNION COVERAGE (the k = 2..8 rets sit at IDX_R8 — the free re-reads!!)
RK = list(range(2, 9))
cov = set()
for k in RK:
    b = xp[k]
    while b:
        lb = b & -b
        cov.add(lb.bit_length() - 1)
        b ^= lb
log('    THE RET-UNION (k=%s): %d/%d roots covered (the v3 design: %s)' % (
    RK, len(cov), v0, 'COMPLETE' if len(cov) == v0 else 'INCOMPLETE (%d missing!!)' % (v0 - len(cov))))

# ============ (8c) THE 119-HUNT: the A-end holders at the E8-internal frames!! ============
# THE v9 DESIGN: the reads = the 7 rets (FREE at IDX_R8!) + THE 119-HOLDER z read TWICE
# (the double-gate: the net 0, the junk += its contents (the missing root 119!!!)).
# THE HUNT: the helpers whose x-part contains the bit 119, sitting at the E8-internal
# frames (cur ⊆ IDX_R8: the FREE same-frame re-reads on the special's chain!!) at the A-end
# (the B-start: NOTHING HAS MOVED: the reads are FREE and their later flows untouched!!)
h119 = []
for r in range(2 * V, nreg):                    # the helpers!!
    f = rep1['cur_aend'][r]
    if not (f == IDX_R8 or (dims[f] < 8 and all(vv[8] == 0 for vv in frames[f]))):
        continue
    x = rep1['vals_aend'][r] & XMASK
    if (x >> 119) & 1:
        h119.append((r, f, dims[f], x, bin(x).count('1')))
h119.sort(key=lambda z: (z[2], z[0]))
log('(8c) THE 119-HUNT (the A-end, the E8-internal frames!!): %d holders' % len(h119))
for (r, f, d, x, sz) in h119[:12]:
    log('    reg %d at frame %d (dim %d, %d lines): x-size %d' % (r, f, d, len(rb_sets[f]), sz))
if not h119:
    log('    NO 119-holder at the A-end E8-internal frames — the mid-B hunt needed!!')
    sys.exit(1)
# THE CHOICE: the smallest-dim holder (the cheapest chain-split!!)
(zreg, zfra, zdim, zx, zsz) = h119[0]
log('    THE CHOICE: reg %d at frame %d (dim %d) — the chain 0 -> %d -> IDX_R8!!' % (
    zreg, zfra, zdim, zfra))
# THE SANITY: the z's frame ⊆ IDX_R8 (nested!!) + the rets' B-flows (the record!)
ret_bfirst = {}
for F, d, srcs in B:
    for q in ret_list:
        if q in srcs and q not in ret_bfirst:
            ret_bfirst[q] = F
log('    the rets first-B-gate frames: %s' % dict(sorted(Counter(
    ret_bfirst.get(q, -1) for q in ret_list).items())))

# ============ (9) THE FIX v9: the row {0..9} + the ret-read + THE DOUBLE-GATE!! ============
scatter[SP] = list(range(10))                   # ALL TEN: the delivered = e120 ^ X!!
# THE READS GO FIRST (the B-start: NOTHING HAS MOVED: the FREE same-frame re-reads!!)
SP_READS = [
    [zfra, V + SP, [zreg]],                     # THE 119-DELIVERY (the special: 0 -> zfra!!)
    [zfra, V + SP, [zreg]],                     # THE CANCEL (the double: the net 0!)
    [IDX_R8, V + SP, [RET_IDX[k] for k in range(2, 9)]],   # the 7 rets (FREE!!)
]
B[0:0] = SP_READS                               # PREPENDED: before all the R420's B-gates!!
zg = [[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)]
C = [[IDX_FULL, d, s] for F, d, s in reversed(zg)]   # the read-gates: target-dests: EXCLUDED!
log('(9) THE FIX v9: the special row [0..9] | the reads: the 7 rets at IDX_R8 + reg %d x2 at frame %d | the C %d' % (
    zreg, zfra, len(C)))
log('    the D-gate UNCHANGED: %s (the net dirt = the ODD-bit!!)' % [
    g for g in D if g[1] == V + SP])

# ============ (10) THE REPLAY #2: THE FIXED WORD — THE FINALS + THE COMPLETENESS!! ============
rep2 = replay(D, A, B, C, scatter)
log('(10) THE FIXED WORD: the finals fails %d (the sources %d, the targets %d, the helpers %d)' % (
    len(rep2['bad']), sum(1 for r in rep2['bad'] if r < V),
    sum(1 for r in rep2['bad'] if V <= r < 2 * V),
    sum(1 for r in rep2['bad'] if r >= 2 * V)))
if rep2['bad']:
    log('    the bad registers (the first 12): %s' % rep2['bad'][:12])
    xres = Counter()
    dres = Counter()
    for t in range(V):
        res = (rep2['tgt_dirt'][t] ^ rep2['tgt_scatter'][t] ^ rep2['tgt_reads'][t]) ^ (1 << t)
        rx = res & XMASK
        rd = res >> V
        if rx:
            xres[bin(rx).count('1')] += 1
        if rd:
            dres[bin(rd).count('1')] += 1
    log('    THE DIAGNOSIS: the x-residues %s | the dirt-residues %s' % (
        dict(sorted(xres.items())), dict(sorted(dres.items()))))
inc2 = completeness(rep2['junk'], 'the AFTER: the fix')
log('    THE SPECIAL (the AFTER): the junk %d bits >= the perp %d: %s' % (
    len(rep2['junk'][SP] - {SP}), len(PERP[SP]),
    'COMPLETE!!' if PERP[SP] <= (rep2['junk'][SP] - {SP}) else 'INCOMPLETE!!'))
for c in [dims[f] for f in ret_frames]:
    rep2['hist'][c] += 1
mass2 = sum(k * n for k, n in rep2['hist'].items())
cst = sum(dims[f] for f in ret_frames)
ident = H * R + cst + 2 * V * (H - 1)
log('    THE HIST: %s | THE CST %d | the mass %d vs the identity %d: %s' % (
    dict(sorted(rep2['hist'].items())), cst, mass2, ident,
    'MATCH!!' if mass2 == ident else 'MISMATCH!!'))
d12 = {k: rep2['hist'][k] - rep1['hist'][k]
       for k in set(rep1['hist']) | set(rep2['hist']) if rep2['hist'][k] != rep1['hist'][k]}
log('    THE HIST SHIFT (the fix - the ext6): %s | the mass %d -> %d (%s)' % (
    d12, mass1, mass2, 'CONSERVED!!' if mass1 == mass2 else 'CHANGED!!'))

# ============ (11) THE EMISSION (the gcheck-format word!) ============
FORM_NUM = [[1 if (i == j and i < 8) else (2 if (i == j == 8) else 0) for j in range(9)]
            for i in range(9)]
word = {
    'h': H, 'v': V, 'R': R,
    'form': {'num': FORM_NUM, 'den': 1},
    'lines': V9,
    'frames': frames,
    'start': start, 'final': final,
    'D': D, 'A': A, 'B': B, 'C': C,
    'ret': ret_list, 'ret_frames': ret_frames,
    'scatter': scatter,
}
OUT = 'research/i13-partition/ii19_ext_word3.json'
with open(OUT, 'w') as f:
    json.dump(word, f)
log('(11) THE WORD EMITTED: %s (%d registers, %d frames, %d D / %d A / %d B / %d C gates!)' % (
    OUT, nreg, len(frames), len(D), len(A), len(B), len(C)))
log('    THE GCHECK NEXT: research/lorentzian-frame-cell-handoff/code/tword/gcheck.py %s --price' % OUT)
log('DONE — THE COMPLETENESS-FIXED WORD (R %d UNCHANGED, ZERO new registers!)' % R)
