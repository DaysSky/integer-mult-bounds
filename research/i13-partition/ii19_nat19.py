"""THE NATIVE-121 v19 (ii19_nat19.py) — THE R=130-COLLAPSE's PRE-EMISSION AUDIT (THE MEASUREMENT!!!)

THE §1-HANDOFF's-DESIGN (the R=130 (the H_u's-121 + the rets-9!!)) — THE REMAINING-CORE:
the residue-fix.  THE AUDIT's-THREE-QUESTIONS (the honest pre-build check (the SS2141-discipline!!)):
  (Q1) THE RESIDUE: the register-self-bits (the rho_t = the D's perp(t)-H_u-bits + the scatter's
       ret-bits!!) — THE FIX (the W4's-own D-EXTENSION-LAW (the SS1862!!)): the D-srcs = the
       parity-merge {the row_t-rets} (+ the H_u-parity IF a B-phase reads them!!).
  (Q2) THE X-BALANCE: the D-runs-FIRST (the gcheck's-line-100!!) -> the D-srcs are PRE-BUILD
       (the pure self-bits, the x-part-0!!!) -> THE D CANNOT DELIVER THE e_u's!!!  The x-parts
       reach the targets ONLY via the scatter (the rets'-x-patterns!!) + the B-reads (the built
       carriers!!) -> the no-B-skeleton's x-residues = the perp(t)-patterns (THE MEASURE!!!).
  (Q3) THE B-WALL: the B-phase's cancellation (the perp(t)-e_u's!!) reads the H_u's at frames
       F_t ⊆ perp-space(t) ⊇ the perp(t)-lines -> F_t = perp-frame(t) FORCED (the dim-8!!)
       -> the H_u's read at the ~64 users'-perp-frames (the PAIRWISE-INCOMPARABLE dim-8's!!)
       -> THE ONE-CLIMB-WALL (the SS1946!!!) — THE MEASURE (the privatization-count!!).

THE ALTERNATIVES'-MATH (the Q2's-closing-channels!!):
  (A) the B-phase: the wall (the nat9-11's-core-conflict!!)
  (B) the scatter-rets (the cancellation-patterns-as-rets!!): the perp-patterns'-GF(2)-RANK (the
      ~112-expected!!) vs the CST-BUDGET (the 256v/288 = 107.6!!) -> THE DEFICIT-DEAD (the measure!!)
"""
import json, time
from collections import Counter

W4 = json.load(open('ii19_own_word4.json', 'rt'))
V, H, SP = W4['v'], W4['h'], 120
lines = W4['lines']
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]

# ============ (0) THE PERPS + THE BROWS + THE CODE + THE MIN-WEIGHT-BASIS ============
PERP = [set(u for u in range(V) if u != t and ip121(lines[t], lines[u]) == 0) for t in range(V)]
log('(0) the perps: the sizes %s (the special: %d)' % (
    dict(sorted(Counter(len(p) for p in PERP).items())), len(PERP[SP])))
Brows = []
for t in range(V):
    m = 1 << t
    for u in PERP[t]: m |= 1 << u
    Brows.append(m)
assert Brows[SP] == (1 << V) - 1, 'the special-Brows = the all-ones!!'
basis = {}; rank = 0
for r in Brows:
    x = r
    while x:
        p = (x & -x).bit_length() - 1
        if p in basis: x ^= basis[p]
        else: basis[p] = x; rank += 1; break
assert rank == 9, 'the Brows-rank %d!!' % rank
piv = sorted(basis.items())
cws = set()
for mask in range(1 << 9):
    x = 0
    for k, (p, r) in enumerate(piv):
        if (mask >> k) & 1: x ^= r
    cws.add(x)
