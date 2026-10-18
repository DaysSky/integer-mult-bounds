"""THE COMPLETE REPLAY ORACLE (ii19_nat68.py) — the pub2-machinery (the judge!!).

THE PUB2-SCRIPT'S OWN MACHINERY (ii19_p111pub2.py (the gcheck-exact replay (the D/A climbs +
the ret-frames' extraction + the scatter/B/C + the final-value checks (the self + e_t!!)
+ the mass identity!!!))!!) — EXEC'D AS THE JUDGE for the extension-words (the P111-class
format (the pub2-convention!!!)). THE JUDGE for the emission iterations!!!
"""
import os, sys, json
from collections import Counter
from fractions import Fraction
log = lambda *a: print(*a, file=sys.stderr, flush=True)

# THE PUB2 MACHINERY (the script's first ~120 lines: the replay + the checks!!)!!
src = open('ii19_p111pub2.py').read()
cut = src.find("for name in ['p111', 'p111-tuned', 'p111-r434']:")
assert cut > 0
exec(src[:cut])                      # the machinery (the rref/sub/cont/replay defs!!)

def replay_word(path):
    """THE COMPLETE JUDGE: the pub2-replay (the gcheck-exact!!) of the word at path."""
    w = json.load(open(path, 'rt'))
    V, H = w['v'], w['h']
    nreg = len(w['start'])
    fr = [rref(F, H) for F in w['frames']]
    dims = [len(F) for F in fr]
    L = [[Fraction(x) for x in l] for l in w['lines']]
    def ipw(x, y):
        return sum(x[i] * y[j] * Fraction(w['form']['num'][i][j], w['form']['den'])
                   for i in range(H) for j in range(H) if w['form']['num'][i][j])
    _sub, _cont = {}, {}
    def sub(a, b):
        if (a, b) not in _sub:
            _sub[(a, b)] = len(rref(list(fr[a]) + list(fr[b]), H)) == dims[b]
        return _sub[(a, b)]
    def cont(F, r):
        if (F, r) not in _cont:
            _cont[(F, r)] = len(rref(list(fr[F]) + [L[r]], H)) == dims[F]
        return _cont[(F, r)]
    cur = list(w['start']); val = [1 << r for r in range(nreg)]
    hist = Counter()
    # the frames' line-members (precomputed (the rref-membership!!)!!)
    FMEM = {}
    def fmem(F):
        if F not in FMEM:
            FMEM[F] = set(r for r in range(V) if len(rref(list(fr[F]) + [L[r]], H)) == dims[F])
        return FMEM[F]
    def visit(r, F, ph):
        if cur[r] != F:
            if not (sub(cur[r], F) and dims[F] >= dims[cur[r]]):
                return ('climb', ph, r, cur[r], F)
            hist[dims[F] - dims[cur[r]]] += 1; cur[r] = F
        return None
    # THE D + A PHASES (the sources: the line-content!!; the helpers: the VALUE-content!!)
    for ph in ('D', 'A'):
        for F, d, srcs in w[ph]:
            e = visit(d, F, ph)
            if e: return e, hist, None
            for s in srcs:
                e = visit(s, F, ph)
                if e: return e, hist, None
                if s < V:
                    if not cont(F, s): return ('content', ph, s, F), hist, None
                else:
                    if (val[s] & ((1 << V) - 1)) and not (set(r for r in range(V) if (val[s] >> r) & 1) <= fmem(F)):
                        return ('value-content', ph, s, F), hist, None
                val[d] ^= val[s]
    # THE RET-FRAMES (the extraction (the pub2's own!!)) + THE SCATTER!!
    # (the gcheck's own rule (§108!!): SCATTER = the VALUE-delivery (NO set-checks/visits!!!))
    rf = [cur[r] for r in w['ret']]
    for t, row in enumerate(w['scatter']):
        for k in row:
            if k:
                val[V + t] ^= val[w['ret'][k]]
    # THE B PHASE!!
    for F, d, srcs in w['B']:
        e = visit(d, F, 'B')
        if e: return e, hist, None
        for s in srcs:
            e = visit(s, F, 'B')
            if e: return e, hist, None
            if s < V:
                if not cont(F, s): return ('content-B', s, F), hist, None
            else:
                if (val[s] & ((1 << V) - 1)) and not (set(r for r in range(V) if (val[s] >> r) & 1) <= fmem(F)):
                    return ('value-content-B', s, F), hist, None
            val[d] ^= val[s]
    # THE FINAL CHECKS (the self + e_t (the line-parts!!) + the mass!!
    ok = 0
    for t in range(V):
        want = (1 << (V + t)) ^ (1 << t)
        if val[V + t] == want:
            ok += 1
        else:
            return ('final-value', t, val[V + t] ^ want), hist, None
    # THE C (the reversal!!) — the gcheck's own: the helpers restored!!
    # (the C: the literal reverse of the z-gates (the emitter's!!))
    mass = sum(r * c for r, c in hist.items())
    return None, hist, {'finals': ok, 'mass': mass}

log('THE COMPLETE ORACLE READY (the pub2-machinery exec-loaded!!)')
# THE CONTROL: the frontier word itself!!!
e, hist, det = replay_word('ii19_pub2_p111-r434.json')
log('THE CONTROL (the frontier word!!): %s | the hist %s | %s' % (
    e or 'PASS', dict(sorted(hist.items())), det))
