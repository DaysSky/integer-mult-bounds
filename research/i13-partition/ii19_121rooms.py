"""THE ROOM MEASUREMENT (the user's SS1601 'no keep pushing'!!; the SS1604 gate: the target-side nesting SOLVED!!).

THE SS1589 GCHECK RULE: ALL the operands (the dest AND the srcs!!) climb to the GATE'S
frame — so the PIECE'S READ FRAMES MUST BE SHARED BY ITS DIM-GROUPS OF USERS (ONE
FRAME PER DIM PER CHAIN!!!).  At each dim d: the reads (t, p) at the slot d form the
bipartite graph; the CONNECTED COMPONENTS = THE ROOMS (the shared dim-d frames!!).

THE ROOM FRAME'S EXISTENCE (THE DECISIVE FIRST GATE!!): each room R needs ONE shared
dim-d frame:
  (1) rank(∪ R's pieces) <= d (the cumulative packing's own check!!);
  (2) ∪ R's pieces ⊆ THE COMMON PERP of ALL R's targets — i.e., EVERY line of every
      piece in R must be ORTHOGONAL to EVERY target in R (the room's frame sits inside
      each member's chain, which ends at the t-perp: R ⊆ t-perp for every member t!!!).
(2) IS THE NEW, DECISIVE CHECK: a piece only guaranteed ⊥ its OWN users; a room merges
targets via shared pieces, so the transitive closure can pull in pieces NOT ⊥ some
member — the room then has NO legal frame -> the reads must be RE-SLOTTED (a different
dim assignment / smaller rooms!!).

THE MEASUREMENT: at the crossing THs (8, 16, 24 — the SS1594 fine-slack +2.32% to
+15.41%!!): per dim: the rooms' count, the room sizes (the pieces + the targets!!),
the PERP-FAILURES (the rooms whose pieces' union is not inside the common perp!!),
and the re-slot options (the failing rooms' pieces: their alternative dims!!!).
"""
import sys, time, itertools
from collections import Counter
import numpy as np

V, H = 121, 9
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

pair_count = Counter(); pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        pair_count[(a, b)] += 1
        pair_junks.setdefault((a, b), []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 4]

def find(dsu, x):
    while dsu[x] != x:
        dsu[x] = dsu[dsu[x]]; x = dsu[x]
    return x
def union(dsu, a, b):
    ra, rb = find(dsu, a), find(dsu, b)
    if ra != rb:
        dsu[ra] = rb

log('TH | per dim: the rooms, the perp-FAILS | the room sizes (pieces x targets)!!')
for TH in (8, 16, 24):
    covered = [set() for _ in range(V)]; assigned = [[] for _ in range(V)]
    pool = []; pool_users = []
    while True:
        best = None
        for (c, (a, b)) in top:
            users = [ti for ti in pair_junks[(a, b)] if a not in covered[ti] and b not in covered[ti]]
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
        if best is None or best[0] < TH:
            break
        _, piece, real_users = best
        pool.append(piece); pool_users.append(real_users)
        for ti in real_users:
            covered[ti] |= set(piece); assigned[ti].append(len(pool) - 1)
    leftovers = [sorted(set(jlines[ti]) - covered[ti]) for ti in range(V)]
    pranks = [span_rank(sorted(p)) for p in pool]
    # the cumulative packing (the SS1604!!) -> the slot per (t, p)
    tgt_slot = {}
    for ti in range(V):
        items = [(pid, pranks[pid]) for pid in assigned[ti]]
        if leftovers[ti]:
            items.append((-1, span_rank(leftovers[ti])))
        items.sort(key=lambda x: -x[1])
        cum = {d: [] for d in range(2, 9)}
        for pid, r in items:
            lines = sorted(pool[pid]) if pid >= 0 else leftovers[ti]
            for d in range(max(2, r), 9):
                if span_rank(cum[d] + lines) <= d:
                    for d2 in range(d, 9):
                        cum[d2] = cum[d2] + lines
                    tgt_slot[(ti, pid)] = d
                    break
    # ============ THE ROOMS: the connected components per dim ============
    fails = 0; room_sizes = Counter(); per_dim = {}
    for d in range(2, 9):
        reads = [(t, p) for (t, p), dd in tgt_slot.items() if dd == d]
        nodes = {}
        for t, p in reads:
            nodes[('t', t)] = True
            nodes[('p', p) if p >= 0 else ('tail', t)] = True
        dsu = {n: n for n in nodes}
        for t, p in reads:
            union(dsu, ('t', t), ('p', p) if p >= 0 else ('tail', t))
        rooms = {}
        for n in nodes:
            rooms.setdefault(find(dsu, n), []).append(n)
        n_fail_d = 0; d_sizes = []
        for r, members in rooms.items():
            ts = [m[1] for m in members if m[0] == 't']
            ps = [m[1] for m in members if m[0] == 'p']
            tls = [m[1] for m in members if m[0] == 'tail']
            # the common perp of the room's targets:
            cp = PERP[ts[0]]
            for t in ts[1:]:
                cp &= PERP[t]
            union_lines = set()
            for p in ps:
                union_lines |= set(pool[p])
            for t in tls:
                union_lines |= set(leftovers[t])
            ok = all((cp >> s) & 1 for s in union_lines)
            if not ok:
                n_fail_d += 1
                fails += 1
            d_sizes.append((len(ps) + len(tls), len(ts), ok))
        per_dim[d] = (len(rooms), n_fail_d)
        for np_, nt_, ok in d_sizes:
            room_sizes[(np_, nt_, ok)] += 1
    log('TH=%d: %s | TOTAL PERP-FAILS %d | the room sizes (pieces, targets, ok) %s'
        % (TH, {d: per_dim[d] for d in range(2, 9)}, fails,
           sorted(room_sizes.items())))
log('DONE')
