"""THE JOINT-MOVE SEARCH, REPAIR RULE (b) (ii19_p111w24c.py) — scratch.

w24 (rule (a): x's skip read off the REFRAMED level structure) returned 706 legal joint words but
701 are hist-neutral SELF-CANCELLATIONS (the repair overrides the seed's raised gate back to its
original frame -> the move set collapses to the identity).  Rule (b), the faithful reading: the
repair is x's OWN level-skip ON THE ORIGINAL WORD (w23's move family for x at the level preceding
the failing gate).  Genuine joint moves only; same scan budget (2232 seeds x depth 4); stop if 0
price-raising admissions.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (1) the T155 helpers')[0])
OUT = argv[0] if argv else 'ii19_r434_jointb.json'
P111 = mp.mpf('0.001733052823330162099157')
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
def levels():
    lev = defaultdict(list)
    for ph in PH:
        for gi, (F, d, srcs) in enumerate(w[ph]):
            for r in [d] + srcs:
                if not lev[r] or lev[r][-1][0] != F:
                    lev[r].append([F, []])
                lev[r][-1][1].append((ph, gi))
    return lev

inC = set(r for F, d, srcs in w['C'] for r in [d] + srcs)
lev0 = levels()
cands = []
for r in range(nreg):
    Ls = lev0[r]
    for j, (Fb, gates) in enumerate(Ls):
        if Fb == w['start'][r]: continue
        Fc = Ls[j + 1][0] if j + 1 < len(Ls) else (1 if r in inC else w['final'][r])
        if Fc == Fb: continue
        cands.append((r, Fb, Fc, tuple(gates)))
c0 = pc(hist0)
log('(1) seeds %d | base c %s (%+.4f%% vs P111)' % (len(cands), mp.nstr(c0, 22), float((c0 / P111 - 1) * 100)))

def repair(e):
    """rule (b): the blocking register's OWN level-skip on the ORIGINAL word."""
    if e[0] == 'climb':
        x, gate = e[2], e[1]           # current level = the original run BEFORE the failing gate's run
    elif e[0] in ('read-content', 'content'):
        x, gate = e[2], e[1]           # current level = the original run AT the failing gate
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

admitted, why, passes = [], Counter(), []
for n, (r, Fb, Fc, gates) in enumerate(cands):
    re = {g: Fc for g in gates}
    for depth in range(DEPTH + 1):
        e, hist, _ = replay_re(re)
        if e is None:
            c = pc(hist)
            why['pass_d%d' % depth] += 1
            passes.append((c, depth, {k: hist[k] - hist0[k] for k in sorted(set(hist) | set(hist0)) if hist[k] != hist0[k]}))
            if c > c0: admitted.append((c, re))
            break
        mv = repair(e)
        if mv is None:
            why['dead_' + e[0]] += 1; break
        re2 = dict(re); re2.update(mv)
        if re2 == re:
            why['no_progress'] += 1; break
        re = re2
    if n % 250 == 0:
        log('    %d/%d: admitted %d | %s' % (n + 1, len(cands), len(admitted), dict(why)))
log('(2) scan done: admitted %d | %s' % (len(admitted), dict(why)))
log('    pass-price census: %d legal joint words | c == base %d | c < base %d | c > base %d | max %+.5f%%' % (
    len(passes), sum(1 for c, d, dh in passes if c == c0), sum(1 for c, d, dh in passes if c < c0),
    sum(1 for c, d, dh in passes if c > c0),
    max(float((c / c0 - 1) * 100) for c, d, dh in passes) if passes else 0.0))
for c, d, dh in sorted(passes, key=lambda x: -x[0])[:10]:
    log('      d%d %+.5f%% | hist delta %s' % (d, float((c / c0 - 1) * 100), dh))

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
log('(3) greedy: %d gates reframed | c %s (%+.5f%% vs P111, %+.5f%% vs the r434 base)' % (
    len(re_all), mp.nstr(best, 22), float((best / P111 - 1) * 100), float((best / c0 - 1) * 100)))
if re_all:
    word = dict(w); word.update(word_with(re_all)); word['C'] = C2
    word['stats'] = dict(w.get('stats', {}), joint_move_reframed_gates=len(re_all))
    json.dump(word, open(OUT, 'w'))
    log('(4) emitted %s' % OUT)
else:
    log('(4) 0 admitted — the joint-move route is STOPPED (the handoff\'s rule).')
