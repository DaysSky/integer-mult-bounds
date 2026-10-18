"""THE 121-LINE SYSTEM v2 — the honest DEMAND/DECODER CONSISTENCY (one family!).

THE SS1402 LESSON: the min-index cancellation junks (33/57 lines) give the junk-pattern B
the GF(2) rank 114 — the decoder would need 114 retained (CST 912!!) -> NO ROOTS: DEAD.

THE CONSISTENT FAMILY (a): THE PERP-PATTERN DECODER: B[t] = {t} ∪ perp(t):
  - the junks = the perps (64 lines for the roots: 63 + the special; 120 for the special):
    the heavy-but-natural demands — THE R420'S OWN FAMILY (the E8's demands are the full
    63-line perps with the rank-9 B0 decoder!!!);
  - the GF(2) rank: the E8 block (9) + the special's row: ~10 (THE MEASUREMENT);
  - the CST: 8 x rank ~ 80;
  - THE PIECE ECONOMY for the 64/120-line demands (the SS1331 greedy, COOC>=4):
    the E8-transplant middle — AND THE SPECIAL'S 120-LINE DEMAND RIDES NEARLY FREE
    (every root-piece ⊆ the special's junk: the special is a user of every piece!!).
THE PRICE BAND at h=9 (v=121, m=73: the P111-analogous window!!) -> THE VERDICT.
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
L.append([0.0] * 8 + [1.0, 1.0])   # the special line (0,1,1)
L = np.array(L, dtype=float)
V = len(L)
FORM = np.zeros((10, 10)); FORM[:8, :8] = np.eye(8); FORM[8, 9] = FORM[9, 8] = 1.0
G = L @ FORM @ L.T
log('the 121-line system: %d lines (h=9 legal: the PD span)' % V)

# the perps
PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
sizes = Counter(bin(p).count('1') for p in PERP)
log('the perps: sizes %s' % dict(sorted(sizes.items())))

# ============ THE CONSISTENT FAMILY: THE PERP-PATTERN DECODER ============
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
Brows = [PERP[t] | (1 << t) for t in range(V)]
rank_B = gf2_rank(Brows)
log('THE PERP-PATTERN DECODER: the GF(2) rank %d (the retained count; the E8 block 9 + the special\'s row)' % rank_B)

# the demands: the junks = the perps (the B-rows off the diagonal)
jlines = [[s for s in range(V) if (PERP[t] >> s) & 1] for t in range(V)]
log('the demands (the perp-junks): mean %.1f lines (64 for the roots; 120 for the special)' % (sum(len(j) for j in jlines) / V))

# ============ THE PIECE ECONOMY (the SS1331 greedy, COOC>=4) ============
pair_count = Counter()
pair_junks = {}
for ti, jl in enumerate(jlines):
    for a, b in itertools.combinations(sorted(jl), 2):
        key = (a, b)
        pair_count[key] += 1
        pair_junks.setdefault(key, []).append(ti)
top = [(c, k) for k, c in pair_count.items() if c >= 4]
log('pair tables: %d total pairs; %d candidates (co-occurrence >= 4)' % (len(pair_count), len(top)))

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
    if best is None or best[0] < 4:
        break
    _, piece, real_users = best
    pool.append(piece)
    pool_users.append(real_users)
    for ti in real_users:
        covered[ti] |= set(piece)
        assigned[ti].append(len(pool) - 1)
leftovers = [set(jlines[ti]) - covered[ti] for ti in range(V)]
carriers = sum(1 for lo in leftovers if lo)
log('THE PIECE ECONOMY: pool %d (mean %.1f lines, mean %.1f users, max u %d), tail carriers %d, leftover lines %d'
    % (len(pool), sum(len(p) for p in pool) / max(1, len(pool)),
       sum(len(us) for us in pool_users) / max(1, len(pool)),
       max((len(us) for us in pool_users), default=0),
       carriers, sum(len(lo) for lo in leftovers)))
# the special's coverage check (the rides-free claim!!)
log('  the special (target %d): covered %d of its %d demand lines by the pieces; leftover %d'
    % (V - 1, len(jlines[V-1]) - len(leftovers[V-1]), len(jlines[V-1]), len(leftovers[V-1])))
R_struct = len(pool) + carriers + rank_B
log('THE HONEST STRUCTURE: %d pieces + %d carriers + %d retained = %d (R/v %.2f)'
    % (len(pool), carriers, rank_B, R_struct, R_struct / V))

# ============ THE PRICE BAND AT h=9, v=121 ============
CST = 9 * rank_B   # THE HONEST: the gathers' content spans dim-9 -> their frames = FULL -> the copy ranks 9 (SS1438!!)

def hist_true(R, variant):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    ident = climb + CST
    if variant == 'A':
        hist = {1: climb, 9: 1.0 * rank_B}
    elif variant == 'B':
        hist = {1: 0.50 * climb, 2: 0.25 * climb / 2.0, 5: 0.25 * climb / 5.0, 9: 1.0 * rank_B}
    elif variant == 'D':
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 9: 1.0 * rank_B}
    else:
        hist = {1: 0.30 * climb, 2: 0.20 * climb / 2.0, 5: 0.50 * climb / 5.0, 9: 1.0 * rank_B}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE PRICE BAND AT h=9, v=%d, CST=%d (the P111-analogous window!!) ===' % (V, CST))
best = None
grid = sorted(set([R_struct, max(R_struct, 200), 250, 300, 350, 400, 440, 480, 520]))
for R in grid:
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
