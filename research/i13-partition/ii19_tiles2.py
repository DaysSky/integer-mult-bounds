"""II19 TILE REFINEMENT — the last compression lever on the middle.
Coordinated tiling v1: pool 5,962 (from 21,273 reads; naive 52,737 -> 11x compression) —
still 2x over the ~2,990 budget.  The v1 greedy was SIZE-first (10*sz + 3*reuse).
THIS: iterative POPULARITY-first refinement — each pass re-tiles every piece choosing
the tiling that maximizes use of globally popular tiles (more reads is fine: reads are
work, the POOL is what registers cost).  Passes converge the pool; report per pass.
Also: the top-3,000 pool coverage — how many tile-uses fall inside/outside a 3,000 budget."""
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
ct_total = d['ct_total']
pieces = sorted(use_count.keys(), key=lambda F: -bin(F).count('1'))
log('pieces: %d' % len(pieces))

# per-piece candidate tiles (rank-2 flats inside the piece)
cand_by_piece = []
for F in pieces:
    lines = [k for k in range(n) if F >> k & 1]
    cands = set()
    for a_i in range(len(lines)):
        for b_i in range(a_i + 1, len(lines)):
            fm = pair_flat.get((lines[a_i], lines[b_i]))
            if fm is not None and not (fm & ~F):
                cands.add(fm)
    cand_by_piece.append((F, list(cands)))
log('candidates built')

def tile_piece(F, cands, pop, mode):
    covered = 0
    used = []
    while covered != F:
        best, bs = None, -1
        for fm in cands:
            if fm & covered: continue
            sz = bin(fm).count('1')
            if mode == 'size':
                s = 10 * sz + 3 * pop.get(fm, 0)
            else:  # popularity-first
                s = 10 * pop.get(fm, 0) + 2 * sz
            if s > bs: bs, best = s, fm
        if best is None: break
        covered |= best
        used.append(best)
    return used

pop = {}
singles = 0
piece_tiles = []
for F, cands in cand_by_piece:      # PASS 1: size-first (replicates v1 tiling)
    used = tile_piece(F, cands, pop, 'size')
    for fm in used: pop[fm] = pop.get(fm, 0) + 1
    singles += bin(F & ~(0 if not used else 0)).count('1') if False else 0
    piece_tiles.append(used)
# compute singles properly
singles = 0
for (F, cands), used in zip(cand_by_piece, piece_tiles):
    cov = 0
    for fm in used: cov |= fm
    singles += bin(F & ~cov).count('1')
log('PASS 1 (size-first): pool %d, reads %d, singles %d' %
    (len(pop), sum(len(u) for u in piece_tiles), singles))

for it in range(1, 6):             # REFINEMENT: popularity-first
    pop = {}
    new_tiles = []
    singles = 0
    for F, cands in cand_by_piece:
        used = tile_piece(F, cands, pop, 'pop')
        for fm in used: pop[fm] = pop.get(fm, 0) + 1
        cov = 0
        for fm in used: cov |= fm
        singles += bin(F & ~cov).count('1')
        new_tiles.append(used)
    piece_tiles = new_tiles
    log('PASS %d (pop-first): pool %d, reads %d, singles %d' %
        (it + 1, len(pop), sum(len(u) for u in piece_tiles), singles))

tiles = len(pop)
R_id = ct_total - n
for decoder in (72, 90):
    R = R_id + tiles + decoder
    log('R = %d + %d + %d = %d (%.1fv) vs BUDGET 5414 (15.0v) -> %s' %
        (R_id, tiles, decoder, R, R / n,
         'FITS' if R <= 5414 else 'OVER'))
# top-3000 budget coverage
if tiles > 0:
    sorted_tiles = sorted(pop.items(), key=lambda kv: -kv[1])
    top = set(fm for fm, c in sorted_tiles[:3000])
    inside = sum(c for fm, c in sorted_tiles[:3000])
    total_reads = sum(pop.values())
    log('top-3000 tiles carry %d of %d reads (%.0f%%); pool beyond 3,000: %d tiles' %
        (inside, total_reads, 100 * inside / total_reads, max(0, tiles - 3000)))
pickle.dump({'pop': pop}, open('ii19_tiles2.pkl', 'wb'))
log('saved ii19_tiles2.pkl')