wts = Counter(bin(x).count('1') for x in cws)
log('    the code: %d codewords | the weights %s' % (len(cws), dict(sorted(wts.items()))))
# the min-weight basis (the 9-lightest-independent (the 8-even + the 1-odd FORCED (the rank-8-even-subcode!!)))
cands = sorted(cws, key=lambda x: (bin(x).count('1'), x))
mw = []; bx = {}
for x in cands:
    y = x
    while y:
        p = (y & -y).bit_length() - 1
        if p in bx: y ^= bx[p]
        else: bx[p] = y; mw.append(x); break
    if len(mw) == 9: break
assert len(mw) == 9
log('    THE MIN-WEIGHT-BASIS: the weights %s (the phis %s)' % (
    [bin(x).count('1') for x in mw], [(x >> SP) & 1 for x in mw]))
# the W-solve (the rows: Brows[t] = XOR(mw[k]: k in row_t)!!)
rowsB = list(mw); augB = [[1 if i == j else 0 for j in range(9)] for i in range(9)]
rB = 0; pivB = []; TB = []
for col in range(V):
    pi = next((i for i in range(rB, 9) if (rowsB[i] >> col) & 1), None)
    if pi is None: continue
    rowsB[rB], rowsB[pi] = rowsB[pi], rowsB[rB]
    augB[rB], augB[pi] = augB[pi], augB[rB]
    for i in range(9):
        if i != rB and (rowsB[i] >> col) & 1:
            rowsB[i] ^= rowsB[rB]; augB[i] = [a ^ b for a, b in zip(augB[i], augB[rB])]
    pivB.append((col, rowsB[rB])); TB.append(list(augB[rB])); rB += 1
assert rB == 9
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
        if W[t][j]: acc ^= mw[j]
    assert acc == Brows[t], 'the W-verification at t=%d!!' % t
scatter = [[j for j in range(9) if W[t][j]] for t in range(V)]
log('    the W-solve verified!! the row-sizes %s (the special: %s)' % (
    dict(sorted(Counter(len(s) for s in scatter).items())), scatter[SP]))

# ============ (1) THE R=130-SKELETON (THE NO-B!!) — THE TWO-D-VARIANTS ============
# the registers: the sources 0..120 | the targets 121..241 | the H_u 242..362 | the rets 363..371
R = 130
nreg = 2 * V + R
HU = [2 * V + u for u in range(V)]                    # 242..362
RET = [2 * V + V + j for j in range(9)]               # 363..371
XMASK = (1 << V) - 1
# the frames (the dims-table (the replay's-climb-mass!!)): 0 | the singletons (1) | FULL (9)
#   | R8 (the roots-span (dim-8!!)) | the perps (dim-8!!)
DIM = {0: 0}
for u in range(V): DIM[1 + u] = 1                       # the singletons
DIM[1 + V] = 9                                          # the FULL
DIM[2 + V] = 8                                          # the R8 (the roots-span!!)
for t in range(V): DIM[3 + V + t] = 8                   # the perps
F_SP, F_FULL, F_R8, F_PERP = lambda u: 1 + u, 1 + V, 2 + V, lambda t: 3 + V + t
# the A-gates: the H_u-builds + the ret-builds (the evens at R8 (the roots-supports!!) + the odd at FULL!!)
A = [[F_SP(u), HU[u], [u]] for u in range(V)]
for j in range(9):
    sup = [i for i in range(V) if (mw[j] >> i) & 1]
    fr = F_R8 if not ((mw[j] >> SP) & 1) else F_FULL
    A.append([fr, RET[j], sup])
log('(1) the A: %d gates (the H_u-builds 121 + the ret-builds 9 (the evens %d at R8 + the odd at FULL!!))' % (
    len(A), sum(1 for j in range(9) if not ((mw[j] >> SP) & 1))))

