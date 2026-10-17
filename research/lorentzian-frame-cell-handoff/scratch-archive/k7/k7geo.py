"""E8 as a Hermitian lattice over Z[(1+sqrt(-7))/2]: K-lines, orthogonality, F2 fitting minrank."""
import numpy as np, itertools, pickle
from fractions import Fraction
# Paley skew conference matrix of order 8 (q = 7)
q = 7
QR = {(x * x) % q for x in range(1, q)}
chi = lambda a: 0 if a % q == 0 else (1 if a % q in QR else -1)
C = np.zeros((8, 8), dtype=int)
for i in range(1, 8):
    C[0, i] = 1; C[i, 0] = -1
    for j in range(1, 8):
        C[i, j] = chi(j - i)
assert (C + C.T == 0).all() and (C @ C.T == 7 * np.eye(8)).all()
# E8 roots (doubled coords to stay integral): D8 roots (2e_i +- 2e_j) and (+-1)^8 even # minus
R = []
for i, j in itertools.combinations(range(8), 2):
    for a, b in itertools.product((2, -2), repeat=2):
        r = [0] * 8; r[i] = a; r[j] = b; R.append(r)
for s in itertools.product((1, -1), repeat=8):
    if s.count(-1) % 2 == 0: R.append(list(s))
R = np.array(R)   # doubled: norm 8
Rset = {tuple(r) for r in R}
def in_E8(v2):   # v2 doubled coordinates (integers); E8 = all-even with sum = 0 mod 4  or all-odd with sum = 0 mod 4
    v2 = np.asarray(v2)
    if (v2 % 2 == 0).all(): return (v2.sum() // 2) % 2 == 0
    if (v2 % 2 == 1).all() or (np.abs(v2) % 2 == 1).all(): return (v2.sum() % 4) == 0
    return False
# A = (I + C)/2 acting on doubled coords: A v2 = (v2 + C v2)/2 must be integral and in E8
ok = True
for sgn_choice in range(2):
    Cs = C if sgn_choice == 0 else -C
    good = True
    for r in R:
        w = r + Cs @ r
        if (w % 2 != 0).any(): good = False; break
        if not in_E8(w // 2): good = False; break
    print('sign', sgn_choice, 'A preserves E8 on roots:', good)
    if good: C = Cs; break
A2 = lambda v: (v + C @ v) // 2
# K-lines: span_Q(r, A r); roots in each line
lines = []; seen = set()
for r in R:
    if tuple(r) in seen: continue
    B = np.array([r, A2(r)], dtype=float)
    members = [tuple(s) for s in R if np.linalg.matrix_rank(np.vstack([B, s])) == 2]
    for s in members: seen.add(s)
    lines.append((r, members))
print('K-lines', len(lines), 'roots per line', sorted({len(m) for _, m in lines}))
V = [np.array([r, A2(r)]) for r, m in lines]
n = len(lines)
orth = [[int(i != j and np.all(V[i] @ V[j].T == 0)) for j in range(n)] for i in range(n)]
deg = [sum(row) for row in orth]
print('orthogonal lines per line', sorted(set(deg)))
pickle.dump(dict(C=C, lines=[(list(map(int, r)), m) for r, m in lines], V=[v.tolist() for v in V], orth=orth), open('k7.pkl', 'wb'))
