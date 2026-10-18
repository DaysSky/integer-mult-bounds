"""THE PUBLISHED-P111-FAMILY CONVERSION (ii19_p111pub.py) — THE GCHECK-FORMAT + THE TRUE-STRUCTURES!!!

THE PUBLISHED-WORDS (the old-convention (the form-TAG (the §61!!) + the line-index-frames!!)):
  - e8-bit-p111/data/bitE8mut-p111.json.gz              (the base!!)
  - e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz   (the TUNED (the c-reference 0.001733427!!))
  - e8-bit-p111-r434/data/bitE8mut-p111-r434.json.gz    (the R434 (the FRONTIER (the c 0.001744386!!!)))
  - e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz        (the E1 (the c 0.001734473!!))

THE CONVERSION: the form -> {num: I8, den: 2} (the ip_half-convention ✓!!) | the frames ->
the VECTOR-lists (the line-index-lists -> the lines[i]-vectors (the w8's-own!!)) -> THE
GCHECK (the PASS-expected (the published!!!)) -> THE TRUE-STRUCTURES (the R | the CST | the
hist | the c!!) -> THE SHAVE-TARGETS!!!
"""
import gzip, json, time, sys
from collections import Counter

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

WORDS = [
    ('p111', '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111/data/bitE8mut-p111.json.gz'),
    ('p111-tuned', '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz'),
    ('p111-r434', '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-r434/data/bitE8mut-p111-r434.json.gz'),
    ('p111-e1', '/Users/dayssky/integer-mult-bounds/research/e8-bit-p111-e1/data/bitE8mut-p111-e1.json.gz'),
]
for name, path in WORDS:
    w = json.load(gzip.open(path, 'rt'))
    v0 = w['v']
    lines = w['lines']
    log('=== %s (%s): v=%d h=%d R=%d | the form %s | the frames %d' % (
        name, path, w['v'], w['h'], w['R'], w.get('form'), len(w['frames'])))
    # the frames'-census (the line-index-lists (the ints!!) vs the raw-vectors!!)
    kinds = Counter()
    for fl in w['frames']:
        for e in fl:
            kinds['int' if isinstance(e, int) else 'vec'] += 1
    log('    the frame-entries: %s' % dict(kinds))
    # the conversion!!
    w2 = dict(w)
    w2['form'] = dict(num=[[1 if i == j else 0 for j in range(w['h'])] for i in range(w['h'])], den=2)
    w2['frames'] = [[[x for x in lines[i]] if isinstance(i, int) and i < v0 else list(i)
                     for i in fl] for fl in w['frames']]
    out = 'ii19_pub_%s.json' % name
    json.dump(w2, open(out, 'w'))
    log('    CONVERTED -> %s' % out)
log('DONE — THE CONVERSION (THE GCHECK-NEXT!!!)')
