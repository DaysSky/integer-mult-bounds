"""Duals of the clique-only hitting LP (cached counts) -> duals0.pkl for colgen.py."""
import pickle, numpy as np
from scipy.optimize import linprog
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
reps = pickle.load(open(D + 'flats_reps.pkl', 'rb'))
flist = [(r, cl) for r in sorted(reps) for cl in reps[r].values()]
orb = pickle.load(open(D + 'corbits2.pkl', 'rb'))
okeys = list(orb)
Ac = np.load(D + 'clique_counts.npz')['A']
csz = np.array([len(orb[k]) for k in okeys], float)
cq = np.array([len(orb[k][0]) for k in okeys], float)
A = np.vstack([Ac, csz])
b = np.array([r for r, cl in flist] + [11], float)
res = linprog(-csz * cq, A_ub=A, b_ub=b, bounds=[(0, None)] * len(okeys), method='highs')
y = -np.asarray(res.ineqlin.marginals)
duals = [(float(y[i]), tuple(flist[i][1]) if i < len(flist) else tuple(range(220)))
         for i in range(len(b)) if y[i] > 1e-9]
print('LP', -res.fun, 'positive duals', len(duals))
pickle.dump(duals, open(D + 'duals0.pkl', 'wb'))
