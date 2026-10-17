"""Exact min-cost B0 decoder for a root-like line system (vectors V with metric eta = diag(1..1,-1)).
B0 = J + G (mod 2) restricted to lines; its row space C (F2) holds every total's support.  A decoder = any F2 basis
of C (c = rank); cost = sum of real ranks of the supports' spans.  Matroid greedy on (real rank) is exact.
Also reports |R(t)| stats and h = real rank of V.  usage: deccost.py FILE.npy"""
import sys, itertools, numpy as np
V = np.load(sys.argv[1]).astype(np.int64)
n1 = V.shape[1]; eta = np.array([1]*(n1-1) + [-1])
G = (V*eta) @ V.T
v = len(V)
assert (np.diag(G) == 2).all()
off = G[~np.eye(v, dtype=bool)]
print('v', v, 'products', sorted(set(off.tolist())))
h = np.linalg.matrix_rank(V.astype(float))
B0 = ((1 + G) % 2).astype(np.uint8); np.fill_diagonal(B0, 1)   # 1 on diagonal and on orthogonal pairs
R = B0.sum(1) - 1
print('h', h, '|R(t)| min/avg/max', R.min(), round(R.mean(), 2), R.max(), 'sum', R.sum())
# F2 row reduction of B0 -> basis of row space
def f2basis(M):
    M = M.copy() % 2; rows = []; piv = []
    A = M.astype(np.uint8)
    r = 0; m, nn = A.shape
    A = A.copy()
    for col in range(nn):
        p = None
        for i in range(r, m):
            if A[i, col]: p = i; break
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(m):
            if i != r and A[i, col]: A[i] ^= A[r]
        r += 1
        if r == m: break
    return A[:r]
Bb = f2basis(B0)
c = len(Bb)
print('F2 rank c =', c)
if c > 22: print('rank too large to enumerate'); sys.exit()
words = []
for mask in range(1, 2**c):
    w = np.zeros(v, dtype=np.uint8)
    for i in range(c):
        if mask >> i & 1: w ^= Bb[i]
    sup = np.nonzero(w)[0]
    rr = np.linalg.matrix_rank(V[sup].astype(float))
    words.append((rr, len(sup), mask))
words.sort()
# greedy F2-independent selection over masks (coordinates in the basis)
basis = []; chosen = []
def reduce(x):
    for b in basis:
        if x ^ b < x: x ^= b
    return x
for rr, wt, mask in words:
    x = mask
    for b in sorted(basis, reverse=True):
        x = min(x, x ^ b)
    if x:
        basis.append(x); basis.sort(reverse=True); chosen.append((rr, wt))
        if len(chosen) == c: break
cst = sum(r for r, _ in chosen)
from collections import Counter
print('min-cost basis: cst', cst, 'x = %.4f' % (cst / v), 'pieces (rank, weight):', Counter(chosen))
print('weight distribution of C:', sorted(Counter(wt for _, wt, _ in words).items())[:12])
