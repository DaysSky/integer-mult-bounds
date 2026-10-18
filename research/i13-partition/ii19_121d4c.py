"""THE 121-LINE'S DESIGN CENSUS v3 — THE ROOM-UNION (THE R-WINDOW'S DECISIVE DATUM!!).

THE SS1778 v2 VERDICT: the disjoint-partition rooms (the ~10-15 distinct D4s!!) DO NOT
COVER the perps (the 112 targets: the 52-LINE REMAINDERS!!!) — the SS1685-partition approach
is DEAD for the covers!! THE REAL STRUCTURE: the 3150-room economy (the SS1772 v1!!): the
per-target 6-room packings (the 5 full + 1 partial + the special!!).

THE R-WINDOW QUESTION (the decisive!!): the R420's own R/v = 3.5 (the 240 carriers + the
180 sums!!); the 121-line's HOSTING WALL: the R <= 484 (= 4v!!); THE ROOM-UNION'S SIZE
DECIDES THE FEASIBILITY!!

THE MEASUREMENTS:
(1) THE ROOMS (the v1's enumeration: the 3150 12-line D4s!!)
(2) THE PER-TARGET PACKINGS (the v1's greedy max-coverage: the ~6 rooms + the special!!)
(3) THE UNION: the distinct rooms used over the 121 packings (the ~726 slots / the sharing!!)
(4) THE ROOMS' USER-COUNTS (the sharing: the targets per room — the E8's '70 x 6' analog!!)
(5) THE CARRIERS' NEEDS: the per-source room-appearances in the union (the ~2-10?! — the
    duplication needs!!) + the hist
(6) THE R ESTIMATE vs THE WALL 484: the carriers + the room-sums + the sums + the gathers!!
"""
import sys, time, itertools
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
log('(0) the system: %d lines; h=%d' % (V, H))

# ============ (1) THE ROOMS (the v1's enumeration!!) ============
seen = set()
r12 = []               # the (mask, frozenset) rooms!!
by_mask = {}
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
                key = frozenset((a, b, c, d))
                if key in seen:
                    continue
                seen.add(key)
                B4 = L[[a, b, c, d]]
                inside = []
                for s in range(V):
                    coef, res, rank, sv = np.linalg.lstsq(B4.T, L[s], rcond=None)
                    if np.linalg.norm(B4.T @ coef - L[s]) < 1e-8:
                        inside.append(s)
                if len(inside) == 12:
                    m = 0
                    for s in inside:
                        m |= (1 << s)
                    if m in by_mask:
                        continue
                    by_mask[m] = True
                    r12.append((m, frozenset(inside)))
log('(1) the rooms: %d (the 12-line D4s!!)' % len(r12))

# ============ (2) THE PER-TARGET PACKINGS (the greedy max-coverage!!) ============
packs = []
for t in range(V):
    cov = 0
    picked = []
    while True:
        best = None
        for m, fl in r12:
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
    packs.append((t, picked, rem))
log('(2) the packings: %s | the remainders %s' % (
    dict(sorted(Counter(len(p[1]) for p in packs).items())),
    dict(sorted(Counter(bin(p[2]).count('1') for p in packs).items()))))

# ============ (3) THE UNION (the distinct rooms used!!) ============
union_masks = set()
for t, picked, rem in packs:
    for m in picked:
        union_masks.add(m)
log('(3) THE UNION: %d distinct rooms (from %d slots!!)' % (
    len(union_masks), sum(len(p[1]) for p in packs)))

# ============ (4) THE ROOMS' USER-COUNTS (the sharing!!) ============
users = Counter()
for t, picked, rem in packs:
    for m in picked:
        users[m] += 1
uh = Counter(users.values())
log('(4) THE SHARING: the users-per-room %s' % dict(sorted(uh.items())))
log('    the E8 analog: the 70 quads x 6 targets (SS466!!) — the 121-line: the %d rooms x the mean %.1f users!!' % (
    len(union_masks), sum(users.values()) / max(1, len(union_masks))))

# ============ (5) THE CARRIERS' NEEDS (the per-source appearances!!) ============
room_lines = defaultdict(list)
for m in union_masks:
    for s in range(120):
        if (m >> s) & 1:
            room_lines[s].append(m)
cnt = Counter(len(v) for v in room_lines.values())
log('(5) THE CARRIERS: the per-source room-appearances: %s' % dict(sorted(cnt.items())))
log('    the duplication needs: the max %d; the sum %d (the carriers if 1 per room-slot!!)' % (
    max(len(v) for v in room_lines.values()), sum(len(v) for v in room_lines.values())))

# ============ (6) THE R ESTIMATE vs THE WALL ============
n_carr_dupe = sum(len(v) for v in room_lines.values())
n_carr_2 = 2 * 120
n_rooms = len(union_masks)
n_sums = 121 + 9           # the per-target leftovers-sums + the gathers (the estimate!!)
wall = 4 * V
for tag, n_carr in (('the duplication (1 per room-slot!!)', n_carr_dupe),
                    ('the R420-style (2 per source!!)', n_carr_2)):
    R = n_carr + n_rooms + n_sums
    log('(6) THE R ESTIMATE (%s): the carriers %d + the rooms %d + the sums %d = %d vs THE WALL %d (%s)' % (
        tag, n_carr, n_rooms, n_sums, R, wall, 'OVER!!' if R > wall else 'WITHIN'))
log('DONE')
