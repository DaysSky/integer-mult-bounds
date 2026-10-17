import sys, numpy as np
from cand import cands, gram
case = sys.argv[1]; V, m = cands(case); G = gram(V, m)
ok = np.isin(G, (0, 2, -2)); np.fill_diagonal(ok, False)
# drop frame (compatible with all) -> graph on non-frame lines
idx = [i for i in range(len(V)) if (V[i, :8] != 0).sum() > 1]
A = ok[np.ix_(idx, idx)]
with open('g%s.txt' % case, 'w') as f:
    f.write('%d\n' % len(idx))
    for i in range(len(idx)):
        f.write(' '.join(str(j) for j in np.nonzero(A[i])[0]) + '\n')
np.save('V%s.npy' % case, V[idx])
print(case, len(idx))
