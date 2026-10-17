"""Structure of window-10 E8 decoders: force B_ts = 0 on one orthogonal pair (t, s) (B0 has 1 there) and inspect
E = B + B0 (support on orthogonal pairs), its rank and pattern."""
import sys, numpy as np, time
from e8dec import G, v, NON, A
from pysat.solvers import Cadical153
from pysat.formula import IDPool
def f2rank(M):
    M = (np.array(M) % 2).astype(np.uint8).copy(); r = 0
    for c in range(M.shape[1]):
        p = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
w = int(sys.argv[1]); nz = int(sys.argv[2])
pool = IDPool(); cl = []
W = [[pool.id(('w', t, j)) for j in range(w)] for t in range(v)]; U = [[pool.id(('u', t, j)) for j in range(w)] for t in range(v)]
def AND(a, b):
    x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
def XOR(lits):
    acc = lits[0]
    for l in lits[1:]:
        x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
    return acc
Bv = {}
orth = [(t, s) for t in range(v) for s in range(v) if t != s and G[t, s] == 0]
for t in range(v):
    for s in range(v):
        if s == t or G[t, s] != 0 or (t, s) in orth[:nz]:
            Bv[t, s] = XOR([AND(W[t][j], U[s][j]) for j in range(w)])
for t in range(v): cl.append([Bv[t, t]])
for t in range(v):
    for s in NON[t]: cl.append([-Bv[t, s]])
for (t, s) in orth[:nz]: cl.append([-Bv[t, s]])
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve(); print('w', w, 'zeroed orth pairs', nz, 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0))
if ok:
    m = set(l for l in S.get_model() if l > 0)
    Wm = np.array([[1 if W[t][j] in m else 0 for j in range(w)] for t in range(v)]); Um = np.array([[1 if U[t][j] in m else 0 for j in range(w)] for t in range(v)])
    B = (Wm @ Um.T) % 2
    B0 = np.array([[1 if (t == s or G[t, s] == 0) else 0 for s in range(v)] for t in range(v)])
    E = (B + B0) % 2
    print('rank B', f2rank(B), 'rank E', f2rank(E), 'nnz E', E.sum(), 'symmetric', (B == B.T).all(), 'row weights B min/avg', B.sum(1).min(), B.sum(1).mean())
    np.save('B_w%d_nz%d.npy' % (w, nz), B)
