"""II19 2-CLASS SLOTS — the joint chain/slot realizability measurement (the push's decisive gate).

THE FORMAT'S CLIMB RULE (one frame per dimension per register chain) implies:
- a piece of content-rank d0 has read-slots at dims d0..8 (one frame each, all ⊇ span(P));
- a user-group reading the piece at dim d must share a frame F_d ⊇ span(P) inside all
  their perps: rank(the group's targets) <= 9 - d  (the R420's own quad mechanism: 12
  targets of rank 3 share the dim-6 quad frame!!);
- each target's chain: one frame per dim: its ~8 pieces pack into the slots dims (d_min..8)
  with the unions' ranks <= the slot dims; the perp (dim 8) is the catch-all BUT each piece
  has only ONE dim-8 frame = one user's perp (the perps are distinct!!).

THE MEASUREMENT (the push's decisive gate):
1. the pieces' content-rank distributions per class (the class-1 spans carry the level
   direction: rank(α's) + 1!!);
2. the per-piece per-slot max user-groups (the greedy rank-bounded subsets);
3. the user-side packing: the pieces per slot, the unions' ranks;
4. THE JOINT VERDICT: the total (piece, user) capacity vs the demand (2,424 pairs) ->
   the pool resize -> THE HONEST R -> THE PRICE BAND at that R.
"""
import sys, time, resource, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V, H = 240, 9
CST = 144

# the 2-class system (verbatim from ii19_2class_push.py)
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
d8 = {}
for r in list(roots) + half: d8[canon(r)] = np.array(r)
AL = list(d8.values())
L = []
CLS = []
for al in AL:
    L.append(list(al) + [0, 0]); CLS.append(0)
for al in AL:
    L.append(list(al) + [1, 0]); CLS.append(1)
L = np.array(L, dtype=float)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and CLS[s] == CLS[t] and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
log('2-class system: %d lines' % V)

# the canonical k=1 junks
JUNKS = []
for t in range(V):
    partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
    x = partners[0]
    JUNKS.append(PERP[t] ^ (PERP[t] & PERP[x]))
jlines = [[s for s in range(V) if (j >> s) & 1] for j in JUNKS]

# the pair tables + the greedy pool at (2,2) — verbatim
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 2]
covered = [set() for _ in range(V)]
assigned = [[] for _ in range(V)]
pool = []
pool_users = []
while True:
    best = None
    for (c, (a, b)) in top:
        users = [ti for ti in pair_junks[(a, b)]
                 if a not in covered[ti] and b not in covered[ti]]
        if len(users) < 2:
            continue
        common = None
        for ti in users:
            unc = set(jlines[ti]) - covered[ti]
            common = unc if common is None else (common & unc)
        if common is None or len(common) < 2:
            continue
        piece = frozenset(common)
        real_users = [ti for ti in users if piece <= set(jlines[ti]) - covered[ti]]
        k = len(piece); u = len(real_users)
        if u < 2:
            continue
        saving = k * u - (k + u)
        if saving <= 0:
            continue
        if best is None or saving > best[0]:
            best = (saving, piece, real_users)
    if best is None or best[0] < 2:
        break
    _, piece, real_users = best
    pool.append(piece)
    pool_users.append(real_users)
    for ti in real_users:
        covered[ti] |= set(piece)
        assigned[ti].append(len(pool) - 1)
leftovers = [set(jlines[ti]) - covered[ti] for ti in range(V)]
carriers = sum(1 for lo in leftovers if lo)
log('pool %d pieces, carriers %d (the SS1354 (2,2) configuration reproduced)' % (len(pool), carriers))

# ============ (1) THE PIECES' CONTENT-RANK DISTRIBUTION ============
def span_rank(line_ids, rows=L):
    if not line_ids:
        return 0
    return int(np.linalg.matrix_rank(np.array([rows[i] for i in line_ids])))

ranks = Counter()
slots_per_piece = []
for pi, piece in enumerate(pool):
    r = span_rank(sorted(piece))
    cls = CLS[next(iter(piece))]
    # the span dim: the class-1 pieces carry the level direction (+1)
    d0 = r + (1 if cls == 1 else 0)
    ranks[d0] += 1
    slots_per_piece.append((d0, len(pool_users[pi])))
log('THE PIECES\' SPAN DIMS (d0): %s' % dict(sorted(ranks.items())))
log('  (the class-1 pieces carry +1 for the level direction; the class-0 are the raw α-ranks)')

# ============ (2) THE PER-PIECE PER-SLOT MAX USER-GROUPS ============
# at slot dim d: the group = a subset of the piece's users with rank(group targets) <= 9-d;
# the greedy rank-bounded growth (the users ordered by their co-rank structure)
def max_group(users, dmax):
    """the max subset of users with rank <= dmax (greedy: add while the rank fits)"""
    if not users:
        return 0
    cur = []
    cur_rank = 0
    for u in users:
        r2 = span_rank(cur + [u])
        if r2 <= dmax:
            cur.append(u)
            cur_rank = r2
    return len(cur)

