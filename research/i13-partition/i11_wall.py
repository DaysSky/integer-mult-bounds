"""THE I11's HOSTING-WALL + DECODER-RANK SCREEN (the SS1830-1831: 'keep finding breakthroughs on lorentzian'!!).

THE I11's COIN-FLIP (the SS755-767: 'a coin-flip, not closed'!!): the budget R=1,652 (7.51v!)
with the layered middle 817 <= 992 (the 17% margin!!) and the read-side gap c_t 8-10 vs <= 7.2
(the sampled 2k-20k vocabularies vs the true ~10^5-10^6 population!!).

THE SS1826 DISCOVERY (the hosting wall!!): the pricer's own check: the nres = 9R vs the
cap = 38v -> R <= 4.22v — the level-2 closed at the wall (the 2.2x over!!); the II19-0: the
1.43x over!! THE I11's WALL: R <= 929 — the budget 1,652 is 1.78x OVER the wall — BUT the
kappa(R) curve is DECLINING: the forced R <= 929 would price ABOVE the 1,652 crossing!!!

THE QUESTIONS:
(1) THE B0 RANK: the GF(2) rank of the perp-pattern decoder (the 220 rows!) — UNMEASURED!!
(2) THE HOSTING WALL + THE PRICE BAND: the pricer's own verdicts at the R 400-1,652 (the
    naive hist + the decoder bands {9: rank} and {12: rank}!!)
(3) THE c_t ARITHMETIC: the hosting needs Σc_t <= wall + v (the c_t <= 5.2!!) vs the
    crossing (the c_t <= 7.22!!) vs the measured (the c_t 8-10!!)
"""
import sys, time
from collections import Counter
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from geom import Geom
from pricer import price as pprice

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

# ============ (0) THE SYSTEM ============
g = Geom(11)
V = g.V
HYP = g.HYP
log('(0) the system: V=%d (the I11: the Geom(11)!!)' % V)
szs = [bin(HYP[t]).count('1') - 1 for t in range(V)]
log('    the perp sizes: %s' % dict(sorted(Counter(szs).items())))

# ============ (1) THE B0 RANK ============
B0 = [HYP[t] for t in range(V)]
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
log('(1) THE GF(2) RANK OF B0: %d (of the %d rows!!)' % (rank, V))
log('    the precedents: the II19-0: the 241 (fatal!!); the level-2: the 531; the E8: the 9')
log('    the I11: %s' % ('SMALL (the E8-grade!!)' if rank <= 30 else
                        'LARGE (the fatal!!)' if rank >= 100 else 'THE MIDDLE'))

# ============ (2) THE HOSTING WALL + THE PRICE BAND ============
H = 12
FRONTIER = 0.001744386
log('(2) THE PRICE BAND (the v=%d, the h=%d, the m=%d!!):' % (V, H, 1 + 9 * (H - 1)))
def mass_of(hist):
    return sum(k * z for k, z in hist.items())
for R in (400, 600, 800, 900, 929, 1000, 1200, 1400, 1652):
    for dr in (9, 12):
        hist = {}
        hist[1] = hist.get(1, 0) + V * (H - 1) * 2
        hist[1] = hist.get(1, 0) + R * H
        hist[dr] = hist.get(dr, 0) + rank
        try:
            res = pprice(dict(hist), V, H, R)
            c = res[0] if isinstance(res, tuple) else res
            det = res[2] if isinstance(res, tuple) and len(res) > 2 else {}
            if c is None or c <= 0:
                err = det.get('error', 'no root') if isinstance(det, dict) else 'no root'
                print('    R %5d | dr %2d | mass %6d | %s' % (R, dr, mass_of(hist), err))
            else:
                d = (c - FRONTIER) / FRONTIER * 100.0
                print('    R %5d | dr %2d | mass %6d | c %.9f | %+.2f%%'
                      % (R, dr, mass_of(hist), c, d))
        except Exception as e:
            print('    R %5d | dr %2d | EXCEPTION %s' % (R, dr, e))

# ============ (3) THE c_t ARITHMETIC ============
wall_R = 4.22 * V
log('(3) THE c_t ARITHMETIC: the wall R <= %.0f; the crossing needs R ~1,652 (7.51v!!)' % wall_R)
log('    the hosting needs: Σc_t <= wall + v = %.0f -> the c_t <= %.2f (the E8-grade!!)'
    % (wall_R + V, (wall_R + V) / V))
log('    the crossing needs: Σc_t <= 1,588 -> the c_t <= 7.22 (the SS846!!)')
log('    the measured: the c_t 8-10 (the sampled 2k-20k!!); the v2 trend: the bulk -> 4!!')
log('DONE')
