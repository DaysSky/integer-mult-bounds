"""II19 COORDINATED TILING — the decisive v3 measurement.
Carrier census: tilings EXIST (30/30 exact, ~8 tiles/piece of size 2-6), naive pool 52,737
(too big), but per-piece tilings need few tiles and reuse material is rich (mean 22x).
THIS: coordinated tiling over all 2,375 pieces — greedy per piece (largest first, tiles
must be disjoint from covered), STRONGLY preferring already-used tiles.  Leftover single
lines are free source-line reads (work only, no registers).
Decisive output: distinct tile pool.  Target <= ~3,000 -> middle = tiles, R under budget."""
import sys, time, itertools, resource, pickle
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8, dtype=int); v[i] = si; v[j] = sj
                roots.append(v)
half = [np.array(s, dtype=float) / 2 for s in itertools.product([1, -1], repeat=8) if s.count(-1) % 2 == 0]
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
lines8 = {}
for r in list(roots) + half: lines8[canon(r)] = r
R8 = list(lines8.values())
L = []
for al in R8:
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
L.append((None, 1, 1))
n = len(L)
coords = [list(al) + [a, b] if al is not None else [0.0] * 8 + [a, b] for al, a, b in L]
LA = np.array(coords)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    gg = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return gg + a1 * b2 + b1 * a2
Gm = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
Zint_row = [sum(1 << k for k in range(n) if Z[i, k]) for i in range(n)]
log('system: %d lines' % n)

pair_flat = {}
for i in range(n):
    for j in range(i + 1, n):
        m = Zint_row[i] & Zint_row[j]
        flat = (1 << n) - 1
        mm = m
        while mm:
            b = mm & -mm
            flat &= Zint_row[b.bit_length() - 1]
            mm ^= b
        pair_flat[(i, j)] = flat
log('rank-2 flat table: %d pairs' % len(pair_flat))

d = pickle.load(open('ii19_design.pkl', 'rb'))
use_count = d['use_count']
pieces = list(use_count.keys())
ct_total = d['ct_total']
pieces.sort(key=lambda F: -bin(F).count('1'))  # largest first: they set the vocabulary
log('pieces: %d (largest first)' % len(pieces))

tile_use = {}       # tile mask -> reuse count
tile_reads = 0      # total tile uses
singleton_reads = 0 # free source-line reads
fails = 0
for pi, F in enumerate(pieces):
    lines = [k for k in range(n) if F >> k & 1]
    cands = set()
    for a_i in range(len(lines)):
        for b_i in range(a_i + 1, len(lines)):
            fm = pair_flat.get((lines[a_i], lines[b_i]))
            if fm is not None and not (fm & ~F):
                cands.add(fm)
    covered = 0
    while covered != F:
        best, bs = None, -1
        for fm in cands:
            if fm & covered: continue          # tiles must be disjoint
            sz = bin(fm).count('1')
            if sz == 0: continue
            s = 10 * sz + 3 * tile_use.get(fm, 0)   # size first, reuse bonus
            if s > bs: bs, best = s, fm
        if best is None:
            break
        covered |= best
        tile_use[best] = tile_use.get(best, 0) + 1
        tile_reads += 1
    left = F & ~covered
    singleton_reads += bin(left).count('1')
    if left and bin(left).count('1') > 0 and len(cands) == 0:
        fails += 1
    if (pi + 1) % 500 == 0:
        log('%d/%d pieces tiled: distinct tiles %d, reads %d, singletons %d' %
            (pi + 1, len(pieces), len(tile_use), tile_reads, singleton_reads))

log('DONE COORDINATED TILING')
log('DISTINCT TILE POOL: %d' % len(tile_use))
hist = {}
for v in tile_use.values(): hist[v] = hist.get(v, 0) + 1
log('tile reuse histogram: %s' % dict(sorted(hist.items())[:25]))
log('tile reads total %d, singleton (free source) reads %d, full-fail pieces %d' %
    (tile_reads, singleton_reads, fails))
R_id = ct_total - n
tiles = len(tile_use)
for decoder in (72, 90, 120):
    R = R_id + tiles + decoder
    log('R = %d (R_id) + %d (tiles) + %d (decoder) = %d (%.1fv) vs BUDGET 5414 (15.0v) / 4846 (13.4v) -> %s' %
        (R_id, tiles, decoder, R, R / n,
         'FITS 15v' if R <= 5414 else ('FITS 13.4v' if R <= 4846 else 'OVER')))
pickle.dump({'tile_use': tile_use, 'tile_reads': tile_reads, 'singleton_reads': singleton_reads},
            open('ii19_tiles.pkl', 'wb'))
log('saved ii19_tiles.pkl')