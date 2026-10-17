# Partial-section tops with a small defect D (lines outside the free sets that remain after choosing c1..c3):
# report the minimum |D| over all section triples / part choices, and the kinds achieving it (D readable at rank <= 2?).
import sys, itertools, numpy as np, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
tname = sys.argv[1]
secs, _ = pickle.load(open('ptop2_%s.pkl' % tname, 'rb'))
from cov2 import mask
t = g.T(0, 1, 2) if tname == 'T' else g.P(0, 1)
Rt = g.HYP[t]
opts = []
for u, H, cov, users in secs:
    o = [('F', mask(H), 0)]
    for (Fa, Fb) in cov:
        I = set(Fa) & set(Fb); a_only = set(Fa) - I; b_only = set(Fb) - I
        o.append(('p', mask(a_only), mask(I))); o.append(('q', mask(b_only) ^ mask(I), mask(I)))
    opts.append(o)
best = 99; hist = collections.Counter(); ex = []
for (i1, i2, i3) in itertools.combinations(range(len(secs)), 3):
    for o1 in opts[i1]:
        for o2 in opts[i2]:
            f12 = o1[1] ^ o2[1]; fr12 = o1[2] | o2[2]
            for o3 in opts[i3]:
                D = (Rt ^ f12 ^ o3[1]) & ~(fr12 | o3[2])
                k = bin(D).count('1')
                if k <= 3:
                    hist[k] += 1
                    if k < best: best = k; ex = []
                    if k == best and len(ex) < 50: ex.append(((i1, o1[0]), (i2, o2[0]), (i3, o3[0]), bits(D)))
print(tname, '| min defect', best, '| counts by defect size <=3:', sorted(hist.items()), flush=True)
for e in ex[:8]:
    D = e[3]
    print('  users', [len(secs[i][3]) for i, f in e[:3]], 'parts', [f for i, f in e[:3]], 'defect', [(g.kind[d], g.supp[d]) for d in D],
          'defect rank', dim(mask(D)) if D else 0)
