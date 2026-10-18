"""nat132: THE B-BASIS RECOMPOSITION PROBE (the trim path (B)'s feasibility).

Per target t: the exact wire-parity W_t = B0[t] XOR (the sources' delivered lines).
The current wire-subset (from the word's B-gates) XORs to W_t. The probe: a local
swap-reduce over the full 225-wire pool (replace k wires with fewer), per target.
Reports: the current uses-total, the improved uses-total, the distinct-wire census
(the union of the improved subsets -> the implied R-floor for path (B)).
"""
import json, gzip
from collections import Counter

W = json.load(gzip.open('/tmp/r434-censusplan-tuned.json.gz', 'rt'))
v = W['v']; R = W['R']; nreg = 2 * v + R
A = W['A']; B = W['B']; D = W['D']
lines = W['lines']

# the replay: the vals after D+A (the wires' contents + the sources)
val = [0] * nreg
for s in range(v):
    val[s] = 1 << s
for F, d, ss in D:
    for s in ss:
        val[d] ^= val[s]
for F, d, ss in A:
    for s in ss:
        val[d] ^= val[s]

mask_of = lambda x: x & ((1 << v) - 1)
wire_mask = {}
for F, d, ss in B:
    for s in ss:
        if s >= 2 * v:
            wire_mask[s] = mask_of(val[s])
POOL = sorted(wire_mask)
print('the pool: %d wires' % len(POOL))

# per target: the B-srcs (the sources + the wires)
cur = {}
for F, d, ss in B:
    if v <= d < 2 * v:
        cur.setdefault(d, set()).update(ss)
ok = True
for t, srcs in cur.items():
    ws = [s for s in srcs if s >= 2 * v]
    ss_ = [s for s in srcs if s < v]
    # W_t = the wires' XOR (the sources deliver their own lines)
    Wt = 0
    for s in ws:
        Wt ^= wire_mask[s]
    cur[t] = (ws, ss_, Wt)
    # the parity check: the wires' XOR + the sources' lines == B0[t]?? (the sources part is implicit)
    # (the word passes gcheck so this is exact by construction)
print('the targets: %d | the current wire-uses: %d' % (len(cur), sum(len(x[0]) for x in cur.values())))

# the local-search sparsification: per target, try to reduce the subset over the pool
def xor_of(subset):
    x = 0
    for s in subset:
        x ^= wire_mask[s]
    return x

improved = {}
total_cur = 0
total_imp = 0
for t, (ws, ss_, Wt) in cur.items():
    cur_set = list(ws)
    total_cur += len(cur_set)
    best = list(cur_set)
    changed = True
    rounds = 0
    while changed and rounds < 8:
        changed = False
        rounds += 1
        # 1: remove a wire if the rest still XORs to Wt (redundant wire)
        for s in list(best):
            if xor_of([x for x in best if x != s]) == Wt:
                best = [x for x in best if x != s]
                changed = True
                break
        if changed:
            continue
        # 2: replace 2 wires with 1 (a pool-wire whose mask = the pair's XOR)
        for i in range(len(best)):
            for j in range(i + 1, len(best)):
                pair = wire_mask[best[i]] ^ wire_mask[best[j]]
                for s2 in POOL:
                    if s2 in best:
                        continue
                    if wire_mask[s2] == pair:
                        best = [x for k, x in enumerate(best) if k not in (i, j)] + [s2]
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break
        if changed:
            continue
        # 3: replace 3 wires with 2
        for i in range(len(best)):
            for j in range(i + 1, len(best)):
                for k2 in range(j + 1, len(best)):
                    tri = wire_mask[best[i]] ^ wire_mask[best[j]] ^ wire_mask[best[k2]]
                    for a2 in POOL:
                        if a2 in best:
                            continue
                        ra = tri ^ wire_mask[a2]
                        for b2 in POOL:
                            if b2 in best or b2 <= a2:
                                continue
                            if wire_mask[b2] == ra:
                                best = [x for kk, x in enumerate(best) if kk not in (i, j, k2)] + [a2, b2]
                                changed = True
                                break
                        if changed:
                            break
                    if changed:
                        break
                if changed:
                    break
            if changed:
                break
    improved[t] = best
    total_imp += len(best)
print('the current uses: %d | the improved uses: %d (the %.1f%% reduction)' % (
    total_cur, total_imp, 100 * (total_cur - total_imp) / total_cur))
dist = Counter(len(x) for x in improved.values())
print('the improved subset-sizes:', dict(sorted(dist.items())))
# the distinct wires in the union
uni = set()
for x in improved.values():
    uni.update(x)
print('the distinct wires in the union: %d (the current 225)' % len(uni))
# the implied R: the distinct wires + the A-DAG intermediates needed for THEM + the 9 totals
print('the recomposition would retire %d wires (if the A-DAG follows)' % (225 - len(uni)))
