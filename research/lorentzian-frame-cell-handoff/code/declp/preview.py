"""Preview (upper estimate) of the clique-hitting LP using only structured flats."""
import sys, pickle, numpy as np, itertools, collections
from scipy.optimize import linprog
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp')
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
import flats
G = g.G
D = '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/'
orb = pickle.load(open(D + 'corbits.pkl', 'rb'))
okeys = list(orb)
fl = []
fl.append(flats.closure([0])); fl.append(flats.closure([55]))
perp = lambda a, b: G[a, b] == 0
for a, b in [(0, 55), (0, 56)] + [(i, j) for i in range(V) for j in range(i + 1, V) if perp(i, j)][:400]:
    if perp(a, b): fl.append(flats.closure([a, b]))
for t in [0, 55]:
    fl.append(flats.closure([s for s in range(V) if s != t and perp(s, t)]))
for p in range(1):
    fl.append(flats.closure([x for x in range(V) if (p in g.supp[x]) == (g.kind[x] == 'T')]))
for k in range(3, 11):
    S = set(range(k)); fl.append(flats.closure([x for x in range(V) if set(g.supp[x]) <= S]))
fl = list({cl: r for cl, r in fl}.items())
print('structured flats', len(fl), flush=True)
def cnt(cl, cliques):
    s = set(cl); return sum(1 for c in cliques if any(x in s for x in c))
A = np.array([[cnt(cl, orb[k]) for k in okeys] for cl, r in fl] + [[len(orb[k]) for k in okeys]], dtype=float)
b = np.array([r for cl, r in fl] + [11], dtype=float)
cobj = -np.array([len(orb[k]) * len(orb[k][0]) for k in okeys], dtype=float)
res = linprog(cobj, A_ub=A, b_ub=b, bounds=[(0, None)] * len(okeys), method='highs')
print('preview LP value (upper estimate of the certified bound): %.4f' % -res.fun, flush=True)
for (cl, r), sl in zip(fl, b[:-1] - A[:-1] @ res.x):
    if sl < 1e-7: print('  tight: rank', r, 'lines', len(cl))
for j, k in enumerate(okeys):
    if res.x[j] > 1e-9: print('  weight %.5f size %d orbit %d' % (res.x[j], len(orb[k][0]), len(orb[k])))
