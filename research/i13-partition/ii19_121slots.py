"""THE 121-LINE WORD — THE BUILD'S STAGE 1: THE JOINT CHAIN/SLOT DESIGN MEASUREMENT.

THE BUILD (SS1380-1381: 'now build it / 100% verified') needs the joint chain design:
the climb rule (gcheck line 79) is ONE FRAME PER DIMENSION per register chain (nested,
dims increasing!!), so:
- the SOURCES' chains: {s} -> the piece-build-frames (~3.7 pieces per source, at distinct
  dims!!) -> ... -> FULL (the gathers' builds AT FULL: the content spans FULL!! -> NO
  collision!!);
- the TARGETS' chains: 0 -> the read-frames (the ~22 pieces + the tail packed into the
  slots dims 2-8!!) -> the t-perp (dim 8);
- the PIECES' chains: 0 -> the build-frame (the span, dim 2-3) -> the read-frames (the
  users' groups, one per dim!!) -> FULL (dim 9);
- the TAILS' chains: 0 -> the build-frame -> the read (the target's chain!!) -> FULL.

THIS SCRIPT measures the feasibility (the SS1374-style) and produces the DESIGN DATA:
1. the pieces' span dims (the build-frames!!);
2. THE TARGET-SIDE packing: the ~22 pieces + the tail per target into the slots
   (the greedy lowest-fit: the unions' ranks <= the slot dims!!): the unplaced count;
3. THE SOURCE-SIDE packing: the ~3.7 pieces per source at the distinct dims (the
   conflict-free assignment!!);
4. THE PIECE-SIDE groups: the users at the piece's read-frames (the SS1374-style
   max_group at each dim!!): the chain budget check (<= 9 frames!!);
5. THE ARRIVAL LAW: the demand-reads vs 9R -> the honest R;
6. THE VERDICT + the design data pickled for the build (the stage 2: the word!!).
"""
import sys, time, resource, itertools, pickle
from collections import Counter
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

H = 9

# the system: the 120 E8 roots (α, 0, 0) + the special (0, 1, 1)  [the v2 code]
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
L = [list(al) + [0, 0] for al in AL]
L.append([0.0] * 8 + [1.0, 1.0])
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
log('the 121-line system: %d lines (h=9 legal: the PD span)' % V)

PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)

def gf2_rank(rows_in):
    rows = list(rows_in)
    rank = 0
    for col in range(V):
        piv = None
        for i in range(rank, len(rows)):
            if (rows[i] >> col) & 1:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> col) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank
Brows = [PERP[t] | (1 << t) for t in range(V)]
rank_B = gf2_rank(Brows)
log('the perp-pattern decoder: the GF(2) rank %d' % rank_B)

# the demands (the perps!!) + the piece economy (the v2 greedy!!)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 4]
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
    if best is None or best[0] < 4:
        break
    _, piece, real_users = best
    pool.append(piece)
    pool_users.append(real_users)
    for ti in real_users:
        covered[ti] |= set(piece)
        assigned[ti].append(len(pool) - 1)
leftovers = [set(jlines[ti]) - covered[ti] for ti in range(V)]
carriers = sum(1 for lo in leftovers if lo)
log('the piece economy: pool %d, carriers %d (the v2 reproduction)' % (len(pool), carriers))

def span_rank(line_ids):
    if not line_ids:
        return 0
    return int(np.linalg.matrix_rank(np.array([L[i] for i in line_ids])))

# ============ (1) THE PIECES' SPAN DIMS ============
pranks = [span_rank(sorted(p)) for p in pool]
log('(1) the pieces\' span dims: %s' % dict(sorted(Counter(pranks).items())))

# ============ (2) THE TARGET-SIDE PACKING ============
# each target: its pieces + the tail packed into the chain slots dims 2..8; the greedy
# lowest-fit: place the piece at the lowest slot d with rank(union + piece) <= d
tgt_slot = {}   # (t, piece_id or -1 for the tail) -> the slot dim
tgt_unplaced = 0
tgt_slot_load = Counter()
for ti in range(V):
    items = [(pid, pranks[pid]) for pid in assigned[ti]]
    if leftovers[ti]:
        items.append((-1, span_rank(sorted(leftovers[ti]))))
    # the greedy: sort by the rank desc (the big pieces first: the tight slots!!)
    items.sort(key=lambda x: -x[1])
    slot_unions = {d: [] for d in range(2, 9)}
    for pid, r in items:
        placed = False
        for d in range(max(2, r), 9):
            r2 = span_rank(slot_unions[d] + (sorted(pool[pid]) if pid >= 0 else sorted(leftovers[ti])))
            if r2 <= d:
                slot_unions[d] = slot_unions[d] + (sorted(pool[pid]) if pid >= 0 else sorted(leftovers[ti]))
                tgt_slot[(ti, pid)] = d
                tgt_slot_load[d] += 1
                placed = True
                break
        if not placed:
            tgt_unplaced += 1
