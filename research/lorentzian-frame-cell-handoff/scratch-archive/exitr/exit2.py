"""Rank-7 helper ends on P111-tuned (bit), the complex-side criterion (#1030/#1090):
  (1) dirt column: column h of the z-part of the raw word W0 = (A, scatter, B) is e_h (h's initial value reaches no
      other z register);
  (2) inverse row: R_h = support of row h of U^{-1} (U = z-to-z part of W0); the end-of-B frames of R_h (incl. h)
      span <= 7 dims.
Then an early cleanup gate h ^= sum_{R_h - h} r at a hyperplane frame restores h, and nobody else needs h_init."""
import gzip, json
import numpy as np
from collections import Counter
w = json.load(gzip.open('/home/user/integer-mult-bounds/research/e8-bit-p111-tuned/tune/bitE8mut-p111-tuned.json.gz', 'rt'))
v = w['v']; R = w['R']; n = 2 * v + R
L = np.array(w['lines'], dtype=float)
FR = w['frames']
def rk(lines): return int(np.linalg.matrix_rank(L[sorted(lines)])) if lines else 0
is_y = lambda r: v <= r < 2 * v
z = [r for r in range(n) if not is_y(r)]
zi = {r: i for i, r in enumerate(z)}
# raw word values (bitmasks over all n columns)
val = [1 << r for r in range(n)]
cur = list(w['start'])
for sec in ('A',):
    for f, d, srcs in w[sec]:
        acc = 0
        for s in srcs: acc ^= val[s]
        val[d] ^= acc
        for r in [d] + srcs: cur[r] = f
copies = [val[q] for q in w['ret']]
for t, row in enumerate(w['scatter']):
    for k in row: val[v + t] ^= copies[k]
for f, d, srcs in w['B']:
    acc = 0
    for s in srcs: acc ^= val[s]
    val[d] ^= acc
    for r in [d] + srcs: cur[r] = f
endB = cur[:]
# U over GF(2): rows = z registers, cols = z registers
N = len(z)
U = np.zeros((N, N), dtype=np.uint8)
for i, r in enumerate(z):
    for j, c in enumerate(z):
        U[i, j] = (val[r] >> c) & 1
# check no target columns in z rows
ymask = ((1 << v) - 1) << v
assert all(val[r] & ymask == 0 for r in z)
# GF(2) inverse
A = np.concatenate([U.copy(), np.eye(N, dtype=np.uint8)], axis=1)
row = 0
for col in range(N):
    piv = None
    for i in range(row, N):
        if A[i, col]: piv = i; break
    assert piv is not None
    A[[row, piv]] = A[[piv, row]]
    for i in range(N):
        if i != row and A[i, col]: A[i] ^= A[row]
    row += 1
Uinv = A[:, N:]
stat = Counter(); good = []
for h in range(2 * v, n):
    i = zi[h]
    colok = (U[:, i].sum() == 1)          # only diagonal
    supp = [z[j] for j in np.nonzero(Uinv[i])[0]]
    lines = set()
    for r in supp: lines |= set(FR[endB[r]])
    d = rk(lines)
    stat[(bool(colok), d, len(supp))] += 1
    if colok and d <= 7: good.append((h, supp, d))
print('helpers by (dirt column clean, span dim, |inverse row|):')
for k in sorted(stat): print('  ', k, stat[k])
print('rank-7-end candidates:', len(good))
for g in good[:20]: print('   helper', g[0] - 2 * v, 'inverse row', [('h%d' % (r - 2 * v)) if r >= 2 * v else ('x%d' % r) for r in g[1]], 'span', g[2])
