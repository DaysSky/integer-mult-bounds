"""THE R420-EXTENSION BUILD — STAGE 2b-ii: THE CONSTRUCTION + THE REPLAY + THE DIAGNOSIS (ii19_ext4.py).

THE STAGE 2b-i (SS1949!!): the replay machinery VALIDATED (the hist EXACTLY the published,
the final-value fails 0, the arithmetic [dirt ^ scatter ^ reads] = x_t for 120/120!).

THE STAGE 2b-ii (this script!): THE CONSTRUCTED WORD + MY OWN REPLAY + THE DIAGNOSIS:
  (1) THE FRAMES: the re-based line-sets (the Stage-1's!) -> the vector lists (the redundant
      bases: the gcheck RREFs them itself!) + THE 2 NEW: the {120}-singleton + the
      120-roots frame (the E8-span: the rets' re-target + the special's target's final!)
  (2) THE REGISTERS: v=121, R=421 (the 420 + the odd!): the sources 0-120, the targets
      121-241, the helpers 242-662 (the remap: the sources +0, the targets +1, the helpers +2!)
  (3) THE GATES: the re-mapped R420's + THE RETS' RE-TARGETING (the rets' F=1 gates ->
      the 120-roots frame: the copy ranks 8 -> the CST 81!) + THE ODD'S BUILD (at the FULL!)
  (4) THE SCATTER: the 121 rows: the roots' = the R420's + the ODD (the index 9!); the
      special's = [9]!
  (5) MY OWN REPLAY (the SS1949 machinery!) -> THE FINALS' CHECK + THE DIAGNOSIS (the
      per-target residues: [dirt ^ scatter ^ reads] ^ x_t — the cancellation needs!)

THE DESIGN CORRECTION (the SS1950 over-generalization fixed!): the ROOTS' targets' chains
  ⊆ their 64-perp-frames (the spans INCLUDE the special!) — the {120}-frame SUBSET-EQ every
  root's perp-span: THE ROOTS CAN READ THE SPECIAL'S CARRIER (the SS1934 design was right!);
  only the SPECIAL'S target is confined to the 120-roots-span (the E8-internal reads only!).
"""
import gzip, json, time
from collections import Counter
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE LOAD + THE 121-LINE SYSTEM ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0, h0, R0 = W['v'], W['h'], W['R']            # 120, 8, 420
frames0, lines0 = W['frames'], W['lines']

V9 = [list(L) + [0] for L in lines0] + [[0] * 8 + [1]]
V, H, SP = 121, 9, 120
R = 541                                        # the 420 + the odd + the 120 carriers!
nreg = 2 * V + R                               # 783!
log('(0) the system: v0=%d h0=%d R0=%d -> V=%d H=%d R=%d nreg=%d' % (v0, h0, R0, V, H, R, nreg))

# ============ (1) THE FRAMES ============
rb_sets = []
for f in frames0:
    fl = list(f)
    if len(fl) == 120 or len(fl) == 63:        # the FULL + the perps: +special!
        fl = fl + [SP]
    rb_sets.append(fl)
IDX_SPS = len(rb_sets); rb_sets.append([SP])               # the {120}-singleton!
IDX_R8 = len(rb_sets); rb_sets.append(list(range(120)))     # the 120-roots (the E8-span!)!
IDX_FULL = 1                                               # the frame-1: the FULL (121-line!)!
frames = [[V9[i] for i in s] for s in rb_sets]
LCDIM = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 64: 8, 121: 9, 120: 8}
dims = [LCDIM[len(s)] for s in rb_sets]
log('(1) the frames: %d (+2 new!) | the dims %s' % (
    len(frames), dict(sorted(Counter(dims).items()))))

# ============ (2) THE REGISTERS' MAP ============
def remap(r):
    if r < v0:
        return r                              # the sources: SAME!
    if r < 2 * v0:
        return r + 1                          # the targets: +1!
    return r + 2                               # the helpers: +2!

ODD = 2 * V + 421 - 1                          # the 662: the odd-gather (the fixed index!)
CARR = [2 * V + 421 + t for t in range(v0)]    # the 663..782: the 120 special-carriers!
log('(2) the remap: the sources +0, the targets +1, the helpers +2; ODD=%d; the carriers %d..%d' % (
    ODD, CARR[0], CARR[-1]))

# ============ (3) THE START / FINAL ============
start = [0] * nreg
for s in range(v0):
    start[s] = 2 + s                           # the singletons: the frames[2..121]!
start[SP] = IDX_SPS
final = [IDX_FULL] * nreg
for t in range(v0):
    final[V + t] = W['final'][v0 + t]           # the t-perp frames (the re-based 64-line!)!
