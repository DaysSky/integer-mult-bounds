"""Exact min decoder cost for a small root system over windows w0..w1: each piece picks a flat pair (A, C) (sources
inside A, readers inside C), cost = pairing rank(A, C) (exact, = rank G[Q,P] for P,Q spanning A,C).  SAT with a
pseudo-Boolean budget.  usage: exactsmall.py NAME budget w0 w1"""
import sys, time, itertools, numpy as np
sys.path.insert(0, '../newunit')
from smallsys import roots, gram
from pysat.solvers import Cadical153
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
name, budget, w0, w1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
R, sc = roots(name); G, A = gram(R, sc); v = len(G); A = A.astype(float)
NON = [[s for s in range(v) if s != t and G[t, s] != 0] for t in range(v)]
def closure(idx):
    if not idx: return frozenset()
    M = A[list(idx)]; r = np.linalg.matrix_rank(M); U, S, Vt = np.linalg.svd(M, full_matrices=False); B = Vt[:r]
    return frozenset(np.where(np.abs(A @ B.T @ B - A).max(1) < 1e-9)[0].tolist())
flats = {frozenset()}; frontier = {frozenset()}
while frontier:
    nxt = set()
    for F in frontier:
        for s in range(v):
            if s not in F:
                C = closure(sorted(F) + [s])
                if C not in flats: flats.add(C); nxt.add(C)
    frontier = nxt
flats = sorted(flats, key=lambda F: (len(F), sorted(F)))
def prk(Aset, Cset):
    if not Aset or not Cset: return 0
    return int(np.linalg.matrix_rank(A[sorted(Aset)] @ A[sorted(Cset)].T))
pairs = [(F1, F2, prk(F1, F2)) for F1 in flats for F2 in flats if F1 and F2]
print(name, 'v', v, 'flats', len(flats), 'flat pairs', len(pairs), flush=True)
for w in range(w0, w1 + 1):
    pool = IDPool(); cl = []
    p = [[pool.id(('p', j, s)) for s in range(v)] for j in range(w)]; q = [[pool.id(('q', j, t)) for t in range(v)] for j in range(w)]
    def AND(a, b):
        x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
    def xor_eq(lits, val):
        acc = lits[0]
        for l in lits[1:]:
            x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
        cl.append([acc] if val else [-acc])
    for t in range(v):
        for s in [t] + NON[t]: xor_eq([AND(q[j][t], p[j][s]) for j in range(w)], 1 if s == t else 0)
    costbits = []
    for j in range(w):
        sel = []
        hmax = max(c for _, _, c in pairs)
        cb = [pool.id(('cb', j, k)) for k in range(hmax)]; costbits.extend(cb)
        for k, (F1, F2, c) in enumerate(pairs):
            sv = pool.id(('sel', j, k)); sel.append(sv)
            for s in range(v):
                if s not in F1: cl.append([-sv, -p[j][s]])
                if s not in F2: cl.append([-sv, -q[j][s]])
            for kk in range(c): cl.append([-sv, cb[kk]])
        # empty piece allowed: if no selector, force p,q empty
        none = pool.id(('none', j)); sel.append(none)
        for s in range(v): cl.extend([[-none, -p[j][s]], [-none, -q[j][s]]])
        cl.append(sel)
    enc = CardEnc.atmost(lits=costbits, bound=budget, vpool=pool, encoding=EncType.seqcounter); cl.extend(enc.clauses)
    S = Cadical153(bootstrap_with=cl); t0 = time.time(); ok = S.solve()
    print('  window %d, cost <= %d:' % (w, budget), 'SAT' if ok else 'UNSAT', '%.0fs' % (time.time() - t0), flush=True)
