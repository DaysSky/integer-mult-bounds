"""THE CONTROL VERIFICATION — the decisive honesty check for the SS1354 crossing result.

THE SS1354 PUSH: the honest 2-class structure (202 pieces + 94 tail carriers + 18 retained
= 314 registers; the pieces read the sources directly, NO conventional per-line carriers)
prices ABOVE THE FRONTIER across the entire shape band:
  A (the finest): +5.45% | B: +13.07% | C: +24.85% | D (the R420's own proportions): +33.12%.

THE DECISIVE QUESTION (the SS1209-1213 calibration lesson: the coarse [7]-model overstated
true c by 1.57x!!): does the REFINED price model (pricer.py), given a TRUE histogram,
reproduce the TRUE published c?  THE CONTROL: the R420's exact true hist
{1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9} (mass 5,112 = 8*420 + 72 + 2*120*7) at
(v=120, h=8, R=420) vs the published c = 0.001653826988146798944268.

  - IF the ratio = 1.000000: the model is EXACT at true hists — the SS1354 band is honest
    at the model level (the remaining uncertainty: the true word's shape, bracketed A-D,
    and the realizability: the pieces' read-frames).
  - IF the ratio != 1: the bias must be applied to the whole band.
"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

PUBLISHED = 0.001653826988146798944268

# === THE CONTROL: the R420's exact true histogram at the R420's parameters ===
ident = 8 * 420 + 72 + 2 * 120 * 7
hist = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
mass = sum(k * n for k, n in hist.items())
print('the R420 control: mass %d vs ident %d %s' % (mass, ident, 'MATCH' if mass == ident else 'MISMATCH'))
cc, _, _ = pprice(hist, 120, 8, 420)
print('CONTROL: the model c = %.18f' % cc)
print('the published c   = %.18f' % PUBLISHED)
ratio = cc / PUBLISHED
if abs(ratio - 1) < 1e-9:
    print('the ratio         = %.9f  EXACT: the refined model reproduces the published c at the true hist' % ratio)
    print('=> the SS1354 band (+5.45%% to +33.12%% at R=314) is honest AT THE MODEL LEVEL')
else:
    print('the ratio         = %.9f  BIASED: apply to the SS1354 band!!' % ratio)
    print('=> the D variant +33.12%% -> %+.2f%%; the A variant +5.45%% -> %+.2f%%'
          % ((0.002322061 * ratio / 0.001744386 - 1) * 100,
             (0.0018395 * ratio / 0.001744386 - 1) * 100))
print()

# === THE D VARIANT'S PEDIGREE CHECK: the fractions ARE the R420's own ===
# the R420's climb family mass (excluding the retained's rank-8 copies):
climb_mass = 1320 * 1 + 1440 * 2 + 60 * 4 + 120 * 5
print('the R420 climb mass (non-retained): %d' % climb_mass)
for rank, n in ((1, 1320), (2, 1440), (4, 60), (5, 120)):
    print('  rank %d: mass fraction %.4f' % (rank, rank * n / climb_mass))
print('the D variant uses {1: 0.262, 2: 0.571, 4: 0.048, 5: 0.119} = THE SAME family (the R420 own proportions)')
