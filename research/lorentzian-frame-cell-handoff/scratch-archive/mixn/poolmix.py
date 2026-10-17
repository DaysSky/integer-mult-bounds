"""Odd-or-zero pools in w-perp of I_{n,1}, w = (1^n; 3): x in Z^n with |x_i| <= XM, |y| <= YM, sum x = 3y,
norm N = sum x^2 - y^2 in NORMS (even, nonzero).  Compatibility: product odd or zero.  Lines up to sign.
usage: poolmix.py n XM YM norms(comma)  -> pool_n{n}_x{XM}_y{YM}_N{norms}.npy + DLS graph file."""
import itertools, numpy as np, sys
n, XM, YM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); NORMS = [int(a) for a in sys.argv[4].split(',')]
vecs = set()
vals = range(-XM, XM + 1)
# enumerate by multiset of entries for speed: choose counts of each value
def rec(i, rem, cur):
    if i == len(vals):
        if rem == 0: yield cur
        return
    for c in range(rem + 1):
        yield from rec(i + 1, rem - c, cur + [c])
for counts in rec(0, n, []):
    s = sum(c*v for c, v in zip(counts, vals)); q = sum(c*v*v for c, v in zip(counts, vals))
    for y in range(-YM, YM + 1):
        if s != 3*y or (q - y*y) not in NORMS: continue
        # all arrangements
        base = []
        for c, v in zip(counts, vals): base += [v]*c
        for perm in set(itertools.permutations(base)) if len(set(base)) > 1 else [tuple(base)]:
            v_ = tuple(perm) + (y,); nv = tuple(-t for t in v_)
            vecs.add(max(v_, nv))
V = np.array(sorted(vecs), dtype=np.int64)
eta = np.array([1]*n + [-1])
N = (V*V*eta).sum(1)
print('size', len(V), flush=True)
if len(V) > 30000: sys.exit()
G = (V*eta) @ V.T
A = (G % 2 == 1) | (G == 0); np.fill_diagonal(A, False); del G
tag = 'n%d_x%d_y%d_N%s' % (n, XM, YM, '-'.join(map(str, NORMS)))
from collections import Counter
print(tag, 'lines', len(V), 'norms', dict(Counter(N.tolist())), 'density %.3f' % A.mean(), flush=True)
np.save('pool_%s.npy' % tag, V)
with open('g_%s.txt' % tag, 'w') as f:
    f.write('%d\n' % len(V))
    for i in range(len(V)): f.write(' '.join(map(str, np.nonzero(A[i])[0])) + '\n')
