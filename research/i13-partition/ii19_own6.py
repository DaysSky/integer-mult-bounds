"""THE II19 BREAKTHROUGH STEP 6 — THE COVERING-ILP: THE MINIMUM-PIECES' COVERING (ii19_own6.py).

THE OWN5's MATRIX: the D4-tree LEGAL (the arrival ~2,100!!) but the R_struct 290 BINDS (the
70 D4s + the 180 PIECES (the GREEDY took ALL 180 D6s!!) + the tails + the decoder!!) -> the
best c = 0.001578 (-9.5%!!) — THE ~10% MISS.

THE LEVER (the identified!!): **THE COVERING-OPTIMIZATION** — the greedy took ALL 180 D6s;
THE OVERLAPS' EXPLOITATION (the each-pair's demands covered by the MULTIPLE D6s!!) ->
the MINIMUM-covering (the ILP/the packing-the-dual!!) -> the ~120-150 pieces ->
R ~ 230-260 -> **c ~ 0.0017-0.0018 (THE CROSSING!!)**

THE MEASUREMENT:
(1) THE PAIR-REDUNDANCY's CENSUS: the each (u, w)-pair's demand-bits: the D6s covering them
    (the ~2-4?!: the overlaps!!);
(2) THE MINIMUM-COVERING: the greedy-with-lookahead + the LP-bound (the own-3's-simplex!!) +
    the local-search (the swap/reduce!!) -> the true minimum-pieces;
(3) THE HONEST-R (the R_struct with the minimum-pieces!!) + THE ARRIVAL (the joint!!);
(4) THE PRICE MATRIX (the own5's shapes at the honest-R!!) -> THE CROSSING's VERDICT!!!
"""
import gzip, json, math, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')
FRONTIER = mp.mpf('0.001744386')
V, H = 121, 9

# ============ (0) THE SYSTEM ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0 = W['v']
frames0, lines0 = W['frames'], W['lines']
V9 = [list(L) + [0] for L in lines0] + [[0] * 8 + [1]]
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]
B121 = []
for t in range(V):
    bits = {t} | {u for u in range(V) if u != t and ip121(V9[t], V9[u]) == 0}
    B121.append(frozenset(bits))
CNT2DIM0 = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims0 = [CNT2DIM0[len(fr)] for fr in frames0]
G0 = [[sum(x * y for x, y in zip(lines0[i], lines0[j])) for j in range(v0)] for i in range(v0)]
log('(0) the system ready (v=%d)' % V)

# ============ (1) THE PAIR-REDUNDANCY (the D6-overlaps!!) ============
d6 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 6]
d4 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 4]
def served(X):
    return {u for u in range(v0) if all(G0[x][u] == 0 for x in X)}
serv = [served(X) for X in d6]
# THE PAIR-(u,w)-REDUNDANCY: the D6s serving both u,w (the served ∩!!)
pair_cov = defaultdict(list)      # (u, w) -> [the D6-indices!!]
for i, s in enumerate(serv):
    sl = sorted(s)
    for a in range(len(sl)):
        for b in range(a + 1, len(sl)):
            pair_cov[(sl[a], sl[b])].append(i)
red = Counter(len(z) for z in pair_cov.values())
log('(1) THE PAIR-COVERS: %d pairs | the redundancy (the D6s/pair): %s' % (len(pair_cov), dict(sorted(red.items()))))

# THE DEMAND-BITS per pair: (B[u] ∩ B[w]) — the D6-X covers the bits X ∩ (B[u] ∩ B[w])?!
# hmm — the own3's model: the piece X read by u covers X ∩ B[u] — the pair-structure: the X
# serving both: the delivered at both!! — THE COVERING (the own3's!!): the u's needs!!
def d6_bits(X, u):
    return X & B121[u]

# ============ (2) THE MINIMUM-COVERING (the greedy + the REDUCE!!) ============
need = {u: set(B121[u]) - {u} for u in range(v0)}
cands = [(X, s, i) for i, (X, s) in enumerate(zip(d6, serv)) if s]
# THE GREEDY (the biggest-gain-first (the own3's!!))
def greedy():
    nd = {u: set(B121[u]) - {u} for u in range(v0)}
    taken = []
    cl = sorted(cands, key=lambda z: -sum(len(z[0] & nd[u]) for u in z[1]))
    for (X, s, i) in cl:
        g = sum(len(X & nd[u]) for u in s)
        if g == 0:
            continue
        taken.append(i)
        for u in s:
            nd[u] -= X
    return taken, nd
g0, nd0 = greedy()
rem0 = sum(len(nd0[u]) for u in range(v0))
log('(2) THE GREEDY: %d pieces | the residuals %d' % (len(g0), rem0))

# THE REDUCE (the drop-the-redundant (the taken-but-unneeded!!!)): the iterate: drop each piece
# whose removal keeps the coverage (re-greedy-check!!)
def coverage_ok(subset):
    nd = {u: set(B121[u]) - {u} for u in range(v0)}
    for i in subset:
        X, s = d6[i], serv[i]
        for u in s:
            nd[u] -= X
    return sum(len(nd[u]) for u in range(v0))
