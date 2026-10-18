"""II19 2-CLASS PUSH — the honest R composition + the threshold-tuned pool + the price grid.

THE USER DIRECTIVE (SS1349): dont try to disprove II19, PUSH it.  THE CONSTRUCTIVE PROGRAM:

- THE SS1331 'R = 480 + mid + 18' ADDED 480 BRANCHES BY CONVENTION (the E8 cell-machinery
  carriers).  But the piece-word builds its pieces DIRECTLY FROM THE SOURCES (the A-phase:
  the helpers read the sources — the identity-word precedent, gcheck-PASS at SS1240!!).
  NO PER-LINE CARRIERS ARE STRUCTURALLY NEEDED.  The honest structure:
      R_struct = the pieces (the shared pool) + the tail carriers (the per-target leftovers)
                 + the retained (the 18 class gathers).
- THE NATURAL KNOB: the greedy's saving threshold -> the pool size -> THE R.  The finer
  pool (threshold 2-3): more, smaller pieces: the singles absorbed: the structure grows
  toward the price-optimal zone with NO empty slack needed.
- THE PRICE GRID at the honest structures + the slack points: the A/B/C/D variants
  (the D = the R420's OWN climb proportions — the family that calibrates at the control
  to 15 digits!!).  THE SS1317 CROSSING: D at R = 560/573/590 prices +4.97/+5.35/+6.79%.
- THE ARRIVAL LAW (the E8-precedent scope: the B-PHASE DEMAND READS — the E8's own
  3,000 = 25/line is the B-phase!!): the demand-reads <= 9 * R.
"""
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

# the 2-class system (verbatim from ii19_2class_middle.py)
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

# the canonical k=1 junks (the SS1317 family)
JUNKS = []
for t in range(V):
    partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
    x = partners[0]
    JUNKS.append(PERP[t] ^ (PERP[t] & PERP[x]))
jlines = [[s for s in range(V) if (j >> s) & 1] for j in JUNKS]
log('junks: mean %.1f lines' % (sum(len(j) for j in jlines) / V))

# the pair co-occurrence tables (once)
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    js = set(jl)
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
log('pair tables: %d total pairs' % len(pair_count))

def greedy_pool(COOC, SAVETH):
    """the SS1331 greedy (the full-common growth + the real_users filter), threshold-tuned"""
    top = [(c, k) for k, c in pair_count.items() if c >= COOC]
    covered = [set() for _ in range(V)]
    assigned = [[] for _ in range(V)]
    pool = []
    pool_users = []
    while True:
        best = None
        for (c, (a, b)) in top:
            users = [ti for ti in pair_junks[(a, b)]
                     if a not in covered[ti] and b not in covered[ti]]
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
        if best is None or best[0] < SAVETH:
            break
        _, piece, real_users = best
        pool.append(piece)
        pool_users.append(real_users)
        for ti in real_users:
            covered[ti] |= set(piece)
            assigned[ti].append(len(pool) - 1)
    return pool, pool_users, covered, assigned

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
log('=== THE THRESHOLD TABLE: the honest structures ===')
results = []
for COOC, SAVETH in ((3, 4), (3, 3), (2, 3), (2, 2)):
    pool, pool_users, covered, assigned = greedy_pool(COOC, SAVETH)
    leftovers = [set(jlines[ti]) - covered[ti] for ti in range(V)]
    carriers = sum(1 for lo in leftovers if lo)
    singles = sum(len(lo) for lo in leftovers)
    R_struct = len(pool) + carriers + 18
    # the demand-reads (the B-phase only — the E8-precedent scope): the piece-reads + one read
    # per target with a leftover tail carrier
    reads_B = sum(len(assigned[ti]) + (1 if leftovers[ti] else 0) for ti in range(V))
    cap = 9 * R_struct
    log('COOC>=%d SAV>=%d: pool %d (mean %.1f lines, mean %.1f users, max u %d), '
        'carriers %d, leftover lines %d'
        % (COOC, SAVETH, len(pool),
           sum(len(p) for p in pool) / max(1, len(pool)),
           sum(len(us) for us in pool_users) / max(1, len(pool)),
           max((len(us) for us in pool_users), default=0),
           carriers, singles))
    log('  THE STRUCTURE: %d + %d + 18 = %d (R/v %.2f); the demand-reads %d vs 9R %d: %s (%.0f%%)'
        % (len(pool), carriers, R_struct, R_struct / V, reads_B, cap,
           'FITS' if reads_B <= cap else 'OVER', 100.0 * reads_B / cap))
    # THE PRICE GRID: the structure + the ladder to 620
    grid = sorted(set([R_struct] + [430, 460, 490, 520, 550, 560, 573, 590, 605, 620]))
    log('  THE PRICE GRID:')
    for R in grid:
        if R < R_struct:
            continue
        line = '    R %3d: ' % R
        for var in ('A', 'B', 'C', 'D'):
            hist = hist_true(R, var)
            cc, _, det = pprice(hist, V, H, R)
            if cc is None:
                line += '%s NO-ROOT  ' % var
            else:
                pct = (cc / FRONTIER - 1) * 100
                line += '%s %+.2f%%  ' % (var, pct)
                results.append((pct, COOC, SAVETH, R, var, cc))
        log(line)
    print()

results.sort(reverse=True)
log('=== THE VERDICT ===')
if not results:
    log('NO ROOTS ANYWHERE — the regimes too light at every threshold')
else:
    for pct, COOC, SAVETH, R, var, cc in results[:8]:
        tag = ' <== THE CROSSING' if pct > 0 else ''
        log('  %.2f%% at (COOC>=%d SAV>=%d, R=%d, variant %s): c = %.9f%s'
            % (pct, COOC, SAVETH, R, var, cc, tag))
    best = results[0]
    log('THE BEST: %+.2f%% at R=%d (%s) — %s'
        % (best[0], best[3], best[4],
           'ABOVE THE FRONTIER: the crossing is ALIVE' if best[0] > 0
           else 'below the frontier'))
log('DONE')
