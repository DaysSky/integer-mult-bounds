"""THE II19's WALL-BAND PRICE SCAN (the SS1845 directive: 'keep going for II19 there is still potential'!!).

THE RE-OPENING (the SS1848 record!!): the SS1112 decoder scan priced at the R ~4,657 — 3x OVER
the hosting wall (the R <= 4.22 x 361 = 1,524!!) — THE WALL-BAND R 600-1,524 NEVER PRICED for
the full-II19 at the refined pricer!! The II19's ceiling: 2.21x (the highest of any viable!!).

THE QUESTIONS:
(1) THE B0 RANK re-verification (the 241 expected — the SS1112's number!)
(2) THE WALL-BAND PRICES: the R 400-1,524 x the hist models (the naive + the D-variant!!) x the
    decoder bands (the {1: 241} best case + the {10: 241} realistic!!) -> the c's + the deltas!
(3) THE VERDICT: does ANY band price above the frontier (0.001744386)?! — X decides the
    vocabulary hunt (the c_t <= 5.22 program!!)
"""
import itertools, time
from collections import Counter
import numpy as np
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM (the II19-0: the 3 root-classes + the special!!) ============
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
log('(0) the system: %d lines (the II19-0!!)' % n)
norms = np.diag(Gm)
log('    the norms: %s' % dict(sorted(Counter(np.round(norms, 2).tolist()).items())))
cls = [(a, b) for al, a, b in L]
log('    the classes: %s' % dict(sorted(Counter(cls).items())))

# ============ (1) THE PERPS + THE B0 RANK ============
Z = np.abs(Gm) < 1e-9
perp_masks = []
for i in range(n):
    m = 0
    for j in range(n):
        if j != i and Z[i, j]:
            m |= (1 << j)
    perp_masks.append(m)
B0 = [(1 << t) | perp_masks[t] for t in range(n)]
basis = {}
rank = 0
for r in B0:
    while r:
        p = (r & -r).bit_length() - 1
        if p in basis:
            r ^= basis[p]
        else:
            basis[p] = r
            rank += 1
            break
log('(1) THE GF(2) RANK OF B0: %d (of the %d!!) — the SS1112 number: the 241' % (rank, n))
szs = [bin(m).count('1') for m in perp_masks]
log('    the perp sizes: %s' % dict(sorted(Counter(szs).items())))

# ============ (2) THE WALL-BAND PRICE SCAN ============
V = n
H = 10
FRONTIER = 0.001744386
log('(2) THE WALL-BAND PRICE SCAN (the v=%d, the h=%d, the m=%d!!):' % (V, H, 1 + 9 * (H - 1)))
log('    the wall: the cap = 38v = %d; the nres = 9R -> the R <= %.0f!!' % (38 * V, 38 * V / 9))
climb_st = 2 * V * (H - 1)
DFRAC = {1: 0.262, 2: 0.571, 4: 0.048, 5: 0.119}
for R in (400, 600, 800, 1000, 1200, 1400, 1524):
    for dec_r in (1, 10):
        for model in ('naive', 'D'):
            climb = climb_st + R * H
            if model == 'naive':
                hist = {1: climb}
            else:
                hist = {}
                used = 0
                for d in (1, 2, 4):
                    z = int(round(DFRAC[d] * climb / d))
                    hist[d] = hist.get(d, 0) + z
                    used += d * z
                rem = climb - used
                hist[5] = hist.get(5, 0) + rem // 5
                if rem % 5:
                    hist[1] = hist.get(1, 0) + rem % 5
            hist[dec_r] = hist.get(dec_r, 0) + rank
            mass = sum(k * z for k, z in hist.items())
            try:
                res = pprice(dict(hist), V, H, R)
                c = res[0] if isinstance(res, tuple) else res
                if c is None or c <= 0:
                    print('    R %4d | dr %2d | %-5s | mass %6d | NO ROOT' % (R, dec_r, model, mass))
                else:
                    d = (c - FRONTIER) / FRONTIER * 100.0
                    print('    R %4d | dr %2d | %-5s | mass %6d | c %.9f | %+.2f%%'
                          % (R, dec_r, model, mass, c, d))
            except Exception as e:
                print('    R %4d | dr %2d | %-5s | EXCEPTION %s' % (R, dec_r, model, e))

# ============ (3) THE c_t ARITHMETIC ============
log('(3) THE c_t ARITHMETIC: the wall R <= %.0f; the identity R = Σc_t − v ->' % (38 * V / 9))
log('    the hosting needs the Σc_t <= %.0f -> the c_t <= %.2f (the E8-grade!!)' % (
    38 * V / 9 + V, (38 * V / 9 + V) / V))
log('    the measured: the c_t 9.5-10.3 (the stall-tail!) — the 2x gap!!')
log('DONE')
