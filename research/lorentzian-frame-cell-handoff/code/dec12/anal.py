import sys, numpy as np, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
X = np.array([[1 if i in g.supp[x] else 0 for i in range(11)] + [1 if g.kind[x] == 'T' else 0] for x in range(V)])
B0 = (1 + X @ X.T) % 2
M = np.array([[(p in g.supp[x]) if g.kind[x] == 'T' else (p not in g.supp[x]) for x in range(V)] for p in range(11)], dtype=np.int64)
B = np.load(sys.argv[1])
def rref(A):
    A = A.copy() % 2; r = 0; piv = []
    for col in range(A.shape[1]):
        p = next((i for i in range(r, A.shape[0]) if A[i, col]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(A.shape[0]):
            if i != r and A[i, col]: A[i] ^= A[r]
        piv.append(col); r += 1
    return A[:r], piv
SB, _ = rref(B); SM, _ = rref(M)
rk = lambda A: rref(A)[0].shape[0]
print('rank B', SB.shape[0], 'dim(S + C11)', rk(np.vstack([SB, SM])), 'dim(S cap C11)', SB.shape[0] + SM.shape[0] - rk(np.vstack([SB, SM])))
same = [t for t in range(V) if (B[t] == B0[t]).all()]
print('rows equal to B0 rows:', len(same), 'of', V)
w = B.sum(1) - 1; w0 = B0.sum(1) - 1
diff = [(t, g.kind[t], tuple(g.supp[t]), int(w[t]), int(w0[t])) for t in range(V) if not (B[t] == B0[t]).all()]
print('differing rows (t, kind, supp, weight, B0 weight):'); [print(' ', d) for d in diff[:40]]
print('total weight', w.sum(), 'B0', w0.sum())
D = (B + B0) % 2
print('rank D = B + B0:', rk(D), '| nonzero rows of D', int((D.sum(1) > 0).sum()), '| nonzero cols', int((D.sum(0) > 0).sum()), '| nnz', int(D.sum()))
rows = sorted(set(tuple(r) for r in D if r.any()))
print('distinct nonzero rows of D:', len(rows), [sum(r) for r in rows][:20])
cols = sorted(set(tuple(c) for c in D.T if c.any()))
print('distinct nonzero cols of D:', len(cols), [sum(c) for c in cols][:20])
for r in rows[:6]:
    s = [x for x in range(V) if r[x]]
    print('  row pattern lines:', [(g.kind[x], tuple(g.supp[x])) for x in s][:12], '...' if len(s) > 12 else '')
for c in cols[:6]:
    s = [x for x in range(V) if c[x]]
    print('  col pattern targets (%d):' % len(s), [(g.kind[x], tuple(g.supp[x])) for x in s][:12])
