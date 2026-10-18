"""THE PUBLISHED-P111's ret_frames-EXTRACTION (ii19_p111pub2.py) — THE GCHECK-PASS-MACHINERY!!!

THE PUBLISHED-WORDS (the R420-convention!!): the 'ret' = the 9-registers | the 'scatter' =
the ret-INDICES-rows | NO 'ret_frames' (the gcheck's-expectation!!) — THE EXTRACTION: the
gcheck-exact-replay (the D+A!!) -> the rets'-cur-frames-at-the-A-end = THE rf!!! -> the
patched-emission -> THE GCHECK (the PASS?! (the published!!!)) -> THE TRUE-C's + THE HISTS!!!
"""
import json, time
from collections import Counter
from fractions import Fraction

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

def rref(rows, n):
    m = [[Fraction(x) for x in r] for r in rows]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]; iv = 1 / m[r][c]; m[r] = [x * iv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]; m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return m[:r]

for name in ['p111', 'p111-tuned', 'p111-r434']:
    w = json.load(open('ii19_pub_%s.json' % name, 'rt'))
    V, H = w['v'], w['h']
    nreg = len(w['start'])
    fr = [rref(F, H) for F in w['frames']]
    dims = [len(F) for F in fr]
    _sub = {}
    def sub(a, b):
        if (a, b) not in _sub:
            _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
        return _sub[(a, b)]
    cur = list(w['start'])
    val = [1 << r for r in range(nreg)]
    for F, d, srcs in w['D']:
        for r in [d] + srcs:
            if cur[r] != F:
                assert sub(cur[r], F) and dims[F] >= dims[cur[r]], 'the D-climb!'
                cur[r] = F
        for s in srcs: val[d] ^= val[s]
    for F, d, srcs in w['A']:
        for r in [d] + srcs:
            if cur[r] != F:
                assert sub(cur[r], F) and dims[F] >= dims[cur[r]], 'the A-climb %d: %d->%d' % (r, cur[r], F)
                cur[r] = F
        for s in srcs: val[d] ^= val[s]
    ret = w['ret']
    rf = [cur[q] for q in ret]
    log('=== %s: the rets %s' % (name, ret))
    log('    the rf: %s (the dims %s!!) (the CST %d!!)' % (rf, [dims[f] for f in rf], sum(dims[f] for f in rf)))
    # the rets'-vals-check (the algebra: the stars?!)
    X = (1 << V) - 1
    log("    the rets-x-weights: %s" % [bin(val[q] & X).count('1') for q in ret])
    w['ret_frames'] = rf
    json.dump(w, open('ii19_pub2_%s.json' % name, 'w'))
    log('    -> ii19_pub2_%s.json' % name)
log('DONE — THE EXTRACTION (THE GCHECK-NEXT!!!)')
