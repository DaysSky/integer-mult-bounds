"""THE R420-EXTENSION v3 — THE SHARED-CARRIER WORD (ii19_ext6.py).

THE SS1985 WORD (ii19_ext4.py, committed fe6301f9!): the 121-line, the gcheck-PASSING
(the R 541!) — closed at the hosting wall (the cap 4,356 vs the nres 4,869: the 111.8%!).
THE SS2012 CENSUS: THE D4-FRAME SHARING — the 42 shared carriers (each at the {120} U a
D4-subsystem frame!) cover ALL 120 targets (2-6 each!): THE R = 463 <= the wall 484 (the
95.7%!) — THE PRICEABLE WORD!!!

THE DESIGN (the ext4's + the shared carriers!):
- THE TARGETS' CHAINS: 0 -> cell(2) -> F_j(5) -> perp(8): the SAME total mass (the 8!),
  the F_j-visit INSERTED BETWEEN the cell-gate and the perp-gate (the ORDER-AWARE: the
  ext4's at-the-end append would be the dim-8 -> dim-5 DECREASING = ILLEGAL!!)
- THE CARRIERS (the 42!): the A-builds at the {120}-singleton (the val = own ^ {120}!)
  -> the ONE climb to F_j (at the first read!) -> the FREE re-reads (the cur == F_j!!)
  -> the final climb (the F_j -> the FULL: the +4!)
- THE D-GATES: the +ODD (all!) + the special's gate + the per-target +CARR[j_t]!
- THE SCATTER + THE RET_FRAMES: the same as the ext4 (the fix-7's CST 83!)
"""
import gzip, json, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE LOAD + THE 121-LINE SYSTEM ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0, h0, R0 = W['v'], W['h'], W['R']            # 120, 8, 420
frames0, lines0 = W['frames'], W['lines']

V9 = [list(L) + [0] for L in lines0] + [[0] * 8 + [1]]
V, H, SP = 121, 9, 120
R = 463                                        # the 420 + the odd + the 42 SHARED carriers!
nreg = 2 * V + R                               # 705!
log('(0) the system: v0=%d h0=%d R0=%d -> V=%d H=%d R=%d nreg=%d' % (v0, h0, R0, V, H, R, nreg))

# ============ (C1) THE CENSUS CORE (the SS2012 groups, recomputed!) ============
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

# ============ (1) THE FRAMES (+ the m shared F_j's!!) ============
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

# ============ (2) THE REGISTERS' MAP ============
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

# ============ (4) THE GATES + THE ORDER-AWARE CARRIER-INSERTION!! ============
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

# ============ (5) THE SCATTER (the same as the ext4!) ============
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
log('(5) the scatter: the 121 rows')

# ============ (6) THE C-PHASE (the H4 literal reverse!) ============
zg = [[F, d, s] for F, d, s in A + B if not (V <= d < 2 * V)]
C = [[IDX_FULL, d, s] for F, d, s in reversed(zg)]
log('(6) the C: %d gates (the H4 reverse of the %d z-gates!)' % (len(C), len(zg)))

# ============ (7) MY OWN REPLAY ============
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

for F, d, srcs in D:                           # THE D-PHASE!
    acc = 0
    for s in srcs:
        acc ^= val[s]
    tgt_dirt[d - V] = acc
    for r in [d] + srcs:
        climb(r, F)
    for s in srcs:
        val[d] ^= val[s]

run(A)                                         # THE A-PHASE!

for t in range(V):                             # THE SCATTER!
    acc = 0
    for k in scatter[t]:
        acc ^= val[ret_list[k]]
    tgt_scatter[t] = acc
    val[V + t] ^= acc

for F, d, srcs in B:                           # THE B-PHASE!
    for r in [d] + srcs:
        climb(r, F)
    if V <= d < 2 * V:
        acc = 0
        for s in srcs:
            acc ^= val[s]
        tgt_reads[d - V] ^= acc
    for s in srcs:
        val[d] ^= val[s]

run(C)                                         # THE C-PHASE!

for r in range(nreg):                          # THE FINAL CLIMBS!
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
    xres = Counter()
    dres = Counter()
    for t in range(V):
        res = (tgt_dirt[t] ^ tgt_scatter[t] ^ tgt_reads[t]) ^ (1 << t)
        rx = res & ((1 << V) - 1)
        rd = res >> V
        if rx:
            xres[bin(rx).count('1')] += 1
        if rd:
            dres[bin(rd).count('1')] += 1
    log('    THE DIAGNOSIS: the x-residues %s | the dirt-residues %s' % (
        dict(sorted(xres.items())), dict(sorted(dres.items()))))

# ============ (9) THE HIST + THE MASS ============
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
OUT = 'research/i13-partition/ii19_ext_word2.json'
with open(OUT, 'w') as f:
    json.dump(word, f)
log('(10) THE WORD EMITTED: %s (%d registers, %d frames, %d D / %d A / %d B / %d C gates!)' % (
    OUT, nreg, len(frames), len(D), len(A), len(B), len(C)))
log('    THE GCHECK NEXT: research/lorentzian-frame-cell-handoff/code/tword/gcheck.py %s --price' % OUT)
log('DONE — THE SHARED-CARRIER WORD')
