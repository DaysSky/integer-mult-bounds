"""THE MIXED-BASIS SOLVE (ii19_nat101.py) — the rich-4 chunks + the triple finishes!!

THE R-LEVER: the wire-size freedom — the B-wires as the rich-4 chunks (5-12-line
inF-sets (the dim-4 homes (1 register + the 1-src ladder (NO sub-wires!!!)))): the
reads HALVED; the pool ~275-325 (the target!!!). THE SOLVE:
(1) THE CANDIDATES: the rich-4 chunks (the nat94 cache!!) + the pool-triples;
(2) THE PER-TARGET BASES: the used-pool-first + the biggest-reduction + the fresh;
(3) THE CENSUS (the pool, the reads, the loads) + THE R + THE PRICE!!!
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
log('the per-target rich-candidates: %d..%d (the mean %.0f)'
    % (min(len(c) for c in CAND), max(len(c) for c in CAND),
       sum(len(c) for c in CAND) / V))

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
        # (a) the USED wires with the biggest (red, uses) — the pool-first!!!
        best_w, best_key = None, None
        for w, cnt in use.items():
            if cnt == 0: continue
            if w[0] == 'T':
                wm_ = sum(1 << s for s in w[1])
            else:
                wm_ = RMASK[w[1]]
            m = pc(wm_ & resm)
            red = m - (pc(wm_) - m)
            if red <= 0: continue
            key = (red, cnt)
            if best_key is None or key > best_key: best_key = key; best_w = w
        if best_w is not None:
            base.append(best_w); use[best_w] += 1
            wmask = RMASK[best_w[1]] if best_w[0] == 'R' else sum(1 << s for s in best_w[1])
            res ^= {s for s in range(V) if (wmask >> s) & 1}
            continue
        # (b) the fresh rich-4 (the biggest reduction!!)
        best_i, best_red = None, 0
        for i in CAND[t]:
            m = pc(RMASK[i] & resm)
            red = m - (pc(RMASK[i]) - m)
            if red > best_red: best_red = red; best_i = i
        if best_i is not None:
            base.append(('R', best_i)); use[('R', best_i)] += 1
            res ^= {s for s in range(V) if (RMASK[best_i] >> s) & 1}
            continue
        # (c) the fresh triple
        tri = best_fresh(res)
        base.append(('T', tri)); use[('T', tri)] += 1
        res ^= set(tri)
    return base

log('\n(1) THE SOLVE:')
for t in range(V):
    BASES[t] = solve_target(t)
live = [k for k, c in use.items() if c > 0]
log('  the pool: %d | the uses %d' % (len(live), sum(use[k] for k in live)))
log('  the reads: %s' % dict(sorted(Counter(len(b) for b in BASES).items())))
log('  the use-census: %s' % dict(sorted(Counter(use[k] for k in live).items())))
log('  the wire-kind census: %s' % dict(sorted(Counter(k[0] for k in live).items())))

# (2) THE VERIFICATION (the XOR == perp(t)!!)
for t in range(V):
    x = 0
    for w in BASES[t]:
        x ^= RMASK[w[1]] if w[0] == 'R' else sum(1 << s for s in w[1])
    assert x == sum(1 << s for s in PERP[t]), 'the target %d XOR FAILED!!' % t
log('  THE XOR-VERIFICATION: 120/120 OK')

# (3) THE R + THE PRICE
pool_n = len(live)
R_est = pool_n + 9 + 130 + 40
log('\n(2) THE R: %d (the pool %d + 9 + ~130 gather + ~40 dups!!)' % (R_est, pool_n))
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
          open('ii19_nat101_design.json', 'wt'))
log('SAVED ii19_nat101_design.json')
