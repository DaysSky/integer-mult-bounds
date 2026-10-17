"""Support ranks of all codewords of the B0 row code C_n (span of the n binlabel-coordinate totals) for I_{n,1}.
If n+ independent codewords have support rank < n-1, B0 has a cheaper n-piece decomposition."""
import sys, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
n = int(sys.argv[1]); g = Geom(n)
lab = [g.binlabel(s) for s in range(g.V)]
L = g.LA
cnt = collections.Counter(); low = []
for m in range(1, 1 << n):
    S = [s for s in range(g.V) if bin(lab[s] & m).count('1') & 1]
    r = int(np.linalg.matrix_rank(L[S])) if S else 0
    cnt[r] += 1
    if r < g.h - 1: low.append((r, len(S), m))
print('n', n, 'h', g.h, 'support-rank histogram', dict(sorted(cnt.items())))
low.sort(); print('low-rank codewords', len(low), low[:20])
# rank of the span of low-rank codewords (as F2 vectors over coordinates = masks)
basis = []
for r, w, m in low:
    x = m
    for b in basis: x = min(x, x ^ b)
    if x: basis.append(x)
print('F2 dim spanned by codewords of support rank < h-1:', len(basis))
