"""THE NATIVE-121 CROSSING MAP (ii19_nat33.py) — the §1398-class structure (R ~ 158, the honest
native 121-line economy: ~101 pieces + ~47 carriers + 10 gathers, CST 73 measured) was NEVER
priced through the exact pricer.  Here: the mass-exact family ladder R 158..472 at (v=121, h=9),
copy-ranks {8: 8, 9: 1} (the nat30-proven CST-73 basis), the climb-mass shapes:
  A   : all-delta-1 (the finest/worst realistic)
  W4  : the word4's own shape (the record word's proportions)
  OG  : the one-gate shape (the A-ladder collapsed; the semi-concentrated)
  MX  : the max-concentration
Mass identity: mass(R) = 9R + 73 + 2*121*8 = 9R + 2009.
"""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

V, H = 121, 9
FRONT = mp.mpf('0.001744385950814795279853')
def pc(hist, R):
    try:
        return price(dict(hist), V, H, R)[0]
    except AssertionError:
        return None

COPY = {8: 8, 9: 1}   # the CST-73 basis (nat30: the proven floor)

def mass_exact(shape, M):
    """shape: {rank: mass-fraction}; returns a hist (Counter) with mass exactly M."""
    h = Counter()
    tot = sum(shape.values())
    for r, f in shape.items():
        h[r] = int(f * M / (tot * r))
    rem = M - sum(r * c for r, c in h.items())
    rr = sorted(shape, key=lambda r: -shape[r] * (M / r))
    while rem > 0:
        for r in rr:
            if r <= rem:
                h[r] += 1
                rem -= r
                break
        else:
            assert 1 <= rem <= 8, rem
            h[rem] += 1
            rem = 0
    assert sum(r * c for r, c in h.items()) == M
    return h

SHAPES = {
    'A  all-delta-1': {1: 1.0},
    'W4 the word4 shape': {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2},
    'OG one-gate': {1: 283, 8: 533, 9: 190},
    'MX max-conc': {9: 1.0},
}
log = lambda *a: print(*a, file=sys.stderr, flush=True)

log('THE NATIVE-121 CROSSING MAP (v=121, h=9, CST 73) | frontier %s' % mp.nstr(FRONT, 22))
for R in (158, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 400, 472):
    M = 9 * R + 2009
    row = []
    for name, sh in SHAPES.items():
        h = mass_exact(sh, M - sum(r * c for r, c in COPY.items()))
        for r, c in COPY.items():
            h[r] += c
        c = pc(h, R)
        row.append('%s %s' % (name.split()[0], ('NO-ROOT' if c is None else '%+.2f%%' % float((c / FRONT - 1) * 100))))
    log('R %3d (R/v %.2f): %s' % (R, R / V, ' | '.join(row)))
