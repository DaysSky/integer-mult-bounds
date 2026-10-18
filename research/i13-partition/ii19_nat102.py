"""THE RICH-4-HEAVY SOLVE (ii19_nat102.py) — the chunk-first B-basis!!

THE LESSONS: the use-priority-first churns (the nat101: 368 triples of 448!!); the
r434's economy = the BIG chunk-wires (~12-line!!!) + the small shared pool (~100!!).
THE PROTOCOL (this script!!): THE RED-DOMINANT GREEDY (the biggest reduction first
(the rich-4 chunks (red 5-10!!!)) with the use-count as the TIE-BREAK only!!) + the
triple-finish (the small residuals (the used-first!!)) + THE ITERATED RE-SOLVE (the
global fixpoint over the fixed pool (the nat97b's lesson APPLIED RIGHT (the rich-4
candidates make the re-solves span-close WITHOUT the partition-rigidity!!!))).
"""
import os, sys, json
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

Z = np.load('ii19_nat94_richpool.npz')
RKEYS = [tuple(int(x) for x in k) for k in Z['keys']]
RMASK = [int(''.join(str(int(b)) for b in m[::-1]), 2) for m in Z['masks']]
RT = [int(''.join(str(int(b)) for b in t[::-1]), 2) for t in Z['Tmat']]
log('the rich-4 cache: %d' % len(RKEYS))
CAND = [[] for _ in range(V)]
for i in range(len(RKEYS)):
    Tm_ = RT[i]
    while Tm_:
        b = Tm_ & -Tm_
        CAND[b.bit_length() - 1].append(i)
        Tm_ ^= b

use = Counter()
BASES = [None] * V

def best_fresh(res):
    rl = sorted(res)
    if len(rl) <= 3:
        return tuple(rl)
    best_tri, best_sc = None, -1
    for i in range(len(rl)):
        a = rl[i]; pa = PM[a]
        for j in range(i + 1, min(len(rl), i + 25)):
            b = rl[j]
            ab = pa & PM[b]
            for c in rl:
                if c in (a, b): continue
                sc = pc(ab & PM[c])
                if sc > best_sc: best_sc = sc; best_tri = (a, b, c)
            if best_sc >= 20: break
        if best_tri is not None and best_sc >= 20: break
    if best_tri is None:
        best_tri = (rl[0], rl[1], rl[2])
    return best_tri

def solve_target(t):
    res = set(PERP[t])
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_w, best_key = None, None
        # the pool wires (the used!!)
        for w, cnt in use.items():
            if cnt == 0: continue
            wm_ = RMASK[w[1]] if w[0] == 'R' else sum(1 << s for s in w[1])
            m = pc(wm_ & resm)
            red = m - (pc(wm_) - m)
            if red <= 0: continue
            key = (red, cnt)                     # red-dominant, the use-tie-break!!
            if best_key is None or key > best_key: best_key = key; best_w = w
        # the fresh rich-4s (the candidates!!)
        for i in CAND[t]:
            if ('R', i) in use and use[('R', i)] > 0: continue
            m = pc(RMASK[i] & resm)
            red = m - (pc(RMASK[i]) - m)
            if red <= 0: continue
            key = (red, 0)
            if best_key is None or key > best_key: best_key = key; best_w = ('R', i)
        if best_w is not None:
            base.append(best_w); use[best_w] += 1
            wmask = RMASK[best_w[1]] if best_w[0] == 'R' else sum(1 << s for s in best_w[1])
            res ^= {s for s in range(V) if (wmask >> s) & 1}
            continue
        tri = best_fresh(res)
        base.append(('T', tri)); use[('T', tri)] += 1
        res ^= set(tri)
    return base

log('\n(1) THE RED-DOMINANT SOLVE:')
for t in range(V):
    BASES[t] = solve_target(t)
live = [k for k, c in use.items() if c > 0]
log('  the pool: %d | the uses %d' % (len(live), sum(use[k] for k in live)))
log('  the reads: %s' % dict(sorted(Counter(len(b) for b in BASES).items())))
log('  the use-census: %s' % dict(sorted(Counter(use[k] for k in live).items())))
log('  the kinds: %s' % dict(sorted(Counter(k[0] for k in live).items())))

for t in range(V):
    x = 0
    for w in BASES[t]:
        x ^= RMASK[w[1]] if w[0] == 'R' else sum(1 << s for s in w[1])
    assert x == sum(1 << s for s in PERP[t]), 'the target %d XOR FAILED!!' % t
log('  THE XOR-VERIFICATION: 120/120 OK')

# (2) THE GLOBAL RE-SOLVE ITERATE (the fixpoint over the fixed pool!!)
log('\n(2) THE GLOBAL ITERATE:')
for ps in range(4):
    snap = dict(use)
    for t in range(V):
        old = BASES[t]
        for w in old: use[w] -= 1
        b2 = solve_target(t)
        if len(b2) <= len(old) + 0:
            BASES[t] = b2
        else:
            for w in b2: use[w] -= 1
            for w in old: use[w] += 1
    live = [k for k, c in use.items() if c > 0]
    log('  pass %d: the pool %d | the uses %d | the reads %s' % (
        ps, len(live), sum(use[k] for k in live),
        dict(sorted(Counter(len(b) for b in BASES).items()))))

live = [k for k, c in use.items() if c > 0]
log('  THE FINAL POOL: %d | the kinds: %s' % (len(live), dict(sorted(Counter(k[0] for k in live).items()))))
log('  the use-census: %s' % dict(sorted(Counter(use[k] for k in live).items())))

pool_n = len(live)
R_est = pool_n + 9 + 85 + 40
log('\n(3) THE R: %d (the pool %d + 9 + ~85 gather + ~40 dups!!)' % (R_est, pool_n))
from pricer import price
from mpmath import mp
TARGET = {1: 1010, 2: 1038, 3: 53, 4: 34, 5: 79, 6: 9, 7: 15}
def synth(R):
    mass = 8 * R + 72 + 2 * V * 7
    d = Counter(TARGET); d[1] += mass - sum(r * z for r, z in d.items())
    return dict(d)
for R in (R_est, R_est + 40, 480):
    c, prof, dd = price(synth(R), V, 8, R)
    log('  R=%3d: %s' % (R, mp.nstr(c, 9) if c is not None else str(dd.get('error', 'NO-ROOT'))))

json.dump({'pool_rich': [list(RKEYS[k[1]]) for k in live if k[0] == 'R'],
           'pool_tri': [list(k[1]) for k in live if k[0] == 'T'],
           'bases': [[(['R', w[1]] if w[0] == 'R' else ['T', list(w[1])]) for w in b]
                     for b in BASES]},
          open('ii19_nat102_design.json', 'wt'))
log('SAVED ii19_nat102_design.json')
