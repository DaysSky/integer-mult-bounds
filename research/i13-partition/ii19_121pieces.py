"""THE PARTITION-STRUCTURED PIECE ECONOMY — THE FEASIBILITY SCAN (the SS1679 insight!!).

THE SS1679 WALL: the rooms' contents (the ~37-line FULL common perps!!) give each
source line ~30-50 room memberships (ALL AT DIM-7!!): the sources' ONE-FRAME-PER-DIM
chains CANNOT host them — THE ROOMS' BUILDS ARE ILLEGAL AS-IS.

THE E8'S RESOLUTION (THE SS1679 DERIVATION!!): THE D4 PARTITION = THE SOURCES' FRAME
PARTITION: the 120 roots in the 30 DISJOINT 4-frames; each source's cells ALL INSIDE
ITS ONE 4-FRAME -> the sources' climbs: THE ONE dim-4 frame per source ✓✓✓ NO
COLLISION — **THE PIECES MUST BE PARTITION-STRUCTURED!!!**

THE SCAN (the full E8-style redesign's feasibility!!):
1. THE PARTITION: the 120 roots -> the ~30 disjoint 4-frames (the mutually-orthogonal
   4-sets: the greedy!!) + the special's singleton;
2. THE PIECES: the INSIDE-the-frames subsets (the pairs {l1, l2} (6 per frame!!), the
   triples, the full 4!!): the users (the targets orthogonal to the WHOLE piece!!!):
   the counts + the SAVINGS k*u - (k + u)!!!;
3. THE GREEDY ECONOMY (the best-saving pieces first: the THRESHOLD-sweepable!!);
4. THE COVERAGE: the targets' perps by the pieces + the tails;
5. THE R + THE ARRIVAL + THE (c)-HIST + THE PRICE (the partition-structured chains:
   the pieces' builds at THEIR 4-FRAMES (the sources' ONE frame!!!) + the pieces'
   read-climbs + the tails!!!).
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
TH_SAVE = 4          # the greedy's saving threshold (the sweep-able!!)
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

# ============ (1) THE PARTITION: the 120 roots -> the disjoint 4-frames ============
# the greedy: the mutually-orthogonal 4-sets covering all the 120 roots!!
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
log('(1) THE PARTITION: %d frames; the size histogram %s; the covered %d/120'
    % (len(frames), dict(sorted(Counter(len(f) for f in frames).items())),
       sum(len(f) for f in frames)))
# the special's singleton frame!!
frame_of = {}
for f in frames:
    for x in f:
        frame_of[x] = ('R', tuple(f))
frame_of[120] = ('S', (120,))

# ============ (2) THE PIECES: the inside-the-frames subsets ============
# the candidates: the pairs/triples/quads within each frame (the special: the singleton!!)
# the users: the targets orthogonal to the WHOLE piece!!!
piece_users = {}
for fi, f in enumerate(frames):
    for r in (2, 3, 4):
        for sub in itertools.combinations(f, r):
            mask = PERP[sub[0]]
            for x in sub[1:]:
                mask &= PERP[x]
            users = [t for t in range(V) if t not in sub and (mask >> t) & 1]
            if len(users) >= 2:
                piece_users[sub] = users
log('(2) THE PIECE CANDIDATES: %d; the user-count histogram %s'
    % (len(piece_users), dict(sorted(Counter(len(u) for u in piece_users.values()).items()))))

# ============ (3) THE GREEDY ECONOMY ============
covered = [set() for _ in range(V)]
pool = []          # (piece, users, frame!!)
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
    fr = frame_of[sub[0]][1]
    pool.append((sub, real, fr))
    for t in real:
        covered[t] |= set(sub)
        assigned[t].append(len(pool) - 1)
leftovers = [sorted(set(jlines[t]) - covered[t]) for t in range(V)]
log('(3) THE GREEDY ECONOMY (TH_SAVE=%d): %d pieces; the piece-size histogram %s; the users-per-piece histogram %s'
    % (TH_SAVE, len(pool), dict(sorted(Counter(len(p) for p, _, _ in pool).items())),
       dict(sorted(Counter(len(u) for _, u, _ in pool).items()))))
log('    the coverage: the leftover-size histogram %s; the mean %.1f; the zero %d'
    % (dict(sorted(Counter(len(x) for x in leftovers).items())),
       float(np.mean([len(x) for x in leftovers])),
       sum(1 for x in leftovers if not x)))

# ============ (4) THE R + THE ARRIVAL + THE (c)-HIST + THE PRICE ============
n_tails = sum(1 for x in leftovers if x)
R_struct = len(pool) + n_tails + 9
demand = sum(len(u) for _, u, _ in pool) + n_tails
R_hon = max(R_struct, -(-demand // 9))
log('(4) THE R: the pieces %d + the tails %d + the gathers 9 = R_struct %d; the demand %d (vs 9R = %d: %d%%); R_hon %d (slack %d)'
    % (len(pool), n_tails, R_struct, demand, 9 * R_hon, 100 * demand // max(1, 9 * R_hon),
       R_hon, R_hon - R_struct))

def jumps(ch):
    ch = sorted(set(ch))
    return [b - a for a, b in zip(ch, ch[1:])]
hist = Counter()
# the pieces' chains: [0, the 4-frame's dim (the BUILD: the sources' ONE frame!!!), the read-dims..., 9]
piece_reads = {}
for t in range(V):
    for pid in assigned[t]:
        piece_reads.setdefault(pid, set()).add(4)     # hmm: the read at the dim-4 frame?! — the honest: the reads at the 4-frames (the build-frames!!!) for the first cut!!!
for pid, (sub, users, fr) in enumerate(pool):
    fd = span_rank(list(fr))
    for j in jumps([0, fd] + sorted(piece_reads.get(pid, set())) + [H]):
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
# the sources' chains: {s} -> THE ONE PARTITION FRAME (the dim 4!!!) -> ... -> FULL!!!
for s in range(V):
    fd = span_rank(list(frame_of[s][1]))
    for j in jumps([1, fd, H]):
        hist[j] += 1
# the targets' chains: 0 -> the read-dims (the 4-frames' dim + the tail spans!!) -> 8
tgt_dims = {}
for t in range(V):
    if assigned[t]:
        tgt_dims.setdefault(t, set()).add(4)
    if leftovers[t]:
        tgt_dims.setdefault(t, set()).add(tail_spans[t])
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
