"""THE R420-EXTENSION PRICE SCAN (the SS1867 audit's hypothesis!!).

THE HYPOTHESIS (the SS1868 record!!): the 121-line system (the unique h=9: the 120 E8 roots +
the special (0,1,1)!) — THE R420's OWN WORD IS THE 120-ROOT-PART's WORD ALREADY!! — the
extension: the special's demand (the 120 roots!) + the roots' +1 (the special in each perp!)
-> the R ~440-450 -> the wall 511 ✓ FITS!! — the window m=73 (the P111-analogous 1.66!!)
-> THE PRICE: THE UNMEASURED — THIS SCAN!!

THE QUESTIONS:
(1) THE B0 RANK (the ~9-10 expected: the E8 block + the special's row!)
(2) THE PRICE BAND: the R 380-511 x the hist models (the naive + the D + the R420-profile!)
    x the decoder copy ranks -> the c's + the deltas vs the frontier!!
(3) THE VERDICT: does the R420-extension window price above the frontier?!
"""
import itertools, time
from collections import Counter
import numpy as np
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM (the 121-line: the E8 roots + the special!!) ============
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
    L.append((al, 0, 0))
L.append((np.zeros(8), 1, 1))     # THE SPECIAL (0,1,1)!!
n = len(L)
coords = np.array([list(al) + [a, b] for al, a, b in L])
def ipv(x, y):
    return float(np.dot(x[:8], y[:8])) + x[8] * y[9] + x[9] * y[8]
Gm = np.array([[ipv(coords[i], coords[j]) for j in range(n)] for i in range(n)])
log('(0) the system: %d lines (the 121: the 120 roots + the special!!)' % n)
norms = np.diag(Gm)
log('    the norms: %s' % dict(sorted(Counter(np.round(norms, 2).tolist()).items())))
rankG = np.linalg.matrix_rank(Gm)
log('    the Gram rank (the span dim, the h!!): %d' % rankG)

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
log('(1) THE GF(2) RANK OF B0: %d (of the %d!!) — the expected ~9-10 (the E8 block!!)' % (rank, n))
szs = [bin(m).count('1') for m in perp_masks]
log('    the perp sizes: %s' % dict(sorted(Counter(szs).items())))

# ============ (2) THE PRICE SCAN (the R420-extension window!!) ============
V = n
H = 9     # the 121-line's h!!
FRONTIER = 0.001744386
log('(2) THE PRICE SCAN (the v=%d, the h=%d, the m=%d!!):' % (V, H, 1 + 9 * (H - 1)))
log('    the wall: the cap = 38v = %d; the nres = 9R -> the R <= %.0f!!' % (38 * V, 38 * V / 9))
climb_st = 2 * V * (H - 1)
DFRAC = {1: 0.258, 2: 0.563, 4: 0.047, 5: 0.117, 8: 0.014}   # the R420's OWN mass fractions!!
for R in (380, 400, 420, 440, 460, 480, 511):
    for dec_r in (1, 9):
        for model in ('naive', 'D', 'R420'):
            climb = climb_st + R * H
            if model == 'naive':
                hist = {1: climb}
            elif model == 'D':
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
            else:   # the R420-profile!!
                hist = {}
                used = 0
                for d in (1, 2, 4, 5):
                    z = int(round(DFRAC[d] * climb / d))
                    hist[d] = hist.get(d, 0) + z
                    used += d * z
                rem = climb - used
                hist[8] = hist.get(8, 0) + rem // 8
                if rem % 8:
                    hist[1] = hist.get(1, 0) + rem % 8
            hist[dec_r] = hist.get(dec_r, 0) + rank
            mass = sum(k * z for k, z in hist.items())
            try:
                res = pprice(dict(hist), V, H, R)
                c = res[0] if isinstance(res, tuple) else res
                if c is None or c <= 0:
                    print('    R %4d | dr %2d | %-4s | mass %6d | NO ROOT' % (R, dec_r, model, mass))
                else:
                    d = (c - FRONTIER) / FRONTIER * 100.0
                    print('    R %4d | dr %2d | %-4s | mass %6d | c %.9f | %+.2f%%'
                          % (R, dec_r, model, mass, c, d))
            except Exception as e:
                print('    R %4d | dr %2d | %-4s | EXCEPTION %s' % (R, dec_r, model, e))

# ============ (3) THE R420 CONTROL ============
log('(3) THE R420 CONTROL (the calibration!!):')
res420 = pprice({1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}, 120, 8, 420)
c420 = res420[0] if isinstance(res420, tuple) else res420
log('    the R420: c %.21f (the published: 0.001653826988146798944268!!)' % c420)
log('DONE')
