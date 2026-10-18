"""THE nat109: THE v=111 FRONTIER HEADROOM MAP (the bound-tight what-ifs!!)
THE QUESTION: the r434 (R=434, cst=63) sits ~45 registers over the v=111 copy bound (~389):
WHERE the trim's mass comes off (which ranks!!) decides the honest gain.
THE METHOD: the pricer what-ifs at (111, 8, R, hist-variants!!) — the mass identity at v=111:
  mass = 8R + 63 + 2*111*7 = 8R + 1833  (the r434's own: 5089 = 8*434 + 63 + 1554 ✓!!)
THE TRIM-SHAPES: the -DM = 8*(434-R) local mass off the r434's hist {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
  (a) off the rank-1s (the dying-wire ladders trimmed!!)
  (b) off the rank-2s
  (c) the 1/2-spread (the r434's own style!!)
  (d) off the rank-5s (its 120 5-climbs!!)
  (e) off the rank-4s (its 60!!)
"""
import os, sys, json
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'tword'))
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import gcheck
from pricer import price
import mpmath as mp
mp.mp.dps = 50

V, H = 111, 8
P111 = mp.mpf('0.001733052823330162099157')
BASE = dict({1: 1311, 2: 1339, 3: 69, 4: 45, 5: 103, 6: 12, 7: 18})  # the r434's OWN v=111 hist!!

def scen(R, dm_off):
    """the trim: dm = 8*(434-R) local mass off the ranks per the variant!!"""
    dm = 8 * (434 - R)
    hist = dict(BASE)
    for r, off in dm_off:
        take = min(off, hist.get(r, 0))
        hist[r] = hist.get(r, 0) - take
    hist = {r: c for r, c in hist.items() if c}
    mass = sum(r * c for r, c in hist.items())
    exp = 8 * R + 63 + 2 * V * (H - 1)
    assert mass == exp, ('the mass identity!!', mass, exp)
    c, prof, d = price(hist, V, H, R)
    return c, hist

def pct(c):
    if c is None: return 'no-root/hosting'
    return '%+.4f%%' % (float((c - P111) / P111) * 100)

log = print
log('THE nat109: THE v=111 FRONTIER HEADROOM MAP (the copy bound ~389!!)')
log('  the r434: R=434, hist %s, c = 0.0017444 (+0.6539%%!!)' % (BASE,))
log('')

VARIANTS = [
    ('(a) the rank-1 trim (the dying-wire ladders!!)', lambda dm: [(1, dm)]),
    ('(b) the rank-2 trim', lambda dm: [(2, dm)]),
    ('(c) the 1/2-spread (the r434-style!!)', lambda dm: [(1, dm // 2), (2, dm - dm // 2)]),
    ('(d) the rank-5 trim (its 120 5-climbs!!)', lambda dm: [(5, dm)]),
    ('(e) the rank-4 trim (its 60 4-climbs!!)', lambda dm: [(4, dm)]),
    ('(f) the 4/5-spread', lambda dm: [(4, dm // 2), (5, dm - dm // 2)]),
]

for name, fn in VARIANTS:
    log('THE TRIM: %s' % name)
    for R in (434, 420, 410, 400, 389, 380):
        try:
            c, hist = scen(R, fn(8 * (434 - R)))
            log('  R=%3d: c = %s  (%s)' % (R, ('None' if c is None else mp.nstr(c, 24)), pct(c)))
        except Exception as e:
            log('  R=%3d: %s' % (R, e))
    log('')

log('THE CONTROL (the untrimmed base at each R (the shape held, the mass padded at rank 1!!)):')
for R in (420, 400, 389):
    hist = dict(BASE)
    exp = 8 * R + 63 + 2 * V * (H - 1)
    mass = sum(r * c for r, c in hist.items())
    if mass < exp: hist[1] = hist.get(1, 0) + (exp - mass)
    c, prof, d = price(hist, V, H, R)
    log('  R=%3d (padded): c = %s  (%s)' % (R, mp.nstr(c, 24), pct(c)))
