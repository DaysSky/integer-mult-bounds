"""F2 minrank of the decoder pattern of the O^eps(8,2) nonsingular configuration: B = W U^T over F2^c with unit
diagonal and B = 0 on non-orthogonal (omega = 1) pairs; clique gauge on a max non-orthogonal clique.  usage: minrank.py eps c"""
import sys, time, numpy as np, networkx as nx
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from minrank_sat import CNF
from pysat.solvers import Cadical153
eps, c = sys.argv[1], int(sys.argv[2]); n = 4
def omega(a, b): return sum(((a >> (2 * i)) & 1) * ((b >> (2 * i + 1)) & 1) + ((a >> (2 * i + 1)) & 1) * ((b >> (2 * i)) & 1) for i in range(n)) % 2
def Q(a):
    s = 0
    for i in range(n):
        x, y = (a >> (2 * i)) & 1, (a >> (2 * i + 1)) & 1
        s += x * y if (eps == '+' or i < n - 1) else (x + x * y + y)
    return s % 2
pts = [a for a in range(1, 256) if Q(a) == 1]; N = len(pts)
Om = [[omega(a, b) for b in pts] for a in pts]
H = nx.Graph(); H.add_edges_from((i, j) for i in range(N) for j in range(i + 1, N) if Om[i][j])
K = max(nx.find_cliques(H), key=len)
f = CNF()
U = [[f.new() for _ in range(c)] for _ in range(N)]; W = [[f.new() for _ in range(c)] for _ in range(N)]
def B(t, s): return f.xorlist([f.AND(W[t][j], U[s][j]) for j in range(c)])
for t in range(N): f.cl.append([B(t, t)])
for t in range(N):
    for s in range(N):
        if s != t and Om[t][s]: f.cl.append([-B(t, s)])
for i, t in enumerate(K):            # gauge: U_K = [I | 0], W_K = [I | 0]  (|K| <= c)
    for j in range(c):
        f.cl.append([U[t][j]] if j == i else [-U[t][j]]); f.cl.append([W[t][j]] if j == i else [-W[t][j]])
s = Cadical153(bootstrap_with=f.cl); t0 = time.time(); r = s.solve()
print('eps %s points %d clique %d: decoder of F2 rank <= %d %s (%.0fs)' % (eps, N, len(K), c, 'EXISTS' if r else 'does not exist (UNSAT)', time.time() - t0), flush=True)
if r:
    m = set(x for x in s.get_model() if x > 0)
    Uv = np.array([[1 if U[t][j] in m else 0 for j in range(c)] for t in range(N)]); Wv = np.array([[1 if W[t][j] in m else 0 for j in range(c)] for t in range(N)])
    Bm = (Wv @ Uv.T) % 2
    assert all(Bm[i, i] == 1 for i in range(N)) and all(Bm[i, j] == 0 for i in range(N) for j in range(N) if i != j and Om[i][j])
    print('row weights (off-diagonal) min/mean/max', (Bm.sum(1) - 1).min(), (Bm.sum(1) - 1).mean(), (Bm.sum(1) - 1).max(), flush=True)
    np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/ominus/B_%s_c%d.npy' % (eps, c), Bm)
