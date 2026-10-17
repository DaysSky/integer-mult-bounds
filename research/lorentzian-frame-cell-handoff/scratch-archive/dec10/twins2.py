"""Doubled E8 decoder rank with gauge fixing: pick 8 pairwise non-orthogonal lines K (B restricted to the 16 ports
of K x {1,2} is I_16), fix W = U = [I_16 | 0] on them (valid gauge since that block is the identity).  usage: twins2.py w"""
import sys, time, itertools
from e8dec import G, v, NON
from pysat.solvers import Cadical153
from pysat.formula import IDPool
w = int(sys.argv[1]); r = 2
# greedy clique of 8 pairwise non-orthogonal lines
K = [0]
for t in range(1, v):
    if all(G[t, k] != 0 for k in K): K.append(t)
    if len(K) == 8: break
assert len(K) == 8
ports = [(t, i) for t in range(v) for i in range(r)]; n = len(ports); idx = {p: k for k, p in enumerate(ports)}
pool = IDPool(); cl = []
W = [[pool.id(('w', p, j)) for j in range(w)] for p in range(n)]; U = [[pool.id(('u', p, j)) for j in range(w)] for p in range(n)]
gauge = [idx[(k, i)] for k in K for i in range(r)]
for c, p in enumerate(gauge):
    for j in range(w):
        cl.append([W[p][j]] if j == c else [-W[p][j]]); cl.append([U[p][j]] if j == c else [-U[p][j]])
def AND(a, b):
    x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
def xor_eq(lits, val):
    acc = lits[0]
    for l in lits[1:]:
        x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
    cl.append([acc] if val else [-acc])
for a, (t, i) in enumerate(ports):
    xor_eq([AND(W[a][j], U[a][j]) for j in range(w)], 1)
    for s in [t] + NON[t]:
        for k in range(r):
            if s == t and k == i: continue
            xor_eq([AND(W[a][j], U[idx[(s, k)]][j]) for j in range(w)], 0)
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
print('doubled E8, gauge-fixed on 16 clique ports, window %d:' % w, 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
