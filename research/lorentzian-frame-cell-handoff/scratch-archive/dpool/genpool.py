"""Pool of low-rank line supports for decoder pieces in I_{11,1}: flats = lines perpendicular to a set of mutually
orthogonal lines (sections {p,q}-perp, rank 9; triple perps, rank 8), plus D10(i), I10(W) and t-perp (rank 10).
Each support is closed (all lines in its span), nondegenerate span required.  Output: pool.txt with
'rank nlines bits...' (220 0/1 chars)."""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(11); V = g.V; G = g.G
eta = np.diag([1.0] * 11 + [-1.0])
def info(S):
    A = g.LA[sorted(S)]
    r = int(np.linalg.matrix_rank(A))
    # basis rows
    q, rr = np.linalg.qr(A.T)
    # nondegeneracy: Gram of an orthonormal (Euclidean) basis of span under eta
    u, s, vt = np.linalg.svd(A, full_matrices=False); B = vt[:r]
    Gm = B @ eta @ B.T
    nd = abs(np.linalg.det(Gm)) > 1e-9
    return r, nd
pool = {}
def add(S, tag):
    key = frozenset(S)
    if key in pool or not S: return
    r, nd = info(S)
    if nd: pool[key] = (r, tag)
R = [set(np.nonzero(G[t] == 0)[0]) - {t} for t in range(V)]
for t in range(V): add(R[t], 'tperp')
for i in range(11): add([s for s in range(V) if g.binlabel(s) >> i & 1], 'D10')
for i in range(11): add([s for s in range(V) if i not in g.supp[s]], 'I10')
for p in range(V):
    for q in R[p]:
        if q > p: add(R[p] & R[q], 'sec')
print('pool size', len(pool), {r: sum(1 for v in pool.values() if v[0] == r) for r in range(12)}, flush=True)
if len(sys.argv) > 1 and sys.argv[1] == 'triples':
    for p in range(V):
        for q in R[p]:
            if q <= p: continue
            for r_ in R[p] & R[q]:
                if r_ > q: add(R[p] & R[q] & R[r_], 'tri')
    print('pool size with triples', len(pool), flush=True)
with open('pool.txt', 'w') as f:
    for S, (r, tag) in pool.items():
        f.write('%d %d %s\n' % (r, len(S), ''.join('1' if s in S else '0' for s in range(V))))
