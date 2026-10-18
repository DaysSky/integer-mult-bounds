"""II_{1,9} exact-cover probe: weight-2/3 covers + 1-line corrections, reuse coordination.
The census passed: R(t) IN SPAN of 3-sections (all 4 tested targets), sizes 48-91 vs demand
120-190, ceiling 1.84x E8.  Now: do exact covers exist at weight <= 3?  (The screen that killed
I9/I10.)  Probe 40 targets with pair-hash."""
import sys, time, collections, pickle, itertools
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# rebuild the line system (same as ii19_census.py)
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
for r in list(roots) + half:
    lines8[canon(r)] = r
R8 = list(lines8.values())
L = []
for al in R8:
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
L.append((None, 1, 1))
n = len(L)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    g = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    return g + a1 * b2 + b1 * a2
G = np.array([[ip(L[i], L[j]) for j in range(n)] for i in range(n)])
Z = np.abs(G) < 1e-9
log('system rebuilt: %d lines' % n)

def sections_of(t):
    mates = [e for e in range(n) if e != t and Z[t, e]]
    secs = []
    for i in range(len(mates)):
        zi = Z[mates[i]]
        for j in range(i + 1, len(mates)):
            if Z[mates[i], mates[j]]:
                m = zi & Z[mates[j]]
                secs.append(sum(1 << k for k in range(n) if m[k]))
    return secs

solutions = {}
sec_use = collections.Counter()
c_hist = collections.Counter()
corrections = {}
for t in list(range(0, n, max(1, n // 40)))[:40]:
    R_t = sum(1 << k for k in range(n) if Z[t, k])
    secs = sections_of(t)
    n_ = len(secs)
    pd = {}
    for i in range(n_):
        si = secs[i]
        for j in range(i + 1, n_):
            x = si ^ secs[j]
            if x not in pd: pd[x] = (i, j)
    best = None
    R_lines = [x for x in range(n) if R_t >> x & 1] + [-1]
    for l in R_lines:
        key = R_t if l == -1 else R_t ^ (1 << l)
        if key in pd:
            i, j = pd[key]
            sc = sec_use[secs[i]] + sec_use[secs[j]]
            if best is None or (2, -sc) < (best[0], -best[1]):
                best = (2, sc, (secs[i], secs[j]), l)
    if best is None:
        for l in R_lines:
            base = R_t if l == -1 else R_t ^ (1 << l)
            for k, s in enumerate(secs):
                key = base ^ s
                if key in pd:
                    i, j = pd[key]
                    if k in (i, j): continue
                    sc = sec_use[s] + sec_use[secs[i]] + sec_use[secs[j]]
                    if best is None or (3, -sc) < (best[0], -best[1]):
                        best = (3, sc, (s, secs[i], secs[j]), l)
    if best is None:
        c_hist['none'] += 1
        log('t=%d |R|=%d secs=%d: NO weight<=3 cover' % (t, bin(R_t).count('1'), len(secs)))
        continue
    w, sc, used, corr = best
    c_hist[w] += 1
    for s in used: sec_use[s] += 1
    corrections[t] = corr
    solutions[t] = used
    log('t=%d |R|=%d: weight %d (corr %s)' % (t, bin(R_t).count('1'), w, 'none' if corr == -1 else corr))
log('DONE: %d/40 solved, weights %s' % (len(solutions), dict(c_hist)))
if solutions:
    content = sum(bin(s).count('1') for s in sec_use)
    ct = sum(len(v) for v in solutions.values()) + sum(1 for c in corrections.values() if c != -1)
    log('distinct sections %d content %d use-hist %s' % (len(sec_use), content, dict(sorted(collections.Counter(sec_use.values()).items()))))
    log('sum c_t = %d -> R_identity = %d + dead' % (ct, ct - n))
pickle.dump({'sec_use': dict(sec_use), 'solutions': {t: list(v) for t, v in solutions.items()},
             'corrections': corrections}, open('ii19_covers.pkl', 'wb'))
log('saved ii19_covers.pkl')