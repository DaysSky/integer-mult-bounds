"""THE NESTING-AWARE TARGET-SIDE PACKING (the user's SS1601: 'no keep pushing'!!).

THE SS1589 GCHECK RULE: every operand's current frame MUST be a SUBSPACE of the gate's
frame and climbs up paying the jump — THE CHAINS ARE FLAGS (nested increasing frames!!).
THE SS1515 AUDIT: the slots.py packing treats the slots as INDEPENDENT BINS -> 121/121
target chains CANNOT NEST -> unrealizable as-is!!

THE FIX — THE CUMULATIVE DESIGN: F_d = span(the items at the dims <= d) (+ the fillers to
reach dim d!!): the AUTOMATIC NESTING (the cumulative unions are increasing by
construction!!).  THE PACKING CONSTRAINT: for each dim d: rank(cumulative union at d)
<= d.  The overlaps between pieces make this much looser than the additive bound; all
items live inside the dim-8 t-perp, so the tail fits at dim 8 automatically.

THE MEASUREMENT: at the crossing THs (8, 16, 24 — the SS1594 fine-slack +2.32% to
+15.41%!!): the cumulative packing's UNPLACED count (the feasibility!!) + the slot
loads.  IF FEASIBLE: the target-side nesting is SOLVED (the cumulative design!!) and
the source-side (the pieces' build frames + the tail-spans: the flag design with the
fillers!!) is the next gate.
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

log('TH | pool carriers | THE CUMULATIVE PACKING: unplaced | the slot loads')
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
    # ============ THE NESTING-AWARE (CUMULATIVE!!) TARGET-SIDE PACKING ============
    unplaced = 0; slot_h = Counter(); item_h = Counter()
    for ti in range(V):
        items = [(pid, pranks[pid]) for pid in assigned[ti]]
        if leftovers[ti]:
            items.append((-1, span_rank(leftovers[ti])))
        items.sort(key=lambda x: -x[1])
        cum = {d: [] for d in range(2, 9)}     # the CUMULATIVE unions per dim!!
        placed_n = 0
        for pid, r in items:
            lines = sorted(pool[pid]) if pid >= 0 else leftovers[ti]
            okd = None
            for d in range(max(2, r), 9):
                if span_rank(cum[d] + lines) <= d:
                    okd = d
                    break
            if okd is None:
                unplaced += 1
            else:
                for d2 in range(okd, 9):
                    cum[d2] = cum[d2] + lines   # the cumulative update (the nesting!!)!!
                slot_h[okd] += 1
                placed_n += 1
        item_h[placed_n] += 1
    log('TH=%d | %d pool, %d carr | UNPLACED %d | the slots %s | the placed-per-target %s'
        % (TH, len(pool), sum(1 for lo in leftovers if lo), unplaced,
           dict(sorted(slot_h.items())), dict(sorted(item_h.items()))))
log('DONE')
