"""II19 CARRIER CENSUS — the v3 (E8 carrier grammar) viability test on the v1 design.
E8's middle is nearly free by GRAMMAR: pieces are XORs of shared small carriers (quads =
2 cells; carriers ride branch slots).  Test whether II19 supports the same grammar:
1. Precompute ALL rank-2 flat closures (pair -> closure mask) of the 361-line system.
2. For each of the v1 design's 2,375 pieces: extract its internal rank-2 carriers
   (closures of internal pairs are automatically inside the piece).
3. Report: global distinct carrier pool + reuse histogram + mean carriers per piece.
   Small pool (~1,000) => middle = carriers, II19 alive; huge pool => carrier grammar dead.
4. Tiling probe: per piece, greedy disjoint cover by rank-2 flats (tiles partition the
   piece's lines exactly => piece total = XOR of tiles).  Sample 30 pieces."""
import sys, time, itertools, resource, pickle, random
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

# 1. precompute all rank-2 closures
pair_flat = {}
for i in range(n):
    for j in range(i + 1, n):
        if np.linalg.matrix_rank(LA[[i, j]]) != 2: continue
        m = Zint_row[i] & Zint_row[j]
        flat = (1 << n) - 1
        mm = m
        while mm:
            b = mm & -mm
            flat &= Zint_row[b.bit_length() - 1]
            mm ^= b
        pair_flat[(i, j)] = flat
log('rank-2 flat table: %d pairs (of %d possible)' % (len(pair_flat), n * (n - 1) // 2))

# 2. per-piece carriers
d = pickle.load(open('ii19_design.pkl', 'rb'))
use_count = d['use_count']
pieces = list(use_count.keys())
log('design pieces: %d' % len(pieces))
carrier_use = {}   # mask -> reuse
per_piece = []
for pi, F in enumerate(pieces):
    lines = [k for k in range(n) if F >> k & 1]
    local = set()
    for a_i in range(len(lines)):
        for b_i in range(a_i + 1, len(lines)):
            fm = pair_flat.get((lines[a_i], lines[b_i]))
            if fm is None: continue
            if fm & ~F: continue  # paranoia: closure must sit inside F
            local.add(fm)
    for fm in local:
        carrier_use[fm] = carrier_use.get(fm, 0) + 1
    per_piece.append(len(local))
    if (pi + 1) % 500 == 0:
        log('%d/%d pieces: distinct carriers so far %d, mean/piece %.1f' %
            (pi + 1, len(pieces), len(carrier_use), sum(per_piece) / len(per_piece)))
log('CARRIER POOL: %d distinct rank-2 carriers across %d pieces' % (len(carrier_use), len(pieces)))
hist = {}
for v in carrier_use.values(): hist[v] = hist.get(v, 0) + 1
log('carrier reuse histogram: %s' % dict(sorted(hist.items())[:20]))
log('mean carriers per piece: %.1f (min %d max %d)' %
    (sum(per_piece) / len(per_piece), min(per_piece), max(per_piece)))

# 3. tiling probe: disjoint cover of a piece by its internal rank-2 flats
rng = random.Random(9)
def tiling(F, maxtiles=25):
    lines = [k for k in range(n) if F >> k & 1]
    tiles = []
    covered = 0
    cands = set()
    for a_i in range(len(lines)):
        for b_i in range(a_i + 1, len(lines)):
            fm = pair_flat.get((lines[a_i], lines[b_i]))
            if fm is not None and not (fm & ~F):
                cands.add(fm)
    while len(tiles) < maxtiles:
        best, bc = None, -1
        for fm in cands:
            c = bin(fm & ~covered).count('1')
            if c > bc: bc, best = c, fm
        if best is None or bc <= 0: break
        covered |= best
        tiles.append(best)
    left = bin(F & ~covered).count('1')
    return tiles, left

sample = rng.sample(pieces, 30)
ok, fails = 0, []
for F in sample:
    tiles, left = tiling(F)
    if left == 0: ok += 1
    else: fails.append((bin(F).count('1'), len(tiles), left))
log('TILING PROBE: %d/30 pieces tile exactly by rank-2 flats' % ok)
for sz, nt, left in fails[:10]:
    log('  fail: size %d, %d tiles, leftover %d' % (sz, nt, left))
sizes = sorted(bin(t).count('1') for F in sample for t in tiling(F)[0])
log('tile sizes: min %d max %d mean %.1f' % (min(sizes), max(sizes), sum(sizes) / len(sizes)))
pickle.dump({'carrier_use': carrier_use}, open('ii19_carriers.pkl', 'wb'))
log('saved ii19_carriers.pkl')