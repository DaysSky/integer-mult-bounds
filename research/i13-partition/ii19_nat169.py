"""nat169: THE FULL TSF TUNING AT THE W4 (the never-tuned word, at its own fee).

The tune434 driver pattern: Tn = tune.Tuner(base, a=fee); the TSF loop over sections AB
until fixed; w = Tn.word(); wlib.paid (the assertion battery); the hist + the price.
"""
import json, gzip, sys
from collections import Counter

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-tuned/tune')
import tune
import wlib

base = wlib.load('/tmp/w4-hub.json.gz')
before = wlib.paid(base)
print('the W4 hub-loaded: R=%s | the paid profile: %s' % (base.get('R'), before), flush=True)

A_FEE = 0.0013359  # the W4's own c
Tn = tune.Tuner(base, a=A_FEE)
total, passes = 0, 0
for _ in range(8):
    n = 0
    for ch in 'TSF':
        for sec in 'AB':
            V = Tn.view(sec)
            ap = (tune.transport_sweep(V, verbose=False) if ch == 'T' else
                  tune.steinberg_sweep(V, verbose=False) if ch == 'S' else
                  tune.transport_sweep(V, verbose=False, allow_move=False))
            n += len(ap)
    total += n
    passes += 1
    print('  pass %d: %d moves' % (passes, n), flush=True)
    if not n:
        break

w = Tn.word()
after = wlib.paid(w)
assert sum(k*c for k, c in before.items()) == sum(k*c for k, c in after.items()), 'MASS CHANGED!'
print('the tuner fixed point: %d passes, %d moves' % (passes, total), flush=True)
print('the paid profile: %s -> %s' % (before, after), flush=True)

sha = wlib.save(w, '/tmp/w4-tuned.json.gz')
print('SAVED /tmp/w4-tuned.json.gz (sha %s)' % sha, flush=True)

# the price at the tuned word
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer

v = w['v']; h = w['h']; R = w['R']
# the hist: the paid profile is the LOCAL hist (the climb census!)
hh = dict(after)
# the copies: the ret-frames
frames = w['frames']
LCDIM = {0: 0, 1: 1, 2: 2, 3: 3, 12: 4, 13: 5, 30: 6, 64: 8, 120: 8, 121: 9}
dims = [LCDIM[len(fr)] if isinstance(fr, list) and len(fr) in LCDIM else None for fr in frames]
for k in w['ret_frames']:
    hh[dims[k]] = hh.get(dims[k], 0) + 1
res = pricer.price(hh, v, h, R)
pub = 0.001733052823330162099157
print('THE TUNED W4 PRICE: %s' % (res[0],), flush=True)
try:
    print('  vs frontier: %+.2f%%' % (100*(float(res[0])/pub - 1)))
except Exception:
    print('  (no root: %s)' % (res[2] if len(res) > 2 else '?',))
