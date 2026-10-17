"""For a decoder B (npy): enumerate codewords of its row space S and column space T, report how many are deficient
(their lines span <= 7 dims), and the min over bases of the number of full-cost pieces (lower bound on cost)."""
import sys, numpy as np
from e8dec import A, v
B = np.load(sys.argv[1]) % 2
def basis_rows(M):
    rows = [int(''.join(map(str, r[::-1])), 2) for r in M]; piv = {}; bas = []
    for r in rows:
        x = r
        while x:
            hb = x.bit_length() - 1
            if hb in piv: x ^= piv[hb]
            else: piv[hb] = x; bas.append(r); break
    return bas
def codewords(bas):
    k = len(bas); c = 0; out = []
    for i in range(1, 1 << k):
        c ^= bas[(i & -i).bit_length() - 1]; out.append(c)
    return out
def span_dim(c):
    idx = [s for s in range(v) if (c >> s) & 1]
    return np.linalg.matrix_rank(A[idx]) if idx else 0
for name, M in (('rows S', B), ('cols T', B.T)):
    bas = basis_rows(M); cw = codewords(bas)
    dims = [span_dim(c) for c in cw]
    defi = [c for c, d in zip(cw, dims) if d <= 7]
    # F2 rank of the deficient codewords
    print(name, 'dim', len(bas), 'codewords', len(cw), 'deficient', len(defi), 'their span dim', len(basis_rows(np.array([[ (c >> s) & 1 for s in range(v)] for c in defi]))) if defi else 0,
          'weights of deficient', sorted(set(bin(c).count('1') for c in defi))[:10], 'dims', sorted(set(d for d in dims if d <= 7)))
