"""Root-spanned hyperplanes of E8 by type (E7 63, D7 42, E6+A1 37, A7 28, ...): sample normals from random 7-line
subsets, then close each type under W(E8) (reflections in all 120 lines, as permutations)."""
import numpy as np, random, pickle, itertools
from e8dec import A, v
Ai = np.rint(A).astype(int)
key = {tuple(r): i for i, r in enumerate(Ai)}
def lid(x):
    t = tuple(x); 
    if t in key: return key[t]
    return key[tuple(-a for a in x)]
# reflection in line r: x -> x - 2 (x.r)/(r.r) r  (doubled coords: r.r = 8)
perms = []
for r in Ai:
    perms.append([lid(x - 2 * (x @ r) // (r @ r) * r) for x in Ai])
def orbit(S):
    S = frozenset(S); seen = {S}; st = [S]
    while st:
        X = st.pop()
        for p in perms[:120]:
            Y = frozenset(p[i] for i in X)
            if Y not in seen: seen.add(Y); st.append(Y)
    return seen
random.seed(0); reps = {}
for it in range(20000):
    idx = random.sample(range(v), 7)
    M = A[idx]
    if np.linalg.matrix_rank(M) < 7: continue
    _, _, Vt = np.linalg.svd(M); n = Vt[-1]
    L = frozenset(np.where(np.abs(A @ n) < 1e-9)[0].tolist())
    if np.linalg.matrix_rank(A[sorted(L)]) != 7: continue
    if len(L) not in reps: reps[len(L)] = L
print('types found (line counts):', sorted(reps))
H = {}
for c, L in sorted(reps.items(), reverse=True):
    if c < 28: continue
    O = orbit(L); H[c] = [sorted(X) for X in O]
    print('type with', c, 'lines: orbit', len(O), flush=True)
pickle.dump(H, open('hyper8.pkl', 'wb'))
