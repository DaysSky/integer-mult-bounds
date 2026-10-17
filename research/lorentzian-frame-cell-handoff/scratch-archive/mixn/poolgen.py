"""Odd-or-zero pools in w-perp of I_{n,1} for a characteristic w = (w_1..w_n; wf): x in Z^n, |x_i| <= XM, |y| <= YM,
w.x = 0 (sum w_i x_i = wf y), norm in NORMS (nonzero even, may be negative).  Writes pool + DLS graph.
usage: poolgen.py XM YM norms wf w1..wn"""
import itertools, numpy as np, sys
XM, YM = int(sys.argv[1]), int(sys.argv[2]); NORMS = set(int(a) for a in sys.argv[3].split(','))
wf = int(sys.argv[4]); w = [int(a) for a in sys.argv[5:]]; n = len(w)
assert all(a % 2 for a in w + [wf])
vecs = set()
rng = range(-XM, XM + 1)
for x in itertools.product(rng, repeat=n):
    s = sum(a*b for a, b in zip(w, x))
    if s % wf: continue
    y = s // wf
    if abs(y) > YM: continue
    N = sum(a*a for a in x) - y*y
    if N not in NORMS: continue
    v = tuple(x) + (y,); nv = tuple(-t for t in v); vecs.add(max(v, nv))
V = np.array(sorted(vecs), dtype=np.int64)
eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T
A = (G % 2 == 1) | (G == 0); np.fill_diagonal(A, False)
from collections import Counter
tag = 'h%d_w%s_%d_x%d_y%d_N%s' % (n, ''.join(map(str, w)), wf, XM, YM, '_'.join(map(str, sorted(NORMS))))
print(tag, 'w^2', sum(a*a for a in w) - wf*wf, 'lines', len(V), 'norms', dict(Counter((V*V*eta).sum(1).tolist())), 'density %.3f' % A.mean(), flush=True)
np.save('pool_%s.npy' % tag, V)
with open('g_%s.txt' % tag, 'w') as f:
    f.write('%d\n' % len(V))
    for i in range(len(V)): f.write(' '.join(map(str, np.nonzero(A[i])[0])) + '\n')
