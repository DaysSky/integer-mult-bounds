"""THE II19 BREAKTHROUGH STEP 5 — THE D4-TREE's HONEST MEASUREMENT (ii19_own5.py).

THE AUDIT-CHAIN (the own3 -> the own4 -> the fix!!):
- the own3: the D6-pieces (the 2-user!!): the rooms-trivial ✓ BUT the direct-builds
  (the ~30-srcs!!): the arrival 5,400 ✗ (the own3's R=220 was the ARRIVAL-ILLEGAL!!)
- the own4: the CELLS-tree (the 2-line-sums!!): the cell-reads 4,860 -> the arrival-floor
  R ~ 634 -> THE HOSTING WALL (484!!) ✗✗ — the cells-level DELIVERS 2-bits/read: the wrong!!
- **THE FIX: THE D4-TREE!!**: the sources -> THE D4-SUMS (the 70 four-line frames, the
  ~12-src builds (+4-climbs!!)) -> THE UNION-PIECES (the D6-unions: the ~5-D4-srcs!!) ->
  the targets (the ~2-3 reads!!):
    THE ARRIVAL: ~840 + ~900-1,080 + ~480 = ~2,220-2,400 -> R-floor ~ 247-267!!!
    THE R_STRUCT: 70 + ~90-180 + ~30 + 10 = ~200-290!!!
    THE ROOMS: TRIVIAL (the pieces read the D4-sums at the pieces' OWN union-frames: the
    D4-contents ⊆ the union (the nested + the content-frame!!) — NO read-frames!!)
    THE WLN: the pieces' +7/+8-builds (2.1-2.2!!) + the D4s' [4,+3,+1] (3.2) + the ladders
    (the 1,936 @ ~3.0): the ln-mass ~ 3.6M -> c = 7,072/3.6M ~ 0.00196 (+12%!!!)

THE MEASUREMENT (THE GO/NO-GO!!!):
(1) THE D4-SUMS' CENSUS (the 70!!) + the sources'-assignments (the ~12-srcs!!);
(2) THE UNION-PIECES' COVERING (the D6s/unions over the D4-sums!!) + the residuals;
(3) THE HONEST-R + THE ARRIVAL (the joint!!);
(4) THE HONIST-WLN-MIX (the per-class chains!!) + THE c (THE PRICER!!!).
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
log('(0) the system: v=%d h=%d | the B-sizes %s' % (V, H, dict(sorted(Counter(len(b) for b in B121).items()))))

# ============ (1) THE D4-SUMS (the 70!!) + THE SOURCES'-ASSIGNMENTS ============
d4 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 4]
d6 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 6]
log('(1) the D4s: %d | the D6s: %d' % (len(d4), len(d6)))
# the sources'-D4-memberships (the each-source in ~the how-many D4s?!)
s4 = defaultdict(list)
for X in d4:
    for x in X:
        s4[x].append(X)
log('    the sources-D4-memberships: %s (the mean %.2f)' % (
    dict(sorted(Counter(len(z) for z in s4.values()).items())),
    sum(len(z) for z in s4.values()) / max(1, len(s4))))
# the D4 -> the D6-memberships!!
d4of = defaultdict(list)
for X in d6:
    for Y in d4:
        if Y <= X:
            d4of[Y].append(X)
log('    the D4-D6-memberships: %s (the mean %.2f)' % (
    dict(sorted(Counter(len(z) for z in d4of.values()).items())),
    sum(len(z) for z in d4of.values()) / max(1, len(d4of))))

# ============ (2) THE COVERING (the own3's greedy over the D6s!!) ============
def served(X):
    out = set()
    for u in range(v0):
        if all(G0[x][u] == 0 for x in X):
            out.add(u)
    return out
serv = [served(X) for X in d6]
cands = sorted([(X, s) for (X, s) in zip(d6, serv) if s], key=lambda z: -len(z[1]))
need = {u: set(B121[u]) - {u} for u in range(v0)}
pieces = []
for (X, s) in cands:
    gain = sum(len(X & need[u]) for u in s)
    if gain == 0:
        continue
    pieces.append((X, s))
    for u in s:
        need[u] -= X
rem = sum(len(need[u]) for u in range(v0))
log('(2) the D6-covering: %d pieces | the residuals %d' % (len(pieces), rem))

# ============ (3) THE HONEST-R + THE ARRIVAL (the D4-tree's!!) ============
# the D4-sums needed: the union of the pieces' D4-memberships (the D4s ⊆ the pieces' frames!!)
used_d4 = set()
for (X, s) in pieces:
    for Y in d4:
        if Y <= X:
            used_d4.add(Y)
n_d4 = len(used_d4)
# the D4-builds: the ~12-srcs (the D4's 12 lines!!)
d4_srcs = 12 * n_d4
# the pieces'-builds: the pieces'-D4-srcs (the D4s ⊆ X!!)
piece_d4reads = sum(len([Y for Y in d4 if Y <= X]) for (X, s) in pieces)
# the sources'-reads (the sources in the used-D4s: the each-source ~the membership!!)
src_reads = sum(min(len(s4[s]), 2) for s in s4)         # the ~2-reads/source (the conservative!!)
tgt_reads = sum(len(s) for (X, s) in pieces) + rem
n_tails = max(1, rem // 4)
R_struct = n_d4 + len(pieces) + n_tails + 10
total_reads = d4_srcs + piece_d4reads + src_reads + tgt_reads
R_arr = total_reads // 9 + 1
R_honest = max(R_struct, R_arr)
log('(3) THE D4-TREE: the D4-sums %d (the %d src-reads at the builds!!)' % (n_d4, d4_srcs))
log('    the pieces %d (the %d D4-reads at the builds!!)' % (len(pieces), piece_d4reads))
log('    the sources %d | the targets %d | the tails %d' % (src_reads, tgt_reads, n_tails))
log('    R_struct %d | the total-reads %d -> R_arr %d -> THE HONEST-R %d' % (
    R_struct, total_reads, R_arr, R_honest))

# ============ (4) THE HONEST-WLN-MIX + THE PRICE ============
log('(4) THE PRICE: the honest per-class chains!!')
m = 1 + 9 * (H - 1)
# the classes: (1) the sources+targets (the 1,936 @ the ladder-wln!!); (2) the D4s (the
# [4,+3,+1]-chains: the ~8-mass each!!); (3) the pieces (the +7/+8-builds + the finals!!);
# (4) the tails; (5) the decoder (the +8s!!)
for (lad_wln, tag2) in [(3.0, 'the ladders [1,5,1] (3.0)'), (2.8, 'the ladders-optimistic (2.8)')]:
    for (pbuild, tag1) in [(7, 'the [7,1]-pieces'), (8, 'the [8,1]-pieces'), (6, 'the [6,1]-pieces')]:
        mass = 9 * R_honest + 83 + 2 * V * (H - 1)
        # the classes' masses!!
        m_lad = 2 * V * (H - 1)                      # the 1,936!!
        m_d4 = 8 * n_d4                              # the [4,+3,+1]-chains!!
        m_pc = (pbuild + 1) * len(pieces)            # the [+7,+1]-chains!!
        m_tl = 9 * (n_tails + 10)                    # the tails/decoder (the ~9 each!!)
        m_rest = mass - m_lad - m_d4 - m_pc - m_tl
        if m_rest < 0:
            log('    %-24s %-16s: the mass-negative!! (%d)' % (tag1, tag2, m_rest))
            continue
        # the wln's: the pieces: the ln(m/pbuild); the D4s: 3.2; the ladders: lad_wln; the rest: 3.0
        lnP = (m_lad * lad_wln + m_d4 * 3.2 + m_pc * math.log(m / pbuild) +
               m_tl * math.log(m / 9) + m_rest * 3.0)
        # the hist (the mass-exact: the 2-rank approximation per class!!)!!
        # THE PRICER-HONEST: build the hist via the _fix-mass on the classes' rank-mixes!!
        out = {}
        # the ladders: the {2, 5}-mix at the wln (the [1,5,1]-style!!)
        f2 = (lad_wln - math.log(m / 5)) / (math.log(m / 2) - math.log(m / 5))
        f2 = max(0.0, min(1.0, f2))
        out[2] = out.get(2, 0) + round(m_lad * f2 / 2)
        out[5] = out.get(5, 0) + round(m_lad * (1 - f2) / 5)
        out[4] = out.get(4, 0) + round(m_d4 / 2 / 4) * 2     # the ~half at the 4s!!
        out[3] = out.get(3, 0) + round(m_d4 / 2 / 3) * 3     # the ~half at the 3s!!
        out[pbuild] = out.get(pbuild, 0) + round(m_pc * 0.85 / pbuild)
        out[1] = out.get(1, 0) + round(m_pc * 0.15 / 1)
        out[9] = out.get(9, 0) + round(m_tl / 9)
        out[1] = out.get(1, 0) + round(m_rest / 2)
        out[2] = out.get(2, 0) + round(m_rest / 2 / 2)
        d = mass - sum(k * z for k, z in out.items())
        out[1] = out.get(1, 0) + d
        out = {k: z for k, z in out.items() if z}
        c, prof, dd = price(out, V, H, R_honest)
        log('    %-24s %-24s -> c = %s (%+0.3f%% vs the frontier!!) | the model-ln-mass %.2fM' % (
            tag1, tag2, mp.nstr(c, 9) if c is not None else 'NONE(%s)' % dd.get('error'),
            float((c / FRONTIER - 1) * 100) if c is not None else 0.0, lnP * 288 / 1e6))
log('DONE — THE D4-TREE (the honest-R + the arrival + the shapes!!)')
