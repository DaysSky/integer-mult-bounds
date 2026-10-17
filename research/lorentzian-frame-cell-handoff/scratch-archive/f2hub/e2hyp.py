# For each E-set / IN content of rank 9: is it inside a union of two hyperplanes of its span?  (quadratic forms
# vanishing on its lines; report the dimension of that space and the min rank found)
import sys, pickle, itertools, collections, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V, nondegenerate, closure
HYP = g.HYP
def pm(m):
    r = g.FULL
    for s in bits(m): r &= HYP[s]
    return r
B2 = lambda x, y: (1 << x) | (1 << y)
L = g.L.astype(float)
def qforms(m):
    X = L[bits(m)]
    U, S, Vt = np.linalg.svd(X); r = int((S > 1e-9).sum()); B = Vt[:r]; C = X @ B.T
    iu = np.triu_indices(r)
    M = np.array([np.outer(c, c)[iu] for c in C])
    _, s, vt = np.linalg.svd(M)
    nul = vt[(s > 1e-9).sum():] if len(s) == M.shape[1] else vt[np.sum(s > 1e-9):]
    k = M.shape[1] - np.linalg.matrix_rank(M)
    return r, k
# representative frames: PPTT and TTTT
frames, pun = pickle.load(open('/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/goodframe/goodpart.pkl', 'rb'))
reps = {}
for q in frames:
    key = ''.join(sorted(g.kind[x] for x in q))
    reps.setdefault(key, q)
for key, q in reps.items():
    t, a, b, c = q
    U = B2(t, a) | B2(b, c); Q = pm(U)
    for x, y in itertools.combinations(q, 2):
        Exy = pm(B2(x, y)) & ~Q & ~U
        zw = [z for z in q if z not in (x, y)]
        for name, m in (('E', Exy), ('E+Q', Exy | Q), ('pm', pm(B2(x, y)))):
            r, k = qforms(m)
            print(key, g.kind[x] + g.kind[y], name, bin(m).count('1'), 'rank', r, 'null quad forms', k)
