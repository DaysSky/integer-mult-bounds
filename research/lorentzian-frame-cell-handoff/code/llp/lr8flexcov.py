"""Exhaustive census (representative covers up to Stab(t)) of 'forced isolated closures': frames of the cover whose
node F-perp has rank 8 and whose exclusive part has rank >= 7 (its part then has rank >= 7 inside a rank-8 node: a
forced rank-7 closure or a spanning part).  Covers with 0 such frames keep every part either on a rank-7 node
(auto-sharing) or of rank <= 6 (closure free).  usage: lr8flexcov.py"""
import pickle, collections
from lgeo import *
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    PRK = {}; hist = collections.Counter(); best = []
    for F1, covs in D['covers'].items():
        for c in covs:
            P = [pm(F) & R for F in c]; bad = 0; desc = []
            for i, F in enumerate(c):
                if F not in PRK: PRK[F] = rank(pm(F))
                ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
                rx = rank(ex) if ex else 0
                if PRK[F] == 8 and rx >= 7: bad += 1
                desc.append((pc(F), pc(pm(F)), PRK[F], pc(ex), rx))
            hist[bad] += 1
            if bad == 0: best.append((c, desc))
    print(kind, 'representative covers by #forced isolated closures:', sorted(hist.items()))
    tc = collections.Counter(tuple(sorted(d)) for c, d in best)
    for k, v in tc.most_common(6): print('   ', k, v)
    pickle.dump(best, open('lr8flex_%s.pkl' % kind, 'wb'))
