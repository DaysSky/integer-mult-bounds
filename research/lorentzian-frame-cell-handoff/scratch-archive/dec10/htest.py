"""Hypothesis H: every valid decomposition has sum_j tr(P_Uj P_Vj) >= 72 (would imply cost >= 72).
Generate window-w decoders by SAT with random extra zeros on orthogonal pairs, decompose in many gauges (random and
deficient-biased), report min of sum tr and min cost."""
import sys, random, itertools, numpy as np, time
from e8dec import A, G, v, NON, pairing_rank
from bestdec import f2_solve_basis, inv2
from pysat.solvers import Cadical153
from pysat.formula import IDPool
An = A / np.linalg.norm(A[0])
def proj(idx):
    if len(idx) == 0: return np.zeros((8, 8))
    U, S, Vt = np.linalg.svd(An[idx], full_matrices=False); B = Vt[:(S > 1e-9).sum()]; return B.T @ B
orth = [(t, s) for t in range(v) for s in range(v) if t != s and G[t, s] == 0]
def decoder(w, nz, rng):
    pool = IDPool(); cl = []
    W = [[pool.id(('w', t, j)) for j in range(w)] for t in range(v)]; U = [[pool.id(('u', t, j)) for j in range(w)] for t in range(v)]
    def AND(a, b):
        x = pool.id(('a', a, b)); cl.extend([[-x, a], [-x, b], [x, -a, -b]]); return x
    def XOR(lits):
        acc = lits[0]
        for l in lits[1:]:
            x = pool.id(('x', acc, l)); cl.extend([[-x, acc, l], [-x, -acc, -l], [x, -acc, l], [x, acc, -l]]); acc = x
        return acc
    zs = rng.sample(orth, nz)
    for t in range(v):
        cl.append([XOR([AND(W[t][j], U[t][j]) for j in range(w)])])
        for s in NON[t]: cl.append([-XOR([AND(W[t][j], U[s][j]) for j in range(w)])])
    for (t, s) in zs: cl.append([-XOR([AND(W[t][j], U[s][j]) for j in range(w)])])
    S = Cadical153(bootstrap_with=cl)
    if not S.solve(): return None
    m = set(l for l in S.get_model() if l > 0)
    Wm = np.array([[1 if W[t][j] in m else 0 for j in range(w)] for t in range(v)]); Um = np.array([[1 if U[t][j] in m else 0 for j in range(w)] for t in range(v)])
    return (Wm @ Um.T) % 2
def gauges(B, rng, n):
    Ub, piv = f2_solve_basis(B); w = len(Ub); Wc = B[:, piv] % 2
    span = lambda idx: np.linalg.matrix_rank(A[idx]) if len(idx) else 0
    defS = [np.array(b, np.uint8) for b in itertools.product((0, 1), repeat=w) if any(b) and span(np.nonzero((np.array(b) @ Ub) % 2)[0]) <= 7] if w <= 12 else []
    out = []
    for it in range(n):
        cols = []
        pool_m = defS[:]; rng.shuffle(pool_m)
        for m in pool_m:
            if rng.random() < 0.8 and len(f2_solve_basis(np.array(cols + [m]))[0]) == len(cols) + 1: cols.append(m)
        while len(cols) < w:
            m = np.array([rng.randint(0, 1) for _ in range(w)], np.uint8)
            if len(f2_solve_basis(np.array(cols + [m]))[0]) == len(cols) + 1: cols.append(m)
        M = np.array(cols).T % 2; Mi = inv2(M)
        P = [list(np.nonzero((M[:, j] @ Ub) % 2)[0]) for j in range(w)]; Q = [list(np.nonzero((Wc @ Mi[j]) % 2)[0]) for j in range(w)]
        out.append((P, Q))
    return w, len(defS), out
rng = random.Random(int(sys.argv[1]))
for trial in range(int(sys.argv[2])):
    w = rng.choice([10, 10, 11]); nz = rng.choice([1, 2, 3, 5, 8])
    B = decoder(w, nz, rng)
    if B is None: print('w', w, 'nz', nz, 'UNSAT'); continue
    rk, nd, decs = gauges(B, rng, 60)
    best = None
    for P, Q in decs:
        tr = sum(np.trace(proj(q) @ proj(p)) for p, q in zip(P, Q)); cost = sum(pairing_rank(p, q) for p, q in zip(P, Q))
        if best is None or tr < best[0]: best = (tr, cost)
        if best is None or cost < best[1]: pass
    mc = min(sum(pairing_rank(p, q) for p, q in zip(P, Q)) for P, Q in decs)
    print('w %d (rank %d) nz %d deficient-in-S %d: min sum tr %.3f (cost there %d), min cost %d' % (w, rk, nz, nd, best[0], best[1], mc), flush=True)
