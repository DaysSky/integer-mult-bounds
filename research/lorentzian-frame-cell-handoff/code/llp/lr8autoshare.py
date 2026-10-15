"""Frame orbits through t (P and T) with the rank of their perp line set; and exhaustive count of 4-covers of R(t)
whose four nodes all have perp RANK 7 ('auto-sharing' nodes: every rank-7 part on such a node has the node itself as
span closure, so all its users share the rank-7 stop).  Uses lr8allcovers_<kind>.pkl.  usage: lr8autoshare.py"""
import pickle, collections, itertools
from lgeo import *
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    prk = {F: rank(pm(F)) for F in fr}
    hist = collections.Counter((pc(F), pc(pm(F)), prk[F]) for F in fr)
    print(kind, SUPP[t], 'frames by (lines, perp lines, perp rank):', sorted(hist.items()))
    tot = 0; auto = 0; auto_types = collections.Counter(); some = collections.Counter()
    for F1, covs in D['covers'].items():
        for c in covs:
            tot += 1
            r7 = sum(1 for F in c if prk.get(F, rank(pm(F))) == 7)
            some[r7] += 1
            if r7 == 4:
                auto += 1; auto_types[tuple(sorted((pc(F), pc(pm(F))) for F in c))] += 1
    print('  representative covers', tot, '| by #rank-7-perp nodes', sorted(some.items()), '| all four rank-7:', auto)
    for k, v in auto_types.most_common(8): print('    ', k, v)
