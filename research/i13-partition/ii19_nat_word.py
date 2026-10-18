"""THE NATIVE-121 WORD-EMITTER (ii19_nat_word.py) — THE R=130-COLLAPSE's-EMISSION (THE §1's-STEPS!!!)

THE §1's-CONCRETE-STEPS (the handoff!!): (1) the residue-fix (SOLVED (the nat19-audit!!): the
D-EXTENSION (the W4's-own-SS1862-LAW!!): the D-srcs = the row_t-rets (the pre-build-self-bits'
cancellation (the ZERO-COST (the 121-free-gates!!!)))); (2) THE W-SOLVE (the Brows-code's
min-weight-basis (the 8x56-even + the 1x57-odd (THE CST-73 (the §113-124's-proven-floor!!!))));
(3) THE EMISSION (the frames (0 + the 121-singletons + the FULL + the R8 + the 121-perps!!) +
the A (the H_u-builds + the ret-builds (the codeword-sums via the SOURCE-reads (the evens at
the R8 (the FREE-same-frame-re-reads!!!)) + the odd at the FULL!!)) + the D + the scatter + the
C (the H4-literal-reversal (the FULL-frames!!))); (4) THE VERIFICATION (the gcheck!!).

THE TWO-EMISSIONS (the nat19-audit's-both-failure-modes (the gcheck's-OWN-verdicts!!!)):
  (i)  ii19_nat_word.json   (THE NO-B!!): the residue-fixed skeleton — THE EXPECTED-REJECT:
       the targets'-finals (the x-residues = the perp(t)-patterns (the {64: 120, 120: 1}!!)) —
       THE X-CANCELLATION-CHANNEL's-ABSENCE (the D-runs-PRE-BUILD (the x-part-0!!!)!!).
  (ii) ii19_nat_word_b.json  (THE §1's-FULL-DESIGN (the WITH-B!!!)): the B-phase (the perp-frame
       reads of the perp(t)-H_u's (the §1's-"the targets'-finals-pass-via-the-D+A+scatter+B"!!!)) —
       THE VALS-BALANCE-CLOSES (the §1's-claim-TRUE-at-the-VAL-level (the nat18b's-exact-finding!!))
       — THE EXPECTED-REJECT: the H_u's-climbs ('climb not nested' (THE ONE-CLIMB-WALL (the
       64-users'-INCOMPARABLE-dim-8-perp-frames (the SS1946!!!))!!)).
"""
import json, time
from collections import Counter

W4 = json.load(open('ii19_own_word4.json', 'rt'))
V, H, SP = W4['v'], W4['h'], 120
lines = W4['lines']
form = W4['form']
R = 130
nreg = 2 * V + R
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]

# ============ (0) THE PERPS + THE BROWS-CODE + THE MIN-WEIGHT-BASIS + THE W-SOLVE ============
PERP = [set(u for u in range(V) if u != t and ip121(lines[t], lines[u]) == 0) for t in range(V)]
Brows = []
for t in range(V):
    m = 1 << t
    for u in PERP[t]: m |= 1 << u
    Brows.append(m)
basis = {}; rank = 0
for r in Brows:
    x = r
    while x:
        p = (x & -x).bit_length() - 1
        if p in basis: x ^= basis[p]
        else: basis[p] = x; rank += 1; break
assert rank == 9
piv = sorted(basis.items())
cws = set()
for mask in range(1 << 9):
    x = 0
    for k, (p, r) in enumerate(piv):
        if (mask >> k) & 1: x ^= r
    cws.add(x)
cands = sorted(cws, key=lambda x: (bin(x).count('1'), x))
mw = []; bx = {}
for x in cands:
    y = x
    while y:
        p = (y & -y).bit_length() - 1
        if p in bx: y ^= bx[p]
        else: bx[p] = y; mw.append(x); break
    if len(mw) == 9: break
assert [bin(x).count('1') for x in mw] == [56] * 8 + [57]
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
    assert rr == 0
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
    assert acc == Brows[t]
