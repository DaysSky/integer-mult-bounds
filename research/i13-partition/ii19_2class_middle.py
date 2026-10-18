"""II19 2-CLASS MIDDLE DESIGN — the piece economy for the cancellation junks.
THE SS1317 BAND: the D variant (the R420's own climb proportions, the family that
calibrates PERFECTLY at the control) prices the 2-class word at +4.97% to +6.79% at the
legal floor (R 560-590), crossing back below at R=620.  THE HONEST GATES:
  (a) THE MIDDLE FEASIBILITY: mid = (R-480-18)/2 = 31-46/class assumed; the demands are
      33-line junks with WEAK sharing (240 distinct, overlaps 6.6): whether ~31-46
      pieces/class can serve 120 x 33 = 3,960 line-slots is THE PIECE ECONOMY question;
  (b) the true shape (between A and D): the build decides.
THIS SCRIPT: THE PIECE ECONOMY (the decisive (a)):
  - the piece calculus: a k-line piece used by u targets costs (k + u) arrivals vs k*u
    for direct reads — a piece PAYS iff u > 2 (k=2) / earlier for bigger k;
  - the pool (the piece registers) trades against the arrival budget (A+B arrivals
    <= 9R per the SS1089-1111 law, the E8's own 89% utilization);
  - THE GREEDY: extract the pieces maximizing the arrival saving per pool slot, growing
    pieces by co-occurrence; the singles (the direct reads) as the fallback;
  - THE HONEST MIDDLE: the pool count + the arrival check -> THE TRUE R ->
    THE A/B/C/D PRICE BAND AT THAT R -> THE VERDICT.
RAM-SAFE (the pairs: 240 x 528 = 127k; the greedy over the piece candidates)."""
import sys, time, resource, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V, H = 240, 9
CST = 144

# the 2-class system (as in ii19_2class_true.py)
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
L = []
CLS = []
for al in AL:
    L.append(list(al) + [0, 0]); CLS.append(0)
for al in AL:
    L.append(list(al) + [1, 0]); CLS.append(1)
L = np.array(L, dtype=float)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and CLS[s] == CLS[t] and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
log('2-class system: %d lines; class perps 63' % V)

# the canonical k=1 junks (the counting-bound-legal family, measured at SS1317)
JUNKS = []
for t in range(V):
    partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
    x = partners[0]
    JUNKS.append(PERP[t] ^ (PERP[t] & PERP[x]))
jlines = [[s for s in range(V) if (j >> s) & 1] for j in JUNKS]
log('junks: mean %.1f lines' % (sum(len(j) for j in jlines) / V))

# ============ THE PIECE ECONOMY ============
# the co-occurrence: for each pair {s,s'}, the junks containing both
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    js = set(jl)
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 3]
log('pair candidates (co-occurrence >= 3): %d of %d total pairs; the top counts: %s'
    % (len(top), len(pair_count), sorted((c for c, _ in top), reverse=True)[:12]))

# the greedy piece extraction with the co-occurrence growth:
# state: covered[ti] = the set of junk lines already covered for target ti
covered = [set() for _ in range(V)]
assigned = [[] for _ in range(V)]   # the piece indices assigned to each target
pool = []
pool_users = []
arrival_saving = 0
while True:
    best = None  # (saving, piece_frozenset, real_users)
    for (c, (a, b)) in top:
        # the candidate piece: grow {a,b} by the lines co-occurring in the still-uncovered parts
        users = [ti for ti in pair_junks[(a, b)]
                 if a not in covered[ti] and b not in covered[ti]]
        if len(users) < 2:
            continue
        # the growth: the lines present in ALL the users' uncovered parts (no cap)
        common = None
        for ti in users:
            unc = set(jlines[ti]) - covered[ti]
            common = unc if common is None else (common & unc)
        if common is None or len(common) < 2:
            continue
        piece = frozenset(common)
        # THE FIX: only the users whose UNCOVERED part actually CONTAINS the piece
        real_users = [ti for ti in users if piece <= set(jlines[ti]) - covered[ti]]
        k = len(piece); u = len(real_users)
        if u < 2:
            continue
        saving = k * u - (k + u)   # the arrival saving
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
    arrival_saving += best[0]
# the singles: the direct reads for the uncovered lines
singles = 0
for ti in range(V):
    singles += len(set(jlines[ti]) - covered[ti])
mid = len(pool)
log('THE PIECE ECONOMY: pool %d pieces (the middle registers), sizes mean %.1f max %d'
    % (mid, sum(len(p) for p in pool) / max(1, mid), max((len(p) for p in pool), default=0)))
log('  users per piece: mean %.1f max %d' % (
    sum(len(us) for us in pool_users) / max(1, len(pool)),
    max((len(us) for us in pool_users), default=0)))
log('  uncovered singles (the direct source reads): %d' % singles)
log('  arrival saving vs the all-direct: %d of %d (%.0f%%)'
    % (arrival_saving, sum(len(j) for j in jlines), 100.0 * arrival_saving / max(1, sum(len(j) for j in jlines))))

# the arrival accounting (A+B <= 9R): the honest count via the assignment tracking
reads_B = sum(len(assigned[ti]) + len(set(jlines[ti]) - covered[ti]) for ti in range(V))
builds_A = sum(len(p) for p in pool) + 30 * 18   # the piece builds + the retained gathers
scatter = V
D_gates = V
arrivals = reads_B + builds_A + scatter + D_gates
log('THE ARRIVALS: B-reads %d + A-builds %d + scatter %d + D %d = %d'
    % (reads_B, builds_A, scatter, D_gates, arrivals))

# ============ THE VERDICT BAND AT THE HONEST R ============
R = 480 + mid + 18   # the pool 'mid' is the TOTAL over BOTH classes (the greedy ran over all 240 junks)
log('THE HONEST R: 480 (branches) + %d (the TOTAL piece pool, both classes) + 18 (retained) = %d (R/v %.2f)' % (mid, R, R / V))
cap = 9 * R
log('the arrival capacity 9R = %d: the arrivals %d: %s (%.0f%% utilization)'
    % (cap, arrivals, 'FITS' if arrivals <= cap else 'OVER', 100.0 * arrivals / cap))

def hist_true(R, variant):
    ident = H * R + CST + 2 * V * (H - 1)
    mids = R - 18
    if variant == 'A':
        hist = {1: 3840.0 + 9.0 * R, 8: 18.0}
    elif variant == 'B':
        hist = {1: 2400.0 + 3.0 * mids + 18.0, 2: 720.0 + 3.0 * mids, 8: 36.0}
    elif variant == 'D':
        climb = 9.0 * R + 3840.0
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 8: 18.0}
    else:
        hist = {1: 1200.0 + 18.0, 2: 960.0 + 2.0 * mids, 4: 180.0, 5: 1.0 * mids, 8: 36.0}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE VERDICT BAND AT THE HONEST R = %d ===' % R)
for var in ('A', 'B', 'C', 'D'):
    hist = hist_true(R, var)
    cc, _, det = pprice(hist, V, H, R)
    if cc is None:
        log('  R %d %s: NO ROOT' % (R, var))
    else:
        pct = (cc / FRONTIER - 1) * 100
        log('  R %d %s: c = %.9f (%+.2f%% vs frontier)' % (R, var, cc, pct))
log('DONE')