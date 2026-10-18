"""THE WORD4 JOINT-MOVE SCAN (ii19_nat23.py) — the Lorentzian push: w24c's scan on OUR OWN word.

r434's joint scan: 0 legal (rule (b), the faithful repair).  The word4's sharing (12 sources per
dim-4 frame, 3 helpers per cell, 98 per dim-8 frame) dissolved the wall for 43 single skips; the
2539 rejected big merges (the ladder concentrations, ceiling +14.87% at the one-gate extreme)
need co-operand repairs.  Rule (b): on each failure, add the blocking register's OWN level-skip
on the ORIGINAL word (w23's move family at the level preceding the failing gate); depth 4;
admit iff replay passes AND the exact price rises; greedy-accumulate (the banked 42 singles
included as depth-0 admissions).
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_nat20.py']
exec(open('ii19_nat20.py').read().split('# (1) chain-shape census')[0])
OUT = argv[0] if argv else 'ii19_word4_joint.json'
FRONT = mp.mpf('0.001744385950814795279853')
R = w['R']
def pc(hist): return price(dict(hist), V, H, R)[0]
PH = ('D', 'A', 'B')
DEPTH = 4

def word_with(re):
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
        if Fb == w['start'][r]: continue
        Fc = Ls[j + 1][0] if j + 1 < len(Ls) else (1 if r in inC else w['final'][r])
        if Fc == Fb: continue
        cands.append((r, Fb, Fc, tuple(gates)))
c0 = pc(hist0)
log('(1) seeds %d | base c %s (%+.4f%% vs frontier)' % (len(cands), mp.nstr(c0, 22), float((c0 / FRONT - 1) * 100)))

def repair(e):
    """rule (b): the blocking register's OWN level-skip on the ORIGINAL word."""
    if e[0] == 'climb':
        x, gate = e[2], e[1]
    elif e[0] in ('read-content', 'content'):
        x, gate = e[2], e[1]
    else:
        return None
    Ls = lev0.get(x) or []
    j = next((j for j, (F, gs) in enumerate(Ls) if gate in gs), None)
    if j is None: return None
    if e[0] == 'climb':
        j -= 1
        if j < 0: return None
    Fb = Ls[j][0]
    Fx = Ls[j + 1][0] if j + 1 < len(Ls) else (1 if x in inC else w['final'][x])
    if Fx == Fb: return None
    mv = {g: Fx for g in Ls[j][1] if g[0] != 'D'}   # H2: never raise a D gate off frame 0
    return mv or None

admitted, why = [], Counter()
for n, (r, Fb, Fc, gates) in enumerate(cands):
    re = {g: Fc for g in gates}
    for depth in range(DEPTH + 1):
        e, hist, _ = replay_re(re)
        if e is None:
            c = pc(hist)
            why['pass_d%d' % depth] += 1
            if c > c0: admitted.append((c, re))
            break
        mv = repair(e)
        if mv is None:
            why['dead_' + e[0]] += 1; break
        re2 = dict(re); re2.update(mv)
        if re2 == re:
            why['no_progress'] += 1; break
        re = re2
    if n % 500 == 0:
        log('    %d/%d: admitted %d | %s' % (n + 1, len(cands), len(admitted), dict(why)))
log('(2) scan done: admitted %d | %s' % (len(admitted), dict(why)))

gain = sorted(admitted, key=lambda x: -x[0])
re_all, best = {}, c0
for c, re in gain:
    t = dict(re_all); t.update(re)
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
    word['stats'] = dict(w.get('stats', {}), joint_move_reframed_gates=len(re_all))
    json.dump(word, open(OUT, 'w'))
    log('(4) emitted %s' % OUT)
else:
    log('(4) 0 admitted.')
