"""Compatibility structure of I_{13,1} good frames (exact).  For each frame type representative, count compatible
frames; vectorised over all 70,785 frames with bitset tricks via numpy boolean matrices."""
import sys, itertools, collections, numpy as np, pickle, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = 13; g = Geom(n); V = g.V; G = g.G
orth = (G == 0); np.fill_diagonal(orth, False)
frames, cand = pickle.load(open('align13_cand.pkl', 'rb'))
F = np.array(frames); nf = len(F)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S = np.zeros((nf, V), dtype=np.uint8)
for k, (a, b) in enumerate(pairs):
    o = [c for c in range(4) if c not in (a, b)]
    E = orth[F[:, a]] & orth[F[:, b]] & ~orth[F[:, o[0]]] & ~orth[F[:, o[1]]]
    S |= (E.astype(np.uint8) << k)
member = np.zeros((nf, V), dtype=bool); member[np.arange(nf)[:, None], F] = True
kinds = np.array([''.join(sorted(g.kind[x] for x in q)) for q in frames])
t0 = time.time()
deg = np.zeros(nf, dtype=np.int64)
comp_lists = []
for i in range(nf):
    s = S[i]
    x = s[F[:, 0]] ^ s[F[:, 1]] ^ s[F[:, 2]] ^ s[F[:, 3]]
    y = S[:, F[i, 0]] ^ S[:, F[i, 1]] ^ S[:, F[i, 2]] ^ S[:, F[i, 3]]
    ok = (x == 0) & (y == 0) & ~member[:, F[i]].any(1)
    js = np.nonzero(ok)[0]; deg[i] = len(js); comp_lists.append(js.astype(np.int32))
    if i % 10000 == 0: print(i, '%.0fs' % (time.time() - t0), flush=True)
for k in ('PPTT', 'TTTT'):
    d = deg[kinds == k]; print(k, 'count', len(d), 'compat degree min/mean/max', d.min(), round(d.mean(), 1), d.max())
pickle.dump((frames, comp_lists, kinds), open('compat13.pkl', 'wb'))
