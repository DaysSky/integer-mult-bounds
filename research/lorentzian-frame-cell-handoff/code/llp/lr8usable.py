"""EXHAUSTIVE: for every frame F through t that occurs in some 4-cover of R(t) (t = P(0,1), T(0,1,2), orbit reps),
which other lines b of F can also use F (F occurs in some 4-cover of R(b))?  Uses canonical forms of (b, F) and the
per-orbit cover counts N(F1) of lr8allcovers_<kind>.pkl.  'Usable users' bounds node sharing in any design whose
nodes are rank-8 sections F-perp.  usage: lr8usable.py"""
import pickle, itertools, collections
from lgeo import *
tabs = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    tabs[kind] = {canon((1 << t, F1))[0]: len(c) for F1, c in D['covers'].items()}
    # include orbits with zero covers: all frame orbits through t
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    for F in fr:
        cf = canon((1 << t, F))[0]
        tabs[kind].setdefault(cf, 0)
def ncov(b, F):
    return tabs[KIND[b]][canon((1 << b, F))[0]]
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    print(kind, SUPP[t])
    for F1, covs in sorted(D['covers'].items(), key=lambda kv: -len(kv[1])):
        if not covs: continue
        us = [b for b in bits(F1)]
        usable = [b for b in us if ncov(b, F1) > 0]
        print('   frame %-40s lines %d perp %d rank %d covers(t) %5d | usable users %d of %d: %s' % (
            ' '.join('%s%s' % (KIND[s], ''.join(map(str, SUPP[s]))) for s in bits(F1)), pc(F1), pc(pm(F1)), rank(pm(F1)), len(covs),
            len(usable), len(us), ' '.join('%s%s' % (KIND[s], ''.join(map(str, SUPP[s]))) for s in usable)), flush=True)
