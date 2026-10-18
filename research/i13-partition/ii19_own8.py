"""THE WORD4: THE SMART-BASIS BUILD (ii19_own8.py) — the CST 83 -> 73 (the SS1492!!).

THE CENSUS'S FINDING (the ii19_fresh1!!): the 121's decoder-rank rho = 9 (NOT 10!!) —
the SS1292/1492's smart-basis (the 8-EVEN + the 1-ODD!!) is a FULL basis of the B0-space!!
The word3's CST-83 (the 7-R8 + the 3-FULL!!) was the transplant-artifact (the OVER-COMPLETE
10-rets (the rank 10!!)!!).

THE WORD4 (the honest-record improvement: the +22 points (the word3 -44.85% -> ~-22%!!)):
    (A) the ret-0/1 frames: the FULL -> the IDX_R8 (the CST 83 -> 81!!);
    (B) the 10-rets -> the 9-rets (the SS1492's: the 8-even (the B[0]^B[k]: the phi-KERNEL
        (the special-free supports -> the dim-8 frames!!)) + the 1-odd (the B[0]: the FULL,
        FORCED (the special in the support!!))): the CST 81 -> 73 (the PROVABLE floor!!)
        -> the deficit 9,952 (the +41% over the word3's 7,072!!).

THE DESIGN (the W'-arithmetic + the ext7's machinery!!):
    (1) the W'-matrix (the 121 x 10!!): the B[t] = XOR(W'[t][k] rets!!) — the UNIQUE
        representations (the 10-xp's GF(2)-independent (the ext7's rank-10!!)!!);
    (2) the SS1492-basis (the 9!!): the 8-even (B[0]^B[k]: phi = 0!!) + the odd (B[0]!!) —
        the representations-over-the-10 = the W'-rows' XORs!!
    (3) THE LEGALITY: the even-representations' ODD-coefficients MUST be ZERO (the phi = 0!!
        the e120-free!!) -> the new-even-rets (the R8!!) read ONLY the {0..8}-rets (the
        (A)-fixed R8-frames!!): the SAME-FRAME FREE reads!! The odd: the {0..8} + the SP!!
    (4) the new-rets' A-builds (the XOR-gates at the IDX_R8 / the FULL!!) + the scatter
        rewrite (the 121 x 9: the B[t] = XOR(W[t][k] new-ret_k!!)) + the ret_frames
        (the 8 x IDX_R8 + the 1 x IDX_FULL!!);
    (5) the replay (the finals-0!!) + the COMPLETENESS (the junk >= perp_121 for ALL!!) +
        the hist/the CST/the mass-identity!!;
    (6) THE GCHECK + THE TRUE-c (the price_damped (the battery-verified!!)!!).
"""
import json, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')

# ============ (0) THE WORD3 LOAD (the ext7's own emission!!) ============
W3 = json.load(open('ii19_ext_word3.json', 'rt'))
V, H, SP, R = W3['v'], W3['h'], 120, W3['R']          # 121, 9, 120, 463
nreg0 = 2 * V + R
lines = W3['lines']; frames = W3['frames']; start = W3['start']; final = W3['final']
D, A, B, C = W3['D'], W3['A'], W3['B'], W3['C']
ret_list = W3['ret']; ret_frames0 = W3['ret_frames']; scatter0 = W3['scatter']
V9 = lines
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] for fr in frames]
IDX_FULL = 1
# find IDX_R8: the frame with the 120 roots!!
IDX_R8 = None
for i, fr in enumerate(frames):
    if len(fr) == 120 and all(abs(x[8]) < 1e-12 for x in fr):
        IDX_R8 = i
        break
log('(0) the word3: v=%d h=%d R=%d | the frames %d | IDX_R8=%d | the ret_frames %s' % (
    V, H, R, len(frames), IDX_R8, ret_frames0))
assert IDX_R8 is not None and dims[IDX_R8] == 8

