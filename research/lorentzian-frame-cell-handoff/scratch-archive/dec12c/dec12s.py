"""Rank-c decoders of I_{11,1} with many sparsified rows.  B = W U^T, B_TT = 1, B_TS = 0 on non-orthogonal pairs,
clique gauge.  B0 has every perp entry 1, so the saving of row t is the number of perp s with B_TS = 0.
Ask: at least m targets each saving >= d.   usage: dec12s.py c m d"""
import sys, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import networkx as nx
G = g.G
c, m, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
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
flags = []
for T in range(V):
    zeros = [-B(T, S) for S in range(V) if S != T and (T, S) not in pattern]
    ft = f.new(); flags.append(ft)
    enc = CardEnc.atleast(lits=zeros, bound=d, top_id=f.n, encoding=EncType.seqcounter)
    f.n = max(f.n, enc.nv)
    for cl in enc.clauses: f.cl.append([-ft] + cl)
enc = CardEnc.atleast(lits=flags, bound=m, top_id=f.n, encoding=EncType.seqcounter)
f.n = max(f.n, enc.nv); f.cl += enc.clauses
s = Cadical153(bootstrap_with=f.cl); t = time.time()
r = s.solve()
print('c=%d, >= %d rows saving >= %d: %s (%.0fs, vars %d, clauses %d)' % (c, m, d, 'SAT' if r else 'UNSAT', time.time() - t, f.n, len(f.cl)), flush=True)
if r:
    mdl = set(x for x in s.get_model() if x > 0)
    Uv = np.array([[1 if U[T][j] in mdl else 0 for j in range(c)] for T in range(V)]); Wv = np.array([[1 if W[T][j] in mdl else 0 for j in range(c)] for T in range(V)])
    Bm = (Wv @ Uv.T) % 2
    assert all(Bm[i, i] == 1 for i in range(V)) and all(Bm[i, j] == 0 for (i, j) in pattern)
    perp = np.array([[1 if (i != j and G[i, j] == 0) else 0 for j in range(V)] for i in range(V)])
    sav = (perp * (1 - Bm)).sum(1)
    print('savings: total', sav.sum(), 'rows saving >= d', (sav >= d).sum(), 'max', sav.max(), 'sorted top', sorted(sav)[-15:], flush=True)
    np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec12c/Bs_c%d_m%d_d%d.npy' % (c, m, d), Bm)
