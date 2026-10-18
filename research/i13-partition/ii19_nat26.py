"""THE CROSSING-TARGET MAP (ii19_nat26.py) — where does the 121-class Lorentzian word cross?

The shared-cell rebuild's two levers stack: the concentration grammar (the one-gate family:
+14.87% at R=472, measured) and the R-reduction (the record's nat12c/13b honest class, R~350-460).
The map: mass-exact hist families priced exactly at (v=121, h=9, R) for R down the ladder —
mass(R) = 9R + 73 + 2*121*8 = 9R + 2009 (the CST-73 smart basis).  Families:
  (a) the word4's own hist, rescaled mass-exact (the reference shape);
  (b) the one-gate-collapse shape (nat22's), rescaled mass-exact;
  (c) the max-concentration shape (all mass at rank 9, largest-remainder, r <= rem);
  (d) the R420-proportioned D-variant (the record's calibrated family, on the non-retained mass).
The crossing: c > 0.001744385950814795279853 (the frontier).
"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
FRONT = mp.mpf('0.001744385950814795279853')

def mass_exact(shape_mass, frac):
    """largest-remainder mass-exact hist from rank MASS fractions, with the r <= rem constraint."""
    M = shape_mass
    raw = {r: f * M / r for r, f in frac.items()}     # expected COUNTS (frac = mass share)
    h = {r: int(x) for r, x in raw.items()}
    rem = M - sum(r * c for r, c in h.items())
    while rem > 0:
        best = max((r for r in raw if rem >= r and h.get(r, 0) >= 1 and (raw[r] - h[r]) >= 0.999),
                   key=lambda r: (raw[r] - h[r]) / r, default=None)
        if best is None:
            best = max((r for r in (1, 2, 3, 4, 5, 6, 7, 8, 9) if rem >= r), default=None)
            if best is None: break
            h[best] = h.get(best, 0) + 1; rem -= best; continue
        h[best] += 1; rem -= best
    return {r: c for r, c in h.items() if c}, rem

def rescaled(base_hist, M):
    """scale the base hist's rank distribution to mass M (largest-remainder, r<=rem)."""
    bm = sum(k * v for k, v in base_hist.items())
    frac = {r: (r * c) / bm for r, c in base_hist.items()}   # mass fractions per rank
    return mass_exact(M, frac)

W4 = dict(hist0)                                   # the word4's own hist (mass 6257)
OG = {1: 618, 2: 721, 3: 331, 4: 84, 6: 332, 8: 105, 9: 4}   # the one-gate collapse (nat22)
DVAR = {1: 0.2619, 2: 0.5714, 4: 0.0476, 5: 0.1190}          # the R420 climb proportions

log('R-ladder: mass(R) = 9R + 2009 | the crossing: c > %s' % mp.nstr(FRONT, 22))
log('%-5s %6s | %-24s | %-24s | %-24s | %-24s' % ('R', 'mass', 'word4-shape', 'one-gate-shape', 'max-concentration', 'D-variant'))
for R in (472, 460, 440, 420, 400, 380, 360, 340, 320, 300, 280, 260):
    M = 9 * R + 2009
    row = []
    for name, fam in (('w4', W4), ('og', OG)):
        h, rem = rescaled(fam, M)
        c = price(h, V, H, R)[0]
        row.append((h, rem, c))
    # max concentration: all mass at rank 9 + remainder
    h9 = {9: M // 9}
    rem = M - 9 * (M // 9)
    if rem: h9[rem] = 1
    c9 = price(h9, V, H, R)[0]
    # D-variant on the non-retained mass: retained = 73-ish at their frame ranks; approximate:
    # the D fractions on the whole mass (the record's convention: the non-retained climb mass)
    hD, remD = mass_exact(M, DVAR)
    cD = price(hD, V, H, R)[0]
    def fmt(c):
        if c is None: return 'NO-ROOT      '
        return '%+.3f%% (%s)' % ((c / FRONT - 1) * 100, mp.nstr(c, 8))
    log('%-5d %6d | %-24s | %-24s | %-24s | %-24s' % (R, M,
        fmt(row[0][2]), fmt(row[1][2]), fmt(c9), fmt(cD)))
    log('      rem w4=%d og=%d D=%d | hists: og %s | max %s' % (
        row[0][1], row[1][1], remD, dict(sorted(row[1][0].items())), dict(sorted(h9.items()))))
