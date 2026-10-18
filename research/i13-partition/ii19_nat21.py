"""THE WORD4 LEVEL-SKIP SCAN (ii19_nat21.py) — the Lorentzian push: w23's scan on OUR OWN word.

r434's scan: 0/2232 legal (the co-operand wall: raising a gate lifts its co-operands
irreversibly; the unshared geometry (single-source cells/homes) made every skip illegal).  The
word4 has REAL sharing (12 sources per dim-4 frame; 3 helpers per cell; 98 helpers per dim-8
frame).  Question: does the sharing dissolve the wall — are there LEGAL level-skips here?

The scan (w23's, verbatim): for every register r and every intermediate level F_b (entered by a
climb), raise all of r's gates at F_b to the next frame (the next D/A/B level, C's frame 1, or
final[r]).  Gate order unchanged -> every value untouched.  Each candidate: the gcheck-exact
replay, then the exact price; the legal price-raisers are greedy-accumulated (best gain first).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
OUT = argv[0] if argv else 'ii19_word4_skip.json'
FRONT = mp.mpf('0.001744385950814795279853')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')

def word_with(re):
    """re: {(phase, pos): frame} -> reframed D/A/B gate lists."""
    return {ph: [[re.get((ph, gi), F), d, list(s)] for gi, (F, d, s) in enumerate(w[ph])] for ph in PH}
def replay_re(re):
    saved = {ph: w[ph] for ph in PH}
    w.update(word_with(re))
    try: return replay(w['A'])
    finally: w.update(saved)

def levels(re):
    lev = defaultdict(list)
    G = word_with(re)
    for ph in PH:
        for gi, (F, d, srcs) in enumerate(G[ph]):
            for r in [d] + srcs:
                if not lev[r] or lev[r][-1][0] != F:
                    lev[r].append([F, []])
                lev[r][-1][1].append((ph, gi))
    return lev

inC = set(r for F, d, srcs in w['C'] for r in [d] + srcs)
lev0 = levels({})
cands = []
for r in range(nreg):
    Ls = lev0[r]
    for j, (Fb, gates) in enumerate(Ls):
        if Fb == w['start'][r]: continue                    # not entered by a climb
        Fc = Ls[j + 1][0] if j + 1 < len(Ls) else (1 if r in inC else w['final'][r])
        if Fc == Fb: continue
        cands.append((r, Fb, Fc, tuple(gates)))
c0 = pc(hist0)
log('(1) intermediate levels: %d | base c %s (%+.4f%% vs the frontier)' % (
    len(cands), mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))

legal, why = [], Counter()
for n, (r, Fb, Fc, gates) in enumerate(cands):
    re = {g: Fc for g in gates}
    e, hist, _ = replay_re(re)
    if e:
        why[e[0]] += 1; continue
    c = pc(hist)
    legal.append((c, r, Fb, Fc, gates))
    if n % 500 == 0: log('    %d/%d legal %d | rejects %s' % (n + 1, len(cands), len(legal), dict(why)))
log('(2) legal skips: %d / %d | rejects %s' % (len(legal), len(cands), dict(why)))
gain = sorted([x for x in legal if x[0] > c0], key=lambda x: -x[0])
log('    legal AND price-raising: %d' % len(gain))
for c, r, Fb, Fc, gates in gain[:10]:
    log('      reg %d: %d(d%d) skipped -> %d(d%d) over %d gates: %+.5f%% vs word4-base, %+.4f%% vs the frontier' % (
        r, Fb, dims[Fb], Fc, dims[Fc], len(gates), float((c / c0 - 1) * 100), float((c / FRONT - 1) * 100)))

re_all, best = {}, c0
for c, r, Fb, Fc, gates in gain:
    t = dict(re_all); t.update({g: Fc for g in gates})
    e, hist, _ = replay_re(t)
    if e is None:
        ct = pc(hist)
        if ct > best: re_all, best = t, ct
e, hist, C2 = replay_re(re_all)
assert e is None
log('(3) greedy: %d gates reframed | c %s (%+.5f%% vs word4-base, %+.4f%% vs the frontier) | hist delta %s' % (
    len(re_all), mp.nstr(best, 22), float((best / c0 - 1) * 100), float((best / FRONT - 1) * 100),
    {k: hist[k] - hist0[k] for k in sorted(set(hist) | set(hist0)) if hist[k] != hist0[k]}))
if re_all:
    word = dict(w); word.update(word_with(re_all)); word['C'] = C2
    word['stats'] = dict(w.get('stats', {}), level_skip_reframed_gates=len(re_all))
    json.dump(word, open(OUT, 'w'))
    log('(4) emitted %s' % OUT)
else:
    log('(4) 0 admitted — the word4 single-skip space is measured.')
