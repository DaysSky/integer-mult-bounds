"""THE READ-ROOMS — THE PIECES' CLIMB-FRAMES (the SS1685 scan's next layer!!).

THE SS1685 FEASIBILITY: the partition-structured piece economy EXISTS (the 210 pieces,
the 13-18 users, the ~2-line leftovers!!!) with THE SOURCES' CHAINS LEGAL BY
CONSTRUCTION (the partition!!!) — the price straddles at the arrival-bound R_hon 390
(+2.77% coarse / -1.22% fine!!).

THE KNOWN LIMITATION (the SS1682 flag!!): the reads-at-the-build collide (the target's
~21 pieces at the ~15-20 different 4-frames vs the ONE dim-4 slot!!!).

THE FIX — THE READ-ROOMS (the E8's quads analog!!): the co-read groups' shared frames:
- the group (the ~4-6 targets: the E8's '6 targets per quad'!!!): the co-read pieces
  (the pool's pieces whose users contain the WHOLE group!!!): the content = the
  co-read pieces' UNION (⊥ the group BY CONSTRUCTION ✓✓ — NOT the full perps: the
  SS1679 wall avoided!!!);
- the frame: the content's span (the dim ~5-7!!!) — the dim-freshness for the members
  (the SS1655's lesson!!!);
- the pieces climb: [0, 4 (the build!!), the read-rooms' dims (the ~1-3!!!), 9] ✓✓✓;
- the targets read the pieces AT the rooms' frames (the ~2-4 read-dims per target!!!).

THE MEASUREMENT:
1. the partition + the pieces' economy [the SS1682 code!!];
2. THE READ-ROOMS' GREEDY (the pairs -> the growth (the +targets while the co-read
   pieces >= 1!!) -> the dim-fresh check -> the rooms!!);
3. the residuals (the pieces' users NOT covered by the rooms!!!);
4. THE (c)-HIST (the pieces' chains [0, 4, the read-dims, 9]!!!) + THE PRICE.
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
frame_of = {}
for f in frames:
    for x in f:
        frame_of[x] = tuple(f)
frame_of[120] = (120,)
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
assigned = [[] for _ in range(V)]
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
        assigned[t].append(len(pool) - 1)
leftovers = [sorted(set(jlines[t]) - covered[t]) for t in range(V)]
log('(1) the pieces: %d; the leftovers: the mean %.1f' % (len(pool), float(np.mean([len(x) for x in leftovers]))))

# ============ (2) THE READ-ROOMS' GREEDY ============
# the piece's delivered-users tracking: (pid) -> the set of users delivered via the rooms!!!
piece_delivered = [set() for _ in range(len(pool))]
piece_read_dims = [set() for _ in range(len(pool))]     # the piece's read-dims (the rooms' dims!!!)
# the candidate pairs: the co-read pieces (the pieces whose users contain BOTH t1, t2 AND
# not-yet-delivered to at least one of them!!!
def coread_of(grp):
    """the co-read pieces: the pool's pieces whose users contain the WHOLE group AND with at least one member not yet delivered!!!"""
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
log('(2) the read-room candidate pairs: %d' % len(cand_pairs))
tgt_dims_used = {t: set() for t in range(V)}
rooms = []          # (grp, pids, lines-union, dim)
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
        piece_read_dims[pid].add(d)
log('    the read-rooms: %d; the dim histogram %s'
    % (len(rooms), dict(sorted(Counter(d for _, _, _, d in rooms).items()))))
residuals = 0
for pid in range(len(pool)):
    r = len(set(pool[pid][1]) - piece_delivered[pid])
    residuals += r
log("    THE RESIDUALS (the pieces' users NOT covered by the rooms!!): %d (of the demand %d)"
    % (residuals, sum(len(u) for _, u in pool)))
# THE PIECE'S READ-ROOM COLLISION CENSUS (the honest measurement: the piece's rooms per dim!!!
# — the piece's chain: the ONE frame per dim: the > 1 rooms at the same dim = the collision!!!)
piece_room_dims = {}
for grp, cr, lines, d in rooms:
    for pid in cr:
        piece_room_dims.setdefault(pid, Counter())[d] += 1
per_dim_hist = Counter()
for pid, dc in piece_room_dims.items():
    for dmv, cnt in dc.items():
        per_dim_hist[cnt] += 1
log("    THE PIECE-ROOM COLLISION CENSUS (the piece's rooms per dim!!!): %s"
    % dict(sorted(per_dim_hist.items())))

# ============ (3) THE (c)-HIST + THE PRICE ============
n_tails = sum(1 for x in leftovers if x)
R_struct = len(pool) + n_tails + 9
demand = sum(len(u) for _, u in pool) + n_tails
R_hon = max(R_struct, -(-demand // 9))
log('(3) THE R: the pieces %d + the tails %d + the gathers 9 = R_struct %d; the demand %d; R_hon %d (slack %d)'
    % (len(pool), n_tails, R_struct, demand, R_hon, R_hon - R_struct))

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
# the pieces' chains: [0, 4 (the build!!), the read-dims (the rooms'!!!), 9]
for pid, (sub, users) in enumerate(pool):
    for j in jumps([0, 4] + sorted(piece_read_dims[pid]) + [H]):
        hist[j] += 1
# the tails' chains
tail_spans = []
for t in range(V):
    if not leftovers[t]:
        tail_spans.append(None)
        continue
    sp = span_rank(leftovers[t])
    tail_spans.append(sp)
    for j in jumps([0, sp, H]):
        hist[j] += 1
# the sources' chains: {s} -> THE ONE PARTITION FRAME (the dim 4!!!) -> FULL
for s in range(V):
    fd = span_rank(list(frame_of[s]))
    for j in jumps([1, fd, H]):
        hist[j] += 1
# the targets' chains: 0 -> the read-rooms' dims + the tail spans -> 8
for t in range(V):
    ch = {0, 8}
    ch |= tgt_dims_used[t]
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
