"""THE TAILS' SOURCE-CHAIN GATE (the decisive check for the room-first designs!!).

THE SS1664 ANALYSIS: THE ONE-ROOM CHAINS (the v3's structure: the 60 dim-7 pair-rooms!!)
ARE LEGAL — the F7 (the pair's content's span) ⊂ the t-perp is AUTOMATIC (perp([t, c1])
⊆ perp(t)!!!): NO nesting problem; the v3's price (+36.81% at R=193!!) is the BEST among
the legal-ish structures.  THE COMMON UNRESOLVED GATE for ALL the room-first versions:
THE TAILS' SOURCE-CHAINS (the SS1589's (b)!!): each source s serves the tails' builds
(the ~27 tails containing s!!); the tails' spans (the dims ~5-8!!) must fit the source's
ONE-FRAME-PER-DIM chain: THE COLLISIONS?!?!

THE CHECK:
1. the v3's structure (the SS1655's greedy: the dim-aware stopping!!): the rooms;
2. the tails: the per-target leftovers + their spans (the dims!!!);
3. THE SOURCES' COLLISION CENSUS: for each source s: the tails containing s: the spans'
   dims: the DISTINCT spans per dim: the collision iff > 1 different spans at the same
   dim!!! (the source's chain: the ONE frame per dim!!!);
4. the verdict: the sources' max-collision histogram + the severity + THE FIX's
   feasibility (the shared tail-frames?!).
"""
import sys, time, itertools
from collections import Counter
import numpy as np

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

# ============ the v3 greedy [the SS1655 code!!] ============
cand = []
for a, b in itertools.combinations(range(V), 2):
    n = bin(PERP[a] & PERP[b]).count('1')
    if n >= TH_ROOM:
        cand.append((n, a, b))
cand.sort(key=lambda x: -x[0])
tgt_dims_used = {t: set() for t in range(V)}
groups = []
n_reject = 0
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
        n_reject += 1
        continue
    lines = [s for s in range(V) if (cp >> s) & 1]
    groups.append((grp, lines, d))
    for t in grp:
        tgt_dims_used[t].add(d)
log('(1) the v3 rooms: %d (the rejects %d!!); the room dims %s'
    % (len(groups), n_reject, dict(sorted(Counter(d for _, _, d in groups).items()))))

# ============ the tails ============
rooms = groups
covered = [0] * V
for grp, lines, d in rooms:
    m = 0
    for s in lines:
        m |= (1 << s)
    for t in grp:
        covered[t] |= m
tails = []
tail_spans = []
for t in range(V):
    unc = [s for s in range(V) if (PERP[t] >> s) & 1 and not (covered[t] >> s) & 1]
    tails.append(unc)
    tail_spans.append(span_rank(unc) if unc else None)
log('(2) the tails: the size histogram %s; the span-dim histogram %s'
    % (dict(sorted(Counter(len(u) for u in tails).items())),
       dict(sorted(Counter(sp for sp in tail_spans if sp is not None).items()))))

# ============ (3) THE SOURCES' COLLISION CENSUS ============
# for each source s: the tails containing s: the DISTINCT spans per dim: the collision iff > 1!!!
src_tail_spans = {}
for t in range(V):
    if not tails[t]:
        continue
    for s in tails[t]:
        src_tail_spans.setdefault(s, set()).add(tail_spans[t])
max_coll = Counter()       # the sources' max distinct-spans-per-dim
n_sources_hit = 0
worst = (0, None)
for s, spans in sorted(src_tail_spans.items()):
    per_dim = Counter(spans)
    mx = max(per_dim.values()) if per_dim else 0
    # hmm: the spans are DIMS: the distinct FRAMES at the same dim: the census needs the
    # frames — the spans' set: the DISTINCT DIMS (the span-dims!!): the source's chain:
    # the one frame per dim: the tails at the same dim: the DIFFERENT frames?!  THE
    # FRAME-level check: the tails' span-FRAMES (the subspaces!!!) at the same dim!!!
    max_coll[mx] += 1
    if mx > 1:
        n_sources_hit += 1
    if mx > worst[0]:
        worst = (mx, s)
log('(3) THE SOURCES x SPAN-DIMS: the sources serving %d; the per-source distinct-dims histogram %s'
    % (len(src_tail_spans), dict(sorted(Counter(len(v) for v in src_tail_spans.values()).items()))))

# THE FRAME-LEVEL COLLISION: the tails' span-FRAMES at the same dim: the distinct subspaces!!!
# the span-frame of a tail: the subspace span(unc): the SAME dim, the DIFFERENT subspaces!!!
def tail_frame(t):
    return tuple(sorted(tails[t]))   # the line-set id (the frame's content-basis id!!)
src_dim_frames = {}
for t in range(V):
    if not tails[t]:
        continue
    s_dim = tail_spans[t]
    for s in tails[t]:
        src_dim_frames.setdefault((s, s_dim), set()).add(t)
# the collision: the (s, dim) with > 1 DISTINCT tail-frames!!!
coll_census = Counter()
n_pair_coll = 0
for (s, dmv), ts in src_dim_frames.items():
    frames = set()
    for t in ts:
        frames.add(tuple(sorted(tails[t])))
    if len(frames) > 1:
        n_pair_coll += len(ts) - 1     # the excess reads needing the resolution
    coll_census[len(frames)] += 1
log('(4) THE FRAME-LEVEL COLLISIONS: the (source, dim) slots %d; the distinct-frames-per-slot histogram %s'
    % (len(src_dim_frames), dict(sorted(coll_census.items()))))
log('    the collision SLOTS ((source, dim) with > 1 distinct tail-frames!!): %d of %d slots (%d sources serving); the worst slot: %d distinct frames'
    % (sum(c for f, c in coll_census.items() if f > 1), len(src_dim_frames),
       len(src_tail_spans), max(coll_census) if coll_census else 0))
log('    THE EXCESS READS (the collision-resolution cost: the tails sharing a slot need the MERGED/raised frames or the per-target fallbacks!!): %d'
    % n_pair_coll)
log('DONE')
