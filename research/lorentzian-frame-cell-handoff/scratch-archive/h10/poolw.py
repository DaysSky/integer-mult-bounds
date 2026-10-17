"""Norm-2 vectors (lines, up to sign) of w-perp in I_{n,1}: x in Z^n, y in Z, sum w_i x_i = wf*y, sum x^2 - y^2 = 2,
|y| <= YMAX.  w must be characteristic (all entries odd) so that w-perp is even.  Saves pool and root-like adjacency.
usage: poolw.py YMAX wf w1 w2 ... wn"""
import itertools, numpy as np, sys
YMAX = int(sys.argv[1]); wf = int(sys.argv[2]); w = [int(a) for a in sys.argv[3:]]; n = len(w)
assert all(a % 2 for a in w + [wf])
def parts(Q, maxv, k):
    if Q == 0: yield []; return
    if k == 0: return
    for a in range(min(maxv, int(Q**0.5)), 0, -1):
        for rest in parts(Q - a*a, a, k - 1): yield [a] + rest
vecs = set()
for y in range(0, YMAX + 1):
    Q = y*y + 2
    for p in parts(Q, 10, n):
        k = len(p)
        for comb in itertools.combinations(range(n), k):
            for perm in set(itertools.permutations(p)):
                for signs in itertools.product((1, -1), repeat=k):
                    x = [0]*n
                    for c, a, s in zip(comb, perm, signs): x[c] = a*s
                    if sum(wi*xi for wi, xi in zip(w, x)) == wf*y:
                        v = tuple(x) + (y,); nv = tuple(-t for t in v)
                        vecs.add(max(v, nv))
V = np.array(sorted(vecs), dtype=np.int64)
eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T
A = (np.abs(G) <= 1); np.fill_diagonal(A, False)
tag = 'w%s_%d_y%d' % (''.join(map(str, w)), wf, YMAX)
print(tag, 'w^2 =', sum(a*a for a in w) - wf*wf, 'lines', len(V), 'by y', {int(y): int((np.abs(V[:, -1]) == y).sum()) for y in range(YMAX+1)},
      'density %.3f' % A.mean())
np.save('pool_%s.npy' % tag, V); np.save('adj_%s.npy' % tag, A)
