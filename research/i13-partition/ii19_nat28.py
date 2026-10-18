"""THE GREEDY PER-GATE RAISE (ii19_nat28.py) — the rung-merge experiment toward the one-climax
bound ({1: 283, 8: 533, 9: 190} = +11.08% vs the frontier, measured).

The skip scan moved a REGISTER's whole level (order fixed) — 43 legal.  Here: every INDIVIDUAL
gate (A and B; D pinned at frame 0 by H2, C pinned at FULL by H4) can be raised to ANY strictly
containing frame from the word's own frame list (the shared 12-frames/perps/FULL supply the
containers).  Greedy fixpoint: simulate the current word once (operand values + cur frames at
each gate), prefilter containers (contain all operand content lines; nested above all cur),
try the highest container first, admit iff the full replay passes AND the exact price does not
fall; repeat until no admission.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
OUT = argv[0] if argv else 'ii19_word4_raise.json'
FRONT = mp.mpf('0.001744385950814795279853')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')

def word_with(re):
    return {ph: [[re.get((ph, gi), F), d, list(s)] for gi, (F, d, s) in enumerate(w[ph])] for ph in PH}
def replay_re(re):
    saved = {ph: w[ph] for ph in PH}
    w.update(word_with(re))
    try: return replay(w['A'])
    finally: w.update(saved)

def simulate(re):
    """one legal-order pass over the reframed D/A/ret/scatter/B; returns {(phase, gi): (val, cur)}
    snapshots (the operand values and current frames AT the gate) or None if anything breaks."""
    W = dict(word_with(re))
    cur = list(w['start']); val = [1 << r for r in range(nreg)]
    def climb(r, F):
        if cur[r] == F: return True
        if not (sub(cur[r], F) and dims[F] > dims[cur[r]]): return False
        cur[r] = F; return True
    snap = {}
    for F, d, srcs in W['D']:
        for r in [d] + list(srcs):
            if not climb(r, F): return None
        for s in srcs: val[d] ^= val[s]
    for gi, (F, d, srcs) in enumerate(W['A']):
        for r in [d] + list(srcs):
            if not climb(r, F): return None
        snap[('A', gi)] = (list(val), list(cur), F, d, list(srcs))
        for s in srcs: val[d] ^= val[s]
    for k, q in enumerate(w['ret']):
        if cur[q] != w['ret_frames'][k]: return None
    for t in range(V):
        for k in w['scatter'][t]: val[V + t] ^= val[w['ret'][k]]
    for gi, (F, d, srcs) in enumerate(W['B']):
        for r in [d] + list(srcs):
            if not climb(r, F): return None
        snap[('B', gi)] = (list(val), list(cur), F, d, list(srcs))
        for s in srcs: val[d] ^= val[s]
    return snap

# containers for every gate-frame in A/B (strict, from the word's frame list)
gframes = sorted(set(F for ph in ('A', 'B') for F, d, s in w[ph]))
conts = {}
for F in gframes:
    conts[F] = sorted((G for G in range(len(fr)) if dims[G] > dims[F] and sub(F, G)),
                      key=lambda G: -dims[G])
log('gate-frames in A/B: %d | containers per frame: %d..%d' % (
    len(gframes), min(len(conts[F]) for F in gframes), max(len(conts[F]) for F in gframes)))

def lines_of(bits):
    out, x = [], bits & ((1 << V) - 1)
    while x:
        b = x & -x; out.append(b.bit_length() - 1); x ^= b
    return out

re = {}
c0 = pc(hist0)
log('base c %s (%+.4f%% vs frontier)' % (mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))
for pas in range(8):
    snap = simulate(re)
    if snap is None:
        log('pass %d: simulation broke'); break
    e, hist, _ = replay_re(re)
    curbest = pc(hist)
    adm, tried = 0, 0
    for key in sorted(snap):
        vv, cc, F, d, srcs = snap[key]
        if key not in (('A', gi) for gi in range(len(w['A']))) and key not in (('B', gi) for gi in range(len(w['B']))):
            continue
        bits = vv[d]
        for s in srcs: bits |= vv[s]
        lines = lines_of(bits)
        for G in conts.get(F, ()):
            if not all(cont(G, s) for s in lines): continue
            if not all(cc[r] == G or (sub(cc[r], G) and dims[G] > dims[cc[r]]) for r in [d] + list(srcs)):
                continue
            tried += 1
            t2 = dict(re); t2[key] = G
            e2, hist2, _ = replay_re(t2)
            if e2 is None:
                c2 = pc(hist2)
                if c2 >= curbest:
                    re, curbest, adm = t2, c2, adm + 1
                    snap[key] = (vv, cc, G, d, srcs)
                    break
    e, hist, C2 = replay_re(re)
    assert e is None
    log('pass %d: admitted %d raises (candidates tried %d) | c %s (%+.4f%% vs frontier) | hist %s' % (
        pas, adm, tried, mp.nstr(curbest, 22), float((curbest / FRONT - 1) * 100), dict(sorted(hist.items()))))
    if adm == 0: break

e, hist, C2 = replay_re(re)
assert e is None
word = dict(w); word.update(word_with(re)); word['C'] = C2
word['stats'] = dict(w.get('stats', {}), per_gate_raises=len(re))
json.dump(word, open(OUT, 'w'))
log('emitted %s (c %s, %+.4f%% vs frontier)' % (OUT, mp.nstr(pc(hist), 22), float((pc(hist) / FRONT - 1) * 100)))
