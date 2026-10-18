"""THE ROOM-FIRST DESIGN — THE DIM-TARGETED CLUSTERING v4 (the SS1657 stuck-dim fix!!).

THE SS1657 FAILURE MECHANISM: the growth's c-selection maximizes the resulting common
perp (n2!!) — the winners are the CP-PRESERVERS (the c's orthogonal to the WHOLE current
common perp: the ⊥-complement's lines!!): they add members WITHOUT shrinking the room ->
THE DIM GETS STUCK AT 7 -> the fresh check never passes -> the growth exhausts -> 7,197
rejects -> the 112 targets with ONE room each (the degenerate +36.81% structure!!).

THE v4 FIXES:
1. THE DIM-TARGETED GROWTH: the c-candidates must (a) keep the content >= TH_ROOM,
   (b) MOVE the dim (d2 != d: the strict droppers — the cp-preservers SKIPPED!!!),
   (c) land on a dim FRESH for ALL the members (the grp + c!!) — the best by content;
2. THE FAST PATH: the room's dim d = 9 - span_rank(grp) (the common perp = the
   ⊥-complement of the group's span: VERIFIED against SS1649/SS1657 (the pair: 9-2=7;
   the 13-group: 9-5=4!!) — the span_rank of the ~2-5 GROUP lines instead of the
   ~37 room lines: the cheap + cached!!!).

THE MEASUREMENT: the same as SS1649 (the rooms/coverage/R/hist/price!!) + the
per-target dim-diversity report (the CHAIN-BUDGET SOLVED BY CONSTRUCTION?!).
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
    """THE FAST PATH: the room's dim = 9 - span_rank(grp) (the ⊥-complement!!)."""
    return H - span_rank(grp)

# ============ THE DIM-TARGETED GREEDY v4 ============
cand = []
for a, b in itertools.combinations(range(V), 2):
    n = bin(PERP[a] & PERP[b]).count('1')
    if n >= TH_ROOM:
        cand.append((n, a, b))
cand.sort(key=lambda x: -x[0])
log('the pairs with the common perp >= %d: %d' % (TH_ROOM, len(cand)))
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
            break          # THE STOPPING: the first fresh dim!!!
        best_c = None; best_n = -1; best_d2 = None
        for c in range(V):
            if c in grp or len(tgt_dims_used[c]) >= 7:
                continue
            cp2 = cp & PERP[c]
            n2 = bin(cp2).count('1')
            if n2 < TH_ROOM:
                continue                       # (a) the content >= 12!!
            d2 = room_dim(grp + [c])
            if d2 == d:
                continue                       # (b) THE DIM-MOVERS ONLY (the cp-preservers SKIPPED!!!)
            if any(d2 in tgt_dims_used[t] for t in grp + [c]):
                continue                       # (c) the FRESH dim for ALL!!!
            if n2 > best_n:
                best_n = n2; best_c = c; best_d2 = d2
        if best_c is None:
            break            # the growth exhausted: no fresh-dim mover -> the reject!!
        grp.append(best_c); cp &= PERP[best_c]; d = best_d2
    if not fresh or d == 0:
        n_reject += 1
        continue
    lines = [s for s in range(V) if (cp >> s) & 1]
    groups.append((grp, lines, d))
    for t in grp:
        tgt_dims_used[t].add(d)
log('(2) THE DIM-TARGETED CLUSTERS: %d groups (the rejects %d!!); the group-size histogram %s'
    % (len(groups), n_reject, dict(sorted(Counter(len(g) for g, _, _ in groups).items()))))
div_counts = Counter(len(s) for s in tgt_dims_used.values())
log('    the per-target dim-diversity: %s; the dims-at-target histogram %s'
    % (dict(sorted(div_counts.items())),
       dict(sorted(Counter(d for s in tgt_dims_used.values() for d in s).items()))))
log('    the room dims histogram %s; the room content-size histogram %s'
    % (dict(sorted(Counter(d for _, _, d in groups).items())),
       dict(sorted(Counter(len(l) for _, l, _ in groups).items()))))

# ============ THE ROOMS / COVERAGE / R / HIST / PRICE [the SS1645 code!!] ============
rooms = groups
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
log('(4) THE COVERAGE: the tail-size histogram %s; the mean tail %.1f; the zero-tail %d'
    % (dict(sorted(Counter(tail_sizes).items())), float(np.mean(tail_sizes)),
       sum(1 for x in tail_sizes if x == 0)))
n_rooms = len(rooms)
n_tails = sum(1 for x in tail_sizes if x > 0)
R_struct = n_rooms + n_tails + 9
demand = sum(len(grp) for grp, _, _ in rooms) + n_tails
R_hon = max(R_struct, -(-demand // 9))
log('(5) THE R: the rooms %d + the tails %d + the gathers 9 = R_struct %d; the demand %d; R_hon %d (slack %d)'
    % (n_rooms, n_tails, R_struct, demand, R_hon, R_hon - R_struct))

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
for grp, lines, d in rooms:
    for j in jumps([0, d, H]):
        hist[j] += 1
tail_spans = []
for t in range(V):
    if tail_sizes[t] == 0:
        tail_spans.append(None)
        continue
    sp = span_rank(tails[t])
    tail_spans.append(sp)
    for j in jumps([0, sp, H]):
        hist[j] += 1
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
tgt_dims = {}
for grp, lines, d in rooms:
    for t in grp:
        tgt_dims.setdefault(t, set()).add(d)
for t in range(V):
    if tail_sizes[t] > 0:
        tgt_dims.setdefault(t, set()).add(tail_spans[t])   # THE TAIL-READ DIM (the SS1589 gate rule!!)
    for j in jumps([0] + sorted(tgt_dims.get(t, set())) + [8]):
        hist[j] += 1
hist[8] += 8; hist[1] += 8; hist[9] += 1
hist[8] += 8; hist[9] += 1
ident = 9 * R_hon + 73 + 2 * V * 8
slack = R_hon - R_struct
LM = sum(r * z * np.log(73.0 / r) for r, z in hist.items() if r < 73)
log('(6) THE HIST: %s | the mass %d (the core!!); the LM %.0f; the identity at R_hon %d: %d'
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