def replay(dsrcs_mode):
    """the D+A+scatter replay (the no-B (the no-C (the nat18b: the C-restores-only-helpers!!!)))"""
    val = [1 << i for i in range(nreg)]
    cur = [0] * nreg
    for u in range(V): cur[u] = F_SP(u)                 # the sources'-starts
    hist = Counter()
    def climb(r, F):
        if cur[r] == F: return
        assert DIM[F] > DIM[cur[r]], 'DECREASING climb (reg %d)!!' % r
        hist[DIM[F] - DIM[cur[r]]] += 1
        cur[r] = F
    # D: [0, V+t, the srcs] (the PRE-BUILD (the pure-self-bits!!!))
    for t in range(V):
        srcs = [RET[k] for k in scatter[t]]
        if dsrcs_mode == 'faithful':
            srcs = srcs + [HU[u] for u in sorted(PERP[t])]
        for r in [V + t] + srcs: climb(r, 0)
        for s in srcs: val[V + t] ^= val[s]
    # A
    for F, d, srcs in A:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    # the scatter (the FREE (the no-climbs (the no-content!!!)))
    for t in range(V):
        for k in scatter[t]: val[V + t] ^= val[RET[k]]
    # the finals'-climbs (the sources/rets/H_u -> FULL | the targets -> the perps!!)
    for u in range(V): climb(u, F_FULL)
    for r in HU + RET: climb(r, F_FULL)
    for t in range(V): climb(V + t, F_PERP(t))
    for c in [8, 8, 8, 8, 8, 8, 8, 8, 9]: hist[c] += 1  # the CST-73 (the copy-ranks!!)
    mass = sum(k * n for k, n in hist.items())
    # the finals'-residues (the targets!!): the x-part (the low-bits!!) + the register-part!!
    xres = Counter(); dres = Counter()
    for t in range(V):
        want = (1 << (V + t)) ^ (1 << t)
        res = val[V + t] ^ want
        rx = bin(res & XMASK).count('1'); rd = bin(res >> V).count('1')
        xres[rx] += 1; dres[rd] += 1
    return dict(hist=hist, mass=mass, xres=xres, dres=dres)

rep_faith = replay('faithful')
log("(2) THE FAITHFUL-D-REPLAY (the §1's-D (the perp(t)-H_u-reads!!)):")
log("    THE REGISTER-RESIDUES (the §1's rho_t!!): %s" % dict(sorted(rep_faith['dres'].items())))
log('    THE X-RESIDUES: %s' % dict(sorted(rep_faith['xres'].items())))
log('    the mass %d vs the identity %d: %s' % (
    rep_faith['mass'], 9 * R + 73 + 2 * V * 8,
    'MATCH!!' if rep_faith['mass'] == 9 * R + 73 + 2 * V * 8 else 'MISMATCH!!'))
rep_fixed = replay('fixed')
log('(3) THE FIXED-D-REPLAY (THE D-EXTENSION (the row_t-rets-ONLY (the SS1862-LAW!!))):')
log('    THE REGISTER-RESIDUES (THE RESIDUE-FIX!!!): %s' % dict(sorted(rep_fixed['dres'].items())))
log('    THE X-RESIDUES (THE CANCELLATION-GAP!!!): %s' % dict(sorted(rep_fixed['xres'].items())))
log('    the hist %s | the mass %d vs the identity %d: %s' % (
    dict(sorted(rep_fixed['hist'].items())), rep_fixed['mass'], 9 * R + 73 + 2 * V * 8,
    'MATCH!!' if rep_fixed['mass'] == 9 * R + 73 + 2 * V * 8 else 'MISMATCH!!'))

# ============ (4) THE B-WALL (THE ONE-CLIMB (the H_u's-users!!)) ============
# the H_u's users: the t's with u in perp(t) = PERP[u] (the symmetry!!) — the reads at the
# perp-frames (the FORCED (the F_t ⊇ span(perp(t)-lines) = perp-space(t) ∧ F_t ⊆ perp-space(t)!!))
# — the pairwise-INCOMPARABLE dim-8's (perp-space(t) == perp-space(w) iff L[t] || L[w]: NEVER!!)
users_sz = Counter(len(PERP[u]) for u in range(V))
privat = sum(len(PERP[u]) - 1 for u in range(V))
log('(4) THE B-WALL: the H_u\'s-users-sizes %s | the ONE-FRAME-BUDGET (the max-chain = 1 (the '
    'incomparables!!)) -> THE PRIVATIZATION-COUNT %d (the R = 130 + %d = %d?!?! (the W4: 472!!))' % (
    dict(sorted(users_sz.items())), privat, privat, R + privat))

