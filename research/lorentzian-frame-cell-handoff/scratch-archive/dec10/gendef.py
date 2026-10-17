"""Decoders for a root system (E7, E6, D5, ...): minimal F2 window c0, then window c0+1 with every piece
'deficient' via a root hyperplane z-perp (cost <= h-1 each), solver choosing sides and centres.
usage: gendef.py NAME extra_window"""
import sys, time, numpy as np
sys.path.insert(0, '../newunit')
from smallsys import roots, gram
from pysat.solvers import Cadical153
from pysat.formula import IDPool
name = sys.argv[1]; extra = int(sys.argv[2])
R, sc = roots(name); G, A = gram(R, sc); v = len(G); A = A.astype(float); h = np.linalg.matrix_rank(A)
NON = [[s for s in range(v) if s != t and G[t, s] != 0] for t in range(v)]
def build(w, deficient):
    pool = IDPool(); cl = []
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
    if deficient:
        for j in range(w):
            sel = []
            for side in 'PQ':
                X = p[j] if side == 'P' else q[j]
                for z in range(v):
                    sv = pool.id(('sel', j, side, z)); sel.append(sv)
                    for s in [z] + NON[z]: cl.append([-sv, -X[s]])
            cl.append(sel)
    S = Cadical153(bootstrap_with=cl); ok = S.solve()
    if not ok: return None
    m = set(l for l in S.get_model() if l > 0)
    P = [[s for s in range(v) if p[j][s] in m] for j in range(w)]; Q = [[t for t in range(v) if q[j][t] in m] for j in range(w)]
    return P, Q
def prk(a, c): return int(np.linalg.matrix_rank(A[a] @ A[c].T)) if a and c else 0
c0 = None
for w in range(int(sys.argv[3]) if len(sys.argv) > 3 else 1, v + 1):
    r = build(w, False)
    if r: c0 = w; P, Q = r; break
print(name, 'v', v, 'h', h, 'min window', c0, 'sample cost', sum(prk(a, c) for a, c in zip(P, Q)), flush=True)
for w in range(c0, c0 + extra + 1):
    t0 = time.time(); r = build(w, True)
    print('  window', w, 'all pieces root-hyperplane deficient (cost <= %d):' % ((h - 1) * w), 'SAT' if r else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
    if r:
        P, Q = r; print('   costs', [prk(a, c) for a, c in zip(P, Q)])
