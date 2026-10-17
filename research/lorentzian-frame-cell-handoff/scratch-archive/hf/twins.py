import numpy as np, itertools
from e8 import P, Rr, V, G, LEG
P = np.array([[(p >> i) & 1 for i in range(9)] for p in P], dtype=np.uint8)
h = P.shape[1]
print('ports', V, 'label dim', h, 'all odd weight', all(int(p.sum()) % 2 == 1 for p in P))
def rref(M):
    M = M.copy() % 2; r = 0; piv = []
    for c in range(M.shape[1]):
        nz = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not nz: continue
        M[[r, nz[0]]] = M[[nz[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        piv.append(c); r += 1
    return M[:r], piv
def perp(M):
    """basis of {z : M z = 0} over F2"""
    R, piv = rref(M)
    free = [c for c in range(M.shape[1]) if c not in piv]
    basis = []
    for f in free:
        z = np.zeros(M.shape[1], dtype=np.uint8); z[f] = 1
        for i, c in enumerate(piv):
            if R[i, f]: z[c] = 1
        basis.append(z)
    return basis
labels = set(tuple(p) for p in P)
twins = {}
for S in range(V):
    supp = [T for T in range(V) if G[S, T] != 0]
    W = P[supp]
    B = perp(W)
    cands = []
    for coeffs in itertools.product((0, 1), repeat=len(B)):
        if not any(coeffs): continue
        z = np.zeros(h, dtype=np.uint8)
        for c, b in zip(coeffs, B):
            if c: z ^= b
        if int(z.sum()) % 2 == 1:
            cands.append(tuple(z))
    twins[S] = cands
cnt = [len(twins[S]) for S in range(V)]
print('perp dims', sorted(set(len(perp(P[[T for T in range(V) if G[S,T]!=0]])) for S in range(V))))
print('ports with >=1 odd twin label', sum(1 for c in cnt if c), 'candidate counts', sorted(set(cnt)))
ex = [S for S in range(V) if twins[S]][:3]
for S in ex:
    print(S, 'label', ''.join(map(str, P[S])), 'twins', [''.join(map(str, z)) for z in twins[S]], 'already label?', [z in labels for z in twins[S]])
