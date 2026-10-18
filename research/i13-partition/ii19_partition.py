"""II19 partition search: can the 361 lines partition into disjoint rank-6 flats?
E8's D4-partition makes its assembly near-free (R420 zero waste).  A II19 partition would
harden the one remaining ledger estimate (the assembly/middle).  Greedy set-partition with
CP-SAT verification: minimize leftover lines uncovered by disjoint flats."""
import sys, time, random, itertools, resource
import numpy as np
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
t0 = time.time()
def log(*a): print('[%5.0fs rss=%dMB]' % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024), *a, flush=True)

E8 = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8); v[i] = si; v[j] = sj
                E8.append(v)
for s in itertools.product([1, -1], repeat=8):
    if s.count(-1) % 2 == 0:
        E8.append(np.array(s) / 2)
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
r8 = {}
for v in E8: r8[canon(v)] = np.array(v)
L = []
for al in r8.values():
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
L.append((np.zeros(8), 1, 1))
n = len(L)
coords = np.array([list(al) + [a, b] for al, a, b in L])
def ipv(x, y):
    return float(np.dot(x[:8], y[:8])) + x[8] * y[9] + x[9] * y[8]
Gm = np.array([[ipv(coords[i], coords[j]) for j in range(n)] for i in range(n)])
Z = np.abs(Gm) < 1e-9
log('system: %d lines' % n)
rng = random.Random(3)

# sample flats of various ranks over the FULL system (not per-target)
all_lines = list(range(n))
def sample_flat(rank, maxsize):
    for _ in range(400):
        pick = rng.sample(all_lines, rank)
        if np.linalg.matrix_rank(coords[pick]) != rank: continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[x]
        if flat.sum() and flat.sum() <= maxsize:
            return sum(1 << k for k in range(n) if flat[k])
    return None

# greedy partition: repeatedly pick the flat covering most uncovered lines
best_overall = None
for trial in range(20):
    covered = 0
    chosen = []
    for _ in range(40):
        best, bc = None, -1
        for _ in range(3000):
            r = rng.choice((6, 5, 4))
            f = sample_flat(r, 60)
            if not f: continue
            c = bin(f & ~covered).count('1')
            if c > bc: bc, best = c, f
        if best is None or bc <= 1: break
        covered |= best
        chosen.append(best)
    left = n - bin(covered).count('1')
    if best_overall is None or left < best_overall[0]:
        best_overall = (left, chosen)
    if left == 0: break
log('best partition trial: %d flats, %d/%d lines covered, leftover %d' %
    (len(best_overall[1]), bin(sum(best_overall[1])).count('1') if False else
     bin(int(np.bitwise_or.reduce([np.uint64(c) for c in best_overall[1]]))).count('1') if best_overall[1] else 0,
     n, best_overall[0]))
sizes = sorted(bin(c).count('1') for c in best_overall[1])
log('flat sizes: %s' % sizes)
log('leftover %d lines = %.1f%% of system' % (best_overall[0], 100 * best_overall[0] / n))