"""THE k=-1 2-CLASS CENSUS (ii19_nat31.py) — a LEGAL h=9 Lorentzian 2-class system.

The 240-line (a,0,0)/(a,1,0) system at h=9 is IMPOSSIBLE (nat182's rank proof: the design Gram
has rank 8; any h=9 realization forces rank 9).  THE FIX: make the level coordinate CONTRIBUTE to
the form: the 9-dim compression B = I8 (+) [-1] (signature (8,1) — LORENTZIAN): the lines
(a, 0) (norm a^2) and (a, 1) (norm a^2 - 1); the class-1 perps: a*b = 1 (the E8 kissing partners!);
the class-0 perps: a*b = 0.  THE CENSUS: legality (the Gram rank 9!!), the perp/junk sizes, the
(2,2) greedy pool + carriers + the R-structure, the price band (the push's A/B/C/D hist family
at the honest R + the ladder).  The question: does the LEGAL h=9 2-class economy sit in the
crossing class?
"""
import sys, time, resource, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // (1024 * 1024)), *a, flush=True)

FRONTIER = 0.001744386
V, H = 240, 9
CST = 144

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
    L.append(list(al) + [0]); CLS.append(0)
for al in AL:
    L.append(list(al) + [1]); CLS.append(1)
L = np.array(L, dtype=float)                 # 240 x 9 (the h=9 lines!!)
B = np.zeros((9, 9)); B[:8, :8] = np.eye(8); B[8, 8] = -1.0
G = L @ B @ L.T
log('(0) the k=-1 system: lines %s | form I8 (+) [-1] (signature (8,1) — LORENTZIAN!!)' % (L.shape,))
log('    det(B) = %.1f | the Gram rank: %d (MUST be 9 for the legal h=9!!)' % (
    np.linalg.det(B), np.linalg.matrix_rank(G)))
assert np.linalg.matrix_rank(G) == 9, 'the legality!!'
n0 = sorted(set(np.diag(G)[:120]))
n1 = sorted(set(np.diag(G)[120:]))
log('    norms: class-0 %s | class-1 %s' % (n0, n1))

PERP = []
for t in range(V):
    m = 0
    for s in range(V):
        if s != t and CLS[s] == CLS[t] and abs(G[s][t]) < 1e-9:
            m |= (1 << s)
    PERP.append(m)
psz = Counter(bin(p).count('1') for p in PERP)
log('(1) the perps: sizes %s' % dict(sorted(psz.items())))

# the canonical k=1 junks + the (2,2) greedy pool (the push's machinery, verbatim)
JUNKS = []
for t in range(V):
    partners = sorted(s for s in range(V) if (PERP[t] >> s) & 1)
    x = partners[0]
    JUNKS.append(PERP[t] ^ (PERP[t] & PERP[x]))
jlines = [[s for s in range(V) if (j >> s) & 1] for j in JUNKS]
log('(2) the junks: mean %.1f lines | sizes %s' % (
    sum(len(j) for j in jlines) / V, dict(sorted(Counter(len(j) for j in jlines).items()))))

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
        users = [ti for ti in pair_junks[(a, b)] if a not in covered[ti] and b not in covered[ti]]
        if len(users) < 2: continue
        common = None
        for ti in users:
            unc = set(jlines[ti]) - covered[ti]
            common = unc if common is None else (common & unc)
        if common is None or len(common) < 2: continue
        piece = frozenset(common)
        real_users = [ti for ti in users if piece <= set(jlines[ti]) - covered[ti]]
        k = len(piece); u = len(real_users)
        if u < 2: continue
        saving = k * u - (k + u)
        if saving <= 0: continue
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
R_struct = len(pool) + carriers + 18
reads_B = sum(len(assigned[ti]) + (1 if leftovers[ti] else 0) for ti in range(V))
log('(3) the (2,2) pool: %d pieces (mean %.1f lines, mean %.1f users) | carriers %d | R = %d + %d + 18 = %d' % (
    len(pool), sum(len(p) for p in pool) / max(1, len(pool)),
    sum(len(us) for us in pool_users) / max(1, len(pool)), carriers, len(pool), carriers, R_struct))
log('    the demand-reads %d vs 9R %d: %s (%.0f%%)' % (
    reads_B, 9 * R_struct, 'FITS' if reads_B <= 9 * R_struct else 'OVER', 100.0 * reads_B / (9 * R_struct)))

# the decoder: the class-blocked perp-pattern blocks' GF(2) rank
def gf2_rank(rows_in):
    rows = list(rows_in); rank = 0
    for col in range(V):
        piv = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if piv is None: continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> col) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank
