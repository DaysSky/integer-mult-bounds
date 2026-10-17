"""Symmetric E8 decoders N = X X^T (x_t in F2^w, odd weight, even overlap on non-orthogonal pairs); piece j =
{t : x_t[j] = 1} has cost dim span.  Require every piece inside a root hyperplane z_j-perp (cost <= 7 each).
usage: symdef.py w"""
import sys, time
from e8dec import G, v, NON
from pysat.solvers import Cadical153
from pysat.formula import IDPool
w = int(sys.argv[1]); pool = IDPool(); cl = []
x = [[pool.id(('x', t, j)) for j in range(w)] for t in range(v)]
def AND(a, b):
    y = pool.id(('a', min(a, b), max(a, b))); cl.extend([[-y, a], [-y, b], [y, -a, -b]]); return y
def xor_eq(lits, val):
    acc = lits[0]
    for l in lits[1:]:
        y = pool.id(('x2', acc, l)); cl.extend([[-y, acc, l], [-y, -acc, -l], [y, -acc, l], [y, acc, -l]]); acc = y
    cl.append([acc] if val else [-acc])
for t in range(v):
    xor_eq(x[t], 1)
    for s in NON[t]:
        if s > t: xor_eq([AND(x[t][j], x[s][j]) for j in range(w)], 0)
for j in range(w):
    sel = [pool.id(('sel', j, z)) for z in range(v)]
    for z in range(v):
        for s in [z] + NON[z]: cl.append([-sel[z], -x[s][j]])
    cl.append(sel)
cl.append([pool.id(('sel', 0, 0))])
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
print('symmetric window %d, all pieces in root hyperplanes (cost <= %d):' % (w, 7 * w), 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
