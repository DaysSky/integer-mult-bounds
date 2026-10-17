# Minimum number of k-subsets of an 8-set whose K_k edge sets XOR to K_8 (every pair covered an odd number of times),
# for k = 4..7.  Exact via F2 linear algebra + exhaustive small searches.
import itertools, numpy as np
pts = range(8); pairs = list(itertools.combinations(pts, 2)); pid = {p: i for i, p in enumerate(pairs)}
def vec(S):
    v = 0
    for p in itertools.combinations(sorted(S), 2): v |= 1 << pid[p]
    return v
full = (1 << len(pairs)) - 1
for k in (4, 5, 6, 7):
    subs = [vec(S) for S in itertools.combinations(pts, k)]
    found = None
    for m in range(1, 9):
        for combo in itertools.combinations(range(len(subs)), m):
            x = 0
            for c in combo: x ^= subs[c]
            if x == full: found = (m, [list(itertools.combinations(pts, k))[c] for c in combo]); break
        if found: break
        if m >= 5 and len(subs) > 60: break
    print('k =', k, '| min parity cover:', found)