# ============ (1) THE W'-MATRIX (the B[t] = XOR(W'[t][k]-rets!!)) ============
XMASK = (1 << V) - 1
# the replay (the ext7's semantics — the values at the A-END: the rets' x-parts!!)
def replay_vals(D_g, A_g):
    val = [1 << i for i in range(nreg0)]
    cur = list(start)
    def climb(r, F):
        if cur[r] != F:
            assert dims[F] >= dims[cur[r]], 'climb %d: %d -> %d' % (r, dims[cur[r]], dims[F])
            cur[r] = F
    for F, d, srcs in D_g:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in A_g:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    return val, cur

valA, curA = replay_vals(D, A)
xp = [valA[r] & XMASK for r in ret_list]              # the 10 x-parts!!
# the B0-rows (the 121!!): the {t} U perp_121(t)!!
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
Brows = []
for t in range(V):
    m = 1 << t
    for u in range(V):
        if u != t and ip121(V9[t], V9[u]) == 0:
            m |= 1 << u
    Brows.append(m)
# the unique solve: the B0-rows over the 10-xp's (the rank 10!!)
piv = []
for k in range(10):
    x = xp[k]
    for p in piv: x = min(x, x ^ p)
    assert x, 'the xp-independence!!'
    piv.append(x); piv.sort(reverse=True)
# the reduced-echelon solve: build the coords tracker!!
rows = list(xp); aug = [[1 if i == j else 0 for j in range(10)] for i in range(10)]
r = 0; pivots = []; T = []
for col in range(V):
    piv_i = next((i for i in range(r, 10) if (rows[i] >> col) & 1), None)
    if piv_i is None: continue
    rows[r], rows[piv_i] = rows[piv_i], rows[r]
    aug[r], aug[piv_i] = aug[piv_i], aug[r]
    for i in range(10):
        if i != r and (rows[i] >> col) & 1:
            rows[i] ^= rows[r]; aug[i] = [a ^ b for a, b in zip(aug[i], aug[r])]
    pivots.append((col, rows[r])); T.append(list(aug[r])); r += 1
assert r == 10, 'the rank %d (expected 10!!)' % r
def solve10(row):
    coords = [0] * 10; rr = row
    for k, (col, rw) in enumerate(pivots):
        if (rr >> col) & 1:
            coords[k] = 1; rr ^= rw
    assert rr == 0, 'the residual!!'
    return coords
Wred10 = [solve10(Brows[t]) for t in range(V)]        # the 121 x 10 (THE REDUCED coords!!)
Wp = []                                               # W_orig = W_red x T (THE SS1500 FIX!!)
for t in range(V):
    w = [0] * 10
    for k in range(10):
        if Wred10[t][k]:
            for j in range(10):
                if T[k][j]:
                    w[j] ^= 1
    Wp.append(w)
# the verification!!
for t in range(V):
    acc = 0
    for k in range(10):
        if Wp[t][k]: acc ^= xp[k]
    assert acc == Brows[t], 'the Wp-verification at t=%d!!' % t
log('(1) the Wp: the 121 x 10 (the rank-10 unique!!) | the verification PASS!!')
PHI = lambda row: (row >> SP) & 1
log('    the xp-phis: %s (the ODD-ret (the index 9): phi = %d!!)' % (
    [PHI(x) for x in xp], PHI(xp[9])))

# ============ (2) THE SS1492-BASIS (the 8-even + the odd!!) ============
# the basis: the odd = B[0] (phi = 1!!); the even = B[0] ^ B[k] (phi = 0!!) for the 8 k's!!
cands = [k for k in range(1, V) if PHI(Brows[k]) == 1]
sel = []; cur = [Brows[0]]
def gf2_rank(rows_in):
    rs = list(rows_in); rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rs)) if (rs[i] >> col) & 1), None)
        if piv is None: continue
        rs[rank], rs[piv] = rs[piv], rs[rank]
        for i in range(len(rs)):
            if i != rank and (rs[i] >> col) & 1: rs[i] ^= rs[rank]
        rank += 1
    return rank
