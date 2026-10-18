"""THE PER-PIECE PER-DIM ROOM-MERGING (the SS1695 collisions' fix!!).

THE SS1695 WALL: the pairs-only read-rooms collide at the piece level (~89% of the
(piece, dim) slots with the 2-9 rooms!!!) + the price drops below (the finer jumps:
the LM up!!!).

THE FIX — THE PER-PIECE PER-DIM MERGED ROOMS: for each piece p and each dim d: the
piece's rooms at the dim d (the groups G1, ..., Gk — p is co-read by ALL (the ⊥!!!)):
THE MERGED ROOM = (the union-group G1 ∪ ... ∪ Gk, the co-read pieces (⊥ the WHOLE
union BY CONSTRUCTION ✓✓✓), the span-frame, the dim) — THE ONE ROOM PER PIECE PER
DIM ✓✓✓ LEGAL BY CONSTRUCTION!!!

THE HONEST COSTS (the measured!!!):
(a) the merged rooms' co-read = the ∩ (the pieces ⊥ the BIG unions: the fewer per
    room!!!) -> the residuals?!;
(b) THE TARGET-LEVEL COLLISIONS: the target's ~21 rooms (the different pieces'
    unions!!!) at the same dim: THE CENSUS (the SS1679-class check at the target
    level!!!) — the target's chain: the ONE frame per dim!!!;
(c) the merged rooms' dims: the re-computed (the fewer pieces: the smaller spans!!).

THE MEASUREMENT: the merged rooms + the piece-level census (the ✓ by construction!!)
+ THE TARGET-LEVEL CENSUS + the residuals + the re-hist (the pieces' [0, 4, the ~1-2
merged read-dims, 9]!!!) + THE RE-PRICE.
"""
import sys, time, itertools
from collections import Counter
import numpy as np
from mpmath import mp
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
mp.dps = 40

FRONTIER = 0.001744386
V, H = 121, 9
TH_SAVE = 4
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# the system [the sweep's code!!]
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
L = np.array([list(al) + [0, 0] for al in AL] + [[0.0] * 8 + [1.0, 1.0]])
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
_sr = {}
def span_rank(ids):
    key = tuple(sorted(ids))
    if key not in _sr:
        _sr[key] = int(np.linalg.matrix_rank(L[list(key)])) if key else 0
    return _sr[key]

# ============ (1) the partition + the pieces' economy [the SS1682 code!!] ============
avail = set(range(120))
frames = []
while avail:
    a = min(avail)
    fr = [a]
    for b in sorted(avail):
        if len(fr) >= 4:
            break
        if all(abs(G[b][x]) < 1e-9 for x in fr):
            fr.append(b)
    for x in fr:
        avail.discard(x)
    frames.append(sorted(fr))
piece_users = {}
for f in frames:
    for r in (2, 3, 4):
        for sub in itertools.combinations(f, r):
            mask = PERP[sub[0]]
            for x in sub[1:]:
                mask &= PERP[x]
            users = [t for t in range(V) if t not in sub and (mask >> t) & 1]
            if len(users) >= 2:
                piece_users[sub] = users
covered = [set() for _ in range(V)]
pool = []
while True:
    best = None
    for sub, users in piece_users.items():
        real = [t for t in users if all(s not in covered[t] for s in sub)]
        if len(real) < 2:
            continue
        k = len(sub); u = len(real)
        saving = k * u - (k + u)
        if saving < TH_SAVE:
            continue
        if best is None or saving > best[0]:
            best = (saving, sub, real)
    if best is None:
        break
    _, sub, real = best
    pool.append((sub, real))
    for t in real:
        covered[t] |= set(sub)
leftovers = [sorted(set(jlines[t]) - covered[t]) for t in range(V)]
log('(1) the pieces: %d; the leftovers: the mean %.1f'
    % (len(pool), float(np.mean([len(x) for x in leftovers]))))

# ============ (2) the pairs-only rooms [the SS1690 code!!] ============
piece_delivered = [set() for _ in range(len(pool))]
piece_room_groups = [{} for _ in range(len(pool))]    # pid -> {dim: [groups]}
def coread_of(grp):
    out = []
    for pid in range(len(pool)):
        users = pool[pid][1]
        if all(t in users for t in grp):
            if any(t not in piece_delivered[pid] for t in grp):
                out.append(pid)
    return out
cand_pairs = []
for a, b in itertools.combinations(range(V), 2):
    cr = coread_of([a, b])
    if len(cr) >= 1:
        cand_pairs.append((len(cr), a, b))
cand_pairs.sort(key=lambda x: -x[0])
tgt_dims_used = {t: set() for t in range(V)}
rooms = []
for ncr, a, b in cand_pairs:
    if len(tgt_dims_used[a]) >= 7 or len(tgt_dims_used[b]) >= 7:
        continue
    grp = [a, b]
    cr = coread_of(grp)
    if not cr:
        continue
    lines = set()
    for pid in cr:
        lines |= set(pool[pid][0])
    d = span_rank(sorted(lines))
    if d > 8 or any(d in tgt_dims_used[t] for t in grp):
        continue
    rooms.append((grp, cr, sorted(lines), d))
    for t in grp:
        tgt_dims_used[t].add(d)
    for pid in cr:
        for t in grp:
            piece_delivered[pid].add(t)
        piece_room_groups[pid].setdefault(d, []).append(list(grp))
log('(2) the pairs-only rooms: %d' % len(rooms))

