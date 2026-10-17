import sys, pickle, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); n = len(good); comp = pickle.load(open('compat.pkl', 'rb'))
F = np.array(good)
cnt = np.zeros((n, V), dtype=np.int32)       # cnt[i, x] = # frames compatible with i that contain x
for i, js in enumerate(comp):
    if len(js): np.add.at(cnt[i], F[js].ravel(), 1)
own = np.zeros((n, V), dtype=bool); own[np.arange(n)[:, None], F] = True
kill = ((cnt == 0) & ~own).sum(1)
kinds = np.array([''.join(sorted(g.kind[x] for x in q)) for q in good])
print('kills per frame: min', kill.min(), 'max', kill.max(), 'histogram', sorted(collections.Counter(kill.tolist()).items())[:15])
for k in ('PPTT', 'TTTT'): print(k, 'min kill', kill[kinds == k].min())
i = int(kill.argmin()); print('min-kill frame', [(g.kind[x], g.supp[x]) for x in good[i]], 'killed', [(g.kind[x], g.supp[x]) for x in np.nonzero((cnt[i] == 0) & ~own[i])[0]][:12])
