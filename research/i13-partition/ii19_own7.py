"""THE II19 BREAKTHROUGH STEP 7 — THE 2-D6-UNIONS' CENSUS (ii19_own7.py).

THE OWN6's DECISIVE FINDING: THE PAIR-REDUNDANCY = 1!!! — the 180 D6s = THE PERFECT PARTITION
(each (u,w)-pair served by exactly ONE D6!!) — the REDUCE/SWAP: ZERO improvement — THE 180 =
THE D6-CLASS's MINIMUM — the D6-tree's floor: R=290, c <= 0.00158 (-9.5%!!) — THE ~10% MISS
IS STRUCTURAL (the D6-class!!).

THE REMAINING LEVER: **THE 2-D6-UNIONS** (the ~90 pieces!!): the pairs-of-D6s merged into the
ONE register (the ~60-line content: the dim-7-union-frame!!!): the R_struct ~200!!! — the
arrival at the D4-LEVEL (the ~12-D4-srcs/union!!): the R_arr ~257 ✓✓ (NOT the cells-level
(the own4's trap (the 4,050-cell-reads ✗!!!)!!) — THE COVERAGE QUESTION (THE OPEN!!): the
union's delivered-bits at its users (the 2-D6s'-∪ ∩ the users'-Bs!!) vs the D6s'-(98.5%!!).

THE MEASUREMENT:
(1) THE UNION-CANDIDATES: the D6-pairs (the WHICH?!: the shared-users' pairs!!) + the served!!
(2) THE COVERING: the greedy + the reduce/swap (the own6's!!) -> the minimum-unions!!
(3) THE HONEST-R + THE ARRIVAL (the D4-level!!) + THE PRICE MATRIX -> THE CROSSING's VERDICT!!!
"""
import gzip, json, math, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
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
d6 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 6]
d4 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 4]
def served(X):
    return {u for u in range(v0) if all(G0[x][u] == 0 for x in X)}
log('(0) the system ready')

# ============ (1) THE UNION-CANDIDATES (the D6-pairs!!) ============
serv6 = [served(X) for X in d6]
# THE D6-PAIRS: the WHICH?! — the natural: the D6-pairs sharing the D4s (the tree-legality!!)
# AND/OR the shared-served!! — THE CENSUS: the D6-pairs (the 180-choose-2 = 16,110!!) with
# the served(union) — hmm: the union-frame: the 2-D6s'-∪ (the ~60-line!!): the frame-legality:
# the span (the ~dim-7-8!!) — THE CENSUS: the pairs with the |served(∪)| >= 1!!!
log('(1) THE UNION-CENSUS: the D6-pairs (the shared-D4-adjacency first!!)')
# the D6-D4 memberships!!
d4in = defaultdict(set)     # the D6-index -> the D4-indices!!
for i, X in enumerate(d6):
    for j, Y in enumerate(d4):
        if Y <= X:
            d4in[i].add(j)
# the adjacency: the D6-pairs sharing >= 1 D4!!
adj = defaultdict(list)
for i in range(len(d6)):
    for j in range(i + 1, len(d6)):
        if d4in[i] & d4in[j]:
            adj[i].append(j)
            adj[j].append(i)
log('    the D6-adjacency (the shared-D4!!): %s' % dict(sorted(Counter(len(z) for z in adj.values()).items())))

# the union-candidates: the adjacent pairs!! — the served: the UNION's!!
ucands = []
for i in range(len(d6)):
    for j in adj[i]:
        if i < j:
            U = d6[i] | d6[j]
            s = served(U)
            if s:
                ucands.append((U, s, (i, j)))
usz = Counter(len(s) for (U, s, p) in ucands)
log('    the union-candidates: %d | the served-sizes %s' % (len(ucands), dict(sorted(usz.items()))))

# ============ (2) THE COVERING (the greedy + the reduce!!) ============
def cover_with(cands):
    nd = {u: set(B121[u]) - {u} for u in range(v0)}
    cl = sorted(cands, key=lambda z: -sum(len(z[0] & nd[u]) for u in z[1]))
    taken = []
    for (X, s, i) in cl:
        g = sum(len(X & nd[u]) for u in s)
        if g == 0:
            continue
        taken.append((X, s, i))
        for u in s:
            nd[u] -= X
    rem = sum(len(nd[u]) for u in range(v0))
    return taken, rem
