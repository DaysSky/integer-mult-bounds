"""Exhaustive: for every node type F (Stab(t)-orbit representative frame through t, t = P(0,1) / T(0,1,2)) that occurs
in 4-covers, the minimum over ALL covers containing F of rank(ex(t,F,c)) (the lines of R(t) covered only by F), versus
the node rank r_F = rank(F-perp).  min rank == r_F means t's part at such a node is ALWAYS full-rank (forced), the
mechanism behind the triangle-node waste.  usage: lr8forced.py"""
import pickle, collections
from lgeo import *
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    print(kind, SUPP[t])
    for F1, covs in sorted(D['covers'].items(), key=lambda kv: -len(kv[1])):
        if not covs: continue
        rF = rank(pm(F1)); mins = 99; hist = collections.Counter()
        for c in covs:
            P = {F: pm(F) & R for F in c}
            ex = P[F1]
            for F in c:
                if F != F1: ex &= ~P[F]
            r = rank(ex) if ex else 0
            hist[r] += 1; mins = min(mins, r)
        print('   %-42s lines %d perp %2d rank %d | covers %5d | ex rank hist %s | forced full-rank: %s' % (
            ' '.join('%s%s' % (KIND[s], ''.join(map(str, SUPP[s]))) for s in bits(F1)), pc(F1), pc(pm(F1)), rF, len(covs),
            dict(sorted(hist.items())), 'YES' if mins == rF else 'no'), flush=True)
