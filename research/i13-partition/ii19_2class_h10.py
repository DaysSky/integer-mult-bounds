"""THE HONEST h: THE 2-CLASS WORD LIVES IN THE 10-DIM AMBIENT (h=10!!) — the decisive price check.

THE DISCOVERY (SS1383-1384, reading the identity-word template + gcheck): the 2-class
system's lines (α,0,0) and (α,1,0) span a 9-dim space whose restricted form is DEGENERATE
(the radical: the level direction (0,1,0)).  The format requires every listed frame
(incl. FULL) NONDEGENERATE (the exact Gram determinant!!), so the FULL frame must be the
10-dim ambient: h = 10, NOT 9.  The t-perps: dim 9, nondegenerate (the normals
(α, 0, a_t) have norm 2 != 0 ✓).

THE CONSEQUENCE: the SS1354/SS1374 crossing bands were computed at h=9 (m=73) — the h was
wrong.  THE HONEST PRICE: h=10 (m=82), v=240, the mass identity
    ident = 10*R + 162 + 2*240*9      (the cst: the retained's copy mass: 18 x 9 at the
    dim-9 gather frames; the sources+targets: 2v(h-1) = 4,320).

THIS SCRIPT: the h=10 band — the A/B/C/D variants at the R grid — THE CROSSING VERDICT AT
THE HONEST h.  IF the band is above the frontier: THE BUILD PROCEEDS AT h=10!!  IF not:
the h=9 -> h=10 penalty kills the crossing (the honest record).
Also: the E8 control re-verified (h=8), and the slot-script's class-1 d0 bug noted (the
level direction double-counted: the conservative direction, the honest capacities better).
"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

FRONTIER = 0.001744386
V = 240
H = 10          # THE HONEST h (the 10-dim ambient; the 9-dim span is degenerate!!)
CST = 162       # the retained's copy mass: 18 gathers x rank 9 at the dim-9 class-perp frames

def hist_true(R, variant):
    """the mass-fraction shape models at the honest h=10: the climb mass (10R + 4,320)
    distributed per the variant's fractions (each frac_r x climb of MASS at rank r, i.e.
    frac_r x climb / r EDGES), plus the retained's copy children {9: 18} (mass 162).
    The fractions sum to 1.000 exactly -> mass-exact BY CONSTRUCTION."""
    climb = 1.0 * H * R + 2.0 * V * (H - 1)
    ident = climb + CST
    if variant == 'A':
        hist = {1: climb, 9: 18.0}
    elif variant == 'B':
        hist = {1: 0.50 * climb, 2: 0.25 * climb / 2.0, 5: 0.25 * climb / 5.0, 9: 18.0}
    elif variant == 'D':
        hist = {1: 0.262 * climb, 2: 0.571 * climb / 2.0, 4: 0.048 * climb / 4.0,
                5: 0.119 * climb / 5.0, 9: 18.0}
    else:
        hist = {1: 0.30 * climb, 2: 0.20 * climb / 2.0, 5: 0.50 * climb / 5.0, 9: 18.0}
    mass = sum(k * n for k, n in hist.items())
    assert abs(mass - ident) < 2, (variant, mass, ident)
    return {k: int(n) for k, n in hist.items()}

print('=== THE 2-CLASS WORD AT THE HONEST h=10 (v=240, m=82) ===')
print('the mass identity: 10R + 162 + 4,320; the frontier %.9f' % FRONTIER)
print()
best = None
for R in (280, 317, 350, 400, 430, 460, 490, 520, 560, 590, 620, 660, 700):
    line = 'R %3d (mass/v %5.1f): ' % (R, (10.0 * R + CST + 4320) / V)
    for var in ('A', 'B', 'C', 'D'):
        hist = hist_true(R, var)
        cc, _, det = pprice(hist, V, H, R)
        if cc is None:
            line += '%s NO-ROOT  ' % var
        else:
            pct = (cc / FRONTIER - 1) * 100
            line += '%s %+.2f%%  ' % (var, pct)
            if best is None or cc > best[0]:
                best = (cc, R, var, pct)
    print(line)
print()
if best:
    print('THE BEST at the honest h=10: %s variant, R=%d: c = %.9f (%+.2f%% vs frontier)'
          % (best[2], best[1], best[0], best[3]))
    if best[0] > FRONTIER:
        print('THE CROSSING SURVIVES THE HONEST h!!  THE BUILD PROCEEDS AT h=10 (the 10-dim ambient,')
        print('the dim-9 t-perps, the mass identity 10R + 162 + 4,320).')
    else:
        print('THE h=9 -> h=10 PENALTY KILLS THE CROSSING: the honest negative.')
else:
    print('NO ROOTS at the honest h=10: the regimes too light.')
