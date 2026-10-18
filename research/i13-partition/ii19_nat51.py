"""THE LORENTZIAN WALL-RATE MAP (ii19_nat51.py) — the 2-class (v=240, h=10) at ITS OWN WALL!!

THE USER'S CATCH: the E8-class (the R420/R434/v-sweep targets) is POSITIVE-DEFINITE — NOT
LORENTZIAN. THE PROGRAM: the II19-family word above the published benchmark (the R434's c!!).
THE REDIRECTION (the nat49 lesson: the old words sit BELOW their walls (the R420: R/v 3.5 vs
the wall 3.92!!)): the 240-line 2-class (the LEGAL Lorentzian (the h=10 (the §88!!))) — its
record-measured band (A +5.17%..D +27.62% at R=317!!) sits at R/v = 1.32 — FAR BELOW ITS WALL
(4v = 960!!).  THE WALL-RATE MODEL: NEVER MEASURED.
HERE: the A/B/C/D shapes + the frontier's shape at (240, 10, R) for R 317..950!!
"""
import os, sys, json
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))
V, H = 240, 10
CST = 144          # the record's 18-retained class (the slots session!!)

# the shapes: the record's A/B/C/D (the 2-class model (the slots session!!)) + the frontier's!!
def shape(fracs, climb):
    acc = Counter(); rem = climb
    for r, f in sorted(fracs.items(), key=lambda kv: -kv[1]):
        n = int(Fraction(climb) * f / r)
        acc[r] = n; rem -= r * n
    while rem > 0:
        for r in sorted(fracs, key=lambda r: -fracs[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[8] += CST // 8
    rest = CST - 8 * (CST // 8)
    if rest: acc[rest] += 1
    return dict(acc)

climb_at = lambda R: H * R + 2 * V * (H - 1) - CST
# A: all-delta-1 (the finest!!)
A = shape({1: Fraction(1)}, climb_at(317))
# B/C/D: the record's (the §453-era (the R420-calibrated!!)): rebuild at each R via fractions!!
# the R420-proportions (the record's D-calibration (the R420's climb proportions!!):
D_FR = {1: Fraction(1320, 2940), 2: Fraction(1440, 2940), 4: Fraction(60, 2940), 5: Fraction(120, 2940)}
# B: the mid (the 50/50-ish (the 1/2-heavy + the 4/5s!!)): use the frontier's climb-shape!!
FR = {1: Fraction(1311, 5026), 2: Fraction(1339, 5026), 3: Fraction(69, 5026),
      4: Fraction(45, 5026), 5: Fraction(103, 5026), 6: Fraction(12, 5026), 7: Fraction(9, 5026)}
MX = {9: Fraction(1)}                       # the max-concentration (rank 9!!)

log('THE LORENTZIAN WALL-RATE MAP: the 2-class (v=240, h=10, CST 144!!) at R 317..950 (the wall 960!!)')
log('  (the record measured band at R=317: A +5.17% / B +12.78% / C +24.57% / D +27.62%!!)')
for R in [317, 350, 400, 460, 520, 590, 660, 730, 800, 870, 940, 950]:
    climb = climb_at(R)
    row = []
    for nm, fr in [('A', {1: Fraction(1)}), ('FR', FR), ('D', D_FR), ('MX', MX)]:
        h = shape(fr, climb)
        c = price(h, V, H, R)
        if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
            row.append('%s %+.1f%%' % (nm, 100 * (float(c[0]) / float(FC) - 1)))
        else:
            row.append('%s NO-ROOT' % nm)
    log('  R %3d (R/v %.2f) | %s' % (R, R / V, ' | '.join(row)))