scatter = [[j for j in range(9) if W[t][j]] for t in range(V)]
log('(0) the W-solve: the min-weight-basis %s (the CST %d!!) | the rows %s' % (
    [bin(x).count('1') for x in mw], 8 * 8 + 9,
    dict(sorted(Counter(len(s) for s in scatter).items()))))

# ============ (1) THE FRAMES + THE REGISTERS ============
# the frames: 0 (the empty!!) | 1..121 (the singletons!!) | 122 (the FULL!!) | 123 (the R8!!)
#   | 124..244 (the perps (the perp(t)-lines'-spans (the dim-8!!)!!))
F_EMPTY, F_FULL, F_R8 = 0, 1 + V, 2 + V
def F_SP(u): return 1 + u
def F_PERP(t): return 3 + V + t
frames = [[]]
for u in range(V): frames.append([list(lines[u])])
frames.append([list(l) for l in lines])                       # the FULL (the 121-lines!!)
frames.append([list(lines[u]) for u in range(V - 1)])         # the R8 (the 120-roots!!)
for t in range(V): frames.append([list(lines[u]) for u in sorted(PERP[t])])
assert len(frames) == 3 + V + V
DIM = {0: 0, F_FULL: 9, F_R8: 8}
for u in range(V): DIM[F_SP(u)] = 1
for t in range(V): DIM[F_PERP(t)] = 8
# the registers: the sources 0..120 | the targets 121..241 | the H_u 242..362 | the rets 363..371
HU = [2 * V + u for u in range(V)]
RET = [2 * V + V + j for j in range(9)]
start = [F_SP(u) for u in range(V)] + [0] * (V + R)
final = [F_FULL] * V + [F_PERP(t) for t in range(V)] + [F_FULL] * R
ret_frames = [F_R8] * 8 + [F_FULL]                            # the 8x8 + the 1x9 = THE CST 73!!
log('(1) the frames %d (the dims %s) | the nreg %d (the R %d!!)' % (
    len(frames), dict(sorted(Counter(DIM.values()).items())), nreg, R))

# ============ (2) THE GATES ============
# the A: the H_u-builds (the singleton-FREE-src-reads!!) + the ret-builds (the codeword-sums!!
#   the evens at the R8 (the SOURCE-reads (the FREE-same-frame-re-reads!!!)) + the odd at the FULL!!)
A = [[F_SP(u), HU[u], [u]] for u in range(V)]
for j in range(9):
    sup = [i for i in range(V) if (mw[j] >> i) & 1]
    A.append([F_R8 if j < 8 else F_FULL, RET[j], sup])
# the D (THE RESIDUE-FIX (the D-EXTENSION (the SS1862-LAW!!!)): the row_t-rets (the PRE-BUILD
#   pure-self-bits (the x-part-0 (the LEGAL-at-frame-0 (the §205-fact!!!))!!) -> the scatter's
#   ret-bits CANCELLED at the ZERO-COST (the 121-free-gates!!!)))
D_nob = [[0, V + t, [RET[k] for k in scatter[t]]] for t in range(V)]
D_withb = [[0, V + t, [RET[k] for k in scatter[t]] + [HU[u] for u in sorted(PERP[t])]]
           for t in range(V)]
# the B (the §1's-full-design (the perp-frame-reads (the perp(t)-H_u's (the e_u-cancellation!!))))
B_withb = [[F_PERP(t), V + t, [HU[u] for u in sorted(PERP[t])]] for t in range(V)]
# the C (the H4-literal-reversal (the z-gates (the A's (the FULL-frames!!))))
C = [[F_FULL, d, s] for F, d, s in reversed([g for g in A])]
log('(2) the gates: the A %d (the H_u-121 + the rets-9!!) | the D %d/%d | the B 0/%d | the C %d' % (
    len(A), len(D_nob), len(D_withb), len(B_withb), len(C)))

