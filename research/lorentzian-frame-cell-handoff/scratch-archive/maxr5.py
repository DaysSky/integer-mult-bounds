import sys, itertools
sys.path.insert(0, '.')
from lclosed import closed_sets
from lgeo import *
t = IDX[('T', (0, 1, 2))]
cands = {}
for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
    m = (1 << t) | (1 << a) | (1 << b)
    if rank(m) != 3: continue
    F = pp(m); P = pm(F)
    key = (pc(F), pc(P), rank(P))
    if key not in cands: cands[key] = F
for key in sorted(cands, key=lambda k: -k[1])[:6]:
    F = cands[key]; U = pm(F)
    lv = closed_sets(U, 5)
    print('node', key, 'max lines in rank-k closed subsets k=1..5:', [max(pc(S) for S in lv[k]) for k in range(1, 6)], flush=True)
