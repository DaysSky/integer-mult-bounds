"""Space of symmetric bilinear forms M on R^8 with e_i^T M e_j = 0 for every orthogonal pair (i,j) of a given line
set (E8 coordinates).  Any realisation of the same projective configuration with the same orthogonality pattern has
Gram lambda_i lambda_j e_i^T M e_j for some M in this space.  dim 1 (M = c G_E8) => only the Euclidean form."""
import sys, itertools, numpy as np
from fractions import Fraction
L = np.load(sys.argv[1]) if len(sys.argv) > 1 else None
def run(L, name):
    n = len(L); G = L @ L.T / 2
    orth = np.isclose(G, 0)
    idx = [(a, b) for a in range(8) for b in range(a, 8)]
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            if orth[i, j]:
                r = [L[i, a]*L[j, b] + (L[i, b]*L[j, a] if a != b else 0) for a, b in idx]
                rows.append(r)
    A = np.array(rows, float)
    rk = np.linalg.matrix_rank(A)
    dim = len(idx) - rk
    print('%s: %d lines, %d orthogonal pairs, form space dimension %d' % (name, n, len(rows), dim), flush=True)
    if dim > 1:
        _, s, vt = np.linalg.svd(A); basis = vt[rk:]
        # check signatures available: sample random combos
        sigs = set()
        rng = np.random.default_rng(0)
        for _ in range(2000):
            c = rng.standard_normal(dim); m = c @ basis
            M = np.zeros((8, 8))
            for (a, b), val in zip(idx, m):
                M[a, b] = M[b, a] = val
            ev = np.linalg.eigvalsh(M)
            pos = int((ev > 1e-9).sum()); neg = int((ev < -1e-9).sum())
            # require nonzero on non-orthogonal pairs and diagonal
            Gm = L @ M @ L.T
            ok = np.all(np.abs(Gm[~orth]) > 1e-6)
            if ok: sigs.add((pos, neg))
        print('   signatures with all non-orthogonal products nonzero:', sorted(sigs))
    return dim
import sys
sys.path.insert(0, '../e8cal'); import e8
E8 = np.array(e8.LINES, float)
run(E8, 'E8 (control)')
run(np.load('p111_lines.npy'), 'P111 lines')
