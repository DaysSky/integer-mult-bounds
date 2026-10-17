"""All flats (line sets closed under span) of E8 by rank, via BFS; saves rank-7 (hyperplane) flats as bitmasks."""
import numpy as np, pickle, time
from e8dec import A, v
Ai = np.rint(A).astype(int)
def closure(idx):
    M = A[list(idx)]; r = np.linalg.matrix_rank(M)
    # lines in span: rank does not increase
    Q, _ = np.linalg.qr(M.T)   # orthonormal basis of span (columns), Q may have extra columns if dependent
    U, S, Vt = np.linalg.svd(M, full_matrices=False); basis = Vt[:r]
    proj = A @ basis.T @ basis
    inside = np.where(np.abs(proj - A).max(1) < 1e-9)[0]
    return frozenset(inside.tolist()), r
t0 = time.time()
level = {closure([i])[0] for i in range(v)}
counts = {1: len(level)}
allflats = {1: level}
for rnk in range(2, 8):
    nxt = set()
    for F in level:
        Fl = sorted(F); seen = set()
        for s in range(v):
            if s in F or s in seen: continue
            C, r = closure(Fl + [s])
            assert r == rnk
            seen |= C
            nxt.add(C)
    level = nxt; counts[rnk] = len(level); allflats[rnk] = level
    print('rank', rnk, 'flats', len(level), '%.0fs' % (time.time() - t0), flush=True)
pickle.dump({r: [sorted(F) for F in fl] for r, fl in allflats.items()}, open('e8flats.pkl', 'wb'))
from collections import Counter
print('hyperplane line counts', sorted(Counter(len(F) for F in allflats[7]).items()))
