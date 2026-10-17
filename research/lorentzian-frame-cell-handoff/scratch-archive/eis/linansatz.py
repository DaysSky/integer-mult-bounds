"""Linear-over-F2 ansatz: B = J + sum x_(u,w) 1_{u^perp} 1_{w^perp}^T over ordered collinear pairs."""
import pickle, numpy as np, itertools
from f2 import rank2
d = pickle.load(open('eis.pkl','rb'))
n = 40
orth = d['orth']; nonorth = d['nonorth']
O = np.array([[(orth[t]>>s)&1 for s in range(n)] for t in range(n)], dtype=np.uint8)
pairs = [(u, w) for u in range(n) for w in range(n) if O[u, w]]
print('ordered collinear pairs', len(pairs))
# constraint rows: entries (t,s) diag -> want B=1, J gives 1 so need sum=0; non-orth -> want 0, J gives 1 so sum=1
cons = [(t, t, 0) for t in range(n)] + [(t, s, 1) for t in range(n) for s in range(n) if (nonorth[t]>>s)&1]
A = np.zeros((len(cons), len(pairs)), dtype=np.uint8)
rhs = np.array([c[2] for c in cons], dtype=np.uint8)
for j, (u, w) in enumerate(pairs):
    for k, (t, s, v) in enumerate(cons):
        A[k, j] = O[t, u] & O[s, w]
rA = rank2(A); rAb = rank2(np.hstack([A, rhs[:, None]]))
print('rank A', rA, 'rank [A|b]', rAb, 'consistent' if rA == rAb else 'INCONSISTENT')
np.save('lin_A.npy', A); np.save('lin_b.npy', rhs)
pickle.dump(pairs, open('lin_pairs.pkl', 'wb'))