# ============ (3) THE PER-PIECE PER-DIM MERGING ============
# for each piece p, dim d: the union of the room-groups; the co-read pieces (⊥ the union!!!)
merged = []          # (the union-group, the pids, the lines, the dim)
piece_read_dims = [set() for _ in range(len(pool))]
for pid in range(len(pool)):
    for d, grps in piece_room_groups[pid].items():
        ugrp = sorted(set(t for g in grps for t in g))
        # the co-read pieces: the pool's pieces ⊥ the WHOLE union!!!
        umask = PERP[ugrp[0]]
        for t in ugrp[1:]:
            umask &= PERP[t]
        pids = []
        for q in range(len(pool)):
            if all((umask >> s) & 1 for s in pool[q][0]):
                if any(t in pool[q][1] for t in ugrp):
                    pids.append(q)
        lines = set()
        for q in pids:
            lines |= set(pool[q][0])
        md = span_rank(sorted(lines))
        if md > 8:
            continue
        merged.append((ugrp, pids, sorted(lines), md))
        piece_read_dims[pid].add(md)
# the dedup: the same (ugrp, dim): the one room!!!
dedup = {}
for ugrp, pids, lines, md in merged:
    key = (tuple(ugrp), md)
    if key in dedup:
        dedup[key][1] = sorted(set(dedup[key][1]) | set(pids))
        dedup[key][2] = sorted(set(dedup[key][2]) | set(lines))
    else:
        dedup[key] = [list(ugrp), list(pids), list(lines), md]
merged = list(dedup.values())
log('(3) THE MERGED ROOMS: %d; the group-size histogram %s; the dim histogram %s'
    % (len(merged), dict(sorted(Counter(len(g) for g, _, _, _ in merged).items())),
       dict(sorted(Counter(d for _, _, _, d in merged).items()))))
# THE PIECE-LEVEL CENSUS (the ✓ by construction — the check!!!)
piece_rooms_per_dim = {}
for ugrp, pids, lines, md in merged:
    for q in pids:
        piece_rooms_per_dim[(q, md)] = piece_rooms_per_dim.get((q, md), 0) + 1
coll_piece = Counter(piece_rooms_per_dim.values())
log("    THE PIECE-LEVEL CENSUS (the piece's rooms per dim!!!): %s (the > 1 = the collision!!)"
    % dict(sorted(coll_piece.items())))
# THE TARGET-LEVEL CENSUS: the target's rooms at the same dim: the DISTINCT frames!!!
tgt_room_frames = {}
for ugrp, pids, lines, md in merged:
    for t in ugrp:
        tgt_room_frames.setdefault((t, md), set()).add(tuple(ugrp))
coll_tgt = Counter(len(fs) for fs in tgt_room_frames.values())
log("    THE TARGET-LEVEL CENSUS (the target's distinct room-frames per dim!!!): %s (the > 1 = the collision!!)"
    % dict(sorted(coll_tgt.items())))

# ============ (4) THE RE-HIST + THE RE-PRICE ============
n_tails = sum(1 for x in leftovers if x)
R_struct = len(pool) + n_tails + 9
demand = sum(len(u) for _, u in pool) + n_tails
R_hon = max(R_struct, -(-demand // 9))
log('(4) THE R: the pieces %d + the tails %d + the gathers 9 = R_struct %d; the demand %d; R_hon %d (slack %d)'
    % (len(pool), n_tails, R_struct, demand, R_hon, R_hon - R_struct))

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
for pid, (sub, users) in enumerate(pool):
    for j in jumps([0, 4] + sorted(piece_read_dims[pid]) + [H]):
        hist[j] += 1
tail_spans = []
for t in range(V):
    if not leftovers[t]:
        tail_spans.append(None)
        continue
    sp = span_rank(leftovers[t])
    tail_spans.append(sp)
    for j in jumps([0, sp, H]):
        hist[j] += 1
for s in range(120):
    for j in jumps([1, 4, H]):
        hist[j] += 1
for j in jumps([1, H]):
    hist[j] += 1      # the special: the singleton frame (the dim 1!!!)
tgt_dims2 = {}
for ugrp, pids, lines, md in merged:
    for t in ugrp:
        tgt_dims2.setdefault(t, set()).add(md)
for t in range(V):
    ch = {0, 8}
    ch |= tgt_dims2.get(t, set())
    if leftovers[t]:
        ch.add(tail_spans[t])
    for j in jumps(sorted(ch)):
        hist[j] += 1
hist[8] += 8; hist[1] += 8; hist[9] += 1
hist[8] += 8; hist[9] += 1
ident = 9 * R_hon + 73 + 2 * V * 8
slack = R_hon - R_struct
LM = sum(r * z * np.log(73.0 / r) for r, z in hist.items() if r < 73)
log('    THE HIST: %s | the mass %d; the LM %.0f; the identity at R_hon %d: %d'
    % (dict(sorted(hist.items())), sum(r * z for r, z in hist.items()), LM, R_hon, ident))
outs = []
for tag, js in (('coarse', [8, 1]), ('fine', [2, 1, 1, 1, 1, 1, 1, 1])):
    h2 = Counter(hist)
    for _ in range(slack):
        for j in js:
            h2[j] += 1
    mass = sum(r * z for r, z in h2.items())
    if mass != ident:
        outs.append('%s MASS-OFF(%d vs %d)' % (tag, mass, ident))
        continue
    c, prof, dd = pprice(dict(h2), V, H, R_hon)
    outs.append('%s %s' % (tag, 'NO-ROOT' if c is None else '%+.2f%%' % ((float(c) / FRONTIER - 1) * 100)))
log('THE PRICE at R_hon %d: %s' % (R_hon, ' | '.join(outs)))
log('DONE')
