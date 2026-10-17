import sys, itertools, collections
sys.path.insert(0, '.')
from lgeo import *
for r in (0, 60):
    R = HYP[r]; fr = {}
    for a, b in itertools.combinations([x for x in range(V) if x != r], 2):
        m = (1 << r) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if F not in fr: fr[F] = pm(F) & R
    sizes = collections.Counter(pc(p) for p in fr.values())
    print(KIND[r], SUPP[r], '|R|', pc(R), 'frames', len(fr), 'perp sizes', sorted(sizes.items()))
    # coverers per element
    cnt = collections.Counter()
    for p in fr.values():
        for u in bits(p): cnt[u] += 1
    print(' coverers per element min/max', min(cnt.values()), max(cnt.values()), 'elements', len(cnt))
