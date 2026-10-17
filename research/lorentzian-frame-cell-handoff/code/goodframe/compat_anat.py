import sys, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); comp = pickle.load(open('compat.pkl', 'rb'))
idx = {tuple(sorted(q)): i for i, q in enumerate(good)}
def pts(q):
    s = set()
    for x in q: s |= set(g.supp[x])
    return s
for q0 in [tuple(sorted((g.P(0,1), g.P(2,3), g.T(0,1,4), g.T(2,3,4)))), tuple(sorted((g.T(0,1,2), g.T(0,3,4), g.T(1,3,5), g.T(2,4,5))))]:
    i0 = idx[q0]; Z = pts(q0)
    cs = set(comp[i0].tolist())
    st = collections.Counter(); tot = collections.Counter()
    for j, q in enumerate(good):
        if set(q) & set(q0): continue
        key = (''.join(sorted(g.kind[x] for x in q)), len(pts(q) & Z), len(pts(q)))
        tot[key] += 1
        if j in cs: st[key] += 1
    print('frame', [(g.kind[x], g.supp[x]) for x in q0], 'support', sorted(Z))
    for k in sorted(tot): print('  ', k, '%d / %d' % (st[k], tot[k]))