Brows = [PERP[t] | (1 << t) for t in range(V)]
r0 = gf2_rank([Brows[t] for t in range(120)])
r1 = gf2_rank([Brows[120 + t] for t in range(120)])
log('(4) the decoder: the full rank %d | class-0 block rank %d | class-1 block rank %d' % (
    gf2_rank(Brows), r0, r1))

# the honest gather basis: the rref pivots of the full row space; their spans
rows = list(Brows)
r = 0
pivots = []
for col in range(V):
    piv = next((i for i in range(r, len(rows)) if (rows[i] >> col) & 1), None)
    if piv is None: continue
    rows[r], rows[piv] = rows[piv], rows[r]
    for i in range(len(rows)):
        if i != r and (rows[i] >> col) & 1:
            rows[i] ^= rows[r]
    pivots.append(rows[r])
    r += 1
def span_dim(mask):
    sup = [s for s in range(V) if (mask >> s) & 1]
    return int(np.linalg.matrix_rank(L[sup])) if sup else 0
spans = [span_dim(p) for p in pivots]
log('    the rref basis: %d rows | span hist %s | the sum %d (the naive CST)' % (
    len(pivots), dict(sorted(Counter(spans).items())), sum(spans)))
# better bases?  the codewords are unenumerable (2^53) — the pivot-row spans are the honest
# upper-bound start; the legality note: each gather's frame = a dim-span span with det != 0.

# the threshold tuning (the pool/carriers/R knob)
for COOC, SAVETH in ((3, 4), (3, 3), (2, 3), (2, 2)):
    covered2 = [set() for _ in range(V)]
    assigned2 = [[] for _ in range(V)]
    pool2 = []; pool_users2 = []
    top2 = [(c, k) for k, c in pair_count.items() if c >= COOC]
    while True:
        best = None
        for (c, (a, b)) in top2:
            users = [ti for ti in pair_junks[(a, b)] if a not in covered2[ti] and b not in covered2[ti]]
            if len(users) < 2: continue
            common = None
            for ti in users:
                unc = set(jlines[ti]) - covered2[ti]
                common = unc if common is None else (common & unc)
            if common is None or len(common) < 2: continue
            piece = frozenset(common)
            real = [ti for ti in users if piece <= set(jlines[ti]) - covered2[ti]]
            k2 = len(piece); u2 = len(real)
            if u2 < 2: continue
            sv = k2 * u2 - (k2 + u2)
            if sv <= 0: continue
            if best is None or sv > best[0]: best = (sv, piece, real)
        if best is None or best[0] < SAVETH: break
        _, piece, real = best
        pool2.append(piece); pool_users2.append(real)
        for ti in real:
            covered2[ti] |= set(piece); assigned2[ti].append(len(pool2) - 1)
    lo2 = [set(jlines[ti]) - covered2[ti] for ti in range(V)]
    car2 = sum(1 for x in lo2 if x)
    R2 = len(pool2) + car2 + len(pivots)
    log('    COOC>=%d SAV>=%d: pool %d, carriers %d, gathers %d -> R = %d' % (
        COOC, SAVETH, len(pool2), car2, len(pivots), R2))

R_struct = len(pool) + carriers + len(pivots)
CST_h = sum(spans)
log('(5) THE HONEST STRUCTURE: R = %d + %d + %d = %d | the naive CST %d' % (
    len(pool), carriers, len(pivots), R_struct, CST_h))

def hist_true(R, variant):
    ident = H * R + CST_h + 2 * V * (H - 1)
    climb = 9.0 * R + 2.0 * V * (H - 1)
    cp = dict(Counter(spans))                      # the copy part = the gather-frame span hist!!
    if variant == 'A':
        hist = {1: climb}
    else:
        frac = {1: 0.262, 2: 0.571 / 2.0, 4: 0.048 / 4.0, 5: 0.119 / 5.0}
        hist = {r: f * climb for r, f in frac.items()}
        rem = climb - sum(k * int(v) for k, v in hist.items())
        hist = {k: int(v) for k, v in hist.items()}
        while rem > 0:
            pick = max((k for k in (1, 2, 4, 5) if rem >= k), default=1)
            hist[pick] += 1; rem -= pick
    for k, v in cp.items():
        hist[k] = hist.get(k, 0) + v
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 4, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print()
log('=== THE PRICE BAND (the honest CST %d, the gathers %d) ===' % (CST_h, len(pivots)))
for R in sorted(set([R_struct, 380, 420, 460, 520, 590])):
    if R < R_struct: continue
    line = '  R %3d: ' % R
    for var in ('A', 'B', 'C', 'D'):
        hist = hist_true(R, var)
        cc, _, det = pprice(hist, V, H, R)
        if cc is None:
            line += '%s NO-ROOT  ' % var
        else:
            line += '%s %+.2f%%  ' % (var, (cc / FRONTIER - 1) * 100)
    log(line)
log('DONE')