# ============ (5) THE ALTERNATIVE-B (THE CANCELLATION-RETS'-CST-MATH!!) ============
# the perp-patterns {Brows[t] ^ (1<<t)}: the GF(2)-RANK (the ret-basis'-minimum!!) vs the CST-budget!!
pp = [Brows[t] ^ (1 << t) for t in range(V)]
pb = {}; prank = 0
for r in pp:
    x = r
    while x:
        p = (x & -x).bit_length() - 1
        if p in pb: x ^= pb[p]
        else: pb[p] = x; prank += 1; break
budget = (256 * V) / 288.0
log('(5) THE CANCELLATION-RETS\'-MATH: the perp-patterns\'-GF(2)-rank %d | the frame-dims >= 1 each '
    '-> the CST >= 73 + %d = %d vs THE BUDGET 256v/288 = %.1f -> %s' % (
    prank, prank, 73 + prank, budget,
    'DEAD (the deficit NEGATIVE!!)' if 73 + prank > budget else 'LIVE!!'))

# ============ (6) THE TWO-PRICE-TESTS (THE DECISIVE-EVIDENCE!!) ============
# (6a) THE R=130-HIST (the IF-IT-CLOSED (the §1's "+50-60%"-claim!!)): the audit's-fixed-hist!!
# (6b) THE NO-B-RETS-ROUTE (R = 251 (the +121-singleton-rets!!), the CST 194 (the deficit-NEGATIVE!!)):
#      the hist {1: 249+121(builds)+121(copies!!), 7: 120, 8: 259+121, 9: 2} (the mass 4389 (the identity!!))
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
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
    if nres > cap: return None, None, dict(error='hosting wall (nres %d > cap %d!!)' % (nres, cap))
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
    return q2, prof, dict(converged=conv, iters=it + 1)

log('(6a) THE R=130-IF-IT-CLOSED-PRICE (the audit\'s-legal-hist (the fixed-D!!)):')
h130 = dict(rep_fixed['hist'])
c130, prof, d130 = price_damped(h130, V, H, R)
if c130 is None:
    log('    NO PRICE (%s)!!' % d130)
else:
    log('    c = %s (%+.2f%% vs the frontier!!) [%s]' % (mp.nstr(c130, 22),
        float((c130 / FRONTIER - 1) * 100), d130))
log('(6b) THE NO-B-RETS-ROUTE-PRICE (R=251, the CST 194 (the deficit %d!!)):' % (256 * V - 288 * 194))
h251 = dict(rep_fixed['hist'])
h251[1] = h251.get(1, 0) + 242      # the 121-SRET-builds (+1!!) + the 121-copies (the CST-part!!)
h251[8] = h251.get(8, 0) + 121      # the SRET-finals (the singleton->FULL!!)
mass251 = sum(k * n for k, n in h251.items())
c251, prof, d251 = price_damped(h251, V, H, 251)
log('    the hist %s (the mass %d vs the identity %d: %s!!)' % (
    dict(sorted(h251.items())), mass251, 9 * 251 + 194 + 2 * V * 8,
    'MATCH' if mass251 == 9 * 251 + 194 + 2 * V * 8 else 'MISMATCH'))
if c251 is None:
    log('    NO PRICE (%s)!!' % d251)
else:
    log('    c = %s (%+.2f%% vs the frontier!!) [%s]' % (mp.nstr(c251, 22),
        float((c251 / FRONTIER - 1) * 100), d251))
log('DONE — THE NAT19-AUDIT (the §1-design\'s-true-state (the measured!!!))')
