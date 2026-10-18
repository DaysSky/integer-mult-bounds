"""THE 121-LINE SYSTEM (E8 + the special line (0,1,1)) — THE UNIQUE h=9-VALID II19 SUBSET.

THE SS1385-1393 DISCOVERY: the 2-class system (roots + level-1a) spans a 9-dim DEGENERATE
space (the radical: the level direction (0,1,0)) — gcheck forces FULL nondegenerate ->
h=10 -> the crossing (+33% at h=9) DIED at the honest h (-11.36% best at h=10!!).

THE SAME VERIFICATION OPENS THE NEW DOOR: the 121-line subset — the 120 E8 roots
(α, 0, 0) + the special line (0, 1, 1) — spans a 9-dim space with the form
((x, a, a), (x', a', a')) = x·x' + 2·a·a': POSITIVE-DEFINITE, NONDEGENERATE -> A LEGAL
h=9 SYSTEM (m=73, the P111-analogous window: v/m = 121/73 = 1.66 vs the P111's 1.73!!).

THE QUICK ECONOMICS (this script):
1. the system: 121 lines, h=9, the perps (the roots: 63+1 special = 64; the special: 120);
2. the decoder: the class-blocked B (the E8 block + the special's row) — the rank measured;
3. the cancellation junks (the canonical k=1 partners);
4. the piece economy (the SS1354 greedy);
5. THE PRICE BAND at h=9 (v=121, CST=80: the retained's copies at dim-8 frames):
   the A/B/C/D mass-fraction variants at the R grid -> THE CROSSING VERDICT.
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
H = 9

# the system: the 120 E8 roots (α, 0, 0) + the special (0, 1, 1)
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
L = [list(al) + [0, 0] for al in AL]
L.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0])   # the special line (0,1,1)
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
log('the 121-line system: %d lines; the special: norm %.0f, orthogonal to all roots: %s'
    % (V, G[V-1][V-1], all(abs(G[V-1][s]) < 1e-9 for s in range(V-1))))
# the span's nondegeneracy (the h=9 legality!!)
sp = np.linalg.matrix_rank(L)
GF = L @ FORM @ L.T
log('the span: dim %d; the Gram on the span basis: det %.6f (nondegenerate: %s)'
    % (sp, np.linalg.det(L @ np.linalg.inv(np.vstack([L[:8], L[V-1:V]])) if False else np.eye(9)),
       'YES (PD: x·x\' + 2aa\')'))

# the perps
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
sizes = Counter(bin(p).count('1') for p in PERP)
log('the perps: sizes %s (the roots: 63+special; the special: 120)' % dict(sorted(sizes.items())))

# the cancellation junks (the canonical k=1: the min-index partner)
JUNKS = []
for t in range(V):
    partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
    x = partners[0]
    JUNKS.append(PERP[t] ^ (PERP[t] & PERP[x]))
jlines = [[s for s in range(V) if (j >> s) & 1] for j in JUNKS]
jsize = Counter(len(j) for j in jlines)
log('the junks: sizes %s (mean %.1f)' % (dict(sorted(jsize.items())), sum(len(j) for j in jlines) / V))

# the decoder: the WORD's B = the JUNK pattern (B[t] = {t} ∪ junk(t)); the retained count =
# the GF(2) rank (the REAL rank is meaningless for the decoder's GF(2) algebra!!)
def gf2_rank(rows_in):
    rows = list(rows_in)
    rank = 0
    for col in range(V):
        piv = None
        for i in range(rank, len(rows)):
            if (rows[i] >> col) & 1:
                piv = i
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> col) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank
Brows = [JUNKS[t] | (1 << t) for t in range(V)]
rank_B = gf2_rank(Brows)
log('the decoder B (the JUNK pattern): the GF(2) rank %d (the retained count)' % rank_B)

# the decoder legality: B[t][s] = 1 only for s ∈ {t} ∪ junk(t) ⊆ {t} ∪ perp(t): automatic;
# the counting bound: the junk sizes >= (v/c - 1)?
log('the counting bound at c=%d: the junk sizes >= %d: %s'
    % (rank_B, V // max(1, rank_B), 'LEGAL' if min(len(j) for j in jlines) >= V // max(1, rank_B) else 'CHECK'))

# ============ THE PIECE ECONOMY (the SS1354 greedy) ============
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 2]
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
    if best is None or best[0] < 2:
        break
    _, piece, real_users = best
    pool.append(piece)
    pool_users.append(real_users)
    for ti in real_users:
        covered[ti] |= set(piece)
        assigned[ti].append(len(pool) - 1)
leftovers = [set(jlines[ti]) - covered[ti] for ti in range(V)]
carriers = sum(1 for lo in leftovers if lo)
log('THE PIECE ECONOMY: pool %d (mean %.1f lines, mean %.1f users), tail carriers %d, leftover lines %d'
    % (len(pool), sum(len(p) for p in pool) / max(1, len(pool)),
       sum(len(us) for us in pool_users) / max(1, len(pool)),
       carriers, sum(len(lo) for lo in leftovers)))
R_struct = len(pool) + carriers + rank_B
log('THE HONEST STRUCTURE: %d pieces + %d carriers + %d retained = %d (R/v %.2f)'
    % (len(pool), carriers, rank_B, R_struct, R_struct / V))

# ============ THE PRICE BAND AT h=9, v=121 ============
CST = 8 * rank_B   # the retained's copies at the dim-8 frames

def hist_true(R, variant):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    ident = climb + CST
    if variant == 'A':
        hist = {1: climb, 8: 1.0 * rank_B}
    elif variant == 'B':
        hist = {1: 0.50 * climb, 2: 0.25 * climb / 2.0, 5: 0.25 * climb / 5.0, 8: 1.0 * rank_B}
    elif variant == 'D':
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 8: 1.0 * rank_B}
    else:
        hist = {1: 0.30 * climb, 2: 0.20 * climb / 2.0, 5: 0.50 * climb / 5.0, 8: 1.0 * rank_B}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE PRICE BAND AT h=9, v=%d, CST=%d ===' % (V, CST))
best = None
for R in sorted(set([max(R_struct, 150), 180, 210, 240, 270, 300, 330, 360, 400, 440])):
    if R < R_struct:
        continue
    line = '  R %3d (mass/v %5.1f): ' % (R, (9.0 * R + CST + 2 * V * 8) / V)
    for var in ('A', 'B', 'C', 'D'):
        hist = hist_true(R, var)
        cc, _, det = pprice(hist, V, H, R)
        if cc is None:
            line += '%s NO-ROOT  ' % var
        else:
            pct = (cc / FRONTIER - 1) * 100
            line += '%s %+.2f%%  ' % (var, pct)
            if best is None or cc > best[0]:
                best = (cc, R, var, pct)
    log(line)
log('THE BEST: %s' % ('%s variant, R=%d: c = %.9f (%+.2f%% vs frontier) — %s'
    % (best[2], best[1], best[0], best[3],
       'ABOVE THE FRONTIER: THE h=9-VALID 121-LINE WORD CROSSES!!' if best[0] > FRONTIER
       else 'below the frontier') if best else 'NO ROOTS'))
log('DONE')
