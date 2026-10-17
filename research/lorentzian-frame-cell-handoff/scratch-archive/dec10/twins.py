"""Repeated-label units: E8 with every line used by r ports (twins share a label).  Decoder pattern: B_PP = 1,
B_PQ = 0 when the labels are non-orthogonal or equal (twins), free on orthogonal labels.  F2 minrank by SAT (B = W U^T).
usage: twins.py r w [symmetric]"""
import sys, time
from e8dec import G, v, NON
from pysat.solvers import Cadical153
from pysat.formula import IDPool
r, w = int(sys.argv[1]), int(sys.argv[2]); sym = len(sys.argv) > 3
ports = [(t, i) for t in range(v) for i in range(r)]; n = len(ports)
pool = IDPool(); cl = []
W = [[pool.id(('w', p, j)) for j in range(w)] for p in range(n)]
U = W if sym else [[pool.id(('u', p, j)) for j in range(w)] for p in range(n)]
def AND(a, b):
    x = pool.id(('a', min(a, b), max(a, b))); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
def xor_eq(lits, val):
    acc = lits[0]
    for l in lits[1:]:
        x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
    cl.append([acc] if val else [-acc])
idx = {p: k for k, p in enumerate(ports)}
for a, (t, i) in enumerate(ports):
    xor_eq([AND(W[a][j], U[a][j]) for j in range(w)], 1)
    for s in [t] + NON[t]:
        for k in range(r):
            if s == t and k == i: continue
            b = idx[(s, k)]
            if sym and b < a: continue
            xor_eq([AND(W[a][j], U[b][j]) for j in range(w)], 0)
# gauge: first clique ports fixed? (skip) 
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
print('E8 x%d (%d ports), window %d%s:' % (r, n, w, ' symmetric' if sym else ''), 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
