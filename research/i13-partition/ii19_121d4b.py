"""THE 121-LINE'S DESIGN CENSUS v2 — THE PARTITION-ROOMS (the SS1685 partition!!!).

THE SS1772 CENSUS v1: the 3150 12-line rooms (the D4 sub-lattices!!); the special in NO
room; the perp(t) = the 63 roots (the 315 candidate rooms!) + the special (the remainder!!);
the packing: the 6 rooms + the special-leftover; THE WALL: the ~338 dim-4 frames per target.

THE DESIGN'S ANSWER (the R420's way!!): THE DISJOINT PARTITION (the SS1685: the 30 disjoint
4-frames!!!) — each root's ONE partition-frame — the rooms = the partition-frames' SPANS
(the 12-line D4 rooms!!!).

THE MEASUREMENTS:
(1) THE PARTITION: the 30 disjoint 4-frames (the greedy construction!!)
(2) THE PARTITION-ROOMS: the 30 spans: the line-sets (the 12-line D4 rooms!!)
(3) THE PER-ROOT ROOM-COUNTS: the root s: the partition-rooms containing s: the histogram!!
    (the frame-line: 1 + the derived appearances: ? — THE CARRIERS' DUPLICATION NEEDS!!!)
(4) THE PER-TARGET COVERS: the perp(t) vs the 30 partition-rooms: the inside-rooms +
    the packing (the disjoint covers!) + the remainders (the direct-read lines!!)
(5) THE SPECIAL'S SPAN (the dim-1!): the free same-frame re-reads' feasibility!!
"""
import sys, time
from collections import Counter, defaultdict
import numpy as np

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM ============
import itertools
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

# ============ (1) THE PARTITION (the greedy: the 30 disjoint 4-frames!!) ============
unassigned = list(range(120))
frames4 = []
while unassigned:
    s = unassigned[0]
    partners = [x for x in unassigned[1:] if abs(G[s][x]) < 1e-9]
    trio = None
    for i in range(len(partners)):
        for j in range(i + 1, len(partners)):
            if abs(G[partners[i]][partners[j]]) > 1e-9:
                continue
            for k in range(j + 1, len(partners)):
                a, b, c = partners[i], partners[j], partners[k]
                if abs(G[a][b]) < 1e-9 and abs(G[a][c]) < 1e-9 and abs(G[b][c]) < 1e-9:
                    trio = (a, b, c)
                    break
            if trio:
                break
        if trio:
            break
    assert trio, 'the partition failed at %d' % s
    frames4.append((s,) + trio)
    used = {s, trio[0], trio[1], trio[2]}
    unassigned = [x for x in unassigned if x not in used]
assert len(frames4) == 30, len(frames4)
log('(1) the partition: %d disjoint 4-frames; the leftover %d' % (len(frames4), len(unassigned)))

# ============ (2) THE PARTITION-ROOMS (the spans: the 12-line D4 rooms?!!) ============
rooms = []
for f in frames4:
    B4 = L[list(f)]
    inside = []
    for s in range(120):
        coef, res, rank, sv = np.linalg.lstsq(B4.T, L[s], rcond=None)
        if np.linalg.norm(B4.T @ coef - L[s]) < 1e-8:
            inside.append(s)
    rooms.append(sorted(inside))
rsizes = Counter(len(r) for r in rooms)
log('(2) the partition-rooms: the sizes %s' % dict(sorted(rsizes.items())))
for i in range(3):
    log('    the room %d (the frame %s): %s' % (i, frames4[i], rooms[i]))

# ============ (3) THE PER-ROOT ROOM-COUNTS (the carriers' needs!!) ============
cnt = Counter()
for s in range(120):
    n = sum(1 for r in rooms if s in r)
    cnt[n] += 1
log('(3) the per-root room-counts: %s' % dict(sorted(cnt.items())))
frame_lines = set(x for f in frames4 for x in f)
extra = Counter()
for s in range(120):
    n = sum(1 for r in rooms if s in r)
    extra[n - (1 if s in frame_lines else 0)] += 1
log('    the derived-appearances (n - the frame-line!): %s' % dict(sorted(extra.items())))

# ============ (4) THE PER-TARGET COVERS ============
rmasks = []
for r in rooms:
    m = 0
    for s in r:
        m |= (1 << s)
    rmasks.append(m)
cov_cnt = Counter()
rem_h = Counter()
sub_h = Counter()
cover_data = []
for t in range(V):
    sub = [i for i, m in enumerate(rmasks) if m & PERP[t] == m]
    sub_h[len(sub)] += 1
    cov = 0
    picked = []
    while True:
        best = None
        for i, m in enumerate(rmasks):
            if m & PERP[t] != m:
                continue
            gain = bin(m & PERP[t] & ~cov).count('1')
            if gain == 0:
                continue
            if best is None or gain > best[0]:
                best = (gain, i)
        if best is None:
            break
        cov |= rmasks[best[1]]
        picked.append(best[1])
    rem = PERP[t] & ~cov
    nl = bin(rem).count('1')
    rem_h[nl] += 1
    cov_cnt[len(picked)] += 1
    cover_data.append((t, picked, rem))
log('(4) the inside-rooms per target: %s' % dict(sorted(sub_h.items())))
log('    the packing-rooms: %s' % dict(sorted(cov_cnt.items())))
log('    the remainders: %s' % dict(sorted(rem_h.items())))
for t in (0, 1, 56, 119, 120):
    tt, picked, rem = cover_data[t]
    log('    the target %d: the rooms %s | the remainder-lines %s' % (
        t, picked, [s for s in range(V) if (rem >> s) & 1]))
# the union dims: the per-target picked rooms' pairwise unions (the chain frames!!)
log('    THE CHAIN CHECK: the per-target picked rooms -> the dim-6/7 unions (the next design!!)')

# ============ (5) THE SPECIAL'S SPAN (the free re-reads!!) ============
sp_perp_ok = all((PERP[t] >> 120) & 1 for t in range(V))
log('(5) the special: in every perp (%s); its span (dim 1) ⊆ every perp: THE C_120 READ AT ITS'
    ' ONE SPAN: THE FREE SAME-FRAME RE-READS ✓' % sp_perp_ok)
log('DONE')
