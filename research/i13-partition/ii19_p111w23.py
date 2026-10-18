"""THE LEVEL-SKIP SCAN (ii19_p111w23.py) — the general form of the v2 hist-reshape.

For every register r with an intermediate level F_b (entered by a climb from F_a, left by a climb
to F_c — the next D/A/B level, C's frame 1, or final[r]): reframe every gate where r sits at F_b to F_c.  r's two climbs (ranks a, b)
merge into one (rank a + b) — the concentration lever — while gate order (so every value) is
unchanged.  Each candidate is checked by the gcheck-exact replay and priced exactly; the legal
gainers are then admitted greedily (best single gain first, re-checked against the running word).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
OUT = argv[0] if argv else 'ii19_r434_skip.json'
P111 = mp.mpf('0.001733052823330162099157')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')

def word_with(re):
    """re: {(phase, pos): frame}"""
    return {ph: [[re.get((ph, gi), F), d, list(s)] for gi, (F, d, s) in enumerate(w[ph])] for ph in PH}
def replay_re(re):
    saved = {ph: w[ph] for ph in PH}
    w.update(word_with(re))
    try: return replay(w['A'])
    finally: w.update(saved)

# the level structure of every register over D, A, B (C is frame 1 = full; final climbs close)
lev = defaultdict(list)          # r -> [[frame, [(phase, pos), ...]], ...]
cur = list(w['start'])
for ph in PH:
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in [d] + srcs:
            if not lev[r] or lev[r][-1][0] != F:
                lev[r].append([F, []])
            lev[r][-1][1].append((ph, gi))
inC = set(r for F, d, srcs in w['C'] for r in [d] + srcs)
cands = []
for r in range(nreg):
    Ls = lev[r]
    for j, (Fb, gates) in enumerate(Ls):
        if Fb == w['start'][r]: continue                    # not entered by a climb
        # the next frame: the next D/A/B level, else C's frame 1, else the final climb
        Fc = Ls[j + 1][0] if j + 1 < len(Ls) else (1 if r in inC else w['final'][r])
        if Fc == Fb: continue
        cands.append((r, Fb, Fc, tuple(gates)))
c0 = pc(hist0)
log('(1) intermediate levels: %d | base c %s' % (len(cands), mp.nstr(c0, 22)))

legal, why = [], Counter()
for n, (r, Fb, Fc, gates) in enumerate(cands):
    re = {g: Fc for g in gates}
    e, hist, _ = replay_re(re)
    if e:
        why[e[0]] += 1; continue
    c = pc(hist)
    legal.append((c, r, Fb, Fc, gates))
    if n % 500 == 0: log('    %d/%d legal %d' % (n, len(cands), len(legal)))
log('(2) legal skips: %d / %d | rejects %s' % (len(legal), len(cands), dict(why)))
gain = sorted([x for x in legal if x[0] > c0], key=lambda x: -x[0])
log('    legal AND price-raising: %d' % len(gain))
for c, r, Fb, Fc, gates in gain[:10]:
    log('      reg %d: %d(d%d) skipped -> %d(d%d) over %d gates: %+.5f%% vs r434' % (
        r, Fb, dims[Fb], Fc, dims[Fc], len(gates), float((c / c0 - 1) * 100)))

re_all, best = {}, c0
for c, r, Fb, Fc, gates in gain:
    t = dict(re_all); t.update({g: Fc for g in gates})
    e, hist, _ = replay_re(t)
    if e is None:
        ct = pc(hist)
        if ct > best: re_all, best = t, ct
e, hist, C2 = replay_re(re_all)
assert e is None
log('(3) greedy: %d gates reframed | c %s (%+.5f%% vs P111, %+.5f%% vs r434) | hist delta %s' % (
    len(re_all), mp.nstr(best, 22), float((best / P111 - 1) * 100), float((best / c0 - 1) * 100),
    {k: hist[k] - hist0[k] for k in sorted(set(hist) | set(hist0)) if hist[k] != hist0[k]}))
if re_all:
    word = dict(w); word.update(word_with(re_all)); word['C'] = C2
    word['stats'] = dict(w.get('stats', {}), level_skip_reframed_gates=len(re_all))
    json.dump(word, open(OUT, 'w'))
    log('(4) emitted %s' % OUT)
