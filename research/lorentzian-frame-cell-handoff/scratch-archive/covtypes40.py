"""Exhaustive census of 4-cover TYPES by node type (frame lines, perp size, usable users) for P and T, from the full
rebuilt lists; reports the types with the largest total usable users (sharing potential).  usage: lr8covtypes.py"""
import pickle, itertools, collections
from lgeo import *
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
tabs = {}; full = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {F: canon((1 << t, F)) for F in fr}
    tabs[kind] = {canon_of[F1][0]: len(c) for F1, c in D['covers'].items()}
    for F in fr: tabs[kind].setdefault(canon_of[F][0], 0)
    full[kind] = (t, D, fr, canon_of)
usable = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    for F1 in D['covers']:
        usable[canon_of[F1][0]] = (sum(1 for b in bits(F1) if KIND[b] == 'P' and tabs['P'][canon((1 << b, F1))[0]] > 0),
                                   sum(1 for b in bits(F1) if KIND[b] == 'T' and tabs['T'][canon((1 << b, F1))[0]] > 0))
ALLT = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    rep_of = {canon_of[F1][0]: F1 for F1 in D['covers']}
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]; F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]; ipF = inv(pF); g = [ipF[p1[x]] for x in range(n)]
        for c in D['covers'][F1]: allc.add(tuple(sorted(act(X, g) for X in c)))
    types = collections.Counter()
    for c in allc:
        types[tuple(sorted(((pc(F), pc(pm(F))) + usable[canon_of[F][0]]) for F in c))] += 1
    ALLT[kind] = types
    print(kind, 'distinct node-type covers', len(types))
    # sharing score: sum over nodes of 1/(usable users)  (node-uses cost if every user shares)
    sc = sorted(types.items(), key=lambda kv: sum(1.0 / (x[2] + x[3]) for x in kv[0]))
    for k, v in sc[:40]:
        print('   %-90s covers %6d  node-cost %.3f' % (k, v, sum(1.0 / (x[2] + x[3]) for x in k)))

