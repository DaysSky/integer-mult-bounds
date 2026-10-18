"""THE 121-LINE'S D4 CENSUS (the R420-style redesign's ground work!!!).

THE R420's MEASURED STRUCTURE (SS1736/SS1742/SS1752!!): the flag 0-1-2-4-6-7-8; the 12-line
dim-4 rooms (THE D4 SUB-LATTICES: the 70!!); the 30-line dim-6 frames (the 180!!); the perps
(the dim 7!); THE TARGETS: the [2, 7] reads (the direct sources + the top-sums!!); the perp(t)
= the ~5-6 12-frame rooms + the remainder (the direct lines!!).

THE 121-LINE'S CENSUS:
(1) THE 12-FRAMES: the mutually-orthogonal quadruples -> the spans -> the line-counts ->
    the dedup -> the D4 rooms (the ~70 E8 analogs + the special's cases!!)
(2) THE PERP-COVERS: perp(t) vs the 12-frames: the cover structure (the ~5-6 per target?!)
    + the remainders (the direct-read lines!)
(3) THE CHAIN FEASIBILITY: the target's cover: the 12-frames' dims (the ONE dim-4?!) +
    the 30-frame unions (the dim-6!) + the remainder reads
(4) THE SPECIAL'S CASES: the special (the line 120: the (0,1) hyperbolic!): the perp =
    the 120 roots: the covers?!
"""
import sys, itertools, time
from collections import Counter, defaultdict
import numpy as np

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM ============
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v8 = np.zeros(8); v8[i] = si; v8[j] = sj
                roots.append(v8)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(vv):
    for x in vv:
        if x != 0:
            return tuple(vv) if x > 0 else tuple(-vv)
    return tuple(vv)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = np.array([list(al) + [0.0] for al in AL] + [[0.0] * 8 + [1.0]])
V = len(L)
H = 9
FORM = np.diag([1.0] * 8 + [2.0])
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
log('(0) the system: %d lines; h=%d' % (V, H))

# ============ (1) THE 12-FRAMES (the D4 rooms!!) ============
# the mutually-orthogonal quadruples -> the spans -> the line-counts -> the dedup!!
seen = set()
rooms = []             # the list of the (frame-lines frozenset, the dim, the mask)
by_mask = {}
cnt_quads = 0
for a in range(120):
    for b in range(a + 1, 120):
        if abs(G[a][b]) > 1e-9:
            continue
        for c in range(b + 1, 120):
            if abs(G[a][c]) > 1e-9 or abs(G[b][c]) > 1e-9:
                continue
            for d in range(c + 1, 120):
                if abs(G[a][d]) > 1e-9 or abs(G[b][d]) > 1e-9 or abs(G[c][d]) > 1e-9:
                    continue
                cnt_quads += 1
                key = frozenset((a, b, c, d))
                if key in seen:
                    continue
                seen.add(key)
                # THE SPAN: the dim-4 subspace span(a,b,c,d) — the lines inside!!!
                B4 = L[[a, b, c, d]]
                # the span's membership: solve B4^T x = L[s] (the 4-dim coords!!)
                inside = []
                for s in range(V):
                    coef, res, rank, sv = np.linalg.lstsq(B4.T, L[s], rcond=None)
                    if np.linalg.norm(B4.T @ coef - L[s]) < 1e-8:
                        inside.append(s)
                if len(inside) >= 8:
                    m = 0
                    for s in inside:
                        m |= (1 << s)
                    if m in by_mask:
                        continue
                    by_mask[m] = len(inside)
                    rooms.append((frozenset(inside), 4, m))
log('(1) the orthogonal quadruples: %d | THE DISTINCT SPANS with >= 8 lines: %d' % (cnt_quads, len(rooms)))
sizes = Counter(len(r[0]) for r in rooms)
log('    THE ROOM SIZES: %s' % dict(sorted(sizes.items())))
# the D4 structures: the 12-line rooms!!!
r12 = [r for r in rooms if len(r[0]) == 12]
r10 = [r for r in rooms if len(r[0]) == 10]
log('    THE 12-LINE ROOMS: %d | the 10-line: %d | the 8-line: %d | the other: %s' % (
    len(r12), len(r10), sum(1 for r in rooms if len(r[0]) == 8),
    {k: v for k, v in sizes.items() if k not in (8, 10, 12)}))
# THE SPECIAL'S ROOMS: the rooms containing the line 120?!
sp_rooms = [r for r in rooms if (r[2] >> 120) & 1]
log('    THE ROOMS CONTAINING THE SPECIAL (120): %d | the sizes: %s' % (
    len(sp_rooms), dict(sorted(Counter(len(r[0]) for r in sp_rooms).items()))))

