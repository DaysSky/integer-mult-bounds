"""Rigid greedy extension of an orthogonal representation in R^{9,1} (Lorentzian II_{9,1}) by abstract classes.
Decoder P = J + Bbar (F2), labels: any vectors (real or complex) with r_a . r_b = 0 whenever Bbar(a,b)=0 (a != b)."""
import numpy as np, itertools, sys
from adj import ip
L = np.load('cand_6_2_2_-2.npy'); C = np.load(sys.argv[1]); V = L[C]
# Z-basis of II_{9,1} = E8 + U in doubled-E8 coords: E8 simple roots (doubled) + U basis
e8b = np.array([[2,-2,0,0,0,0,0,0],[0,2,-2,0,0,0,0,0],[0,0,2,-2,0,0,0,0],[0,0,0,2,-2,0,0,0],[0,0,0,0,2,-2,0,0],[0,0,0,0,0,2,-2,0],[0,0,0,0,0,2,2,0],[-1,-1,-1,-1,-1,-1,-1,-1]])
Bz = np.zeros((10, 10), dtype=np.int64); Bz[:8, :8] = e8b; Bz[8, 8] = 1; Bz[9, 9] = 1
# express vectors in this basis: solve real system
Mreal = np.hstack([Bz[:, :8].astype(float)/2, Bz[:, 8:].astype(float)])   # rows = basis vectors in true coords
def coords(Vv):
    T = np.hstack([Vv[:, :8].astype(float)/2, Vv[:, 8:].astype(float)])
    X = np.linalg.solve(Mreal.T, T.T).T
    Xi = np.rint(X).astype(np.int64); assert np.abs(X - Xi).max() < 1e-9
    return Xi
G0 = ip(Bz, Bz) % 2          # Gram mod 2 in basis
def Bbar(x, y): return int(x @ G0 @ y) % 2
cls0 = coords(V) % 2
# true-coordinate real vectors with Lorentz metric: use (e8 part/2, p, q) and metric diag(I8, U)
eta = np.zeros((10, 10)); eta[:8, :8] = np.eye(8); eta[8, 9] = eta[9, 8] = 1
R = [np.hstack([v[:8]/2.0, v[8:]]).astype(complex) for v in V]
S = [tuple(c) for c in cls0]
assert len(set(S)) == len(S)
allc = [c for c in itertools.product((0, 1), repeat=10) if any(c)]
def try_add(a):
    a = np.array(a)
    cons = [R[i] for i, b in enumerate(S) if Bbar(a, np.array(b)) == 0 or tuple(a) == b]
    if not cons: return None
    A = np.array(cons) @ eta          # constraint rows: (r_b^T eta) x = 0
    u, s, vh = np.linalg.svd(A)
    tol = 1e-8 * max(1, s[0])
    null = vh[(s > tol).sum():].conj()   # basis of nullspace (rows)
    if len(null) == 0: return None
    # find nonisotropic vector in null space: try basis vectors and random combos
    for k in range(20):
        x = null[k] if k < len(null) else np.random.default_rng(k).standard_normal(len(null)) @ null
        if abs(x @ eta @ x) > 1e-6 * (abs(x) ** 2).sum():
            return x
    return None
added = 0
changed = True
while changed:
    changed = False
    cand = [c for c in allc if c not in set(S)]
    best = None
    for c in cand:
        x = try_add(c)
        if x is not None:
            R.append(x); S.append(c); added += 1; changed = True
            print('added', c, 'size', len(S), flush=True)
print('final size', len(S), 'added', added)
# export: classes as ints (bit order), vectors converted to standard complex bilinear form
import json
w, Q = np.linalg.eigh(eta)
T = (np.sqrt(w.astype(complex))[:, None] * Q.T)
Rstd = np.array([T @ r for r in R])
Sint = [int(''.join(map(str, c)), 2) for c in S]
json.dump(dict(G0=G0.tolist(), S=Sint, Rre=Rstd.real.tolist(), Rim=Rstd.imag.tolist()), open('ext176.json', 'w'))
print('exported', len(S))
