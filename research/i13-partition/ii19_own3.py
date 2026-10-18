"""THE II19 BREAKTHROUGH STEP 3 — THE PIECES'-ECONOMY CENSUS AT THE BREAKTHROUGH ZONE
(ii19_own3.py).

THE OWN1/OWN2's MAP: c = (256*121 - 288*CST)/ln-mass: THE ZONE: (R <= 160) ∧ (wln <= 3.0)
-> c >= 0.001744 (THE FRONTIER!!!): up to +17.4% at (R=121, wln=2.4!!).

THE DESIGN'S TENSION (the record's ground truth!!):
- THE E8's-WAY (the big running-sums, the 1-2 reads: the SS1736!!): the rooms TRIVIAL but
  the R ~ 420 (the DEAD-END: the 48-regime!!!)
- THE SS1685's PAIRS/QUADS (the 2-4-line pieces, the 13-18 users): the R = 210 pieces +
  the tails + the gathers = 339 (THE ZONE's EDGE!!) BUT the read-rooms' collisions (the
  SS1695: 89%!!; the SS1702: the target-level 74%!!!)
- **THE MIDDLE (the target!!): the ~130 pieces x the ~8-9 reads (the demand ~1,080-1,170 =
  the TRUE incidence 9/line!!!) at the FEW SHARED ROOM-FRAMES (the dims 7-8!!): the pieces
  at the D6-STARTS (the +6 builds!!): the chains [6, +1, +1]: the wln ~2.4-2.6!!!**

THE MEASUREMENT (THE GO/NO-GO!!!):
(1) THE PIECES'-CANDIDATES' CENSUS: the D6-sums (the 30-line frames' sums!!): the served-
    sets (the SS1685's served(): X's lines ⊥ u ∧ prior_span[u] ⊆ X!!); the users-counts!!
(2) THE COVERING: the greedy (the SS1685's!!): the pieces' count at the full coverage!!
    -> THE R-ESTIMATE (the pieces + the tails + the decoder!!)
(3) THE WLN-ESTIMATE: the pieces' chains ([6, reads, 9]: the +6s + the read-climbs + the
    +1s!!) + the sources'/targets' ladders -> THE (R, wln) vs THE ZONE!!!
(4) THE ROOMS' FIRST-LOOK: the per-piece read-frames' dims (the collisions' count!!)
"""
import gzip, json, sys, time
from collections import Counter, defaultdict
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')
FRONTIER = mp.mpf('0.001744386')
V, H, SP = 121, 9, 120

# ============ (0) THE 121-LINE SYSTEM + THE B-PATTERNS ============
W = json.load(gzip.open('research/e8-bit-r420/data/bitE8mut-r420.json.gz', 'rt'))
v0, h0, R0 = W['v'], W['h'], W['R']
frames0, lines0 = W['frames'], W['lines']
V9 = [list(L) + [0] for L in lines0] + [[0] * 8 + [1]]

def dot(a, b): return sum(x * y for x, y in zip(a, b))
def ip121(a, b): return sum(a[i] * b[i] for i in range(8)) + 2 * a[8] * b[8]

# THE B-PATTERNS: B[t] = {t} ∪ perp_121(t) (the 65-bit roots / the 121-bit special!!)
G0 = [[dot(lines0[i], lines0[j]) for j in range(v0)] for i in range(v0)]
B121 = []
for t in range(V):
    bits = {t}
    for u in range(V):
        if u != t and ip121(V9[t], V9[u]) == 0:
            bits.add(u)
    B121.append(frozenset(bits))
log('(0) THE B-PATTERNS: the sizes %s (the roots 65, the special 121!!)' % (
    dict(sorted(Counter(len(b) for b in B121).items()))))

# THE DEMAND-MASS (the honest!!): the sum over the targets of |B[t]| MINUS the diagonal-sharings!!
dem = sum(len(B121[t]) for t in range(V)) - V          # the off-diagonal demands!!
log('    the demand-mass (the off-diagonal): %d = %.1f/line' % (dem, dem / V))

# ============ (1) THE PIECES'-CANDIDATES (the D6-sums!!) ============
CNT2DIM0 = {0: 0, 1: 1, 2: 2, 12: 4, 30: 6, 63: 7, 120: 8}
dims0 = [CNT2DIM0[len(fr)] for fr in frames0]
# the D6-frames: the 30-line!! — the pieces' bases (the +6 builds!!)
d6 = [frozenset(frames0[fi]) for fi in range(len(frames0)) if dims0[fi] == 6]
log('(1) THE D6-CANDIDATES: %d frames' % len(d6))

