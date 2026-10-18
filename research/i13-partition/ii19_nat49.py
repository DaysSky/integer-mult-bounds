"""THE E8-120 DECOMPOSITION (ii19_nat49.py) — the shape-part vs the R-part of the R420's gap.

THE R420 (v=120, h=8, R=420, c=0.0016538) sits -5.2% under the frontier. THE QUESTION:
how much is the HIST SHAPE vs the R?!  THE GRID: the frontier's shape vs the R420's own
shape at (120, 8, R) for R 420-470.  IF THE SHAPE-PART CROSSES: THE R420-WORD'S IN-PLACE
MOVES-SPACE (the nat21-class scans (NEVER SWEPT on the R420!!!)) IS THE IMMEDIATE TARGET.
"""
import os, sys, json
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))

# the two shapes:
FRONT = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18}     # the frontier's (cst 63!!)
R420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}                    # the published R420's (cst 72!!)
log('the masses: the frontier-shape %d | the R420-shape %d' % (
    sum(r * c for r, c in FRONT.items()), sum(r * c for r, c in R420.items())))
# the controls:
c = price(R420, 120, 8, 420)
log('THE CONTROL (the R420 own): %s (the published 0.001653826988146798944268)' % (c[0] if c else 'NO-ROOT'))
c = price(FRONT, 111, 8, 434)
log('THE CONTROL (the frontier): %s (the published 0.001744385950814795279853)' % (c[0] if c else 'NO-ROOT'))

# the mass-exact shape-transplant: the frontier's CLIMB-shape onto (120, 8, R)!!
base = dict(FRONT); base[7] -= 9                   # the climb part (the copy = 9 rank-7!!)
bm = sum(r * c for r, c in base.items())
def transplant(v, R, cst_copy):
    climb = 8 * R + 2 * v * 7
    acc = Counter()
    for r in sorted(base, key=lambda r: -base[r] * r):
        n = int(Fraction(climb * (base[r] * r), bm) / r)
        acc[r] = n
    rem = climb - sum(r * c for r, c in acc.items())
    while rem > 0:
        for r in sorted(base, key=lambda r: -base[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[7] += 9                                    # the frontier's copy structure (cst 63!!)
    return dict(acc)

log('')
log('THE DECOMPOSITION GRID: the frontier climb-shape at (120, 8, R)!!')
for R in [420, 424, 430, 434, 440, 446, 452, 460, 470]:
    h = transplant(120, R, 63)
    c = price(h, 120, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('  R %3d | c %.20g (%+.2f%% vs the frontier)' % (R, float(c[0]), 100 * (float(c[0]) / float(FC) - 1)))
    else:
        log('  R %3d | NO-ROOT/spurious' % R)
log('')
log('THE SAME AT v=111 (the frontier own system, R-swept!!):')
for R in [434, 440, 444]:
    h = transplant(111, R, 63)
    c = price(h, 111, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        log('  R %3d | c %.20g (%+.2f%% vs the frontier)' % (R, float(c[0]), 100 * (float(c[0]) / float(FC) - 1)))
    else:
        log('  R %3d | NO-ROOT/spurious' % R)
