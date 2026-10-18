"""THE REBUILD-CLASS CEILING PROBE (ii19_p111w26.py) — scratch: price the reshape classes.

The v2-class ceiling is measured (+1.038% over r434).  A structural rebuild would aim at the
larger merges; each is a pure mass-preserving redistribution of the base hist (per-register
start/final dims are fixed, so any legal word's mass is 5089 — the class deltas are count-level
redistributions with zero mass delta).  Prices are EXACT (pricer control reproduces the published
c at the base hist); they are CEILINGS for hypothetical words, not prices of existing words.
"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
P111 = mp.mpf('0.001733052823330162099157')
R = w['R']
def pc(hist): return price({int(k): int(v) for k, v in hist.items()}, V, H, R)[0]

c0 = pc(hist0)
log('base %s (%+.4f%% vs P111)  [control: the published r434 c]' % (mp.nstr(c0, 22), float((c0 / P111 - 1) * 100)))

N = 151   # standard (1,2,4,6)-ladder helpers
def reshaped(delta):
    h = Counter(hist0)
    for r, d in delta.items(): h[r] += d * N
    assert all(v >= 0 for v in h.values()), dict(h)
    assert sum(k * v for k, v in h.items()) == sum(k * v for k, v in hist0.items())
    return h

classes = {
    'v2  (0,1,2,4,6)->(0,2,4,6): {1: -2, 2: +1}': {1: -2, 2: 1},
    'v4  (0,2,4,6)->(0,6):       {1: -2, 2: -2, 6: +1}': {1: -2, 2: -2, 6: 1},
    'v4b (2,4,6)->(4,6):         {2: -2, 4: +1}': {2: -2, 4: 1},
    'v6  (0,4,6) one big skip:     {1: -2, 2: -1, 4: +1}': {1: -2, 2: -1, 4: 1},
}
for name, delta in classes.items():
    h = reshaped(delta)
    c = pc(h)
    log('%-52s hist %s' % (name, dict(sorted(h.items()))))
    log('    c %s  (%+.4f%% vs r434, %+.4f%% vs P111)' % (mp.nstr(c, 22),
        float((c / c0 - 1) * 100), float((c / P111 - 1) * 100)))