final[V + SP] = IDX_R8                          # the special's: the 120-roots!
log('(3) the start/final: the special start %d; the special final %d' % (IDX_SPS, IDX_R8))

# ============ (4) THE GATES' RE-MAP + THE RETS' RE-TARGETING ============
def remap_gate(g):
    F, d, srcs = g
    return [F, remap(d), [remap(s) for s in srcs]]

D = [remap_gate(g) for g in W['D']]
A = [remap_gate(g) for g in W['A']]
B = [remap_gate(g) for g in W['B']]
RET_IDX = [remap(q) for q in W['ret']]
ret_set = set(RET_IDX)
n_retarget = 0
for g in A:
    if g[1] in ret_set and g[0] == 1:           # the rets' FULL-dest gates -> the 120-roots!
        g[0] = IDX_R8
        n_retarget += 1
log('(4) the gates: D %d | A %d (the %d ret-gates re-targeted -> the 120-roots!) | B %d' % (
    len(D), len(A), n_retarget, len(B)))

# THE FIX-5b (the A part!): THE +120 CARRIERS FIRST (the SP at the {120}-frame: the FREE
# re-reads!): the x_120-delivery to the roots' reads (the {120}-span NOT-SUBSET the E8-span:
# the per-target carriers are the ONLY legal channel!)
for t in range(v0):
    A.append([IDX_SPS, CARR[t], [SP]])           # the carrier's build: the val = own-dirt ^ {120}!
# THEN THE ODD'S A-BUILD (the SP: the {120} -> the FULL: the +8 — AFTER the carriers!)
# (the SS1964 diagnosis: the odd's x-part must be the v_0 ^ e_120 — the ROW-0's rets!)
odd_srcs = [RET_IDX[k] for k in W['scatter'][0]] + [SP]
A.append([IDX_FULL, ODD, odd_srcs])
log('    the A-builds: %d carriers (at the {120}-frame!) THEN the odd (at the FULL!)' % v0)

# THE FIX-5a: THE D-GATES' +[ODD] + the special's NEW D-gate (the {662}-cancels at the D-time:
# the helpers' INITIAL vals = the OWN DIRT (the single bits!) — the A-phase has not run yet!)
for g in D:
    g[2].append(ODD)                      # the roots' D-srcs: +the ODD (the {662}-cancel!)
D.append([0, V + SP, [ODD]])              # the special's D-gate (the {662}-cancel!)!
# THE FIX-5b (the B/D parts!): the carriers' reads at the targets' perps + the own-cancels!
for t in range(v0):
    B.append([final[V + t], V + t, [CARR[t]]])   # the x_120-read at the target's perp!
    D[t][2].append(CARR[t])                      # the carrier's own-bit-cancel at the D-time!
log('    the fix-5a/5b: the +ODD to %d D-gates + the special D-gate; the %d carriers (B+D gates!)' % (
    v0 + 1, v0))

# ============ (5) THE SCATTER ============
ret_list = RET_IDX + [ODD]
# THE FIX-7 (the SS1981 reject!): the odd's build climbs the ROW-0's rets (its srcs!) to the
# FULL -> their ret_frames = THE FULL (the truth!): the copy ranks {9, 9} + 7x8 + 9 = 83!
row0_rets = set(W['scatter'][0])                     # the ret-list indices read by the odd's build!
ret_frames = [(IDX_FULL if (k in row0_rets or k == 9) else IDX_R8) for k in range(10)]
scatter = []
row0 = list(W['scatter'][0])
for t in range(V):
    if t < v0:
        sel = list(W['scatter'][t]) + row0 + [9]         # + the ROW-0: the v_0-cancel (B[t] = v_t ^ e_120!)
        cnt = Counter(sel)
        scatter.append(sorted(k for k in cnt if cnt[k] % 2))
    else:
        sel = [9] + row0                                 # the special's: [the odd] + the ROW-0 (the v_0-cancel!)!
        cnt = Counter(sel)
        scatter.append(sorted(k for k in cnt if cnt[k] % 2))
log('(5) the scatter: the 121 rows | the ret-list %d (the 9 + the ODD!) | the ret_frames %s' % (
    len(ret_list), ['R8' if f == IDX_R8 else 'FULL' for f in ret_frames]))

# ============ (6) THE C-PHASE (the H4 literal reverse!) ============
zg = [[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)]
C = [[IDX_FULL, d, s] for F, d, s in reversed(zg)]
log('(6) the C: %d gates (the H4 reverse of the %d z-gates!)' % (len(C), len(zg)))

