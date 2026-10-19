"""nat182: THE 241-LINE DEEPER-SHELL'S SHARED-WIRE POOL -- the delivery economy's first census.
The feasibility bound: rho < 5.4 at (v=241, h=9) for any root to exist.
The rho: the shared-wire economy -- the perp-intersections' pool + the reuse-first estimate.
Run AFTER/alongside nat181 (recomputes the system inline -- self-contained).
"""
from itertools import combinations
import numpy as np
from collections import Counter, defaultdict

# the system (inline, self-contained!!)
roots = []
for i in range(8):
    for j in range(i+1, 8):
        for si in (1, -1):
            for sj in (1, -1):
                v8 = [0]*8
                v8[i] = si; v8[j] = sj
                if tuple(v8) not in [tuple(-np.array(x)) for x in roots]:
                    roots.append(v8)
for p in combinations(range(8), 4):
    for signs in [(1,1,1,1), (1,1,-1,-1), (1,-1,1,-1), (1,-1,-1,1)]:
        v8 = [0]*8
        for k, s in zip(p, signs): v8[k] = s
        if tuple(v8) not in [tuple(-np.array(x)) for x in roots]:
            roots.append(v8)

lines = []
for r in roots: lines.append(tuple(r) + (0,))
lines.append((0,)*8 + (1,))
for r in roots: lines.append(tuple(r) + (1,))
V = len(lines)

def ip(a, b):
    return sum(x*y for x, y in zip(a[:8], b[:8])) + 2*a[8]*b[8]

perp = [frozenset(j for j in range(V) if j != i and ip(lines[i], lines[j]) == 0) for i in range(V)]
pc = Counter(len(p) for p in perp)
print('the perp-counts: %s (the mean %.1f)' % (dict(sorted(pc.items())), sum(len(p) for p in perp)/V), flush=True)

# the shared-wire pool: the pair-intersections (>= 20 lines!!)
def mask_of(S):
    m = 0
    for i in S: m |= 1 << i
    return m

pool = {}
for i, j in combinations(range(V), 2):
    S = perp[i] & perp[j]
    if len(S) >= 20:
        pool[mask_of(S)] = {i, j}
print('the pair-wire pool (>=20-line intersections): %d' % len(pool), flush=True)

szs = Counter(bin(m).count('1') for m in pool)
print('the pool-contents sizes: %s' % dict(sorted(szs.items())), flush=True)

# the distinct-wire estimate: the reuse-first greedy over the demands (perp(t) itself!)
# (the crude estimate: each target's perp as the XOR of the pool-contents + the raw leftovers)
used = set()
total_reads = 0
fail = 0
for t in range(V):
    need = perp[t]
    reads = []
    # the greedy: the biggest pool-content ⊆ need
    while len(need) >= 20:
        best, bm = None, None
        for m in pool:
            S = frozenset(i for i in range(V) if (m >> i) & 1)
            if S <= need and (best is None or len(S) > len(best)):
                best, bm = S, m
        if best is None:
            break
        reads.append(bm)
        need = need - best
    if len(reads) == 0:
        fail += 1
    used.update(reads)
    total_reads += len(reads) + len(need)
print('the reuse-first: %d distinct wires | the total reads %d (the mean %.1f/target) | the no-wire targets %d' % (
    len(used), total_reads, total_reads/V, fail), flush=True)
print('THE RHO-ESTIMATE: (wires %d + the raw ~%d + the pieces) / %d = the rho ~%.1f (the bound 5.4!!)' % (
    len(used), total_reads/V*V, V, (len(used) + total_reads/V*V + 300)/V), flush=True)
