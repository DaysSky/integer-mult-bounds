"""THE CHAIN TRACE (ii19_nat75.py) — the reg-249 failure's exact point!!

THE GCHECK RULE (§593!!): the climbs STRICTLY dim-increasing + nested (sub!!). THE REJECT
moved 240 -> 249 (the first 9 pass!!). HERE: the word's replay (the same semantics (the
nat68/oracle-class!!)) with the per-gate traces (the reg-249's visit-sequence!!).
"""
import json, sys
from collections import Counter
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

w = json.load(open('ii19_ext120_ladder2.json', 'rt'))
v, h = w['v'], w['h']
nreg = len(w['start'])

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

fr = [rref([[Fraction(x) for x in row] for row in F], h) for F in w['frames']]
dims = [len(F) for F in fr]
L = [[Fraction(x) for x in l] for l in w['lines']]
_sub = {}
def sub(a, b):
    if (a, b) not in _sub:
        _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), h)) == dims[b]
    return _sub[(a, b)]
cur = list(w['start'])
TARGET_REG = 1
visits = []
def climb(r, F, ph):
    if cur[r] == F:
        visits.append((ph, r, cur[r], F, 'no-climb'))
        return None
    ok = sub(cur[r], F) and dims[F] > dims[cur[r]]
    visits.append((ph, r, cur[r], F, 'CLIMB %d->%d %s' % (dims[cur[r]], dims[F], 'OK' if ok else 'FAIL!!!')))
    if not ok:
        return 'climb not nested (reg %d): %d (dim %d) -> %d (dim %d) | sub %s' % (
            r, cur[r], dims[cur[r]], F, dims[F], sub(cur[r], F))
    cur[r] = F
    return None
for ph in ('D', 'A'):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in [d] + srcs:
            e = climb(r, F, '%s[%d]' % (ph, gi))
            if e:
                log('THE FAILURE: %s' % e)
                log('THE REG %d VISITS:' % TARGET_REG)
                for vv in visits:
                    if vv[1] == TARGET_REG:
                        log('  %s' % (vv,))
                log('THE LAST 8 VISITS (all regs!!):')
                for vv in visits[-8:]:
                    log('  %s' % (vv,))
                sys.exit(1)
log('THE D+A PHASES PASS (the reg-249 chain OK?!)')
for vv in visits:
    if vv[1] == TARGET_REG:
        log('  reg 249: %s' % (vv,))