for k in cands:
    if gf2_rank(cur + [Brows[k]]) == len(cur) + 1:
        sel.append(k); cur = cur + [Brows[k]]
        if len(sel) == 8: break
assert len(sel) == 8 and gf2_rank(cur) == 9, 'the SS1492-basis!!'
basis = [Brows[0] ^ Brows[k] for k in sel] + [Brows[0]]     # the 8-even + the odd!!
log('(2) the SS1492-basis: the even k = %s + the odd (B[0]!!) | the phis: %s' % (
    sel, [PHI(b) for b in basis]))
# the basis-rows' representations-over-the-10 = the Wp-rows' XORs!!
repB = []
for j, brow in enumerate(basis):
    # the brow = B[0] ^ B[k] (the even!!): the rep = Wp[0] ^ Wp[k]; the odd: the Wp[0]!!
    if j < 8:
        rep = [Wp[0][q] ^ Wp[sel[j]][q] for q in range(10)]
    else:
        rep = list(Wp[0])
    # the verification!!
    acc = 0
    for q in range(10):
        if rep[q]: acc ^= xp[q]
    assert acc == brow, 'the rep-verification (the basis-row %d!!)' % j
    repB.append(rep)
log('    the reps-over-the-10 verified!! (the ODD-coefficients: %s — MUST be 0 for the evens!!)' % (
    [repB[j][9] for j in range(8)]))
assert all(repB[j][9] == 0 for j in range(8)), 'THE EVEN-REPS MUST NOT USE THE ODD-RET!!'

# ============ (3) THE ODD-REP ANALYSIS (the 9th-ret = the OLD-ODD (the 662!!)!!) ============
# THE DISCOVERY: the odd-rep = [0,...,0,1] — the B[0]-pattern IS the OLD-ODD-ret (the 662)'s
# x-part ALONE!! -> the 9th-ret = the 662 REUSED (no new odd-register!!)!! And the ret-0/1
# (605/570) are NOT rets anymore (the internal helpers (the OLD-ODD's build-srcs!!)!!)!!
log('(3) the odd-rep (the B[0] over the 10!!): %s (the old-ODD-coeff = %d!!) -> THE 9th-RET = THE OLD-ODD (662!!)!!' % (
    repB[8], repB[8][9]))
assert repB[8][9] == 1 and sum(repB[8]) == 1, 'the odd-rep = the OLD-ODD alone!!'

# ============ (4) THE NEW-RETS (the 8-even!!) + THE A-BUILDS (BEFORE the ODD!!) ============
NEW0 = 2 * V + R                                      # the first new register (the R+9 = 472!!)
NEW = [NEW0 + j for j in range(8)]                    # the 8-even!!
ret_list_new = NEW + [ret_list[9]]                    # the 8-even + the OLD-ODD (the 662!!)
ret_frames_new = [IDX_R8] * 8 + [IDX_FULL]            # the 8 x dim-8 + the 1 x dim-9 = THE CST 73!!
# THE BUILD-ORDER-CONCERN: the ret-0/1 (605/570) climb to the FULL at the OLD-ODD's build
# gate ([IDX_FULL, 662, [605, 570, SP]]!!) — the 8-even's builds MUST GO BEFORE IT (while
# the 605/570 still sit at the IDX_R8 (dim-8!!): the SAME-FRAME FREE reads!!
odd_gate_ix = next(i for i, g in enumerate(A) if g[1] == ret_list[9])
log('(4) the 8-even A-builds (the INSERT before the ODD-gate (the A-index %d!!)!!)' % odd_gate_ix)
builds = [[IDX_R8, NEW[j], [ret_list[q] for q in range(10) if repB[j][q]]] for j in range(8)]
# (4a) THE O0-CARRIER (NEW8!!): the SPECIAL's channel needs val[605] (= O_0!!) delivered
# at IDX_R8 — but 605 sits at the FULL after the ODD-gate!!  THE LAW: w* = e_0 (the rho=9
# complement!!) -> the NEW-rets can NEVER deliver the coord-0 (repB[.][0] = 0 for ALL j!!)
# and xp[0] is independent of xp[2..8] -> THE ONLY ROUTE: a fresh carrier built from 605
# BEFORE its FULL-climb: val[NEW8] = 1<<NEW8 ⊕ O_0 (the FULL value: x + dirt!!)!!
NEW8 = NEW0 + 8
builds.append([IDX_R8, NEW8, [ret_list[0]]])
log('    the srcs-sizes: %s (the ret-0/1-involved: %s!!) + THE O0-CARRIER NEW8=%d' % (
    [len(g[2]) for g in builds],
    [j for j in range(8) if repB[j][0] or repB[j][1]], NEW8))
