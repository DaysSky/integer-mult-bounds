"""THE POOL-FIX + THE FOREST CENSUS (ii19_nat100.py)!!

(1) THE CONSTRAINED LOCAL SEARCH: the singleton-elimination with the re-solves
    CONSTRAINED to the existing pool (NO NEW WIRES (the nat98's lesson!!!)) —
    the re-solve over the pool-only + the parity-finish (the 1-2-3-line pieces
    (the DEDUP'd (the existing pool preferred!!!)));
(2) THE FOREST CENSUS: per wire (the nat97 design!!): its readers (the loads!!):
    the rich-4 nodes (the nat94 cache!!) ⊇ its home with the T-sets covering the
    readers: the node-count needed (1-2 nested?!): THE DUP-BUDGET (the forest-fit!!)
"""
import os, sys, json
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join('..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
log = lambda *a: print(*a, file=sys.stderr, flush=True)

SPEC = json.load(open('ii19_nat69_spec.json', 'rt'))
V = len(SPEC['lines'])
PERP = [set(p) for p in SPEC['PERP']]
PM = [sum(1 << s for s in PERP[t]) for t in range(V)]
pc = lambda x: x.bit_count()

DES = json.load(open('ii19_nat97_design.json', 'rt'))
POOL = [tuple(p) for p in DES['pool']]
BASES = [[tuple(w) for w in b] for b in DES['bases']]
pool = set(POOL)
use = Counter()
for b in BASES:
    for w in b: use[w] += 1
log('the nat97 design: the pool %d | the uses %d' % (len(pool), sum(use.values())))

# (1) THE CONSTRAINED RE-SOLVE: over the pool-only + the small-piece finish!!
def solve_pool_only(t, res, poolset):
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_w, best_key = None, None
        for w in poolset:
            m = pc(w & 0 if isinstance(w, int) else 0)
        # the pool wires are line-tuples!!
        wm = sum(1 << s for s in w)
        for w in poolset:
            pass
        break
    return base
# (proper impl!!)
def wm(w): return sum(1 << s for s in w)
def solve_constrained(t, poolset):
    res = set(PERP[t])
    base = []
    while res:
        resm = sum(1 << s for s in res)
        best_w, best_key = None, None
        for w in poolset:
            m = pc(wm(w) & resm)
            red = m - (len(w) - m)
            key = (red,)
            if red > 0 and (best_key is None or key > best_key):
                best_key = key; best_w = w
        if best_w is not None:
            base.append(best_w)
            res ^= set(best_w)
            continue
        # the finish: the small pieces from the residual (dedup'd into the pool!!)
        rl = sorted(res)
        for i in range(0, len(rl), 3):
            base.append(tuple(rl[i:i+3]))
        break
    return base

log('\n(1) THE CONSTRAINED LOCAL SEARCH:')
for it in range(8):
    singles = [w for w in list(use) if use[w] == 1]
    elim, kept = 0, 0
    for w in singles:
        t_use = next((t for t in range(V) if w in BASES[t]), None)
        if t_use is None: continue
        old = BASES[t_use]
        b2 = solve_constrained(t_use, pool - {w})
        if len(b2) <= len(old) + 1:
            for x in old: use[x] -= 1
            for x in b2: use[x] += 1
            BASES[t_use] = b2
            elim += 1
        else:
            kept += 1
    live = [w for w in use if use[w] > 0]
    log('  iter %d: elim %d | the pool %d' % (it, elim, len(live)))
    if elim == 0: break
live = [w for w in use if use[w] > 0]
log('  THE FINAL POOL: %d | the reads %s' % (
    len(live), dict(sorted(Counter(len(b) for b in BASES).items()))))

# (2) THE FOREST CENSUS: the wires' readers vs the rich-4 nodes!!
log('\n(2) THE FOREST CENSUS:')
import numpy as np
Z = np.load('ii19_nat94_richpool.npz')
keys = [tuple(k) for k in Z['keys']]
masks = Z['masks']                       # (9661, 120) uint8: the inF-sets
Tm = Z['T']                              # (9661, 120): the T-sets!!!
log('  the rich pool: %d' % len(keys))
readers = defaultdict(list)
for t, b in enumerate(BASES):
    for w in b: readers[w].append(t)
# per wire: the home-span (the triple): the nodes ⊇ home: the rich-4s whose KEY-span
# contains the wire's lines: approximate via: the wire's lines ⊆ the rich's inF AND
# the 4 key-lines ⊥ all the wire's lines (the span-containment (the PROXY (the inF
# ⊇ the wire (a NECESSARY condition (the span ⊇!!))))
node_cov = []
rich_span_mask = []
for ki in range(len(keys)):
    k = keys[ki]
    # the key-span's perp: the lines ⊥ all 4 keys = the T-set... the lines INSIDE the
    # span: the inF!! the wire's home ⊆ the span ⟺ the wire's lines ∈ inF (PROXY!!)
    rich_span_mask.append(masks[ki])
rich_span_mask = np.array(rich_span_mask, dtype=np.uint8)
for w, rs in sorted(readers.items(), key=lambda kv: -len(kv[1])):
    if len(rs) <= 1: continue
    wm_ = np.zeros(V, dtype=np.uint8)
    for s in w: wm_[s] = 1
    # the nodes: the rich-4s ⊇ home (the wire's lines in inF!!)
    sup = np.where((rich_span_mask & wm_).sum(axis=1) == len(w))[0]
    # the coverage: the best node's T ∩ the readers!!
    best = 0; best2 = 0
    for ni in sup:
        cov = int(Tm[ni][rs].sum())
        if cov > best: best2 = best; best = cov
        elif cov > best2: best2 = cov
    node_cov.append((len(rs), best, best2, len(sup)))
node_cov.sort(reverse=True)
log('  the wire (readers, best-node-cov, 2nd, #nodes): the top-12: %s' % node_cov[:12])
log('  the census (the best-cov/readers): %s' % dict(sorted(Counter(
    '%d/%d' % (c[1], c[0]) for c in node_cov).items())))
one = sum(1 for c in node_cov if c[1] == c[0])
two = sum(1 for c in node_cov if c[1] + c[2] >= c[0] and c[1] < c[0])
log('  the one-node wires: %d/%d | the two-node: %d' % (one, len(node_cov), two))
json.dump({'pool': [list(w) for w in live],
           'bases': [[list(x) for x in b] for b in BASES]},
          open('ii19_nat100_design.json', 'wt'))
log('SAVED ii19_nat100_design.json')