# THE SERVED-SETS: the D6 X serves u iff X's lines ⊥ u (the room-frame's orthogonality!!)
# (the piece's content X must be ⊥ u for u's chain to read it — the gcheck's line-⊥ rule!!)
def served_d6(X):
    """the u's with all X's lines ⊥ u (the room-legality!!)."""
    out = set()
    for u in range(v0):                        # the roots (the special's reads: the odd!!)
        ok = all(G0[x][u] == 0 for x in X)
        if ok:
            out.add(u)
    return out

serv = [served_d6(X) for X in d6]
usz = Counter(len(s) for s in serv)
log('    the served-sizes: %s | the D6s serving >=1: %d' % (
    dict(sorted(usz.items())), sum(1 for s in serv if s)))

# ============ (2) THE COVERING (the SS1685's greedy!!) ============
# the coverage: the target u's B[u]-bits: the pieces' deliveries: the piece X read by u
# covers X ∩ B[u] (the off-diagonal!!); the goal: every (u, w) with w ∈ B[u]\{u} covered!!
need = defaultdict(set)                        # u -> the uncovered bits!!
for u in range(v0):
    need[u] = set(B121[u]) - {u}
cands = [(X, s) for (X, s) in zip(d6, serv) if s]
cands.sort(key=lambda z: -len(z[1]))
pieces = []
covered = defaultdict(set)
for (X, s) in cands:
    # the piece's value: the newly-covered (u, w) pairs!!
    gain = 0
    for u in s:
        gain += len((X & need[u]))
    if gain == 0:
        continue
    pieces.append((X, s, gain))
    for u in s:
        need[u] -= X
rem = sum(len(need[u]) for u in range(v0))
log('(2) THE GREEDY COVERING: %d pieces | the residuals %d bits (the %.1f%% of the demand!!)' % (
    len(pieces), rem, 100 * rem / dem))
gz_ = Counter(g for (X, s, g) in pieces)
log('    the per-piece gains (the top-10): %s' % dict(sorted(gz_.items(), reverse=True)[:10]))
log('    the users-per-piece: %s' % dict(sorted(Counter(len(s) for (X, s, g) in pieces).items())))
# ============ (3) THE R-ESTIMATE + THE WLN ============
# the R: the pieces + the tails (the residuals' direct reads!!) + the decoder (~10!!)!!
tail_reads = rem                                   # the residual bits: the direct reads (the ~1 per bit!!)
n_pieces = len(pieces)
R_est = n_pieces + tail_reads // 4 + 10            # the tails: the shared-ish (the ~4 bits/register!!)
log('(3) THE R-ESTIMATE: the pieces %d + the tails ~%d + the decoder 10 = ~%d' % (
    n_pieces, tail_reads // 4, R_est))
# THE READS (the arrival!!): the pieces' reads = the Σ users!!
reads = sum(len(s) for (X, s, g) in pieces)
log('    the pieces- reads: %d (the arrival: 9R = %d vs the demand %d + the reads!!)' % (
    reads, 9 * R_est, dem))
# THE WLN-ESTIMATE: the pieces' chains [0->6 (+6), the reads at the dims 7-8 (+1/+2!!), the final (+1!!)]!!
# the sources: [1, 6, 1]-ish?!! the targets: [0, 2, 6?, 8]: hmm — the honest model:
# the mass = 9R + 83 + 1936: the pieces' contribution: the +6s (n_pieces) + the +1s (the finals!!)
# the model-hist: {6: n_pieces, 1: the ~finals + the sources'/targets' low-climbs, ...}
# THE SIMPLE HONEST BOUNDS:
for (wln_tag, wln) in [('the pieces [6,1,1]: ~2.44', 2.44), ('the mixed: ~2.8', 2.8), ('the conservative: ~3.0', 3.0)]:
    mass = 9 * R_est + 83 + 2 * V * (H - 1)
    import math
    # the 2-rank mix {6, 1} realizing the wln!!
    lhi, llo = math.log(73 / 6), math.log(73 / 1)
    f = (wln - llo) / (lhi - llo)                # the fraction of the mass at the rank 6!!
    m6 = mass * f
    out = {6: round(m6 / 6), 1: round((mass - m6) / 1)}
    d = mass - sum(k * z for k, z in out.items())
    out[1] = out.get(1, 0) + d
    c, prof, dd = price({k: z for k, z in out.items() if z}, V, H, R_est)
    log('    %-28s -> c = %s (%+0.3f%% vs the frontier!!)' % (
        wln_tag, mp.nstr(c, 9) if c is not None else 'NONE', 
        float((c / FRONTIER - 1) * 100) if c is not None else 0))
log('DONE — THE PIECES-ECONOMY CENSUS AT THE ZONE!!')
