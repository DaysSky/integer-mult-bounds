# maximum edge-disjoint K4 packing of K11 (exhaustive branch and bound with symmetry: first block fixed)
import itertools, sys
P = list(range(11))
K4 = [frozenset(c) for c in itertools.combinations(P, 4)]
E = lambda b: [frozenset(e) for e in itertools.combinations(sorted(b), 2)]
best = [[]]
def rec(chosen, used, start):
    if len(chosen) > len(best[0]): best[0] = list(chosen); print(len(chosen), [sorted(b) for b in chosen], flush=True)
    # bound: remaining edges / 6 and degree bound
    free = 55 - len(used)
    if len(chosen) + free // 6 <= len(best[0]): return
    deg = [0] * 11
    for e in used:
        for v in e: deg[v] += 1
    ub = sum((10 - d) // 3 for d in deg) // 4
    if len(chosen) + ub <= len(best[0]): return
    for i in range(start, len(K4)):
        b = K4[i]; es = E(b)
        if any(e in used for e in es): continue
        rec(chosen + [b], used | set(es), i + 1)
rec([K4[0]], set(E(K4[0])), 1)
print('max', len(best[0]))
