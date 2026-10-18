"""THE NATIVE-121 v13 (ii19_nat13.py) — THE D6-ANALOG CENSUS (THE SHARED-STRUCTURAL-PIECES!!)
THE R420's-OWN-SOLUTION: the D6s (the dim-6-subspaces (the ~30-lines (the u-in-the-~1-3!!!)):
the 121's-EQUIVALENT (the shared-pieces (the NOT-the-private-splits!!!)) — THE CENSUS (THE
triples' perp-complements?! — the dim-6-subspaces (the lines-inside?! — the u-memberships!!!
"""
import sys, json, time, itertools
from collections import Counter, defaultdict
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

# ============ (1) THE D6-ANALOGS (the perp-intersections (the pair/triple-commons!!)) ============
# the pair-commons: the perp(t) & perp(u) (the ~31-37-lines (the dim ~6-7?!!)
pair_common = {}
for t in range(120):
    for u in range(t + 1, 120):
        c = tuple(sorted(set(x for x in range(120) if x != t and x != u and iph(L[t], L[x]) == 0 and iph(L[u], L[x]) == 0)))
        if len(c) >= 15:
            pair_common[(t, u)] = c
log('(1) THE PAIR-COMMONS: %d (the sizes %s)' % (len(pair_common),
    dict(sorted(Counter(len(c) for c in pair_common.values()).items()))))
# the DISTINCT-common-SETS (the shared-structures!!!)
distinct = Counter(pair_common.values())
log('    the DISTINCT-common-sets: %d (the multiplicities %s)' % (len(distinct),
    dict(sorted(Counter(distinct.values()).items()))))
# the SPAN-DIMS of the distinct sets (the D6-analog-check!!!
span_dims = Counter()
for c in distinct:
    span_dims[int(np.linalg.matrix_rank(np.array([L[x] for x in c])))] += 1
log('    the span-dims: %s' % dict(sorted(span_dims.items())))
# ============ (2) THE u-MEMBERSHIPS (the sources'-frames-count (THE BUDGET!!!)) ============
# the distinct-common-sets-as-PIECES?! — the u (the ∈ the ~?! — the counts!!!
best_sets = [c for c, m in distinct.items() if m >= 2 or len(c) >= 20]
log('(2) the candidate-sets (m>=2 or len>=20): %d' % len(best_sets))
src_mem = Counter()
for c in best_sets:
    for x in c:
        src_mem[x] += 1
log('    the u-memberships (the candidate-pieces): %s (the mean %.1f!!) | the OVER-8: %d/120' % (
    dict(sorted(Counter(src_mem.values()).items())), float(np.mean(list(src_mem.values()))),
    sum(1 for x in src_mem.values() if x > 8)))
# the targets'-perp-coverage?! — the per-target (the sets ⊆ perp(t) (the coverage!!!
log('DONE — THE NAT13 (the D6-analog-census!!!)')
