"""Mixed-sign root-like pools: w-perp of I_{n,1}, w characteristic, norms +-2, compatibility |product| <= 1.
usage: poolrl.py XM YM wf w1..wn"""
import itertools, numpy as np, sys
XM, YM = int(sys.argv[1]), int(sys.argv[2]); wf = int(sys.argv[3]); w = [int(a) for a in sys.argv[4:]]; n = len(w)
vecs = set()
for x in itertools.product(range(-XM, XM + 1), repeat=n):
    s = sum(a*b for a, b in zip(w, x))
    if s % wf: continue
    y = s // wf
    if abs(y) > YM: continue
    N = sum(a*a for a in x) - y*y
    if N not in (2, -2): continue
    v = tuple(x) + (y,); nv = tuple(-t for t in v); vecs.add(max(v, nv))
V = np.array(sorted(vecs), dtype=np.int64)
eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T
A = np.abs(G) <= 1; np.fill_diagonal(A, False)
from collections import Counter
tag = 'rl_h%d_w%s_%d_x%d_y%d' % (n, ''.join(map(str, w)), wf, XM, YM)
print(tag, 'lines', len(V), 'norms', dict(Counter((V*V*eta).sum(1).tolist())), 'density %.3f' % A.mean(), flush=True)
np.save('pool_%s.npy' % tag, V)
with open('g_%s.txt' % tag, 'w') as f:
    f.write('%d\n' % len(V))
    for i in range(len(V)): f.write(' '.join(map(str, np.nonzero(A[i])[0])) + '\n')
