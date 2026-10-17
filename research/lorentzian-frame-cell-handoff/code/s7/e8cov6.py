"""Complete check that the 120 E8 lines admit no cover by 3 hyperplanes z-perp.
Every hyperplane that could matter is spanned by lines (else replace it by a larger line-spanned one containing the
same lines... a hyperplane's line set spans <= rank 7; any line set of rank <= 7 lies in a line-spanned hyperplane
or in a rank-<=6 flat contained in many hyperplanes).  We enumerate normals over a generous box and keep rank-7 sets;
then, by transitivity of W(E8) on roots and on norm-4 vectors, fix the largest set to one E7 rep or one D7 rep."""
import numpy as np, itertools
from collections import Counter
from e8geo import e8_roots
L = e8_roots(); n = len(L)
cands = []
for c in itertools.product(range(-3, 4), repeat=8):
    if sum(c) % 2 == 0 and 0 < sum(x * x for x in c) <= 16: cands.append(tuple(2 * x for x in c))
for c in itertools.product((-5, -3, -1, 1, 3, 5), repeat=8):
    if sum(x * x for x in c) <= 64 and sum(c) % 4 == 0: cands.append(tuple(c))
Z = np.array(cands); print('normals', len(Z), flush=True)
P = (L @ Z.T) == 0
cnt = P.sum(axis=0)
sets = {}
for j in np.nonzero(cnt >= 7)[0]:
    key = np.packbits(P[:, j]).tobytes()
    if key not in sets: sets[key] = j
keys = list(sets)
M = np.array([P[:, sets[k]] for k in keys])
rk = np.array([np.linalg.matrix_rank(L[M[i]].astype(float)) for i in range(len(keys))])
H = M[rk == 7]
sizes = H.sum(axis=1)
print('line-spanned hyperplanes', len(H), Counter(sizes.tolist()).most_common(20), flush=True)
reps = [np.nonzero(sizes == 63)[0][0], np.nonzero(sizes == 42)[0][0]]
lineset = [0] * n
for j in range(len(H)):
    for l in np.nonzero(H[j])[0]: lineset[l] |= 1 << j
found = None
for ai in reps:
    rest = [l for l in range(n) if not H[ai][l]]
    for bi in range(len(H)):
        need = [l for l in rest if not H[bi][l]]
        if len(need) > 63: continue
        acc = -1
        for l in need:
            acc &= lineset[l]
            if not acc: break
        if acc:
            ci = (acc & -acc).bit_length() - 1
            found = (int(sizes[ai]), int(sizes[bi]), int(sizes[ci])); break
    if found: break
    print('rep of size', int(sizes[ai]), 'done: no 3-cover with it', flush=True)
print('3-cover:', found)
