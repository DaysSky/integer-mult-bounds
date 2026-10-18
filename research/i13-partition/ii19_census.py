"""II_{1,9} = E8 (+) U line-system census.  The code's I_{n,1} convention: minimal levels.
Classes: A = (alpha, 0, 0) E8 roots (120 lines); B = (alpha, 1, 0) and (alpha, 0, 1) (240);
C = (0, 1, 1) (1 line).  Total 361 lines, h = 10 (ambient rank).  Census: demand sizes,
3-section span test, section sizes/users, exact-cover probe."""
import sys, time, collections, itertools
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8 as e8mod
import numpy as np
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# E8 root lines: use the module's V (lines) and their Gram/coordinates
V8 = e8mod.V
# build E8 root vectors as integer coordinates: derive from e8.py's structures.
# e8.py exposes lines; we need representatives.  Construct E8 roots directly:
roots = []
for i in range(8):
    for j in range(i + 1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v = np.zeros(8, dtype=int); v[i] = si; v[j] = sj
                roots.append(v)
                if si * sj == 1:  # avoid duplicates for the half class counting
                    pass
for s in itertools.product([1, -1], repeat=8):
    if s[0] * s[1] * s[2] * s[3] * s[4] * s[5] * s[6] * s[7] == 1:  # even # of minus
        v = (np.array(s, dtype=int) - 1) // 2  # placeholder
# standard half-integer roots: (1/2)(±1,...,±1) with even number of minus signs
half = []
for s in itertools.product([1, -1], repeat=8):
    if s.count(-1) % 2 == 0:
        half.append(np.array(s, dtype=float) / 2)
roots8 = [r.astype(float) for r in roots] + half
# dedupe up to sign: canonical form: first nonzero positive
def canon(v):
    for x in v:
        if x != 0:
            return tuple(v) if x > 0 else tuple(-v)
    return tuple(v)
lines8 = {}
for r in roots8:
    lines8[canon(r)] = r
R8 = list(lines8.values())
log('E8 root lines:', len(R8), '(expect 120)')

# II_{1,9} classes: (alpha, a, b) with alpha in R8 (or 0), U-coords (a,b)
def mk(alpha, a, b):
    return (alpha, a, b)
def ip(x, y):
    (u, a1, b1), (w, a2, b2) = x, y
    g = float(np.dot(u, w)) if u is not None and w is not None else 0.0
    if u is None or w is None:
        g = 0.0
    return g + a1 * b2 + b1 * a2
L = []
for al in R8:
    L.append((al, 0, 0))          # class A
    L.append((al, 1, 0))          # class B1
    L.append((al, 0, 1))          # class B2
L.append((None, 1, 1))            # class C
n = len(L)
log('II19 line system:', n, 'lines;  norms check:', collections.Counter(round(ip(v, v), 3) for v in L))
G = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        G[i, j] = ip(L[i], L[j])
# pairwise orthogonality: exact zeros
Z = np.abs(G) < 1e-9
log('orthogonality: mean perp per line %.1f' % (Z.sum(axis=1).mean() - 1))
R_of = [Z[i] & ~Z[i].astype(bool) for i in range(n)]
# demand sizes: |R(t)| = lines orthogonal to t (excluding t itself... t is not orthogonal to itself: norm 2)
demand = Z.sum(axis=1) - 0  # t not orthogonal to itself (norm 2 != 0)
log('demand sizes: min %d max %d mean %.1f hist %s' % (
    demand.min(), demand.max(), demand.mean(), dict(sorted(collections.Counter(demand.tolist()).items())[:8])))
# 3-section span test for a few targets: sections {t,e1,e2}-perp for orthogonal triples
def sections_of(t):
    mates = [e for e in range(n) if e != t and Z[t, e]]
    secs = []
    for i in range(len(mates)):
        for j in range(i + 1, len(mates)):
            if Z[mates[i], mates[j]]:
                mask = Z[mates[i]] & Z[mates[j]]
                secs.append(mask)
    return secs
for t in (0, 60, 200, n - 1):
    secs = sections_of(t)
    if not secs:
        log('t=%d: no sections (orthogonal mates: %d)' % (t, sum(Z[t]) ))
        continue
    sizes = collections.Counter(int(s.sum()) for s in secs)
    # span test
    basis = {}
    for c in secs:
        v = int(0)
        # use bitmask int over n lines
    # bitmask representation
    secs_i = [sum(1 << k for k in range(n) if s[k]) for s in secs]
    basis = {}
    for c in secs_i:
        v = c
        while v:
            b = v & -v
            if b in basis: v ^= basis[b][0]
            else: basis[b] = (v, c); break
    R_t = sum(1 << k for k in range(n) if Z[t, k])
    v = R_t
    miss = 0
    while v:
        b = v & -v
        if b not in basis:
            miss += 1
            v = 0  # count remaining bits
            break
        v ^= basis[b][0]
    if v:
        rest = bin(R_t).count('1')
        log('t=%d |R|=%d secs=%d sizes=%s span-miss=%d' % (t, bin(R_t).count('1'), len(secs), dict(sorted(sizes.items())), miss))
    else:
        log('t=%d |R|=%d secs=%d sizes=%s IN SPAN' % (t, bin(R_t).count('1'), len(secs), dict(sorted(sizes.items()))))