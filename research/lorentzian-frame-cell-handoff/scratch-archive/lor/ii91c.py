"""Search large sets of norm-2 vectors in II_{9,1} = E8 + U with pairwise products in {0} U odd (distinct lines)."""
import numpy as np, itertools, random, sys, pickle, time
# E8 vectors in doubled coords (integers): norm (doubled) 8 -> actual norm 2; norm 16 -> 4
def e8_vectors(maxnorm_doubled):
    out = []
    rng = range(-4, 5)
    # enumerate doubled coords: all even entries with sum%4==0, or all odd with sum%4==0
    for parity in (0, 1):
        vals = [x for x in rng if x % 2 == parity]
        for v in itertools.product(vals, repeat=8):
            s = sum(x * x for x in v)
            if 0 < s <= maxnorm_doubled * 4 // 4 and sum(v) % 4 == 0:
                out.append(v)
    return out
t0 = time.time()
E = e8_vectors(24)   # doubled norm <= 24 -> actual norm <= 6
E = np.array(E)
nrm = (E * E).sum(1) // 4   # actual norm
print('E8 vectors norm<=4:', {k: int((nrm == k).sum()) for k in sorted(set(nrm.tolist()))}, '%.0fs' % (time.time() - t0), flush=True)
R2 = E[nrm == 2]; R4 = E[nrm == 4]
# II_{9,1} vectors: (e, a, b), norm = |e|^2 + 2ab = 2
pool = []
A = int(sys.argv[1]) if len(sys.argv) > 1 else 2
for r in R2:
    for a in range(-A, A + 1):
        pool.append((tuple(r), a, 0))
        if a != 0: pool.append((tuple(r), 0, a))
for e in R4:
    for a in (1, -1):
        pool.append((tuple(e), a, -a))
pool.append((tuple([0] * 8), 1, 1)); pool.append((tuple([0] * 8), -1, -1))
if len(sys.argv) > 3 and sys.argv[3] == 'n6':
    R6 = E[nrm == 6]
    for e in R6:
        for a, b in ((1, -2), (2, -1), (-1, 2), (-2, 1)):
            pool.append((tuple(e), a, b))
# canonical line representative (first nonzero coordinate positive)
def canon(v):
    e, a, b = v
    flat = list(e) + [a, b]
    for x in flat:
        if x != 0:
            if x < 0: return (tuple(-y for y in e), -a, -b)
            return v
lines = sorted(set(canon(v) for v in pool))
print('pool lines', len(lines), flush=True)
L = np.array([list(e) + [a, b] for e, a, b in lines], dtype=np.int64)
Ee = L[:, :8]; ab = L[:, 8:]
# product: e.e'/4 (doubled coords) + a b' + b a'
P = (Ee @ Ee.T) // 4 + np.outer(ab[:, 0], ab[:, 1]) + np.outer(ab[:, 1], ab[:, 0])
assert (np.diag(P) == 2).all()
compat = (P == 0) | (P % 2 != 0)
np.fill_diagonal(compat, False)
deg = compat.sum(1)
print('compat degree min/mean/max', deg.min(), deg.mean(), deg.max(), flush=True)
np.save('compat_%s.npy' % (sys.argv[3] if len(sys.argv) > 3 else 'base'), compat)
pickle.dump(dict(lines=lines), open('lines_%s.pkl' % (sys.argv[3] if len(sys.argv) > 3 else 'base'), 'wb'))
print('saved', flush=True)
