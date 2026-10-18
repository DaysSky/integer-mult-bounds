"""II19 partition exploitation: re-find the 15-flat zero-leftover partition, SAVE it, and
census its free-piece value: per flat (rank, size, perp size = users), and per target
(how many partition flats serve t, and how many of R(t)'s lines they cover for free).
The partition flats are free pieces: already assembled for the skeleton, read by any t in perp(F)."""
import sys, time, random, itertools, resource, pickle
import numpy as np
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

all_lines = list(range(n))
def sample_flat(rank, maxsize):
    for _ in range(400):
        pick = rng.sample(all_lines, rank)
        if np.linalg.matrix_rank(coords[pick]) != rank: continue
        m = Z[pick[0]]
        for p in pick[1:]: m = m & Z[p]
        flat = np.ones(n, dtype=bool)
        for kk in [x for x in range(n) if m[x]]: flat = flat & Z[kk]
        if flat.sum() and flat.sum() <= maxsize:
            return sum(1 << k for k in range(n) if flat[k])
    return None

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
left, chosen = best_overall
log('partition: %d flats, leftover %d' % (len(chosen), left))
pickle.dump({'flats': chosen}, open('ii19_partition.pkl', 'wb'))
log('saved ii19_partition.pkl')

# census: per flat
log('per-flat census (size, perp=users, overlap with other flats):')
for i, f in enumerate(chosen):
    perp = np.ones(n, dtype=bool)
    for k in range(n):
        if f >> k & 1: perp = perp & Z[k]
    log('flat %d: size %d, users %d' % (i, bin(f).count('1'), int(perp.sum())))

# per-target free coverage
cov_hist = {}
free_lines = {}
for t in range(n):
    R_t = [k for k in range(n) if Z[t, k]]
    Rmask = sum(1 << k for k in R_t)
    cnt, covered = 0, 0
    for f in chosen:
        # t reads F's total iff t perp F: t orthogonal to all lines of F
        tp = True
        for k in range(n):
            if f >> k & 1 and not Z[t, k]:
                tp = False; break
        if tp:
            cnt += 1
            covered |= f
    free = bin(covered & Rmask).count('1')
    cov_hist[cnt] = cov_hist.get(cnt, 0) + 1
    free_lines[t] = (cnt, free)
tot_free = sum(v[1] for v in free_lines.values())
tot_dem = sum(int(Z[t].sum()) for t in range(n))
log('targets by #partition-flats-served: %s' % dict(sorted(cov_hist.items())))
log('free coverage: %d of %d demand slots = %.1f%%' % (tot_free, tot_dem, 100 * tot_free / tot_dem))
cls = {}
for t in (0, 121, 241, 360):
    log('example t=%d: served %d flats, %d free lines of %d demand' %
        (t, free_lines[t][0], free_lines[t][1], int(Z[t].sum())))
pickle.dump({'free_lines': free_lines}, open('ii19_free_lines.pkl', 'wb'))
log('saved ii19_free_lines.pkl')