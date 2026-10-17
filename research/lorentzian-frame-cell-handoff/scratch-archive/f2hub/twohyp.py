# Can R(t) be covered by two hyperplanes of t-perp?  (u.n1)(u.n2) = 0 for all lines u in R(t) is a symmetric
# quadratic form q vanishing on R(t); if the lines impose full rank on Sym^2(t-perp) no such q exists.
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid'))
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, bits, V
L = g.L.astype(float)
for t in (0, 55):
    R = bits(g.HYP[t])
    X = L[R]
    # basis of span of R(t)
    U, S, Vt = np.linalg.svd(X); r = int((S > 1e-9).sum()); B = Vt[:r]
    C = X @ B.T                      # coordinates in r-dim span
    rows = [np.outer(c, c)[np.triu_indices(r)] for c in C]
    M = np.array(rows)
    print('t', t, g.kind[t], '|R(t)|', len(R), 'span rank', r, 'Sym^2 dim', r * (r + 1) // 2, 'rank of conditions', np.linalg.matrix_rank(M))
t = 0; R = bits(g.HYP[t]); X = L[R]
U, S, Vt = np.linalg.svd(X); B = Vt[:10]; C = X @ B.T
iu = np.triu_indices(10)
M = np.array([np.outer(c, c)[iu] for c in C])
_, s, vt = np.linalg.svd(M); z = vt[-1]
Q = np.zeros((10, 10)); Q[iu] = z; Q = (Q + Q.T) / 2
ev = np.linalg.eigvalsh(Q); print('null form eigenvalues', np.round(ev / np.abs(ev).max(), 4))
# express in ambient coords: q(x) = (Bx)^T Q (Bx)
Qa = B.T @ Q @ B
vals = [(L[u] @ Qa @ L[u]) for u in range(V)]
print('q on R(t) max', max(abs(vals[u]) for u in R), '| q on t', vals[t])
