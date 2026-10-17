"""Largest E8 line subset S admitting a Lorentzian form M (signature (7,1)) under which S keeps E8's orthogonality
pattern exactly, with odd-integer products on non-orthogonal pairs and even non-zero norms (after the common scale
of Hamming coordinates, products x^T M y / 2).  Family: M = diag(m_0..m_7) in the Hamming frame basis with integer
entries, exactly one negative.  Conflict: a pair whose M-product is non-zero-even / zero-on-non-orth / nonzero-on-orth;
bad single lines: M-norm zero or odd.  Exact max independent set by CP-SAT."""
import sys, itertools, numpy as np
sys.path.insert(0, '../e8cal'); import e8
from ortools.sat.python import cp_model
X = np.array(e8.LINES, dtype=np.int64); n = len(X)
G8 = (X @ X.T)
orth = (G8 == 0)
def best_for(mdiag, tl=60):
    M = np.diag(mdiag)
    P = X @ M @ X.T            # = 2 * product
    if np.any(P % 2): return -1, None   # products must be integers
    P //= 2
    good = [i for i in range(n) if P[i, i] != 0 and P[i, i] % 2 == 0]
    m = cp_model.CpModel(); y = {i: m.NewBoolVar('') for i in good}
    for a, b in itertools.combinations(good, 2):
        ok = (P[a, b] == 0) if orth[a, b] else (P[a, b] % 2 == 1)
        if not ok: m.AddBoolOr([y[a].Not(), y[b].Not()])
    m.Maximize(sum(y.values())); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
    st = s.Solve(m)
    sel = [i for i in good if s.Value(y[i])]
    return int(s.ObjectiveValue()), sel
results = []
for neg in (-1, -3, -5, -7, -9, -15):
    for pos in ((1,)*7, (1,1,1,1,1,1,3), (1,1,1,1,3,3,3), (3,)*7, (1,1,1,1,1,1,5)):
        md = [neg] + list(pos)
        val, sel = best_for(md)
        if val < 0: continue
        nt = sum(1 for i in sel if (X[i] @ np.diag(md) @ X[i]) < 0) if sel else 0
        results.append((val, md, nt)); print('M =', md, '-> max |S| =', val, 'timelike', nt, flush=True)
print('best', max(results))