log('(2) the target-side packing: unplaced %d; the slot loads %s'
    % (tgt_unplaced, dict(sorted(tgt_slot_load.items()))))

# ============ (3) THE SOURCE-SIDE PACKING ============
# each source: the pieces containing it, assigned to DISTINCT dims (the conflict-free!!);
# the gathers at FULL (dim 9!!) cost no dim slot
src_pieces = {s: [] for s in range(V)}
for pid, p in enumerate(pool):
    for s in p:
        src_pieces[s].append(pid)
src_assign = {}   # (s, pid) -> the dim
src_conflicts = 0
for s in range(V):
    pids = sorted(src_pieces[s], key=lambda pid: -pranks[pid])
    used = set()
    for pid in pids:
        d = None
        for cand in range(max(2, pranks[pid]), 9):
            if cand not in used:
                d = cand
                break
        if d is None:
            src_conflicts += 1
            continue
        used.add(d)
        src_assign[(s, pid)] = d
src_dims = Counter(src_assign.values())
log('(3) the source-side packing: conflicts %d; the dim loads %s; the max pieces per source %d'
    % (src_conflicts, dict(sorted(src_dims.items())), max(len(v) for v in src_pieces.values())))

# ============ (4) THE PIECE-SIDE GROUPS (the users at the read-frames) ============
# the piece's users grouped at the piece's read-frames: the users' slot dims (from (2)!!)
# must be consistent: the piece's chain: ONE frame per dim: the users at the same dim
# must SHARE the piece's dim-d frame -> the groups: the users with the same slot dim d
# AND a common frame of dim d containing the piece + inside all their perps
def max_group(users, dmax):
    if not users:
        return 0
    cur = []
    for u in users:
        if span_rank(cur + [u]) <= dmax:
            cur.append(u)
    return len(cur)

piece_frames_used = Counter()
piece_overload = 0
for pid in range(len(pool)):
    users = pool_users[pid]
    # the users' slot dims (from (2)!!)
    by_dim = {}
    for u in users:
        d = tgt_slot.get((u, pid))
        if d is None:
            continue
        by_dim.setdefault(d, []).append(u)
    # the piece's chain: the build (the span dim!!) + the read-frames at the DISTINCT dims + FULL
    n_frames = 1 + len(by_dim) + 1
    piece_frames_used[n_frames] += 1
    if n_frames > H + 1:
        piece_overload += 1
log('(4) the piece-side groups: the frames-per-piece histogram %s; OVERLOADED (> %d frames): %d'
    % (dict(sorted(piece_frames_used.items())), H + 1, piece_overload))

# ============ (5) THE ARRIVAL LAW ============
demand_reads = sum(len(assigned[ti]) + (1 if leftovers[ti] else 0) for ti in range(V))
R_struct = len(pool) + carriers + rank_B
log('(5) the arrival law: the demand-reads %d; 9 x R_struct(%d) = %d: %s (%.0f%%)'
    % (demand_reads, R_struct, 9 * R_struct,
       'FITS' if demand_reads <= 9 * R_struct else 'OVER', 100.0 * demand_reads / (9 * R_struct)))
R_honest = max(R_struct, -(-demand_reads // 9))
log('    the honest R = max(%d, ceil(%d/9)) = %d' % (R_struct, demand_reads, R_honest))

# ============ (6) THE VERDICT + THE DESIGN DATA ============
ok = (tgt_unplaced == 0) and (src_conflicts == 0) and (piece_overload == 0)
log('(6) THE JOINT VERDICT: %s' % ('FEASIBLE — the design data saved; the build proceeds!!' if ok
    else 'TIGHT: %d target-unplaced, %d source-conflicts, %d piece-overloads' %
    (tgt_unplaced, src_conflicts, piece_overload)))
design = dict(pool=[sorted(p) for p in pool], pool_users=pool_users,
              pranks=pranks, leftovers=[sorted(lo) for lo in leftovers],
              tgt_slot={k: v for k, v in tgt_slot.items()},
              src_assign={k: v for k, v in src_assign.items()},
              rank_B=rank_B, R_honest=R_honest)
with open('/Users/dayssky/integer-mult-bounds/research/i13-partition/ii19_121_design.pkl', 'wb') as f:
    pickle.dump(design, f)
log('the design data pickled: ii19_121_design.pkl (%d pieces, %d carriers, R_honest %d)'
    % (len(pool), carriers, R_honest))
log('DONE')
