"""Window-w E8 decoders in which every piece is E7-deficient: its sources P_j or its readers Q_j lie in z_j^perp for
some line z_j (cost <= 7 each).  The solver chooses side and z_j.  Symmetry: piece 0 uses z = line 0 (side given).
usage: e7def.py w side0(P|Q) [n_full]   (n_full extra unrestricted pieces, cost 8 each)"""
import sys, time
from e8dec import G, v, NON
from pysat.solvers import Cadical153
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
SIDES = sys.argv[4] if len(sys.argv) > 4 else "PQ"
w = int(sys.argv[1]); side0 = sys.argv[2]; nfull = int(sys.argv[3]) if len(sys.argv) > 3 else 0
W = w + nfull
pool = IDPool(); cl = []
p = [[pool.id(('p', j, s)) for s in range(v)] for j in range(W)]
q = [[pool.id(('q', j, t)) for t in range(v)] for j in range(W)]
def AND(a, b):
    x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
def xor_eq(lits, val):
    acc = lits[0]
    for l in lits[1:]:
        x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
    cl.append([acc] if val else [-acc])
for t in range(v):
    for s in [t] + NON[t]:
        xor_eq([AND(q[j][t], p[j][s]) for j in range(W)], 1 if s == t else 0)
for j in range(w):
    sel = {}
    for side in SIDES:
        for z in range(v):
            sel[side, z] = pool.id(('sel', j, side, z))
            X = p[j] if side == 'P' else q[j]
            for s in [z] + NON[z]:            # lines not orthogonal to z (z itself too) are excluded
                cl.append([-sel[side, z], -X[s]])
    lits = list(sel.values())
    cl.append(lits)                           # at least one deficiency certificate
    if j == 0:
        cl.append([sel[side0, 0]])
S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
print('window %d: %d E7-deficient pieces (piece 0 side %s) + %d full -> cost <= %d :' % (W, w, side0, nfull, 7 * w + 8 * nfull),
      'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
if ok:
    import numpy as np
    from e8dec import pairing_rank
    m = set(l for l in S.get_model() if l > 0)
    P = [[s for s in range(v) if p[j][s] in m] for j in range(W)]; Q = [[t for t in range(v) if q[j][t] in m] for j in range(W)]
    print('  costs', [pairing_rank(a, c) for a, c in zip(P, Q)], 'sizes', [(len(a), len(c)) for a, c in zip(P, Q)])
