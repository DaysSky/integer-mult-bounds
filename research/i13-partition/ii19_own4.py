"""THE II19 BREAKTHROUGH STEP 4 — THE DISMISSALS' AUDIT + THE CELLS-PIECES-TREE's HONEST-R
(ii19_own4.py).

THE USER'S AUDIT DIRECTIVE (SS2119!!): 'go back to any dismissed idea and think about if it
is really 100% not possible or there was an error in the dismissal'!!

THE AUDIT'S FINDINGS (the dismissals' review!!):
(1) THE ROOMS-DISMISSAL (the §1423's 'rigorous negative'!!): **THE ERROR CONFIRMED!!** — the
    SS1695/1702's rooms-failures were the PAIRS/QUADS-DESIGN-SPECIFIC (the 13-18-user pieces!!):
    the own3's D6-pieces (THE 2-USERS!!) have TRIVIAL rooms (the SS1736's E8-own 1-2-read
    economy!!) — the dismissal GENERALIZED a design-point into a 'rigorous negative'!!!
(2) THE OWN3's OWN R-ESTIMATE (220!!): **THE ARRIVAL BUG (caught in this audit!!!!)** — the
    D6-pieces built DIRECT from ~30 sources each: 180 x 30 = 5,400 source-reads vs 9R = 1,980
    at R=220 — THE ARRIVAL-ILLEGAL (the 2.7x over!!!) — the honest-R needs THE TREE (the shared
    sub-sums!!!): the cells (the ~120, the ~2-src builds!!) -> the union-pieces (the ~15-cell-src
    builds!!): the ~2,000-2,400 reads -> the R ~ 250-270 LEGAL!!!
(3) THE 2-CLASS's h=10-DISMISSAL (the #89/#95!!): **THE BORDERLINE (NOT the 100%!!)** — the
    best: the -11.36% at the (R=280, the D-hist!!): the MASTER LAW: the deficit = 256*240 -
    288*CST (the h-INDEPENDENT!!!): the levers: the R down (~255: the arrival!!) + the wln down
    (the high-rank ladders!!) -> the re-measurement could reach the ~-0--5%!!!
(4) THE SOLID (checked, no error!!): the 361's rank-241 (the GF(2)-algebra!!); the I8-I13's
    measured incidences!!; the all-word-bound's flaw (the record's own fix!!); the transplant's
    420-base!!; the 121-line's form-legality!!

THE MEASUREMENT (THE HONEST-R!!!): the CELLS-PIECES-TREE:
  the sources -> the cells (the {s,s'}-sums: the ~120-180, the 2-src builds: the +1-climbs!!)
  -> the union-pieces (the ~60-90-line contents: the ~15-cell-src builds: the +7-climbs!!)
  -> the targets' reads (the ~2-3 pieces each: the room-frames!!)
  THE ARRIVAL: the ~2,000-2,400 reads -> the R-floor ~ 230-270!!
  THE PRICE: the (R ~ 250-270, the wln ~2.3-2.5!!) -> the c-grid -> THE BREAKTHROUGH's GO/NO-GO!!!
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
log('(0) the system: v=%d h=%d | the B-sizes %s' % (V, H, dict(sorted(Counter(len(b) for b in B121).items()))))

# ============ (1) THE CELLS (the {s,s'}-sums' bases!!) ============
# the cells: the dim-2 frames (the 180!!) — the sources' pairwise-sums' bases!!
cells = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 2]
log('(1) the cells: %d (the {s,s}-pair-frames!!)' % len(cells))

# ============ (2) THE UNION-PIECES' CANDIDATES + THE COVERING ============
# the union-piece: the frame X (the dim-6/7!!) serving the target u iff X's lines ⊥ u!!
# the candidates: the D6s (the 30-line!!) + the D7-UNIONS (the pairs-of-D6s?!)
# — the own3's finding: the D6s serve exactly 2 targets each!!
G0 = [[sum(x * y for x, y in zip(lines0[i], lines0[j])) for j in range(v0)] for i in range(v0)]
d6 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 6]
def served(X):
    out = set()
    for u in range(v0):
        if all(G0[x][u] == 0 for x in X):
            out.add(u)
    return out
# THE CELL-COVERAGE-COST (the honest!!): the piece's build reads the CELLS ⊆ X!!
def cells_in(X, cellmap):
    return sorted(cellmap[c] for c in cells if c <= X)

# the cell -> the first D6 containing it (the cellmap!!)
cellmap = {}
for X in d6:
    for c in cells:
        if c <= X and c not in cellmap:
            cellmap[c] = None
# hmm — a cell can be in multiple D6s!! the assignment: the FIRST (the cheap!!)
# the honest: the cells' D6-memberships!!
d6of = defaultdict(list)
for ci, c in enumerate(cells):
    for X in d6:
        if c <= X:
            d6of[ci].append(X)
log('    the cells: %d | the D6-memberships: %s (the mean %.1f D6s/cell!!)' % (
    len(cells), dict(sorted(Counter(len(z) for z in d6of.values()).items())),
    sum(len(z) for z in d6of.values()) / max(1, len(cells))))

# THE COVERING (the greedy over the D6s (the own3's!) + THE UNION-COSTS!!)
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
# ============ (3) THE HONEST-R + THE ARRIVAL (the tree's!!!) ============
# THE TREE: the cells (the first-level sums (the ~2-src builds!!)) + the pieces (the D6-sums:
# the ~15-cell-src builds?!) + the tails (the residuals' direct (the ~4-bits/reg?!)) + the decoder!
n_cells = len(cells)
n_pieces = len(pieces)
cell_reads = sum(len([c for c in cells if c <= X]) for (X, s) in pieces)     # the pieces' cell-srcs!!
src_reads = 2 * n_cells                                                      # the cells' source-srcs!!
tgt_reads = sum(len(s) for (X, s) in pieces) + rem                            # the targets' reads!!
n_tails = max(1, rem // 4)
R_struct = n_cells + n_pieces + n_tails + 10
total_reads = src_reads + cell_reads + tgt_reads
R_arr = total_reads // 9 + 1
log('(3) THE HONEST-TREE: the cells %d (the %d src-reads!!) + the pieces %d (the %d cell-reads!!)' % (
    n_cells, src_reads, n_pieces, cell_reads))
log('    + the tails %d + the decoder 10 = R_struct %d | the targets-reads %d' % (
    n_tails, R_struct, tgt_reads))
log('    THE ARRIVAL: the total-reads %d -> the R_floor ~ %d | THE STRUCT-R %d -> THE HONEST-R ~ %d' % (
    total_reads, R_arr, R_struct, max(R_struct, R_arr)))
R_honest = max(R_struct, R_arr)

# ============ (4) THE PRICE (the honest shapes!!) ============
log('(4) THE PRICE at the honest-R: the shapes-grid (the wln-targets!!)!!')
for (tag, wln) in [('the [7,1,1]-pieces (2.3!!)', 2.3), ('the [6,1,1]-pieces (2.44)', 2.44),
                   ('the mixed (2.6)', 2.6), ('the ladders-heavy (2.8)', 2.8), ('the worst (3.0)', 3.0)]:
    mass = 9 * R_honest + 83 + 2 * V * (H - 1)
    m = 1 + 9 * (H - 1)
    # the 2-rank mix {hi, lo} realizing the wln!!
    best = None
    for hi in (6, 7, 8, 9):
        for lo in (1, 2, 3):
            lhi, llo = math.log(m / hi), math.log(m / lo)
            if not (llo <= wln <= lhi or lhi <= wln <= llo):
                continue
            f = (wln - llo) / (lhi - llo)
            if 0 <= f <= 1:
                if best is None or abs(best[0] - wln) < 1e-9:
                    pass
                if best is None:
                    best = (hi, lo, f)
    if best is None:
        # the wln below all: the pure-hi!!
        hi = 9
        out = {hi: mass // hi}
        d = mass - hi * out[hi]
        out[1] = out.get(1, 0) + d
    else:
        hi, lo, f = best
        m_hi = mass * f
        out = {hi: round(m_hi / hi), lo: round((mass - m_hi) / lo)}
        d = mass - sum(k * z for k, z in out.items())
        out[1] = out.get(1, 0) + d
    out = {k: z for k, z in out.items() if z}
    c, prof, dd = price(out, V, H, R_honest)
    log('    %-28s -> c = %s (%+0.3f%% vs the frontier!!)' % (
        tag, mp.nstr(c, 9) if c is not None else 'NONE(%s)' % dd.get('error'),
        float((c / FRONTIER - 1) * 100) if c is not None else 0.0))
log('DONE — THE CELLS-PIECES-TREE (the honest-R + the arrival!!!)')