# ============ (7) MY OWN REPLAY (the SS1949 machinery!) ============
val = [1 << i for i in range(nreg)]
cur = list(start)
hist = Counter()
moves = 0

def climb(r, F):
    global moves
    if cur[r] == F:
        return
    hist[dims[F] - dims[cur[r]]] += 1
    moves += 1
    cur[r] = F

def run(gates):
    for F, d, srcs in gates:
        for r in [d] + srcs:
            climb(r, F)
        for s in srcs:
            val[d] ^= val[s]

tgt_dirt = [0] * V
tgt_scatter = [0] * V
tgt_reads = [0] * V

# THE D-PHASE!
for F, d, srcs in D:
    acc = 0
    for s in srcs:
        acc ^= val[s]
    tgt_dirt[d - V] = acc
    for r in [d] + srcs:
        climb(r, F)
    for s in srcs:
        val[d] ^= val[s]

# THE A-PHASE!
run(A)

# THE SCATTER!
for t in range(V):
    acc = 0
    for k in scatter[t]:
        acc ^= val[ret_list[k]]
    tgt_scatter[t] = acc
    val[V + t] ^= acc

# THE B-PHASE!
for F, d, srcs in B:
    for r in [d] + srcs:
        climb(r, F)
    if V <= d < 2 * V:
        acc = 0
        for s in srcs:
            acc ^= val[s]
        tgt_reads[d - V] ^= acc
    for s in srcs:
        val[d] ^= val[s]

# THE C-PHASE!
run(C)

# THE FINAL CLIMBS!
for r in range(nreg):
    climb(r, final[r])

# ============ (8) THE FINALS' CHECK + THE DIAGNOSIS ============
bad = []
for r in range(nreg):
    want = (1 << r) ^ ((1 << (r - V)) if V <= r < 2 * V else 0)
    if val[r] != want:
        bad.append(r)
log('(8) THE FINALS: the fails %d (the sources %d, the targets %d, the helpers %d)' % (
    len(bad), sum(1 for r in bad if r < V), sum(1 for r in bad if V <= r < 2 * V),
    sum(1 for r in bad if r >= 2 * V)))
if bad:
    log('    the bad registers (the first 12): %s' % bad[:12])

# THE DIAGNOSIS: the per-target residues [dirt ^ scatter ^ reads] ^ x_t!
xbad = 0
dbad = 0
xres = Counter()
dres = Counter()
for t in range(V):
    res = (tgt_dirt[t] ^ tgt_scatter[t] ^ tgt_reads[t]) ^ (1 << t)
    rx = res & ((1 << V) - 1)                 # the x-bits (the lines 0-120!)!
    rd = res >> V                              # the dirt-bits (the registers beyond v!)!
    if rx:
        xbad += 1
        xres[bin(rx).count('1')] += 1
    if rd:
        dbad += 1
        dres[bin(rd).count('1')] += 1
log('    THE DIAGNOSIS: the x-residue targets %d/%d (the sizes %s)' % (
    xbad, V, dict(sorted(xres.items()))))
log('    the dirt-residue targets %d/%d (the sizes %s)' % (
    dbad, V, dict(sorted(dres.items()))))
# the special's residue (the target 120!):
resS = (tgt_dirt[SP] ^ tgt_scatter[SP] ^ tgt_reads[SP]) ^ (1 << SP)
log('    THE SPECIAL: the residue x-bits %d, dirt-bits %d (the target 120)' % (
    bin(resS & ((1 << V) - 1)).count('1'), bin(resS >> V).count('1')))

# THE HIST + THE MASS!
for c in [dims[f] for f in ret_frames]:
    hist[c] += 1
mass = sum(k * n for k, n in hist.items())
cst = sum(dims[f] for f in ret_frames)
ident = H * R + cst + 2 * V * (H - 1)
log('(9) THE HIST: %s | THE CST %d | the mass %d vs the identity %d: %s' % (
    dict(sorted(hist.items())), cst, mass, ident, 'MATCH!!' if mass == ident else 'MISMATCH!!'))

# ============ (10) THE EMISSION (the gcheck-format word!!) ============
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
OUT = 'research/i13-partition/ii19_ext_word.json'
with open(OUT, 'w') as f:
    json.dump(word, f)
log('(10) THE WORD EMITTED: %s (%d registers, %d frames, %d D / %d A / %d B / %d C gates!)' % (
    OUT, nreg, len(frames), len(D), len(A), len(B), len(C)))
log('    THE GCHECK NEXT: research/lorentzian-frame-cell-handoff/code/tword/gcheck.py %s --price' % OUT)
log('DONE — STAGE 2b-ii-alpha')
