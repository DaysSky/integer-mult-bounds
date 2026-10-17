import sys, random
sys.path.insert(0, '.')
import numpy as np
from lgeo import *
from lclosed import closure_vec
for kind in ('T', 'P'):
    if kind == 'T':
        t = IDX[('T', (0, 1, 2))]; U = sum(1 << s for s in bits(HYP[t]) if KIND[s] == 'T')
    else:
        t = IDX[('P', (0, 1))]; U = sum(1 << s for s in bits(HYP[t]) if KIND[s] == 'T' and not ({0, 1} & set(SUPP[s])))
    Ub = bits(U); best = {}
    random.seed(1)
    for trial in range(20000):
        S = 0; r = 0; order = Ub[:]; random.shuffle(order)
        for u in order:
            c, rr = closure_vec(Ub, S | (1 << u))
            if rr <= 6: S, r = c, rr
            if r == 6 and random.random() < 0.3: break
        for k in (5, 6):
            pass
        best[r] = max(best.get(r, 0), pc(S))
    print(kind, 'random greedy max lines in rank-<=6 closed subsets:', best, flush=True)
