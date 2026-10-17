"""Linear-over-F2 model: B = sum_j x_j 1_{F_j} 1_{G_j}^T over flat pairs (F_j,G_j); which cost classes span the target?"""
import pickle, numpy as np
from f2 import rank2
d = pickle.load(open('eis.pkl','rb'))
n = 40; fl = d['flat_list']; C = d['cost'].astype(int); nonorth = d['nonorth']
nf = len(fl)
cons = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t]>>s)&1]
ti = np.array([c[0] for c in cons]); si = np.array([c[1] for c in cons]); b = np.array([c[2] for c in cons], dtype=np.uint8)
mem = np.array([[(f >> t) & 1 for t in range(n)] for f in fl], dtype=np.uint8)  # nf x n
def col(a, g):
    return mem[a][ti] & mem[g][si]
res = {}
for cmax in (1, 2, 3, 4):
    idx = [(a, g) for a in range(nf) for g in range(nf) if fl[a] and fl[g] and C[a, g] <= cmax]
    # dedupe identical columns
    M = np.array([col(a, g) for a, g in idx], dtype=np.uint8)
    Mu, inv = np.unique(M, axis=0, return_index=True)
    r = rank2(Mu); rb = rank2(np.vstack([Mu, b[None, :]]))
    print('cost<=%d pairs %d distinct cols %d rank %d with target %d -> %s' % (cmax, len(idx), len(Mu), r, rb, 'IN SPAN' if r == rb else 'not in span'), flush=True)
