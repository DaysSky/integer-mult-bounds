"""THE NATIVE-121 v12c (ii19_nat12c.py) — THE DIRECT PERP-SPLITS (the users-measure!!)
THE STRUCTURAL-FIX: the pieces = the perps'-OWN-subsets (NOT the partition-cliques!!) — the
perp(t) (the ~64-lines) -> the DIRECT-SPLITS (the ~21-34-line pieces!!) — the users (the ⊥-ALL?!
(the ~1-8-EXPECTED?!)) — THE MEASURE (THE HONEST-VERDICT (THE BUILD-SCOPE!!!))
"""
import sys, json, time
from collections import Counter
import numpy as np

W4 = json.load(open('ii19_own_word4.json'))
L = [np.array(l, dtype=float) for l in W4['lines']]
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def iph(a, b): return float(np.dot(a, b)) / 2

perps = [sorted(u for u in range(120) if u != t and iph(L[t], L[u]) == 0) for t in range(120)]

# ============ (1) THE DIRECT PERP-SPLITS (the ~21-34-line pieces (the users-measure!!)) ============
# THE SPLIT-STRATEGY: the perp(t) (the ~63+special?! — hmm: the special (the 120?! — the
# perps (the 120-roots-only?! — the t's-perp (the ~63-roots?! — the 120 (the SPECIAL?! —
# the iph(L[t], L[120])?! — hmm: the special ⊥-ALL?! (the (0,...,0,1)-line?! — the iph?! —
# the special (the ⊥-ALL-120-roots?!?! (the §94 ("the special orthogonal to all 120 roots"!!!
# — the perps (the ~63-ROOTS + THE SPECIAL?! — hmm: my-perps (the 120-range (the roots-only
# (the ~63?! — the SPECIAL (the line-120 (the ∈-perp(t) (the ✓✓✓ (the ADD (the special's
# bit (the EVERY-target's-perp!!! — the perps (the +the-special (the ~64!!
# THE SPLIT (the ~21-34-line pieces (the DIRECT (the perp-internal-structure?! — the SPLIT:
# the GREEDY (the sort (the perp'-lines (the mutual-perp-clustering?! — the SIMPLE: the
# contiguous-chunks (the sorted-by-perp-size!!! — the MEASURE (the users?!)
def users_of(S, t):
    return [u for u in range(120) if u != t and all(iph(L[u], L[x]) == 0 for x in S)]

all_users = []
split_sizes = []
for t in range(120):
    pool = list(perps[t])
    pool.sort(key=lambda u: -len(perps[u]))
    # the 2-3 splits (the ~21-32-each!!!
    n = len(pool)
    k = 2 if n <= 44 else 3
    bounds = [int(round(n * (i + 1) / k)) for i in range(k)]
    prev = 0
    for b in bounds:
        S = pool[prev:b]
        prev = b
        us = users_of(S, t)
        all_users.append(len(us))
        split_sizes.append(len(S))
log('(1) THE DIRECT-SPLITS: %d pieces (the sizes %s (the mean %.1f!!))' % (
    len(split_sizes), dict(sorted(Counter(split_sizes).items())), float(np.mean(split_sizes))))
log('    THE USERS: %s (the mean %.1f!!) | the OVER-8: %d/%d' % (
    dict(sorted(Counter(all_users).items())), float(np.mean(all_users)),
    sum(1 for u in all_users if u > 8), len(all_users)))
log('DONE — THE NAT12C (the direct-splits-users!!!)')