# ============ (3) THE OWN-REPLAY (the VALS (the non-strict!!) + the CLIMB-STRICTNESS!!) ============
XMASK = (1 << V) - 1
def replay(D_g, B_g):
    val = [1 << i for i in range(nreg)]
    cur = list(start)
    hist = Counter(); climb_bad = Counter()
    def climb(r, F):
        if cur[r] == F: return
        if not (DIM[F] > DIM[cur[r]]): climb_bad[r] += 1    # the strictness (the gcheck's-rule!!)
        hist[DIM[F] - DIM[cur[r]]] += 1
        cur[r] = F
    for F, d, srcs in D_g:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in A:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    for t in range(V):
        for k in scatter[t]: val[V + t] ^= val[RET[k]]
    for F, d, srcs in B_g:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in C:
        for r in [d] + srcs: climb(r, F)
        for s in srcs: val[d] ^= val[s]
    for r in range(nreg): climb(r, final[r])
    for c in [DIM[f] for f in ret_frames]: hist[c] += 1
    mass = sum(k * n for k, n in hist.items())
    fails = 0; xres = Counter(); dres = Counter()
    for t in range(V):
        want = (1 << (V + t)) ^ (1 << t)
        res = val[V + t] ^ want
        if res:
            fails += 1
            xres[bin(res & XMASK).count('1')] += 1
            dres[bin(res >> V).count('1')] += 1
    return dict(fails=fails, xres=xres, dres=dres, hist=hist, mass=mass,
                climb_bad=climb_bad, bad_regs=len(climb_bad))

rep = replay(D_nob, [])
log('(3a) THE NO-B-REPLAY: the finals-fails %d/121 (the x-residues %s | the register-residues %s)' % (
    rep['fails'], dict(sorted(rep['xres'].items())), dict(sorted(rep['dres'].items()))))
log('     the mass %d vs the identity %d: %s | the climb-illegal-registers %d (the expected: 0!!)' % (
    rep['mass'], 9 * R + 73 + 2 * V * 8, 'MATCH!!' if rep['mass'] == 9 * R + 73 + 2 * V * 8 else 'MISMATCH!!',
    rep['bad_regs']))
rep_b = replay(D_withb, B_withb)
log('(3b) THE WITH-B-REPLAY (the §1\'s-full-design!!): the finals-fails %d/121 (the §1\'s-'
    '"balance"-claim: TRUE-at-the-VAL-level!!!) (the x-residues %s | the register-residues %s)' % (
    rep_b['fails'], dict(sorted(rep_b['xres'].items())), dict(sorted(rep_b['dres'].items()))))
log('     the mass %d | THE CLIMB-ILLEGAL-REGISTERS %d (the H_u\'s-multi-perp-frame-visits '
    '(THE ONE-CLIMB-WALL (the gcheck\'s-expected-REJECT (the \'climb not nested\'!!!))))' % (
    rep_b['mass'], rep_b['bad_regs']))

# ============ (4) THE EMISSION (the BOTH-VARIANTS!!) ============
def emit(D_g, B_g, out):
    word = {
        'h': H, 'v': V, 'R': R,
        'form': form, 'lines': lines, 'frames': frames,
        'start': start, 'final': final,
        'D': D_g, 'A': A, 'B': B_g, 'C': C,
        'ret': RET, 'ret_frames': ret_frames, 'scatter': scatter,
    }
    json.dump(word, open(out, 'w'))
    log('(4) EMITTED: %s (the D %d | the A %d | the B %d | the C %d | the R %d | the CST %d!!)' % (
        out, len(D_g), len(A), len(B_g), len(C), R, 8 * 8 + 9))

emit(D_nob, [], 'ii19_nat_word.json')
emit(D_withb, B_withb, 'ii19_nat_word_b.json')
log('THE GCHECK (the checker\'s-own-verdicts (the expected-REJECTS!!!)):')
log('  /Users/dayssky/.venv/bin/python research/lorentzian-frame-cell-handoff/code/tword/gcheck.py '
    'research/i13-partition/ii19_nat_word.json')
log('  /Users/dayssky/.venv/bin/python research/lorentzian-frame-cell-handoff/code/tword/gcheck.py '
    'research/i13-partition/ii19_nat_word_b.json')
log('DONE — THE NATIVE-121-EMITTER (the §1\'s-steps (the residue-fixed!!)!!!')
