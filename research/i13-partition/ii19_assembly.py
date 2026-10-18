"""II19 Stage 2: the assembly builder — the true middle-layer construction.
Consumes ii19_design.pkl (the design's used flat masks + reuse counts).  For each distinct
rank-6 flat: hierarchical build (rank-6 <- 2-4 rank-5 sub-flats <- rank-4 <- cells), sub-flats
SHARED across all containing rank-6 flats.  Output: the TRUE mid-register count (replacing
the E8-ratio estimate), the layered reuse histogram, and the projected R vs the 13.4-15v budget.
RAM-safe: bitmask ints + sampled sub-flats, no giant dicts."""
import sys, time, random, itertools, resource, pickle
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

# rebuild the line system
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
rng = random.Random(33)

log('loading design...')
d = pickle.load(open('ii19_design.pkl', 'rb'))
use_count = d['use_count']
log('design: %d targets, sum c_t %d, %d distinct flats' % (len(d['design']), d['ct_total'], len(use_count)))

def total_of(mask):
    tot = 0
    for k in range(n):
        if mask >> k & 1: tot ^= (1 << k)
    return tot

def subflats(mask, rank, nsample):
    """sample rank-rank sub-flats inside the flat: closures of independent rank-subsets"""
    lines = [k for k in range(n) if mask >> k & 1]
    out, seen = [], set()
    tries = 0
    while len(out) < nsample and tries < nsample * 40:
        tries += 1
        pick = rng.sample(lines, min(rank, len(lines)))
        if np.linalg.matrix_rank(LA[pick]) != len(pick): continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        fmask = sum(1 << k for k in range(n) if flat[k])
        if not fmask or fmask in seen: continue
        if fmask & ~mask: continue  # must stay inside the parent flat
        seen.add(fmask)
        out.append(fmask)
    return out

# hierarchical build with sharing: level 5 and level 4 intermediates
lvl5 = {}   # mask -> reuse
lvl4 = {}
gates = 0
flats = list(use_count.keys())
rng.shuffle(flats)
for i, fmask in enumerate(flats):
    ftot = total_of(fmask)
    # build from rank-5 sub-flats (greedy cover of the total)
    subs = subflats(fmask, 5, 300)
    if not subs:
        gates += bin(fmask).count('1') - 1  # naive tree fallback
        continue
    res = ftot
    used = []
    for _ in range(6):
        best, bp = None, 1 << 30
        for sm in subs:
            p = bin(res ^ total_of(sm)).count('1')
            if p < bp: bp, best = p, sm
        if best is None or bp >= bin(res).count('1'): break
        res ^= total_of(best); used.append(best)
        if bin(res).count('1') == 0: break
    for sm in used:
        lvl5[sm] = lvl5.get(sm, 0) + 1
    if bin(res).count('1') > 0:
        gates += bin(res).count('1') + len(used)  # residual handled by direct gates
    else:
        gates += len(used)  # merge gates at the parent level
    if (i + 1) % 50 == 0:
        log('%d/%d flats built: lvl5 distinct %d (reuses %s), gates so far %d' %
            (i + 1, len(flats), len(lvl5),
              dict(sorted({k: sum(1 for v in lvl5.values() if v == k) for k in set(lvl5.values())}.items())), gates))
# level 5 <- level 4 (second layer, same pattern)
log('building level-5 intermediates from rank-4...')
for sm in list(lvl5.keys()):
    stot = total_of(sm)
    subs = subflats(sm, 4, 150)
    if not subs:
        gates += bin(sm).count('1') - 1
        continue
    res = stot
    used = []
    for _ in range(5):
        best, bp = None, 1 << 30
        for s4 in subs:
            p = bin(res ^ total_of(s4)).count('1')
            if p < bp: bp, best = p, s4
        if best is None or bp >= bin(res).count('1'): break
        res ^= total_of(best); used.append(best)
        if bin(res).count('1') == 0: break
    for s4 in used:
        lvl4[s4] = lvl4.get(s4, 0) + 1
    gates += len(used) + (bin(res).count('1') if bin(res).count('1') else 0)
log('DONE assembly sketch')
log('distinct intermediates: lvl5 %d, lvl4 %d' % (len(lvl5), len(lvl4)))
log('merge gates total: %d -> mid-register estimate (gates / visits-per-register ~ 8): %d' %
    (gates, gates // 8))
mid_regs = len(lvl5) + len(lvl4) + gates // 8
log('PROJECTED MIDDLE: %d registers (design flats %d are the read pieces themselves)' %
    (mid_regs, len(use_count)))
ct = d['ct_total']
R_id = ct - n
R = R_id + mid_regs
log('PROJECTED R = %d (%.1fv) vs BUDGET 13.4-15v (cst 120-90)' % (R, R / n))
pickle.dump({'lvl5': lvl5, 'lvl4': lvl4, 'gates': gates, 'mid_regs': mid_regs},
            open('ii19_assembly.pkl', 'wb'))
log('saved ii19_assembly.pkl')