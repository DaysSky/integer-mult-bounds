import sys, pickle, collections, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
good = pickle.load(open('good4.pkl', 'rb'))
F = np.array(good, dtype=np.int64); n = len(good)
orth = (G == 0); np.fill_diagonal(orth, False)
# signature S[i, x] = 6-bit: bit k = [x in E_i(cell k)]
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S = np.zeros((n, V), dtype=np.uint8)
for k, (a, b) in enumerate(pairs):
    o = [c for c in range(4) if c not in (a, b)]
    t, e, o1, o2 = F[:, a], F[:, b], F[:, o[0]], F[:, o[1]]
    E = orth[t] & orth[e] & ~orth[o1] & ~orth[o2]          # n x V
    S |= (E.astype(np.uint8) << k)
mask = np.zeros((n, V), dtype=bool); mask[np.arange(n)[:, None], F] = True
t0 = time.time()
deg = np.zeros(n, dtype=np.int64); comp = []
for i in range(n):
    s = S[i]
    x = s[F[:, 0]] ^ s[F[:, 1]] ^ s[F[:, 2]] ^ s[F[:, 3]]      # from i's side
    ok1 = x == 0
    # from j's side: parity of E_j(cell) on frame i
    y = S[:, F[i, 0]] ^ S[:, F[i, 1]] ^ S[:, F[i, 2]] ^ S[:, F[i, 3]]
    ok = ok1 & (y == 0) & ~mask[:, F[i]].any(1)
    js = np.nonzero(ok)[0]
    deg[i] = len(js); comp.append(js.astype(np.int32))
    if i % 5000 == 0: print(i, time.time() - t0, flush=True)
print('compat degree min/mean/max', deg.min(), deg.mean(), deg.max())
kinds = np.array([''.join(sorted(g.kind[x] for x in q)) for q in good])
for k in ('PPTT', 'TTTT'): print(k, 'mean deg', deg[kinds == k].mean())
pickle.dump(comp, open('compat.pkl', 'wb'))