group_stats = Counter()
piece_capacity = []
for pi, piece in enumerate(pool):
    d0, _ = slots_per_piece[pi]
    users = sorted(pool_users[pi])
    caps = {}
    total_cap = 0
    remaining = list(users)
    for d in range(d0, 9):
        # the users assigned to this slot dim: the max group among the REMAINING users
        g = max_group(remaining, 9 - d) if remaining else 0
        caps[d] = g
        total_cap += g
        # remove the grouped users (greedy: the strongest groups at the low dims)
        if g:
            cur = []
            for u in remaining:
                if span_rank(cur + [u]) <= 9 - d:
                    cur.append(u)
            remaining = [u for u in remaining if u not in cur]
    piece_capacity.append((total_cap, len(users), caps))
    group_stats[min(total_cap, 20)] += 1
log('THE PER-PIECE SLOT CAPACITIES (the sum over the slots of the max rank-bounded groups):')
log('  capacity histogram (capped at 20): %s' % dict(sorted(group_stats.items())))
short = [(tc, u) for tc, u, _ in piece_capacity]
log('  the pieces with capacity < users (NEED RESIZE): %d of %d'
    % (sum(1 for tc, u in short if tc < u), len(short)))
log('  mean capacity %.1f vs mean users %.1f'
    % (sum(tc for tc, _ in short) / len(short), sum(u for _, u in short) / len(short)))

# ============ (3) THE USER-SIDE PACKING: the pieces per slot, the unions' ranks ============
# each target: its pieces (assigned + the tail carrier): packed into the slots dims 4..8:
# the lowest slot whose dim >= the union's rank (greedy by size)
slot_load = Counter()
unfit = 0
for ti in range(V):
    ps = assigned[ti]
    pl = sorted((pool[p] for p in ps), key=len, reverse=True)
    if leftovers[ti]:
        pl.append(leftovers[ti])
    # the greedy packing: the slot dims 4..8; each slot holds pieces while the union's rank <= d
    slot = 4
    cur_union = []
    for p in pl:
        placed = False
        for d in range(max(4, span_rank(sorted(p)) + (1 if CLS[next(iter(p))] == 1 else 0)), 9):
            # try to place at the current slot dim d (the union's rank check)
            r2 = span_rank(cur_union + sorted(p))
            if r2 <= d:
                cur_union = cur_union + sorted(p)
                slot_load[d] += 1
                placed = True
                break
            # else move to the next slot dim (reset the union)
            cur_union = sorted(p)
            slot_load[d + 1] += 1
            placed = True
            break
        if not placed:
            unfit += 1
log('THE USER-SIDE PACKING (the greedy lowest-fit): the slot loads %s' % dict(sorted(slot_load.items())))
log('  unplaced pieces: %d' % unfit)

# ============ (4) THE JOINT VERDICT ============
demand = sum(len(us) for us in pool_users)
capacity = sum(tc for tc, _, _ in piece_capacity)
log('THE JOINT: the (piece, user) demand %d vs the slot capacity %d (%.0f%%)'
    % (demand, capacity, 100.0 * demand / max(1, capacity)))
if capacity >= demand:
    log('  FEASIBLE at the piece side: the pool %d STANDS (with the per-dim group coordination)' % len(pool))
    resize = len(pool)
else:
    resize = int(len(pool) * demand / capacity) + 1
    log('  TIGHT: the pool resizes to ~%d (the sharing capped by the slots)' % resize)

R_struct = resize + carriers + 18
log('THE HONEST R: %d + %d + 18 = %d (R/v %.2f)' % (resize, carriers, R_struct, R_struct / V))

def hist_true(R, variant):
    ident = H * R + CST + 2 * V * (H - 1)
    mids = R - 18
    if variant == 'A':
        hist = {1: 3840.0 + 9.0 * R, 8: 18.0}
    elif variant == 'B':
        hist = {1: 2400.0 + 3.0 * mids + 18.0, 2: 720.0 + 3.0 * mids, 8: 36.0}
    elif variant == 'D':
        climb = 9.0 * R + 3840.0
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 8: 18.0}
    else:
        hist = {1: 1200.0 + 18.0, 2: 960.0 + 2.0 * mids, 4: 180.0, 5: 1.0 * mids, 8: 36.0}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE PRICE BAND AT THE HONEST R = %d ===' % R_struct)
for R in sorted(set([R_struct, 430, 460, 490, 520, 550, 560, 590])):
    if R < R_struct:
        continue
    line = '  R %3d: ' % R
    for var in ('A', 'B', 'C', 'D'):
        hist = hist_true(R, var)
        cc, _, det = pprice(hist, V, H, R)
        if cc is None:
            line += '%s NO-ROOT  ' % var
        else:
            line += '%s %+.2f%%  ' % (var, (cc / FRONTIER - 1) * 100)
    log(line)
log('DONE')
