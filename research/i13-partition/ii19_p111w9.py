"""THE P111-WORD v9 (ii19_p111w9.py) — THE GCHECK-REJECT's DIAGNOSIS (the climb-illegality's exact-structure!!)

THE w8-WORD (ii19_p111_word.json: R=455!!): the full-replay PASSED (the 677-finals (the vals!!))
BUT THE GCHECK: 'climb not nested (reg 2)' — THE §1928's-B-ENTANGLEMENT.  THIS-SCRIPT: the
gcheck-EXACT-replay (the Fractions-rref frames + the sub-containment + the dims-strictness!!):
(1) THE FIRST-ILLEGAL-CLIMB (the full-context: the phase, the gate, the register, the cur/target
    frames (the dims + the nestedness!!));
(2) THE AGGREGATE (ALL the illegal-climbs (by the phase + the register-class!!));
(3) THE FIX's-SCOPE-MEASURE (the star-builds'-srcs' chains vs the R420's-B-reads (the down-climb
    structure (the §1928's-'the-B's-down-climbs'!!!))).
"""
import json, time
from collections import Counter
from fractions import Fraction

W = json.load(open('ii19_p111_word.json', 'rt'))
V, H, R = W['v'], W['h'], W['R']
nreg = len(W['start'])
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
XMASK = (1 << V) - 1

# ============ (0) THE FRAMES (the exact rref-bases!!) ============
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
log('(0) the frames: %d (the rref!!)' % len(W['frames']))
fr = [rref(F, H) for F in W['frames']]
dims = [len(F) for F in fr]
log('    the dims-census: %s' % dict(sorted(Counter(dims).items())))
_sub = {}
def sub(a, b):
    k = (a, b)
    if k not in _sub:
        _sub[k] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
    return _sub[k]
def contains(F, x): return len(rref(list(fr[F]) + [x], H)) == dims[F]

# ============ (1) THE GCHECK-EXACT-REPLAY (the reporting!!) ============
cur = list(W['start']); val = [1 << i for i in range(nreg)]
first_bad = None; bad_climbs = []
def climb(r, F, phase, gi):
    global first_bad
    if cur[r] == F: return
    ok = sub(cur[r], F) and dims[F] > dims[cur[r]]
    if not ok:
        bad_climbs.append((phase, gi, r, cur[r], F, dims[cur[r]], dims[F], sub(cur[r], F)))
        if first_bad is None:
            first_bad = bad_climbs[-1]
    cur[r] = F
def run(gates, phase):
    for gi, (F, d, srcs) in enumerate(gates):
        for r in [d] + srcs: climb(r, F, phase, gi)
        for s in srcs: val[d] ^= val[s]

run(W['D'], 'D')
run(W['A'], 'A')
# the scatter
for t in range(V):
    for k in W['scatter'][t]: val[V + t] ^= val[W['ret'][k]]
run(W['B'], 'B')
run(W['C'], 'C')
for r in range(nreg): climb(r, W['final'][r], 'FINAL', -1)

if first_bad:
    ph, gi, r, cf, tf, cd, td, nst = first_bad
    rcls = 'source' if r < V else ('target' if r < 2 * V else 'helper')
    log('(1) THE FIRST-ILLEGAL-CLIMB: the phase %s (the gate %d!!) | the reg %d (%s!!)' % (ph, gi, r, rcls))
    log('    the cur-frame %d (the dim %d, the len %d!!) -> the F %d (the dim %d!!) | the nested %s' % (
        cf, cd, len(W['frames'][cf]), tf, td, nst))
log('(2) THE AGGREGATE: %d illegal-climbs' % len(bad_climbs))
by_phase = Counter(b[0] for b in bad_climbs)
by_cls = Counter(('source' if b[2] < V else ('target' if b[2] < 2 * V else 'helper')) for b in bad_climbs)
by_dir = Counter(('DOWN (the dims-decrease!!)' if b[6] < b[5] else
                  ('SAME-DIM (the incomparables!!)' if b[6] == b[5] else 'UP-NOT-NESTED!!')) for b in bad_climbs)
log('    by phase: %s | by class: %s | by dir: %s' % (
    dict(by_phase), dict(by_cls), dict(sorted(by_dir.items()))))
bad_regs = Counter(b[2] for b in bad_climbs)
log('    the bad-registers: %d (the top: %s)' % (len(bad_regs), bad_regs.most_common(8)))
for b in bad_climbs[:12]:
    ph, gi, r, cf, tf, cd, td, nst = b
    rcls = 'source' if r < V else ('target' if r < 2 * V else 'helper')
    log('    [%s] gate %d reg %d (%s): %d(d%d) -> %d(d%d) | the nested %s' % (
        ph, gi, r, rcls, cf, cd, tf, td, nst))
log('DONE — THE v9-DIAGNOSIS!!')
