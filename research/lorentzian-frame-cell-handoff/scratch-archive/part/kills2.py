import sys, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); n = len(good); comp = pickle.load(open('compat.pkl', 'rb'))
F = np.array(good)
C = np.zeros((n, n), dtype=bool)
for i, js in enumerate(comp): C[i, js] = True
inc = np.zeros((V, n), dtype=bool)
for i, q in enumerate(good): inc[list(q), i] = True
idx = {tuple(sorted(q)): i for i, q in enumerate(good)}
reps = [idx[tuple(sorted((g.P(0,1), g.P(2,3), g.T(0,1,4), g.T(2,3,4))))], idx[tuple(sorted((g.T(0,1,2), g.T(0,3,4), g.T(1,3,5), g.T(2,4,5))))]]
for i in reps:
    ks = []
    for j in comp[i]:
        both = C[i] & C[j]
        cov = (inc[:, both].any(1))
        own = np.zeros(V, dtype=bool); own[list(good[i]) + list(good[j])] = True
        ks.append(int((~cov & ~own).sum()))
    ks = np.array(ks)
    print('rep', [(g.kind[x], g.supp[x]) for x in good[i]], 'pair kills: min', ks.min(), 'mean %.1f' % ks.mean(), 'max', ks.max(), 'pairs with kill<=4:', int((ks <= 4).sum()), 'of', len(ks))
