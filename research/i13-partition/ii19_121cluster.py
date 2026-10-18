"""THE ROOM-FIRST DESIGN — THE CLUSTER CENSUS (the user's SS1643: 'context is NOT LOW ASSUME ITS INFINITE'!!).

THE SS1636 STRUCTURAL WALL: the naive piece economies are NOT REALIZABLE (the room-safety:
repairable 0 at every TH!!).  THE SS1642 IDENTIFIED PATH: THE ROOM-FIRST DESIGN (the E8's
actual order!!): the perp-safe co-read groups FIRST (the room-totals' contents ⊆ the common
perps -> PERP-SAFE BY CONSTRUCTION!!!), the shared frames, then the pieces as the
room-contents.

THE E8'S REFERENCE: the R420's rooms (the '70 quads x 6 targets'!!): the ~12-line shared
frames (the '12-frames'!!) serving ~6 targets each — the co-read sets ARE the D4 structures:
perp-safe BY CONSTRUCTION!!!

THE MEASUREMENT (the first cut, TH_ROOM = 12: the E8's quad-size analog!!):
1. THE PAIR CENSUS: the pairs' common-perp sizes (the lines orthogonal to both!!): the histogram;
2. THE GREEDY CLUSTERS: the groups grown while the common perp >= TH_ROOM: the maximal groups
   (the per-target group cap ~8: the chain budget!!);
3. THE ROOMS: the groups' common perps: the spans' dims + the line-counts;
4. THE COVERAGE: per target: the union of its groups' room-lines vs perp(t): the tails (the uncovered!!);
5. THE R: the rooms + the tails + the gathers: the estimate;
6. THE (c)-HIST + THE PRICE: the room-first structure's honest model (the rooms' chains
   [0, the room's frame, FULL] — THE READS AT THE BUILD FRAME: NO EXTRA CLIMBS!!! + the
   sources' climbs to the rooms' frames + the targets' cumulative chains!!).

THE HONEST CAVEATS: (a) the targets' chains: the rooms' frames' NESTING assumed (the
cumulative: the SS1604-style!!) — NOT CHECKED (the next layer!!!); (b) the threshold 12:
the E8's analog — the sensitivity sweep: the next; (c) the mass identity: checked!!
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
TH_ROOM = 12          # the E8's quad-size analog (the 12-line frames!!!)
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

# ============ (1) THE PAIR CENSUS ============
pair_sizes = Counter()
for a, b in itertools.combinations(range(V), 2):
    n = bin(PERP[a] & PERP[b]).count('1')
    pair_sizes[n] += 1
log('(1) THE PAIR CENSUS: the common-perp size histogram: %s' % dict(sorted(pair_sizes.items())))

# ============ (2) THE GREEDY CLUSTERS ============
cand = []
for a, b in itertools.combinations(range(V), 2):
    n = bin(PERP[a] & PERP[b]).count('1')
    if n >= TH_ROOM:
        cand.append((n, a, b))
cand.sort(key=lambda x: -x[0])
log('    the pairs with the common perp >= %d: %d' % (TH_ROOM, len(cand)))
groups = []
covered_t = Counter()     # the per-target group-membership cap (the chain budget!!)
for n, a, b in cand:
    if covered_t[a] >= 8 or covered_t[b] >= 8:
        continue
    grp = [a, b]
    cp = PERP[a] & PERP[b]
    while True:
        best_c = None; best_n = -1
        for c in range(V):
            if c in grp or covered_t[c] >= 8:
                continue
            n2 = bin(cp & PERP[c]).count('1')
            if n2 >= TH_ROOM and n2 > best_n:
                best_n = n2; best_c = c
        if best_c is None:
            break
        grp.append(best_c); cp &= PERP[best_c]
    groups.append((grp, cp))
    for t in grp:
        covered_t[t] += 1
log('(2) THE GREEDY CLUSTERS: %d groups; the group-size histogram %s; the per-target group-counts %s'
    % (len(groups), dict(sorted(Counter(len(g) for g, _ in groups).items())),
       dict(sorted(Counter(covered_t.values()).items()))))

# ============ (3) THE ROOMS ============
rooms = []
for grp, cp in groups:
    lines = [s for s in range(V) if (cp >> s) & 1]
    d = span_rank(lines)
    rooms.append((grp, lines, d))
log('(3) THE ROOMS: the dims histogram %s; the content-size histogram %s; the room-reads %d'
    % (dict(sorted(Counter(d for _, _, d in rooms).items())),
       dict(sorted(Counter(len(l) for _, l, _ in rooms).items())),
       sum(len(grp) for grp, _, _ in rooms)))

# ============ (4) THE COVERAGE ============
covered = [0] * V
for grp, lines, d in rooms:
    m = 0
    for s in lines:
        m |= (1 << s)
    for t in grp:
        covered[t] |= m
tail_sizes = []
tails = []
for t in range(V):
    unc = [s for s in range(V) if (PERP[t] >> s) & 1 and not (covered[t] >> s) & 1]
    tail_sizes.append(len(unc))
    tails.append(unc)
log('(4) THE COVERAGE: the tail-size histogram %s; the mean tail %.1f; the zero-tail targets %d'
    % (dict(sorted(Counter(tail_sizes).items())), float(np.mean(tail_sizes)),
       sum(1 for x in tail_sizes if x == 0)))

# ============ (5) THE R ============
n_rooms = len(rooms)
n_tails = sum(1 for x in tail_sizes if x > 0)
R_struct = n_rooms + n_tails + 9
demand = sum(len(grp) for grp, _, _ in rooms) + n_tails
R_hon = max(R_struct, -(-demand // 9))
log('(5) THE R: the rooms %d + the tails %d + the gathers 9 = R_struct %d; the demand %d; R_hon %d (slack %d)'
    % (n_rooms, n_tails, R_struct, demand, R_hon, R_hon - R_struct))

# ============ (6) THE (c)-HIST + THE PRICE ============
def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
# the rooms' chains: [0, the room's frame (the build!!), FULL] — THE READS AT THE BUILD FRAME!!!
for grp, lines, d in rooms:
    for j in jumps([0, d, H]):
        hist[j] += 1
# the tails' chains: [0, the tail's span, FULL]
tail_spans = []
for t in range(V):
    if tail_sizes[t] == 0:
        tail_spans.append(None)
        continue
    sp = span_rank(tails[t])
    tail_spans.append(sp)
    for j in jumps([0, sp, H]):
        hist[j] += 1
# the sources' chains: {s} -> the rooms' frames containing s -> the tails' spans -> FULL!!
src_rooms = {}
for grp, lines, d in rooms:
    for s in lines:
        src_rooms.setdefault(s, set()).add(d)
tail_span_of = {}
for t in range(V):
    if tail_sizes[t] == 0:
        continue
    for s in tails[t]:
        tail_span_of.setdefault(s, set()).add(tail_spans[t])
for s in range(V):
    for j in jumps([1] + sorted(src_rooms.get(s, set()) | tail_span_of.get(s, set())) + [H]):
        hist[j] += 1
# the targets' chains: 0 -> the rooms' dims (the cumulative!!) -> the t-perp (8!!)
tgt_dims = {}
for grp, lines, d in rooms:
    for t in grp:
        tgt_dims.setdefault(t, set()).add(d)
for t in range(V):
    if tail_sizes[t] > 0:
        tgt_dims.setdefault(t, set()).add(tail_spans[t])   # THE TAIL-READ DIM (the SS1589 gate rule!!)
    for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
        hist[j] += 1
# the gathers + the copies (cst = 73!!)
hist[8] += 8; hist[1] += 8; hist[9] += 1
hist[8] += 8; hist[9] += 1
ident = 9 * R_hon + 73 + 2 * V * 8
slack = R_hon - R_struct
LM = sum(r * z * np.log(73.0 / r) for r, z in hist.items() if r < 73)
mass_core = sum(r * z for r, z in hist.items())
log('(6) THE HIST: %s | the mass %d (the core!!); the LM %.0f; the identity at R_hon %d: %d'
    % (dict(sorted(hist.items())), mass_core, LM, R_hon, ident))
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
