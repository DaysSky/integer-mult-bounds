"""E8 decoders with F full pieces plus tiny pieces whose source set has <= k lines (cost <= rank <= k).
usage: tiny.py F n_tiny k [readers_tiny_max]"""
import sys, time, numpy as np
from e8dec import G, v, NON, A, pairing_rank
from pysat.solvers import Cadical153
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
F, nt, k = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
w = F + nt; pool = IDPool(); cl = []
p = [[pool.id(('p', j, s)) for s in range(v)] for j in range(w)]
q = [[pool.id(('q', j, t)) for t in range(v)] for j in range(w)]
def AND(a, b):
    x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
def xor_eq(lits, val):
    acc = lits[0]
    for l in lits[1:]:
        x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
    cl.append([acc] if val else [-acc])
for t in range(v):
    for s in [t] + NON[t]:
        xor_eq([AND(q[j][t], p[j][s]) for j in range(w)], 1 if s == t else 0)
for j in range(F, w):
    enc = CardEnc.atmost(lits=p[j], bound=k, vpool=pool, encoding=EncType.seqcounter); cl.extend(enc.clauses)
# symmetry: line 0 in source set of the first tiny piece (all lines equivalent under W(E8))
if nt: cl.append([p[F][0]])
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
print('full %d + tiny %d (<= %d lines): window %d, cost <= %d ->' % (F, nt, k, w, 8 * F + k * nt), 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
if ok:
    m = set(l for l in S.get_model() if l > 0)
    P = [[s for s in range(v) if p[j][s] in m] for j in range(w)]; Q = [[t for t in range(v) if q[j][t] in m] for j in range(w)]
    costs = [pairing_rank(a, c) for a, c in zip(P, Q)]
    print('  piece costs', costs, 'total', sum(costs), 'sizes', [(len(a), len(c)) for a, c in zip(P, Q)])
    np.save('tiny_%d_%d_%d.npy' % (F, nt, k), np.array([[1 if s in P[j] else 0 for s in range(v)] for j in range(w)] + [[1 if t in Q[j] else 0 for t in range(v)] for j in range(w)]))
