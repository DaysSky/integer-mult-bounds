"""THE LEVEL-2 PRICE CHECK (the SS1814 rank 531: FATAL-ISH PENDING THE PRICE!!).

THE QUESTION (the SS1112-style!!): does the 2.6x window (the v/m: the 929/82 = 11.3 vs the
level-0's 4.4!!) absorb the 2.2x decoder (the rank 531 vs the 241!!)?

THE LEVEL-0'S PRECEDENT (SS1112!!): the width 241 -> the best case (all rank-1 totals!!)
the c = 0.00073949773 (-57.61% vs the frontier!!); every realistic ([r=2]-[r=10] x 241)
the NO ROOT (the pricer refuses!!).

THE LEVEL-2's MODELS (the honest bands!!):
(1) THE R BAND: the identity arithmetic: the c_t ~10-12 -> the R ~8,000-12,000 (the honest
    band; the ceiling 4.74x E8's 3.5 = the R/v allowance ~16.6!!)
(2) THE DECODER BAND: the {r: 531} for the r in 1-10 (the copy ranks!!)
(3) THE REST (the naive all-1 model!!): the sources + the targets (the 929 x 9 1-climbs
    each: the {s}->FULL (h-1=9!!) + the 0->t-perp (9!!)) + the helpers (the R x 10!!)
(4) THE CONTROLS: the R420's true hist -> the published c (the SS1362 calibration!!)
"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

V = 929
H = 10
FRONTIER = 0.001744386     # the E8 R434 (the current frontier!!)

def mass_of(hist):
    return sum(k * z for k, z in hist.items())

def price_band(tag, hist, R):
    try:
        res = pprice(dict(hist), V, H, R)
        c = res[0] if isinstance(res, tuple) else res
        det = res[2] if isinstance(res, tuple) and len(res) > 2 else {}
        if c is None or c <= 0:
            err = det.get('error', 'no root') if isinstance(det, dict) else 'no root'
            print('  %-34s R %6d | mass %7d | %s' % (tag, R, mass_of(hist), err))
            return None
        d = (c - FRONTIER) / FRONTIER * 100.0
        print('  %-34s R %6d | mass %7d | c %.9f | %+.2f%%' % (tag, R, mass_of(hist), c, d))
        return c
    except Exception as e:
        print('  %-34s R %6d | EXCEPTION %s' % (tag, R, e))
        return None

print('THE CONTROLS (the calibration!!):')
res420 = pprice({1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}, 120, 8, 420)
c420 = res420[0] if isinstance(res420, tuple) else res420
print('  the R420 control: c %.21f' % c420)
print('  the published:    0.001653826988146798944268 | the ratio %.6f'
      % (c420 / 0.001653826988146798944268))

print()
print('THE LEVEL-2 BANDS (the v=%d, the h=%d, the m=82!!):' % (V, H))
print('  the naive rest: the sources+targets %d x 9 1-climbs x2 + the helpers R x 10' % V)
print('  the decoder: the 531 x the copy rank r (the band r=1 (the best case!!) - r=10!!)')
for R in (8000, 9000, 10000, 12000):
    for r in (1, 4, 9, 10):
        hist = {}
        hist[1] = hist.get(1, 0) + V * 9 * 2        # the sources + the targets
        hist[1] = hist.get(1, 0) + R * 10           # the helpers (the naive!!)
        hist[r] = hist.get(r, 0) + 531              # the decoder!!
        price_band('R %d, the decoder r=%d' % (R, r), hist, R)

print()
print('THE BEST-CASE SCAN (the r=1: the physically unrealizable but the bound!!):')
for R in (4000, 6000, 8000, 10000, 15000, 20000):
    hist = {}
    hist[1] = hist.get(1, 0) + V * 9 * 2
    hist[1] = hist.get(1, 0) + R * 10
    hist[1] = hist.get(1, 0) + 531
    price_band('R %d, the best case r=1' % R, hist, R)
print('DONE')