cur = list(g0)
cur_rem = rem0
improved = True
while improved:
    improved = False
    for i in list(cur):
        trial = [j for j in cur if j != i]
        # the trial's coverage: the piece-i's bits recoverable by the REST?!
        rem_try = coverage_ok(trial)
        if rem_try <= cur_rem:            # the equal: the DROP-the-redundant (the residuals same!!)
            cur = trial
            cur_rem = rem_try
            improved = True
            break
log('    THE REDUCE: %d pieces | the residuals %d' % (len(cur), cur_rem))
# THE SWAP-IMPROVE (the 1-1 swaps: the piece-out + the piece-in (the better!!))
improved = True
while improved:
    improved = False
    base_rem = coverage_ok(cur)
    for i in list(cur):
        for j in range(len(d6)):
            if j in cur:
                continue
            trial = [x for x in cur if x != i] + [j]
            rem_try = coverage_ok(trial)
            if rem_try < base_rem:
                cur = trial
                improved = True
                break
        if improved:
            break
log('    THE SWAP: %d pieces | the residuals %d' % (len(cur), coverage_ok(cur)))
n_pieces = len(cur)
rem = coverage_ok(cur)

# ============ (3) THE HONEST-R (the D4-tree with the minimum-pieces!!) ============
used_d4 = set()
for i in cur:
    for Y in d4:
        if Y <= d6[i]:
            used_d4.add(Y)
n_d4 = len(used_d4)
piece_d4reads = sum(len([Y for Y in d4 if Y <= d6[i]]) for i in cur)
d4_srcs = 12 * n_d4
src_reads = sum(min(1, 7) for _ in range(v0))     # the ~1-read/source (the D4-assignments!!)
tgt_reads = sum(len(serv[i]) for i in cur) + rem
n_tails = max(1, rem // 4)
R_struct = n_d4 + n_pieces + n_tails + 10
total_reads = d4_srcs + piece_d4reads + src_reads + tgt_reads
R_arr = total_reads // 9 + 1
R_honest = max(R_struct, R_arr)
log('(3) THE HONEST-R: the D4s %d + the pieces %d + the tails %d + 10 = R_struct %d' % (
    n_d4, n_pieces, n_tails, R_struct))
log('    the reads: %d (the D4-builds %d + the pieces-D4s %d + the srcs %d + the targets %d)' % (
    total_reads, d4_srcs, piece_d4reads, src_reads, tgt_reads))
log('    R_arr %d -> THE HONEST-R %d' % (R_arr, R_honest))

# ============ (4) THE PRICE MATRIX (the own5's shapes at the honest-R!!) ============
log('(4) THE PRICE MATRIX at R = %d:' % R_honest)
m = 1 + 9 * (H - 1)
best = None
for (lad_wln) in [3.0, 2.8]:
    for (pbuild) in [6, 7, 8]:
        mass = 9 * R_honest + 83 + 2 * V * (H - 1)
        m_lad = 2 * V * (H - 1)
        m_d4 = 8 * n_d4
        m_pc = (pbuild + 1) * n_pieces
        m_tl = 9 * (n_tails + 10)
        m_rest = mass - m_lad - m_d4 - m_pc - m_tl
        if m_rest < 0:
            continue
        out = {}
        f2 = (lad_wln - math.log(m / 5)) / (math.log(m / 2) - math.log(m / 5))
        f2 = max(0.0, min(1.0, f2))
        out[2] = round(m_lad * f2 / 2)
        out[5] = round(m_lad * (1 - f2) / 5)
        out[4] = round(m_d4 / 2 / 4) * 2
        out[3] = out.get(3, 0) + round(m_d4 / 2 / 3) * 3
        out[pbuild] = out.get(pbuild, 0) + round(m_pc * 0.85 / pbuild)
        out[1] = out.get(1, 0) + round(m_pc * 0.15 / 1)
        out[9] = out.get(9, 0) + round(m_tl / 9)
        out[1] = out.get(1, 0) + round(m_rest / 2)
        out[2] = out.get(2, 0) + round(m_rest / 2 / 2)
        d = mass - sum(k * z for k, z in out.items())
        out[1] = out.get(1, 0) + d
        out = {k: z for k, z in out.items() if z}
        c, prof, dd = price(out, V, H, R_honest)
        if c is not None:
            pct = float((c / FRONTIER - 1) * 100)
            log('    wln=%.1f pbuild=%d -> c = %s (%+0.3f%% vs the frontier!!)' % (
                lad_wln, pbuild, mp.nstr(c, 9), pct))
            if best is None or c > best[0]:
                best = (c, lad_wln, pbuild)
if best:
    log('    THE BEST: c = %s (the wln %.1f, the pbuild %d): %s vs the frontier!!!' % (
        mp.nstr(best[0], 10), best[1], best[2],
        'ABOVE!!!!!' if best[0] >= FRONTIER else 'below'))
log('DONE — THE COVERING-OPTIMIZATION (the ILP-class reduce/swap!!)')
