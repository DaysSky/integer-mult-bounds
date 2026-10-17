import sys, pickle, random, time, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V
good = pickle.load(open('good4.pkl', 'rb')); n = len(good); comp = pickle.load(open('compat.pkl', 'rb'))
C = np.zeros((n, n), dtype=bool)
for i, js in enumerate(comp): C[i, js] = True
incf = np.zeros((V, n), dtype=np.float32)
for i, q in enumerate(good): incf[list(q), i] = 1
seed = int(sys.argv[1]); T = float(sys.argv[2]); rng = random.Random(seed); np.random.seed(seed)
t0 = time.time(); best = (0, None)
while time.time() - t0 < T:
    cand = np.ones(n, dtype=bool); covered = np.zeros(V, dtype=bool); chosen = []; punct = 0
    while True:
        cnt = incf @ cand.astype(np.float32)
        free = ~covered
        zero = free & (cnt == 0)
        if zero.any():
            nz = int(zero.sum())
            if punct + nz > 4: break
            punct += nz; covered |= zero
            for x in np.nonzero(zero)[0]: cand &= incf[x] == 0
            continue
        if not free.any(): break
        fl = np.nonzero(free)[0]
        x = fl[np.argmin(cnt[fl] + np.random.rand(len(fl)) * 0.5)]
        cx = np.nonzero(cand & (incf[x] > 0))[0]
        if len(cx) > 40: cx = np.random.choice(cx, 40, replace=False)
        scores = []
        for j in cx:
            nc = cand & C[j]
            c2 = incf @ nc.astype(np.float32)
            cov2 = covered.copy(); cov2[list(good[j])] = True
            f2 = ~cov2
            z = int((f2 & (c2 == 0)).sum())
            m = c2[f2].min() if f2.any() else 99
            scores.append((z, -m - rng.random(), j))
        scores.sort()
        z, _, j = scores[0]
        chosen.append(int(j)); covered[list(good[j])] = True; cand &= C[j]
    ncov = int(covered.sum()) - punct
    if ncov > best[0]:
        best = (ncov, list(chosen), punct); print('covered', ncov, 'frames', len(chosen), 'punct', punct, round(time.time() - t0), flush=True)
        pickle.dump(best, open('alignla_%d.pkl' % seed, 'wb'))
        if ncov >= 216: break
print('best', best[0])
