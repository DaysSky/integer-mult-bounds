"""THE V-SWEEP AT H=8 (ii19_nat46.py) — the frontier's TRUE HIST + the untouched v-lever!!

THE RECORD'S OWN DATA: the E8-120 (R420) 0.0016538 < the P111 (R434) 0.0017444 — SMALLER v
WON +5.4%!!  THE V-SWEEP NEVER MEASURED.  HERE: the frontier word replayed (the w21-oracle!!)
-> its TRUE hist -> the mass-exact v-sweep at h=8 (the shape scaled per the identity
mass = 8R + cst + 14v, R ~ 4v - 10 (the hosting wall!!)) -> the c-vs-v verdict map.
"""
import os, sys, json
from collections import Counter
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({int(k): int(val) for k, val in hist.items()}, v, h, R)

# (1) the frontier word's TRUE HIST (the w21-oracle replay!!)
sys.argv = ['ii19_p111w21.py']
exec('\n'.join(open('ii19_p111w21.py').readlines()[:94]))
hist0 = dict(hist0)
V0, H0, R0 = w['v'], w['h'], w['R']
CST0 = sum(r * c for r, c in hist0.items()) - (H0 * R0 + 2 * V0 * (H0 - 1))
log('')
log('THE FRONTIER: v %d | h %d | R %d | the cst %d | the mass %d' % (
    V0, H0, R0, CST0, sum(r * c for r, c in hist0.items())))
log('  THE TRUE HIST: %s' % dict(sorted(hist0.items())))
c0 = price(hist0, V0, H0, R0)
log('  the price control: %s' % (c0[0] if c0 else 'NO-ROOT'))
FC = Fraction(str('0.001744385950814795279853'))

# (2) the mass-exact v-sweep (the frontier's shape!!)
base = {int(r): int(c) for r, c in hist0.items() if int(r) > 0}
base[7] = base.get(7, 0) - 9                          # the copy: 9 rank-7 climbs (cst 63!!)
assert base[7] >= 0
bm = sum(r * c for r, c in base.items())               # the climb mass of the frontier!!
def sweep(v, R):
    climb = 8 * R + 2 * v * 7                          # the climb mass at the new (v, R)!!
    acc = Counter(); rem = climb
    for r in sorted(base, key=lambda r: -base[r] * r):
        n = int(Fraction(climb * (base[r] * r), bm) / r)   # the count: the mass fraction!!
        acc[r] = n; rem -= r * n
    rr = sorted(base, key=lambda r: -base[r])
    while rem > 0:
        for r in rr:
            if r <= rem:
                acc[r] += 1; rem -= r; break
        else:
            acc[max(1, rem)] += 1; rem = 0
    acc[7] += 9                                        # the copy (cst 63)!!
    return dict(acc)

log('')
log('THE V-SWEEP AT H=8 (the frontier shape, mass-exact!!)')
# the sanity: (111, 434) must reproduce ~the frontier!!
hh = sweep(111, 434)
log('  the sanity at (111, 434): %s (the frontier: %s)' % (dict(sorted(hh.items())), dict(sorted(hist0.items()))))
cc = price(hh, 111, 8, 434)
log('  the sanity price: %s' % (cc[0] if cc else 'NO-ROOT'))
for v in [120, 125, 130, 140, 150, 160, 180, 200, 220, 240, 280, 320]:
    R = 4 * v - 10
    h = sweep(v, R)
    c = price(h, v, 8, R)
    if c and c[0] and 1e-4 < float(c[0]) < 1e-2:
        pc = 100 * (float(c[0]) / float(FC) - 1)
        log('  v %3d | R %3d | c %.20g (%+.2f%% vs the frontier)' % (v, R, float(c[0]), pc))
    else:
        log('  v %3d | R %3d | NO-ROOT/spurious' % (v, R))
