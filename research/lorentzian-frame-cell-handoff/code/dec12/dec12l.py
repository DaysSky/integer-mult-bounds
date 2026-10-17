"""Rank-c decoders of I_{11,1} whose row space S contains two independent vectors of weight <= w.
S = column space of U (B = W U^T); y_i = U a_i, a_1, a_2, a_1 + a_2 nonzero, |y_i| <= w, y_i != 0.
(If rank B = c then U has full column rank, so y_1, y_2 are independent.)  usage: dec12l.py c w"""
import sys, numpy as np, time, os
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import networkx as nx
G = g.G
c, w = int(sys.argv[1]), int(sys.argv[2])
pattern = {(i, j) for i in range(V) for j in range(V) if i != j and G[i, j] != 0}
H = nx.Graph(); H.add_edges_from((i, j) for (i, j) in pattern if i < j)
K = max(nx.find_cliques(H), key=len)
f = CNF()
U = [[f.new() for _ in range(c)] for _ in range(V)]
W = [[f.new() for _ in range(c)] for _ in range(V)]
def B(T, S): return f.xorlist([f.AND(W[T][j], U[S][j]) for j in range(c)])
for T in range(V): f.cl.append([B(T, T)])
for (T, S) in pattern: f.cl.append([-B(T, S)])
for i, T in enumerate(K):
    for j in range(c):
        f.cl.append([U[T][j]] if j == i else [-U[T][j]]); f.cl.append([W[T][j]] if j == i else [-W[T][j]])
A = [[f.new() for _ in range(c)] for _ in range(2)]
f.cl.append(A[0]); f.cl.append(A[1]); f.cl.append([f.XOR(A[0][j], A[1][j]) for j in range(c)])
for a in A:
    y = [f.xorlist([f.AND(U[s][j], a[j]) for j in range(c)]) for s in range(V)]
    f.cl.append(y)
    enc = CardEnc.atmost(lits=y, bound=w, top_id=f.n, encoding=EncType.seqcounter)
    f.n = max(f.n, enc.nv); f.cl += enc.clauses
s = Cadical153(bootstrap_with=f.cl); t = time.time()
r = s.solve()
print('c=%d two independent row-space vectors of weight <= %d: %s (%.0fs, vars %d, clauses %d)' % (c, w, 'SAT' if r else 'UNSAT', time.time() - t, f.n, len(f.cl)), flush=True)
if r:
    mdl = set(x for x in s.get_model() if x > 0)
    Uv = np.array([[1 if U[T][j] in mdl else 0 for j in range(c)] for T in range(V)]); Wv = np.array([[1 if W[T][j] in mdl else 0 for j in range(c)] for T in range(V)])
    Bm = (Wv @ Uv.T) % 2
    assert all(Bm[i, i] == 1 for i in range(V)) and all(Bm[i, j] == 0 for (i, j) in pattern)
    av = [np.array([1 if A[i][j] in mdl else 0 for j in range(c)]) for i in range(2)]
    ys = [(Uv @ a) % 2 for a in av]
    print('weights', [int(y.sum()) for y in ys], [[(g.kind[x], tuple(g.supp[x])) for x in range(V) if y[x]] for y in ys], flush=True)
    np.save(os.path.dirname(os.path.abspath(__file__)) + '/Bl_c%d_w%d.npy' % (c, w), Bm)
