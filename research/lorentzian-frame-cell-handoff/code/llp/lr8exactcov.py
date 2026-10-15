"""Exhaustive: 4-covers of R(t) by rank-3-frame perps that are EXACT (pairwise disjoint perps inside R(t)), and
near-exact ones (total overlap small).  Rebuilds the full cover lists as lr8flexpool.py.  usage: lr8exactcov.py"""
import pickle, itertools, collections
from lgeo import *
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {F: canon((1 << t, F)) for F in fr}
    rep_of = {canon_of[F1][0]: F1 for F1 in D['covers']}
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]; F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]; ipF = inv(pF); g = [ipF[p1[x]] for x in range(n)]
        for c in D['covers'][F1]: allc.add(tuple(sorted(act(X, g) for X in c)))
    ov = collections.Counter(); ex = []
    for c in allc:
        P = [pm(F) & R for F in c]
        o = sum(pc(p) for p in P) - pc(R)
        ov[o] += 1
        if o == 0: ex.append(c)
    print(kind, 'covers', len(allc), '| overlap (sum |perp| - |R|) histogram (smallest 8):', sorted(ov.items())[:8], flush=True)
    pickle.dump(ex, open('lr8exactcov_%s.pkl' % kind, 'wb'))
