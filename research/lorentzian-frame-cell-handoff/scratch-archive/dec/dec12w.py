# Window-12 decoders with sparse rows: B = W U^T (labels in F2^12), B_TT = 1, B_TS = 0 on non-orthogonal pairs,
# every row's off-diagonal weight <= K.  SAT (CaDiCaL) with sequential-counter cardinality.
import sys, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import networkx as nx
G = g.G
c, K = int(sys.argv[1]), int(sys.argv[2])
pattern = {(i, j) for i in range(V) for j in range(V) if i != j and G[i, j] != 0}
H = nx.Graph(); H.add_edges_from((i, j) for (i, j) in pattern if i < j)
Kl = max(nx.find_cliques(H), key=len)
f = CNF()
U = [[f.new() for _ in range(c)] for _ in range(V)]
W = [[f.new() for _ in range(c)] for _ in range(V)]
def Bv(T, S): return f.xorlist([f.AND(W[T][j], U[S][j]) for j in range(c)])
for T in range(V): f.cl.append([Bv(T, T)])
for (T, S) in pattern: f.cl.append([-Bv(T, S)])
for i, T in enumerate(Kl):
    for j in range(c):
        f.cl.append([U[T][j]] if j == i else [-U[T][j]]); f.cl.append([W[T][j]] if j == i else [-W[T][j]])
rowvars = {}
for T in range(V):
    rowvars[T] = [Bv(T, S) for S in range(V) if S != T and (T, S) not in pattern]
for T in range(V):
    enc = CardEnc.atmost(lits=rowvars[T], bound=K, top_id=f.n, encoding=EncType.seqcounter)
    f.n = max(f.n, enc.nv); f.cl += enc.clauses
s = Cadical153(bootstrap_with=f.cl); t = time.time()
r = s.solve()
print('c=%d rows<=%d: %s (%.0fs, vars %d, clauses %d)' % (c, K, 'SAT' if r else 'UNSAT', time.time() - t, f.n, len(f.cl)), flush=True)
if r:
    mdl = set(x for x in s.get_model() if x > 0)
    Uv = np.array([[1 if U[T][j] in mdl else 0 for j in range(c)] for T in range(V)]); Wv = np.array([[1 if W[T][j] in mdl else 0 for j in range(c)] for T in range(V)])
    B = (Wv @ Uv.T) % 2
    w = B.sum(1) - 1
    print('row weights min/mean/max', w.min(), w.mean(), w.max(), '| total', w.sum(), '(B0 total 26070)')
    np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec/B12_K%d.npy' % K, B)
