"""Decoder cost of a numerical realisation of the O^eps(8,2) nonsingular configuration: for every nonzero vector of
the decoder row space (B0 = J + Omega, or a saved SAT decoder), frame rank = numerical rank of its support vectors
plus the radical dimension if that span is degenerate under the form; min-cost basis by matroid greedy.
usage: deccost.py eps p q realisation.npy [decoder.npy]"""
import sys, numpy as np, collections
eps, p, q, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]; n = 4
def omega(a, b): return sum(((a >> (2 * i)) & 1) * ((b >> (2 * i + 1)) & 1) + ((a >> (2 * i + 1)) & 1) * ((b >> (2 * i)) & 1) for i in range(n)) % 2
def Q(a):
    s = 0
    for i in range(n):
        x, y = (a >> (2 * i)) & 1, (a >> (2 * i + 1)) & 1
        s += x * y if (eps == '+' or i < n - 1) else (x + x * y + y)
    return s % 2
pts = [a for a in range(1, 256) if Q(a) == 1]; N = len(pts)
X = np.load(fn).reshape(N, p + q); sig = np.diag([1.0] * p + [-1.0] * q)
B = np.load(sys.argv[5]) if len(sys.argv) > 5 else (1 + np.array([[omega(a, b) for b in pts] for a in pts])) % 2
def rref(A):
    A = A.copy() % 2; r = 0
    for c in range(A.shape[1]):
        piv = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if piv is None: continue
        A[[r, piv]] = A[[piv, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, c]: A[i] ^= A[r]
        r += 1
    return A[:r]
S = rref(B.astype(np.int64)); k = S.shape[0]
def frame_rank(sup):
    V = X[sup]; sv = np.linalg.svd(V, compute_uv=False); r = int((sv > 1e-6 * sv[0]).sum())
    U = np.linalg.svd(V, full_matrices=False)[2][:r]          # orthonormal (Euclidean) basis of the span
    Gm = U @ sig @ U.T; ev = np.linalg.eigvalsh(Gm); rad = int((np.abs(ev) < 1e-6 * max(1, np.abs(ev).max())).sum())
    return r + rad, r, rad
vecs = []
for m in range(1, 2 ** k):
    v = (np.array([(m >> i) & 1 for i in range(k)]) @ S) % 2
    fr, r, rad = frame_rank(np.nonzero(v)[0]); vecs.append((fr, int(v.sum()), r, rad, v))
vecs.sort(key=lambda t: (t[0], t[1]))
basis = []; cost = 0; chosen = []
for fr, w, r, rad, v in vecs:
    if rref(np.array(basis + [v])).shape[0] > len(basis):
        basis.append(v); cost += fr; chosen.append((fr, w, rad))
        if len(basis) == k: break
print('decoder rank', k, 'cost', cost, 'pieces (frame rank, weight, radical)', chosen)
print('frame-rank distribution over all row-space vectors', sorted(collections.Counter(t[0] for t in vecs).items()))
