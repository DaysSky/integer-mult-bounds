"""THE RECURSIVE ROOM-FIRST — THE TAIL-ROOMS (the SS1671 wall's fix!!).

THE SS1671 WALL: the tails' source-chains collide TOTALLY (143/203 slots, the worst
42 distinct frames, the excess 3,081!!!): the per-target tails (~27-line leftovers at
the ~dim-7 spans!!) are ILLEGAL AS-IS — every room-first version stands on them.

THE RECURSIVE FIX — THE TAIL-ROOMS: the leftover-lines co-occur across targets (the
ℓ ⊥ multiple targets ✓!!): the tail-pairs' SHARED leftover-lines form the tail-rooms:
- the content: the shared leftover-lines (⊥ both targets BY CONSTRUCTION ✓✓);
- the frame: the CONTENT'S SPAN (the ~dim 4-6 — NOT the ⊥-complement: the content is
  the few shared lines, not the full perp!!!);
- the sources: the content's lines climb to the ONE shared frame per tail-room ✓✓;
- each line is CONSUMED ONCE (the greedy!!): the sources serve ~1-2 tail-rooms ✓✓✓
  THE COLLISIONS RESOLVED;
- the residual tails (the post-tail-room leftovers!!): the ~few lines: the spans
  dim <= ~4: the sources' ~few-per-dim: the smallness resolves the rest!!!

THE MEASUREMENT:
1. the v3's rooms + the leftovers [the SS1667 code!!];
2. THE TAIL-ROOMS' GREEDY: the pairs (t1, t2) sorted by the shared-leftover-count
   desc; the content = the shared leftover-lines; the saving = |content| - 2 (>= 1!!);
3. THE RESIDUALS + the collision re-check (the SS1671's census on the NEW structure!!);
4. THE R + the honest (c)-hist + THE PRICE.
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
TH_ROOM = 12
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
_sr = {}
def span_rank(ids):
    key = tuple(sorted(ids))
    if key not in _sr:
        _sr[key] = int(np.linalg.matrix_rank(L[list(key)])) if key else 0
    return _sr[key]
def room_dim(grp):
    return H - span_rank(grp)

# ============ (1) the v3 rooms [the SS1655/SS1667 code!!] ============
cand = []
for a, b in itertools.combinations(range(V), 2):
    n = bin(PERP[a] & PERP[b]).count('1')
    if n >= TH_ROOM:
        cand.append((n, a, b))
cand.sort(key=lambda x: -x[0])
tgt_dims_used = {t: set() for t in range(V)}
groups = []
for n, a, b in cand:
    if len(tgt_dims_used[a]) >= 7 or len(tgt_dims_used[b]) >= 7:
        continue
    grp = [a, b]
    cp = PERP[a] & PERP[b]
    fresh = False
    d = room_dim(grp)
    while True:
        if all(d not in tgt_dims_used[t] for t in grp):
            fresh = True
            break
        best_c = None; best_n = -1
        for c in range(V):
            if c in grp or len(tgt_dims_used[c]) >= 7:
                continue
            n2 = bin(cp & PERP[c]).count('1')
            if n2 >= TH_ROOM and n2 > best_n:
                best_n = n2; best_c = c
        if best_c is None:
            break
        grp.append(best_c); cp &= PERP[best_c]; d = room_dim(grp)
    if not fresh or d == 0:
        continue
    lines = [s for s in range(V) if (cp >> s) & 1]
    groups.append((grp, lines, d))
    for t in grp:
        tgt_dims_used[t].add(d)
rooms = groups
covered = [0] * V
for grp, lines, d in rooms:
    m = 0
    for s in lines:
        m |= (1 << s)
    for t in grp:
        covered[t] |= m
leftovers = [[s for s in range(V) if (PERP[t] >> s) & 1 and not (covered[t] >> s) & 1] for t in range(V)]
log('(1) the v3 rooms: %d; the room dims %s; the mean leftover %.1f'
    % (len(rooms), dict(sorted(Counter(d for _, _, d in rooms).items())),
       float(np.mean([len(x) for x in leftovers]))))

# ============ (2) THE TAIL-ROOMS' GREEDY ============
# the pairs with the shared leftover-lines: the content = the shared lines (⊥ both ✓!!)
pair_shared = []
for a, b in itertools.combinations(range(V), 2):
    sh = sorted(set(leftovers[a]) & set(leftovers[b]))
    if len(sh) >= 3:          # the saving = |content| - 2 >= 1!!!
        pair_shared.append((len(sh), a, b, sh))
pair_shared.sort(key=lambda x: -x[0])
log('(2) the tail-room candidate pairs: %d (the shared >= 3!!)' % len(pair_shared))
tail_rooms = []          # (grp, lines, dim!!)
tail_consumed = {}       # the line -> the tail-rooms using it (the ~1-2 per line!!)
t_left = [set(x) for x in leftovers]
for nsh, a, b, sh in pair_shared:
    # the FRESH shared lines only (the unconsumed!!!)
    sh2 = [s for s in sh if s not in tail_consumed]
    if len(sh2) < 3:
        continue
    # the per-target: the lines still in BOTH targets' remaining leftovers!!!
    la = [s for s in sh2 if s in t_left[a]]
    lb = [s for s in sh2 if s in t_left[b]]
    content = sorted(set(la) & set(lb))
    if len(content) < 3:
        continue
    d = span_rank(content)
    if d > 8:
        continue
    tail_rooms.append(((a, b), content, d))
    for s in content:
        tail_consumed[s] = True
        t_left[a].discard(s)
        t_left[b].discard(s)
log('    the tail-rooms: %d; the content-size histogram %s; the dim histogram %s'
    % (len(tail_rooms), dict(sorted(Counter(len(c) for _, c, _ in tail_rooms).items())),
       dict(sorted(Counter(d for _, _, d in tail_rooms).items()))))
residuals = [sorted(t_left[t]) for t in range(V)]
log('    THE RESIDUALS: the size histogram %s; the mean %.1f; the zero %d'
    % (dict(sorted(Counter(len(r) for r in residuals).items())),
       float(np.mean([len(r) for r in residuals])),
       sum(1 for r in residuals if not r)))

# ============ (3) THE COLLISION RE-CHECK (the SS1671 census on the NEW structure!!) ============
# the tail-rooms' frames: the shared content-spans ✓; the residuals: the per-target spans.
src_dim_frames = {}
for grp, lines, d in rooms:
    for s in lines:
        src_dim_frames.setdefault((s, d), set()).add(('RM', tuple(grp)))
for grp, content, d in tail_rooms:
    for s in content:
        src_dim_frames.setdefault((s, d), set()).add(('TR', grp))
for t in range(V):
    if residuals[t]:
        rsp = span_rank(residuals[t])
        for s in residuals[t]:
            src_dim_frames.setdefault((s, rsp), set()).add(('RS', t))
coll_census = Counter()
n_coll_slots = 0
worst = 0
for (s, dmv), frames in src_dim_frames.items():
    coll_census[len(frames)] += 1
    if len(frames) > 1:
        n_coll_slots += 1
        worst = max(worst, len(frames))
log('(3) THE COLLISION RE-CHECK: the (source, dim) slots %d; the frames-per-slot histogram %s'
    % (len(src_dim_frames), dict(sorted(coll_census.items()))))
log('    THE COLLISION SLOTS: %d/%d; the worst slot: %d frames'
    % (n_coll_slots, len(src_dim_frames), worst))

# ============ (4) THE R + THE (c)-HIST + THE PRICE ============
n_res = sum(1 for r in residuals if r)
R_struct = len(rooms) + len(tail_rooms) + n_res + 9
demand = sum(len(grp) for grp, _, _ in rooms) + 2 * len(tail_rooms) + n_res
R_hon = max(R_struct, -(-demand // 9))
log('(4) THE R: the rooms %d + the tail-rooms %d + the residuals %d + the gathers 9 = R_struct %d; the demand %d; R_hon %d (slack %d)'
    % (len(rooms), len(tail_rooms), n_res, R_struct, demand, R_hon, R_hon - R_struct))

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
for grp, lines, d in rooms:
    for j in jumps([0, d, H]):
        hist[j] += 1
for grp, content, d in tail_rooms:
    for j in jumps([0, d, H]):
        hist[j] += 1
res_spans = []
for t in range(V):
    if not residuals[t]:
        res_spans.append(None)
        continue
    sp = span_rank(residuals[t])
    res_spans.append(sp)
    for j in jumps([0, sp, H]):
        hist[j] += 1
# the sources' chains: {s} -> the room-frames + the tail-room frames + the residual spans -> FULL!!
src_frames = {}
for grp, lines, d in rooms:
    for s in lines:
        src_frames.setdefault(s, set()).add(d)
for grp, content, d in tail_rooms:
    for s in content:
        src_frames.setdefault(s, set()).add(d)
for t in range(V):
    if residuals[t]:
        for s in residuals[t]:
            src_frames.setdefault(s, set()).add(res_spans[t])
for s in range(V):
    for j in jumps([1] + sorted(src_frames.get(s, set())) + [H]):
        hist[j] += 1
# the targets' chains: 0 -> the room dims + the tail-room dims (the reads!!!) + the residual spans -> 8!!
tgt_dims = {}
for grp, lines, d in rooms:
    for t in grp:
        tgt_dims.setdefault(t, set()).add(d)
for grp, content, d in tail_rooms:
    for t in grp:
        tgt_dims.setdefault(t, set()).add(d)
for t in range(V):
    if residuals[t]:
        tgt_dims.setdefault(t, set()).add(res_spans[t])   # THE RESIDUAL-READ DIM!!!
    for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
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
