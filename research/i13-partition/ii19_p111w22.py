"""THE V2-RESCUE (ii19_p111w22.py) — the 9 no-cell build-srcs, joint reframe (handoff option (b)).

w21's verdict: 0/151 single v2-moves legal — every build-src s1 already owns a dim-2 cell C1 != F2
(0/108 srcs have C1 == F2 of any of their builds), so s1 would climb F2 -> C1 sideways.  The only
srcs with no own cell are the 9 no-cell srcs; their blocker is a later read at their singleton frame
(an A build after the 2nd gate, or the B dim-1 read).  Here each such move is the joint set:
  build b -> just before its 2nd gate, frame F2;  every later gate reading s1 at its singleton -> F2.
Admitted greedily iff the gcheck-exact replay passes AND the exact price rises.
"""
import json, os, sys
from collections import defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
from pricer import price
from mpmath import mp

argv = sys.argv[1:]
sys.argv = ['ii19_p111w21.py']
exec(open('ii19_p111w21.py').read().split('# (2) greedy admission')[0])
OUT = argv[0] if argv else 'ii19_r434_v2r.json'
P111 = mp.mpf('0.001733052823330162099157')
R = w['R']
def pc(hist):
    c, _, _ = price(dict(hist), V, H, R)
    return c

path = defaultdict(list)
for ph in ('A', 'B'):
    for gi, (F, d, srcs) in enumerate(w[ph]):
        for r in [d] + srcs: path[r].append((ph, gi, F))
near = [(h, b, s, F2, s1) for (h, b, s, F2, s1) in cands
        if not any(dims[F] == 2 for ph, gi, F in path[s1])]

def build(movesA, reB):
    """movesA: {A-pos: (new-key-pos or None, frame)}; reB: {B-pos: frame}."""
    key = [2 * movesA[gi][0] - 1 if gi in movesA and movesA[gi][0] is not None else 2 * gi
           for gi in range(len(w['A']))]
    A = [[movesA[i][1] if i in movesA else w['A'][i][0], w['A'][i][1], list(w['A'][i][2])]
         for i in sorted(range(len(w['A'])), key=lambda i: key[i])]
    B = [[reB.get(gi, F), d, list(srcs)] for gi, (F, d, srcs) in enumerate(w['B'])]
    return A, B

def replayAB(A, B):
    saved = w['B']; w['B'] = B
    try: return replay(A)
    finally: w['B'] = saved

c0 = pc(hist0)
log('(0) the 9 no-cell candidates: %d | base c %s (%+.4f%% vs P111)' % (
    len(near), mp.nstr(c0, 22), float((c0 / P111 - 1) * 100)))
movesA, reB, best = {}, {}, c0
for (h, b, s, F2, s1) in near:
    S = w['start'][s1]
    tA = dict(movesA); tB = dict(reB)
    tA[b] = (s, F2)
    extra = []
    for ph, gi, F in path[s1]:
        if F != S: continue
        if ph == 'A' and gi > s: tA[gi] = (None, F2); extra.append(('A', gi, w['A'][gi]))
        if ph == 'B': tB[gi] = F2; extra.append(('B', gi, w['B'][gi]))
    e, hist, _ = replayAB(*build(tA, tB))
    c = pc(hist) if e is None else None
    verdict = 'REJECT %s' % (e,) if e else ('ADMIT' if c > best else 'no-gain')
    log('    h %d s1 %d F2 %d (+%d reframed: %s) -> %s%s' % (h, s1, F2, len(extra),
        [(p, g, x[1]) for p, g, x in extra], verdict,
        '' if c is None else ' c %+.5f%%' % float((c / P111 - 1) * 100)))
    if e is None and c > best:
        movesA, reB, best = tA, tB, c

A2, B2 = build(movesA, reB)
e, hist, C2 = replayAB(A2, B2)
assert e is None
log('(1) admitted moves: A %d / B %d | hist delta %s' % (len(movesA), len(reB),
    {k: hist[k] - hist0[k] for k in sorted(set(hist) | set(hist0)) if hist[k] != hist0[k]}))
log('    c %s (%+.5f%% vs P111, %+.5f%% vs the r434 frontier)' % (mp.nstr(best, 22),
    float((best / P111 - 1) * 100), float((best / c0 - 1) * 100)))
if movesA:
    word = dict(w); word['A'] = A2; word['B'] = B2; word['C'] = C2
    word['stats'] = dict(w.get('stats', {}), v2_rescued_builds=sum(1 for k, v in movesA.items() if v[0] is not None))
    json.dump(word, open(OUT, 'w'))
    log('(2) emitted %s' % OUT)
