"""Largest pairwise NON-orthogonal set among E8+E8 norm-4 lines (lower bound for the decoder rank of the E8^2 pattern:
B[K,K] = I on such a set).  Randomised greedy.  usage: e8sq_alpha.py seconds seed"""
import itertools, sys, time, numpy as np
T = float(sys.argv[1]); rng = np.random.default_rng(int(sys.argv[2]))
R = []
for i, j in itertools.combinations(range(8), 2):
    for a, b in itertools.product((2, -2), repeat=2):
        v = [0] * 8; v[i] = a; v[j] = b; R.append(v)
for s in itertools.product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0: R.append(list(s))
R = np.array(R); G = R @ R.T
N4 = set()
for a in range(240):
    for b in np.nonzero(G[a] == 0)[0]: N4.add(tuple(R[a] + R[b]))
N4 = np.array(sorted(N4)); Z4 = np.zeros((2160, 8), int)
V = np.vstack([np.hstack([N4, Z4]), np.hstack([Z4, N4]), np.array([np.concatenate([r, s]) for r in R for s in R])])
def canon(v):
    nz = np.nonzero(v)[0][0]; return v if v[nz] > 0 else -v
L = np.unique(np.array([canon(v) for v in V]), axis=0); n = len(L)
deg = None
print('lines', n, flush=True)
best = 0; t0 = time.time(); it = 0
while time.time() - t0 < T:
    it += 1; order = rng.permutation(n); alive = np.ones(n, bool); S = []
    for v in order:
        if not alive[v]: continue
        S.append(v); alive &= (L @ L[v]) != 0; alive[v] = False
    if len(S) > best:
        best = len(S); print('it', it, 'pairwise non-orthogonal set size', best, '%.0fs' % (time.time() - t0), flush=True)
print('best', best, '(decoder rank >= this; the mod-4 decoder has rank 815)')