A[odd_gate_ix:odd_gate_ix] = builds
# the scatter: the 121 x 9: the B[t] = XOR(W[t][j] NEW[j]!!)!!
#   the W: the B[t]'s-representation-over-the-9-basis (the SS1500's solve!!)!!
rowsB = list(basis); augB = [[1 if i == j else 0 for j in range(9)] for i in range(9)]
rB = 0; pivB = []; TB = []
for col in range(V):
    piv_i = next((i for i in range(rB, 9) if (rowsB[i] >> col) & 1), None)
    if piv_i is None: continue
    rowsB[rB], rowsB[piv_i] = rowsB[piv_i], rowsB[rB]
    augB[rB], augB[piv_i] = augB[piv_i], augB[rB]
    for i in range(9):
        if i != rB and (rowsB[i] >> col) & 1:
            rowsB[i] ^= rowsB[rB]; augB[i] = [a ^ b for a, b in zip(augB[i], augB[rB])]
    pivB.append((col, rowsB[rB])); TB.append(list(augB[rB])); rB += 1
assert rB == 9, 'the basis-rank %d!!' % rB
def solve9(row):
    coords = [0] * 9; rr = row
    for k, (col, rw) in enumerate(pivB):
        if (rr >> col) & 1: coords[k] = 1; rr ^= rw
    assert rr == 0, 'the 9-residual!!'
    return coords
Wred = [solve9(Brows[t]) for t in range(V)]
W = []
for t in range(V):
    w = [0] * 9
    for k in range(9):
        if Wred[t][k]:
            for j in range(9):
                if TB[k][j]: w[j] ^= 1
    W.append(w)
for t in range(V):
    acc = 0
    for j in range(9):
        if W[t][j]: acc ^= basis[j]
    assert acc == Brows[t], 'the W-verification at t=%d!!' % t
scatter = [[j for j in range(9) if W[t][j]] for t in range(V)]
log('    the W (the 121 x 9!!) verified!! the row-sizes: %s (the special: %s)' % (
    dict(sorted(Counter(len(s) for s in scatter).items())), scatter[SP]))

# ============ (4b) THE D-EXTENSION (the self-bits cancel — THE BALANCE LAW!!) ============
# THE LAW: val[NEW_j] = 1<<NEW_j ⊕ (⊕_{q∈repB[j]} val[old_q]) -> the NEW row's value =
# the OLD row's value ⊕ (⊕_{j∈W[t]∖{8}} 1<<NEW_j) (the expansion ⊕ repB[j] = Wp[t] —
# AUTOMATIC!!).  The D-gates run BEFORE the A-builds (the helpers = the PURE self-bits,
# the EMPTY x-content: legal at frame 0!!) -> the extension [0, V+t, NEWS] cancels the
# self-bits for EVERY target: THE WORD3 BALANCE RESTORED VERBATIM (the B UNTOUCHED!!)
dext = []
for t in range(V):
    news = [NEW[j] for j in scatter[t] if j < 8]
    if news:
        dext.append([0, V + t, news])