def rem_of(taken):
    nd = {u: set(B121[u]) - {u} for u in range(v0)}
    for (X, s, i) in taken:
        for u in s:
            nd[u] -= X
    return sum(len(nd[u]) for u in range(v0))

# (a) THE PURE-UNIONS (the D6s-FREE!!)
tu, remu = cover_with(ucands)
log('(2a) THE PURE-UNION-COVERING: %d unions | the residuals %d' % (len(tu), remu))
# (b) THE MIXED (the unions + the single-D6s (the fillers!!))
mix = ucands + [(d6[i], serv6[i], i) for i in range(len(d6)) if serv6[i]]
tm, remm = cover_with(mix)
log('(2b) THE MIXED-COVERING: %d pieces | the residuals %d' % (len(tm), remm))
nun = sum(1 for (X, s, i) in tm if isinstance(i, tuple))
log('    the composition: %d unions + %d single-D6s' % (nun, len(tm) - nun))

# THE REDUCE (the drop-the-redundant!!)
cur = list(tm)
cur_rem = remm
improved = True
while improved:
    improved = False
    for k in range(len(cur)):
        trial = cur[:k] + cur[k + 1:]
        rt = rem_of(trial)
        if rt <= cur_rem:
            cur = trial
            cur_rem = rt
            improved = True
            break
log('    THE REDUCE: %d pieces | the residuals %d' % (len(cur), cur_rem))
nun2 = sum(1 for (X, s, i) in cur if isinstance(i, tuple))
log('    the composition: %d unions + %d single-D6s' % (nun2, len(cur) - nun2))

# ============ (3) THE HONEST-R + THE ARRIVAL (the D4-level!!) ============
used_d4 = set()
piece_d4reads = 0
for (X, s, i) in cur:
    for Y in d4:
        if Y <= X:
            used_d4.add(Y)
            piece_d4reads += 1
n_d4 = len(used_d4)
d4_srcs = 12 * n_d4
src_reads = v0                       # the ~1-read/source!!
tgt_reads = sum(len(s) for (X, s, i) in cur) + cur_rem
n_tails = max(1, cur_rem // 4)
R_struct = n_d4 + len(cur) + n_tails + 10
total_reads = d4_srcs + piece_d4reads + src_reads + tgt_reads
R_arr = total_reads // 9 + 1
R_honest = max(R_struct, R_arr)
log('(3) THE HONEST-R: the D4s %d + the pieces %d + the tails %d + 10 = %d' % (
    n_d4, len(cur), n_tails, R_struct))
log('    the reads: %d (the builds %d + the pieces-D4s %d + the srcs %d + the targets %d)' % (
    total_reads, d4_srcs, piece_d4reads, src_reads, tgt_reads))
log('    R_arr %d -> THE HONEST-R %d' % (R_arr, R_honest))

# ============ (4) THE PRICE MATRIX ============
log('(4) THE PRICE MATRIX at R = %d:' % R_honest)
m = 1 + 9 * (H - 1)
best = None
for lad_wln in [3.0, 2.8]:
    for pbuild in [7, 8]:
        mass = 9 * R_honest + 81 + 2 * V * (H - 1)     # the CST-81 (the audit's +8%!!)
        m_lad = 2 * V * (H - 1)
        m_d4 = 8 * n_d4
        m_pc = (pbuild + 1) * len(cur)
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
            log('    wln=%.1f pbuild=%d -> c = %s (%+0.3f%%)' % (
                lad_wln, pbuild, mp.nstr(c, 9), float((c / FRONTIER - 1) * 100)))
            if best is None or c > best[0]:
                best = (c, lad_wln, pbuild)
if best:
    log('    THE BEST: c = %s (wln %.1f, pbuild %d): %s!!!' % (
        mp.nstr(best[0], 10), best[1], best[2],
        'ABOVE THE FRONTIER!!!!' if best[0] >= FRONTIER else 'below'))
log('DONE — THE 2-D6-UNIONS (the census!!)')