# ============ (2) THE PERP-COVERS ============
# perp(t) vs the 12-frames: the cover structure!!
print()
log('(2) THE PERP-COVERS (the perp(t) = the ~5-6 12-frame rooms + the remainder?!):')
# the 12-frame rooms' masks: the per-frame: the targets whose perps CONTAIN the room
# (the t -> the rooms: the room-mask & PERP[t] == room-mask!!!)
room_masks = [(r[2], r[0]) for r in r12]
tgt_rooms = defaultdict(list)
for t in range(V):
    for m, fl in room_masks:
        if m & PERP[t] == m:
            tgt_rooms[t].append(m)
covers = Counter(len(v) for v in tgt_rooms.values())
log('    the per-target 12-frame covers: %s' % dict(sorted(covers.items())))
for t in (0, 1, 2, 56, 119, 120):
    ms = tgt_rooms[t]
    cov = 0
    for m in ms:
        cov |= m
    rem = PERP[t] & ~cov
    rem_lines = [s for s in range(V) if (rem >> s) & 1]
    log('    the target %d: the covers %d | the covered %d/%d | THE REMAINDER %d: %s' % (
        t, len(ms), bin(cov & PERP[t]).count('1'), len(jlines[t]), len(rem_lines),
        rem_lines[:12]))
# the disjoint-cover packing (the greedy: the max-coverage!!) — the design's data!!
print()
log('    THE DISJOINT-COVER PACKING (the greedy max-coverage per target!!):')
pack_stats = []
rem_hist = Counter()
for t in range(V):
    cov = 0
    picked = []
    while True:
        best = None
        for m, fl in room_masks:
            if m & PERP[t] != m:
                continue
            gain = bin(m & PERP[t] & ~cov).count('1')
            if gain == 0:
                continue
            if best is None or gain > best[0]:
                best = (gain, m)
        if best is None:
            break
        cov |= best[1]
        picked.append(best[1])
    rem = PERP[t] & ~cov
    nl = bin(rem).count('1')
    rem_hist[nl] += 1
    pack_stats.append((t, len(picked), nl))
log('    the packing: the covers-per-target: %s' % dict(sorted(Counter(p[1] for p in pack_stats).items())))
log('    the packing: THE REMAINDERS: %s' % dict(sorted(rem_hist.items())))
bad = [p for p in pack_stats if p[1] > 6]
log('    the targets with > 6 covers: %d %s' % (len(bad), bad[:8]))

# ============ (3) THE 30-FRAMES (the dim-6 unions?!) ============
# the pairwise unions of the 12-frames: the spans' dims: the dim-6 candidates!!!
print()
log('(3) THE 30-FRAME ANALOGS (the pairwise unions of the 12-frames!!):')
u30 = set()
for i in range(len(r12)):
    for j in range(i + 1, len(r12)):
        u = r12[i][0] | r12[j][0]
        if len(u) > 40:
            continue
        M = L[sorted(u)]
        dim = np.linalg.matrix_rank(M)
        if dim == 6:
            key = frozenset(u)
            if key not in u30:
                u30.add(key)
log('    THE DIM-6 UNIONS: %d (the distinct line-sets!!)' % len(u30))
usizes = Counter(len(u) for u in u30)
log('    the union sizes: %s' % dict(sorted(usizes.items())))

# ============ (4) THE CHAIN FEASIBILITY (the design's verdict!!) ============
print()
log('(4) THE CHAIN FEASIBILITY (the R420-style [2, 7]-analog!!):')
# the target's chain: 0 -> (the 12-frames' reads: the ONE dim-4?!) -> the dim-6 unions -> the perp (8!)
# the honest check: the per-target: the covers' dims: the chain: the ~4-6 dim-4 frames?! — the collision!!
feas = Counter()
for t in range(V):
    ms = tgt_rooms[t]
    dims = sorted(set([4] * len(ms)))
    feas['covers %d' % len(ms)] += 1
log('    the honest: the ~%d dim-4 frames per target: THE ONE-PER-DIM WALL unless the unions!!' % (
    sum(len(v) for v in tgt_rooms.values()) // V))
log('    THE DESIGN: the S_t chains: 0 -> the 12-frames (the FREE re-reads at the SAME frame?!) -> the dim-6 unions -> the t-perp (8!!)')
log('    (the full joint design: the next script — the build!!)')
log('DONE')