dext.append([0, V + SP, [NEW8]])         # THE SPECIAL: the NEW8 self-bit cancel!!
D = list(D) + dext
# (4c) THE SPECIAL's B-CHANNEL: the 7-old-rets read (the OLD split-delivery!!) -> THE
# NEW8 read (the O_0-delivery!!): the new row delivers ALL-ONES alone (the unique
# Wp[120] = {1,9}!! — the old row was the NON-UNIQUE all-10 combo (the coord-0!!)) ->
# the old read would DOUBLE-DELIVER: REPLACE it (the [253]x2 stay: value-neutral!!).
old7 = [IDX_R8, V + SP, [ret_list[q] for q in range(2, 9)]]
ix7 = B.index(old7)
B[ix7] = [IDX_R8, V + SP, [NEW8]]
log('(4b) THE D-EXTENSION: %d gates (the src-sizes %s) + THE SPECIAL: the B#%d 7-ret read -> THE NEW8!!' % (
    len(dext), dict(sorted(Counter(len(g[2]) for g in dext).items())), ix7))

# ============ (5) THE REPLAY (the ext7's full semantics!!) ============
nreg = nreg0 + 9
startN = start + [0] * 9                          # the ext7 convention (the identity h·R!!)
finalN = final + [IDX_FULL] * 9
C = [[IDX_FULL, d, s] for F, d, s in
     reversed([[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)])]
def replay(D_g, A_g, B_g, C_g, rows, retl, retf):
    val = [1 << i for i in range(nreg)]
    cur = list(startN)
    hist = Counter(); junk = [set() for _ in range(V)]
    tgt_dirt = [0] * V; tgt_scatter = [0] * V; tgt_reads = [0] * V
    def climb(r, F):
        if cur[r] == F: return
        assert dims[F] >= dims[cur[r]], 'DECREASING climb (reg %d): %d -> %d' % (
            r, dims[cur[r]], dims[F])
        hist[dims[F] - dims[cur[r]]] += 1
        cur[r] = F
    def run(gates):
        for F, d, srcs in gates:
            for r in [d] + srcs: climb(r, F)
            for s in srcs: val[d] ^= val[s]
    for F, d, srcs in D_g:
        acc = 0
        for s in srcs: acc ^= val[s]
        tgt_dirt[d - V] ^= acc
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    run(A_g)
    for t in range(V):
        acc = 0
        for k in rows[t]: acc ^= val[retl[k]]
        tgt_scatter[t] = acc
        xj = acc & XMASK
        while xj:
            b = xj & -xj
            junk[t].add(b.bit_length() - 1)
            xj ^= b
        val[V + t] ^= acc
    for F, d, srcs in B_g:
        for r in [d] + srcs: climb(r, F)
        if V <= d < 2 * V:
            acc = 0
            for s in srcs:
                acc ^= val[s]
                xs = val[s] & XMASK
                while xs:
                    b = xs & -xs
                    junk[d - V].add(b.bit_length() - 1)
                    xs ^= b
            tgt_reads[d - V] ^= acc
        for s in srcs: val[d] ^= val[s]
    run(C_g)
    for r in range(nreg): climb(r, finalN[r])
    bad = []
    want0 = [(1 << r) ^ ((1 << (r - V)) if V <= r < 2 * V else 0) for r in range(nreg)]
    for r in range(nreg):
        if val[r] != want0[r]: bad.append(r)
    return dict(bad=bad, hist=hist, junk=junk, tgt_dirt=tgt_dirt,
                tgt_scatter=tgt_scatter, tgt_reads=tgt_reads, cur=cur)
rep = replay(D, A, B, C, scatter, ret_list_new, ret_frames_new)
log('(5) THE REPLAY: the finals fails %d (the sources %d, the targets %d, the helpers %d)' % (
    len(rep['bad']),
    sum(1 for r in rep['bad'] if r < V),
    sum(1 for r in rep['bad'] if V <= r < 2 * V),
    sum(1 for r in rep['bad'] if r >= 2 * V)))
