# I_{11,1} decoder pattern: B_TT = 1, B_TS = 0 for non-orthogonal T != S.  (a) minrank: is c = 10 SAT?
# (b) uniqueness at c = 11: is there B != B0 = (J + G) mod 2 (asymmetric labels allowed)?
import sys, numpy as np, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec')
from lw import g, V
from minrank_sat import solve_asym
import networkx as nx
G = g.G
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
assert all(B0[i, i] == 1 for i in range(V)) and all(B0[i, j] == 0 for (i, j) in pattern)
print('rank B0 over F2:', np.linalg.matrix_rank(B0.astype(float)), '(real rank; F2 rank checked below)', flush=True)
def f2rank(M):
    M = M.copy() % 2; r = 0; rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(rows):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
print('F2 rank B0 =', f2rank(B0), '| clique', len(K), flush=True)
c, mode = int(sys.argv[1]), sys.argv[2]
t = time.time()
r = solve_asym(V, pattern, B0, c, mode, K)
print('c=%d mode=%s -> %s (%.0fs, vars %d, clauses %d)' % (c, mode, r['result'], time.time() - t, r['vars'], r['clauses']), flush=True)
if r['result'] == 'SAT':
    B = r['B']
    print('F2 rank B', f2rank(B), '| row weights (off-diagonal) min/mean/max', (B.sum(1) - 1).min(), (B.sum(1) - 1).mean(), (B.sum(1) - 1).max(),
          '| B0 row weights mean', (B0.sum(1) - 1).mean(), '| entries differing from B0', int((B != B0).sum()), flush=True)
    np.save('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/dec/B_c%d_%s.npy' % (c, mode), B)
