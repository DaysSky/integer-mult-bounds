"""THE V-SWEEP AT H=8 (ii19_nat45.py) — the untouched lever (the record's own direction!!).

THE RECORD'S OWN DATA: the E8-120 (v=120, h=8, R=420) prices 0.0016538; the P111 (v=111,
h=8, R=434) prices 0.0017444 — SMALLER v WON +5.4%!!!  THE V-SWEEP NEVER MEASURED.
HERE: the frontier word's TRUE hist (loaded!!) -> the mass-exact v-sweep at h=8 (the shape
scaled per the identity mass = 8R + CST + 2v*7, R ~ 4v - 10 (the hosting wall R <= 4v!!))
-> the c-vs-v map -> the verdict: does the c improve at v < 111?!?
"""
import os, sys, json
from collections import Counter
import numpy as np
from fractions import Fraction
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer
log = lambda *a: print(*a, file=sys.stderr, flush=True)
price = lambda hist, v, h, R: pricer.price({str(k): val for k, val in hist.items()}, v, h, R)
FR = os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price')
SRC = os.path.join('..', 'lorentzian-frame-cell-handoff')

# (1) the frontier word (the P111-R434!!)
for p in [os.path.join(SRC, 'ii19_pub2_p111-r434.json'), os.path.join(SRC, 'code', 'ii19_pub2_p111-r434.json'),
          os.path.join('.', 'ii19_pub2_p111-r434.json')]:
    if os.path.exists(p):
        SRC = p; break
else:
    # the search!!
    import glob
    cands = glob.glob(os.path.join('..', '**', 'ii19_pub2*.json'), recursive=True)
    log('the frontier-word candidates: %s' % cands)
    SRC = cands[0]
fr = json.load(open(SRC))
log('THE FRONTIER WORD: %s' % SRC)
log('  v %s | h %s | R %s | cst %s' % (fr.get('v'), fr.get('h'), fr.get('R'), fr.get('cst', '?')))
V0, H0, R0 = fr['v'], fr['h'], fr['R']
CST0 = fr.get('cst')
if CST0 is None:
    # the mass identity: mass = 8R + cst + 2v(h-1): the hist's mass!!
    hist0 = Counter(fr.get('hist', {}))
    mass = sum(int(r) * int(c) for r, c in hist0.items())
    CST0 = mass - (H0 * R0 + 2 * V0 * (H0 - 1))
    log('  the cst derived: %d (the mass %d)' % (CST0, mass))
hist0 = {int(k): int(v) for k, v in fr.get('hist', {}).items()}
log('  THE TRUE HIST: %s | the mass %d (the identity %d)' % (
    dict(sorted(hist0.items())), sum(r * c for r, c in hist0.items()),
    H0 * R0 + CST0 + 2 * V0 * (H0 - 1)))
c0 = price(hist0, V0, H0, R0)
log('  the price control: %s' % (c0[0] if c0 else 'NO-ROOT'))
FC = Fraction(str('0.001744385950814795279853'))

# (2) the mass-exact v-sweep: the shape scaled per the identity!!
def sweep(v, R, cst):
    M = 8 * R + cst + 2 * v * 7
    climb = M - cst
    # the shape: the R434's hist proportions on the CLIMB mass (mass-exact: the largest-remainder!!)
    base = {r: c for r, c in hist0.items()}
    bm = sum(r * c for r, c in base.items()) - CST0
    h = {}
    rem = climb
    frac = {r: Fraction(c * r, bm) for r, c in base.items() if r * c and r not in (0,)}
    # the counts: n_r = frac_r * climb / r
    acc = Counter()
    for r, f in frac.items():
        acc[r] = int(Fraction(climb) * f / r)
    mass_now = sum(r * c for r, c in acc.items())
    diff = climb - mass_now
    rr = sorted(frac, key=lambda r: -frac[r] * r)
    while diff > 0:
        for r in rr:
            if r <= diff:
                acc[r] += 1; diff -= r; break
        else:
            acc[max(1, diff)] += 1; diff = 0
    for r, c in {8: 8, 9: 1}.items() if False else []:
        pass
    # the copy ranks (the cst part): the cst distributed as the frontier's own copy structure!!
    # (the frontier's hist INCLUDES its copy; our climb-only scaling: add the copy back!!)
    copy = {r: c for r, c in hist0.items()}
    # the cst split: unknown -> use the E8-class {8: cst/8}-ish: the dominant copy at rank 8!!
    acc[8] += cst // 8
    rest = cst - 8 * (cst // 8)
    if rest: acc[rest] += 1
    return dict(acc)

log('')
log('THE V-SWEEP AT H=8 (the frontier shape, mass-exact!!) | R ~ 4v - 10 (the wall!!)')
for v in [120, 115, 111, 105, 100, 96, 92, 88, 84, 80]:
    for R in [min(4 * v - 10, R0), int(3.9 * v)]:
        if R < 100: continue
        cst = max(56, CST0 - 2 * (111 - v) // 2)      # the cst guess: shrinking with v!!
        h = sweep(v, R, cst)
        c = price(h, v, 8, R)
        if c and c[0]:
            pc = 100 * (float(c[0]) / float(FC) - 1)
            log('  v %3d | R %3d | cst %2d | c %s (%+.2f%% vs the frontier)' % (v, R, cst, c[0], pc))
        else:
            log('  v %3d | R %3d | cst %2d | NO-ROOT' % (v, R, cst))