if rep['bad']:
    xres = Counter(); dres = Counter()
    for t in range(V):
        res = (rep['tgt_dirt'][t] ^ rep['tgt_scatter'][t] ^ rep['tgt_reads'][t]) ^ (1 << t)
        rx = res & XMASK; rd = res >> V
        if rx: xres[bin(rx).count('1')] += 1
        if rd: dres[bin(rd).count('1')] += 1
    log('    THE DIAGNOSIS: the x-residues %s | the dirt-residues %s' % (
        dict(sorted(xres.items())), dict(sorted(dres.items()))))
    sys.exit(1)

# ============ (6) THE COMPLETENESS + THE HIST + THE CST!! ============
PERP = [set() for _ in range(V)]
for t in range(V):
    for u in range(V):
        if u != t and ip121(V9[t], V9[u]) == 0:
            PERP[t].add(u)
inc = [t for t in range(V) if not (PERP[t] <= (rep['junk'][t] - {t}))]
log('(6) THE COMPLETENESS: the incomplete %d/121 | the junk-minus-self sizes %s' % (
    len(inc), dict(sorted(Counter(len(rep['junk'][t] - {t}) for t in range(V)).items()))))
assert not inc, 'THE INCOMPLETE TARGETS: %s!!' % inc[:12]
for f in ret_frames_new:
    rep['hist'][dims[f]] += 1
cst = sum(dims[f] for f in ret_frames_new)
mass = sum(k * n for k, n in rep['hist'].items())
ident = H * (R + 9) + cst + 2 * V * (H - 1)
log('    THE HIST: %s' % dict(sorted(rep['hist'].items())))
log('    THE CST = %d (the word3: 83!!) | the mass %d vs the identity %d: %s' % (
    cst, mass, ident, 'MATCH!!' if mass == ident else 'MISMATCH!!'))
assert mass == ident, 'the mass-identity!!'

# ============ (7) THE EMISSION + THE TRUE-PRICE!! ============
word = {
    'h': H, 'v': V, 'R': R + 9,
    'form': W3['form'], 'lines': lines, 'frames': frames,
    'start': startN, 'final': finalN,
    'D': D, 'A': A, 'B': B, 'C': C,
    'ret': ret_list_new, 'ret_frames': ret_frames_new, 'scatter': scatter,
}
OUT = 'ii19_own_word4.json'
json.dump(word, open(OUT, 'w'))
log('(7) THE WORD4 EMITTED: %s (the nreg %d, the R %d (+9!!), the CST %d!!)' % (
    OUT, nreg, R + 9, cst))
log('    THE GCHECK NEXT: /Users/dayssky/.venv/bin/python '
    'research/lorentzian-frame-cell-handoff/code/tword/gcheck.py %s --price' % OUT)
# THE TRUE-PRICE (the price_damped (the battery-verified!!)!!)
import pricer
pricer.price = None  # the safety: no-undamped!!
from pricer import idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')
def price_damped(local, v, h, R, K=4, T=32, w=None, max_iter=200):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L; W_ = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, None, dict(error='hosting wall')
    q = mpf('0.0017'); q2 = None; conv = False
    for it in range(max_iter):
        rem = host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W_)
        if q2 is None: return None, prof, dict(error='no root')
        if abs(q2 - q) < mpf(10) ** -25: conv = True; break
        q = (q + q2) / 2
    d = dict(converged=conv, iters=it + 1)
    return q2, prof, d
hist = dict(rep['hist'])
c4, prof, d4 = price_damped(hist, V, H, R + 9)
if c4 is None:
    log('    THE TRUE-PRICE: NO ROOT (%s)!!' % d4)
else:
    pct = (c4 / FRONTIER - 1) * 100
    log('    THE TRUE-PRICE (the hist %s): c = %.9f (%+.2f%% vs frontier) [%s]' % (
        dict(sorted(hist.items())), c4, pct, d4))
log('DONE — THE WORD4 (the CST %d!!)' % cst)
