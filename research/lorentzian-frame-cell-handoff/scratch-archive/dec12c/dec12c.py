"""Rank-c decoders of I_{11,1} whose row space does NOT contain C_11.
B = W U^T (labels in F2^c), B_TT = 1, B_TS = 0 on non-orthogonal pairs, clique gauge U_K = W_K = [I|0];
witness z in F2^220 with U^T z = 0 (so z is orthogonal to the row space of B) and M z != 0 (M = D10 incidence,
row space C_11).  UNSAT  <=>  every rank-<=c decoder's row space contains C_11 (ker U^T is gauge invariant).
usage: dec12c.py c"""
import sys, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import CNF
from pysat.solvers import Cadical153
import networkx as nx
G = g.G
c = int(sys.argv[1])
pattern = {(i, j) for i in range(V) for j in range(V) if i != j and G[i, j] != 0}
H = nx.Graph(); H.add_edges_from((i, j) for (i, j) in pattern if i < j)
K = max(nx.find_cliques(H), key=len)
def vec(x):
    m = np.zeros(12, dtype=np.int64)
    for i in g.supp[x]: m[i] = 1
    if g.kind[x] == 'T': m[11] = 1
    return m
X = np.array([vec(x) for x in range(V)])
B0 = (1 + X @ X.T) % 2
# D10 incidence: P(ij) in D10(p) for p not in ij; T(abc) in D10(p) for p in abc
M = np.zeros((11, V), dtype=np.int64)
for x in range(V):
    s = set(g.supp[x])
    for p in range(11):
        M[p, x] = (p in s) if g.kind[x] == 'T' else (p not in s)
def f2rank(A):
    A = A.copy() % 2; r = 0
    for col in range(A.shape[1]):
        piv = next((i for i in range(r, A.shape[0]) if A[i, col]), None)
        if piv is None: continue
        A[[r, piv]] = A[[piv, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, col]: A[i] ^= A[r]
        r += 1
    return r
print('kinds', {k: list(g.kind).count(k) for k in set(g.kind)}, 'rank M', f2rank(M), 'rank B0', f2rank(B0),
      'rank [M;B0]', f2rank(np.vstack([M, B0])), 'clique', len(K), flush=True)
f = CNF()
U = [[f.new() for _ in range(c)] for _ in range(V)]
W = [[f.new() for _ in range(c)] for _ in range(V)]
def B(T, S): return f.xorlist([f.AND(W[T][j], U[S][j]) for j in range(c)])
for T in range(V): f.cl.append([B(T, T)])
for (T, S) in pattern: f.cl.append([-B(T, S)])
for i, T in enumerate(K):
    for j in range(c):
        f.cl.append([U[T][j]] if j == i else [-U[T][j]]); f.cl.append([W[T][j]] if j == i else [-W[T][j]])
z = [f.new() for _ in range(V)]
for j in range(c): f.parity([f.AND(z[s], U[s][j]) for s in range(V)], 0)
f.cl.append([f.xorlist([z[s] for s in range(V) if M[p, s]]) for p in range(11)])
s = Cadical153(bootstrap_with=f.cl); t = time.time()
r = s.solve()
print('c=%d row space misses C_11: %s (%.0fs, vars %d, clauses %d)' % (c, 'SAT' if r else 'UNSAT', time.time() - t, f.n, len(f.cl)), flush=True)
if r:
    mdl = set(x for x in s.get_model() if x > 0)
    Uv = np.array([[1 if U[T][j] in mdl else 0 for j in range(c)] for T in range(V)]); Wv = np.array([[1 if W[T][j] in mdl else 0 for j in range(c)] for T in range(V)])
    Bm = (Wv @ Uv.T) % 2; zv = np.array([1 if z[x] in mdl else 0 for x in range(V)])
    assert all(Bm[i, i] == 1 for i in range(V)) and all(Bm[i, j] == 0 for (i, j) in pattern)
    print('rank B', f2rank(Bm), 'B z = 0:', not ((Bm @ zv) % 2).any(), 'M z', (M @ zv) % 2, '|z|', zv.sum(),
          'rank [B;M]', f2rank(np.vstack([Bm, M])), 'row weights', (Bm.sum(1) - 1).min(), (Bm.sum(1) - 1).mean(), (Bm.sum(1) - 1).max(), flush=True)
    np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec12c/B_c%d.npy' % c, Bm)
