"""nat168: THE TUNER AT THE W4 (the transport/Steinberg sweeps - never run on own8's emission).

The merge (nat167): +0.85 points. The TSF sweeps: the richer operator classes.
Route: the W4 (own8 format: frames as line-VECTORS) -> the hub format (frames as
line-INDEX lists) -> tune.py's transport_sweep + steinberg_sweep at the true fee
-> the back-adapter -> the hist + the price at fixed R.
"""
import json, sys
from collections import Counter

sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-tuned/tune')

W4 = json.load(open('ii19_own_word4.json'))
v = W4['v']; h = W4['h']; R = W4['R']

# (1) the adapter: the frames (the line-vector lists) -> the index lists
lidx = {}
for i, l in enumerate(W4['lines']):
    lidx[tuple(int(c) for c in l)] = i
    lidx[tuple(-int(c) for c in l)] = i
new_frames = []
bad = 0
for fr in W4['frames']:
    idxs = []
    for x in fr:
        t = tuple(int(c) for c in x)
        if t in lidx:
            idxs.append(lidx[t])
        else:
            bad += 1
    new_frames.append(sorted(set(idxs)))
print('the frames adapted: %d | the unmapped vectors: %d' % (len(new_frames), bad), flush=True)

Hub = dict(W4)
Hub['frames'] = new_frames
Hub['form'] = {'num': 'I8+U', 'den': 2} if h == 9 else W4.get('form')
import gzip
json.dump(Hub, gzip.open('/tmp/w4-hub.json.gz', 'wt'))
print('SAVED /tmp/w4-hub.json.gz', flush=True)

# (2) the tuner's load + the sweeps
try:
    import tune
    w = tune.load('/tmp/w4-hub.json') if hasattr(tune, 'load') else None
    if w is None:
        # try wlib
        sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-tuned')
        import wlib
        w = wlib.load('/tmp/w4-hub.json.gz')
    print('the tuner loaded the W4: R=%s' % (w.get('R') if isinstance(w, dict) else '?'), flush=True)
    print('the tune module API:', [x for x in dir(tune) if not x.startswith('_')][:20], flush=True)
except Exception as e:
    print('the tune load failed: %s' % e)
    import traceback
    traceback.print_exc()
