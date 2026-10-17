"""Combinatorics of the nonsingular points of O^eps(8,2) under 'orthogonal iff omega = 0'."""
import sys, collections, numpy as np, networkx as nx
eps = sys.argv[1]; n = 4
def omega(a, b): return sum(((a >> (2 * i)) & 1) * ((b >> (2 * i + 1)) & 1) + ((a >> (2 * i + 1)) & 1) * ((b >> (2 * i)) & 1) for i in range(n)) % 2
def Q(a):
    s = 0
    for i in range(n):
        x, y = (a >> (2 * i)) & 1, (a >> (2 * i + 1)) & 1
        s += x * y if (eps == '+' or i < n - 1) else (x + x * y + y)
    return s % 2
pts = [a for a in range(1, 256) if Q(a) == 1]; N = len(pts)
Om = np.array([[omega(a, b) for b in pts] for a in pts])
B0 = (1 + Om) % 2          # unit diagonal, zero on non-orthogonal pairs
def f2rank(M):
    M = M.copy() % 2; r = 0
    for c in range(M.shape[1]):
        p = next((i for i in range(r, M.shape[0]) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
perp = [(B0[i].sum() - 1) for i in range(N)]
H = nx.Graph(); H.add_edges_from((i, j) for i in range(N) for j in range(i + 1, N) if Om[i, j])
cl = max(nx.find_cliques(H), key=len)
print('eps', eps, 'points', N, 'F2 rank of B0', f2rank(B0), '| |t-perp| values', sorted(collections.Counter(perp).items()),
      '| max non-orthogonal clique', len(cl), flush=True)
# max mutually orthogonal sets (frames)
Hp = nx.Graph(); Hp.add_edges_from((i, j) for i in range(N) for j in range(i + 1, N) if not Om[i, j])
print('max mutually orthogonal set', len(max(nx.find_cliques(Hp), key=len)), flush=True)
# row-space codeword weights
S = []
M = B0.copy() % 2; r = 0
for c in range(N):
    p = next((i for i in range(r, N) if M[i, c]), None)
    if p is None: continue
    M[[r, p]] = M[[p, r]]
    for i in range(N):
        if i != r and M[i, c]: M[i] ^= M[r]
    r += 1
S = M[:r]
w = collections.Counter(int(((np.array([(m >> i) & 1 for i in range(r)]) @ S) % 2).sum()) for m in range(1, 2 ** r))
print('row-space weight distribution', sorted(w.items()), flush=True)
