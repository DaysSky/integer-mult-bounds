"""THE LEVEL-2 DECODER-RANK SCREEN (the SS1799 direction: 'keep pushing lorentzian'!!).

THE LEVEL-0'S FATAL PRECEDENT: the decoder rank 241 (the width forced >= 241 -> the price
dead!!). THE LEVEL-2's RANK: UNMEASURED — THE FIRST CHECK of the SS1799 screen!!

THE SYSTEM (the ii19_l2_probe.py construction, SS1810!!): the 929 lines = the 360 (the 3
root-layers: (al,0,0), (al,1,0), (al,0,1)) + the 568 (the norm-4 vectors at (lm,1,-1)) +
the 1 (the special (0,1,1)); the form x.x' + a.d + b.c (the 10-dim: h=10!!).

THE MEASUREMENTS:
(1) THE GRAM + THE PERPS: the per-line orthogonality masks
(2) B0: the perp-pattern decoder rows ({t} U perp(t)!!)
(3) THE GF(2) RANK of the 929 rows (the pivot elimination!!) — THE DECISIVE CHECK:
    the level-0's 241 was fatal; the level-2's: ??? (the small -> PASS; the large -> FAIL!!)
(4) THE DEMANDS: the per-class perp sizes (the c_t arithmetic's input!)
"""
import itertools, time
from collections import Counter
import numpy as np

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM (the SS1810 construction!!) ============
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
norm4 = []
for i in range(8):
    for s in (2, -2):
        v = np.zeros(8); v[i] = s
        norm4.append(v)
for combo in itertools.combinations(range(8), 4):
    for signs in itertools.product([1, -1], repeat=4):
        v = np.zeros(8)
        for k, idx in enumerate(combo): v[idx] = signs[k]
        norm4.append(v)
n4 = {}
for v in norm4: n4[canon(v)] = np.array(v)
L = []
for al in r8.values():
    L.append((al, 0, 0)); L.append((al, 1, 0)); L.append((al, 0, 1))
for lm in n4.values():
    L.append((lm, 1, -1))
L.append((np.zeros(8), 1, 1))
n = len(L)
coords = np.array([list(al) + [a, b] for al, a, b in L])
def ipv(x, y):
    return float(np.dot(x[:8], y[:8])) + x[8] * y[9] + x[9] * y[8]
Gm = np.array([[ipv(coords[i], coords[j]) for j in range(n)] for i in range(n)])
norms = np.diag(Gm)
log('(0) the system: %d lines; the norms %s' % (
    n, dict(sorted(Counter(np.round(norms, 2).tolist()).items()))))
cls = [(a, b) for al, a, b in L]
log('    the classes: %s' % dict(sorted(Counter(cls).items())))

# ============ (1) THE PERPS ============
Z = np.abs(Gm) < 1e-9
perp_masks = []
for i in range(n):
    m = 0
    for j in range(n):
        if j != i and Z[i, j]:
            m |= (1 << j)
    perp_masks.append(m)
szs = [bin(m).count('1') for m in perp_masks]
log('(1) the perp sizes: %s' % dict(sorted(Counter(szs).items())))

# ============ (2) B0: the perp-pattern decoder rows ============
B0 = [(1 << t) | perp_masks[t] for t in range(n)]
log('(2) B0 built: the %d rows' % n)

# ============ (3) THE GF(2) RANK (the pivot elimination!!) ============
basis = {}
rank = 0
pivots = []
for r in B0:
    while r:
        p = (r & -r).bit_length() - 1
        if p in basis:
            r ^= basis[p]
        else:
            basis[p] = r
            rank += 1
            pivots.append(p)
            break
log('(3) THE GF(2) RANK OF B0: %d (of the %d rows!!)' % (rank, n))
log('    the level-0 precedent: the 241 was fatal (the width >= 241!!)')
log('    the level-2: %s' % ('PASS-ish (the small rank!!)' if rank <= 60 else
                             'FATAL-ISH (the large rank!!)' if rank >= 400 else
                             'THE MIDDLE (the cst arithmetic decides!!)'))
log('    the retained implication: the decoder width >= %d -> the CST ~ the width x the copy rank' % rank)

# ============ (4) THE DEMANDS (the c_t arithmetic's input!) ============
by_cls = Counter()
for t in range(n):
    by_cls[cls[t]] += szs[t]
log('(4) THE DEMANDS by class: %s' % {str(k): v for k, v in sorted(by_cls.items())})
log('DONE')
