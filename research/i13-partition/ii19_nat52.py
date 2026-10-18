"""THE 2-CLASS WALL-RATE REDO (ii19_nat52.py) — the record's exact shapes + the unmeasured zone.

THE RECORD'S h=10 GRID (ii19_2class_h10.py (the §1393!!)) STOPPED AT R=700 (R/v 2.92!!) —
THE WALL-RATE ZONE (R 700-960 (R/v to 4!!)) NEVER MEASURED + THE FRONTIER-SHAPE TRANSPLANT
NEVER RUN AT h=10.  HERE: the record's hist_true VERBATIM (A/B/C/D, CST 162!!) + the
frontier's climb-shape + the MX: the FULL MAP R 280..950.
"""
import os, sys
from collections import Counter
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)
FC = Fraction(str('0.001744385950814795279853'))
V, H = 240, 10
CST = 162

# the record's hist_true (VERBATIM (the float-shape models, mass-exact by construction!!))
def hist_true(R, variant):
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    if variant == 'A': hist = {1: climb, 9: 18.0}
    elif variant == 'B': hist = {1: 0.50 * climb, 2: 0.25 * climb / 2.0, 5: 0.25 * climb / 5.0, 9: 18.0}
    elif variant == 'D': hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                                 5: 0.119 * climb / 5.0, 9: 18.0}
    elif variant == 'C': hist = {1: 0.30 * climb, 2: 0.20 * climb / 2.0, 5: 0.50 * climb / 5.0, 9: 18.0}
    return {k: int(n) for k, n in hist.items()}

# the frontier's climb-shape transplant (the mass-exact largest-remainder!!):
FR = {1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 9}    # the frontier's climb part!!
def front_transplant(R):
    climb = H * R + 2 * V * (H - 1)
    bm = sum(r * c for r, c in FR.items())
    acc = Counter()
    for r in sorted(FR, key=lambda r: -FR[r] * r):
        n = int(Fraction(climb * (FR[r] * r), bm) / r)
        acc[r] = n
    rem = climb - sum(r * c for r, c in acc.items())
    while rem > 0:
        for r in sorted(FR, key=lambda r: -FR[r]):
            if r <= rem: acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[9] += 18                                # the copy (CST 162!!)
    return dict(acc)

def mx(R):
    climb = H * R + 2 * V * (H - 1)
    n9 = climb // 9 + 18
    rest = climb - 9 * (climb // 9)
    h = {9: n9}
    if rest: h[max(1, rest)] = 1
    return h

log('THE 2-CLASS AT THE HONEST h=10 (v=240, CST 162!!) — THE FULL R MAP (the record grid stopped at 700!!)')
for R in [280, 317, 350, 400, 460, 520, 590, 660, 700, 760, 820, 880, 940, 950]:
    row = []
    for nm, h in [('A', hist_true(R, 'A')), ('B', hist_true(R, 'B')), ('C', hist_true(R, 'C')),
                  ('D', hist_true(R, 'D')), ('FR', front_transplant(R)), ('MX', mx(R))]:
        c = price(h, V, H, R)
        if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
            row.append('%s %+.1f' % (nm, 100 * (float(c[0]) / float(FC) - 1)))
        else:
            row.append('%s --' % nm)
    log('  R %3d (R/v %.2f) | %s' % (R, R / V, ' | '.join(row)))
