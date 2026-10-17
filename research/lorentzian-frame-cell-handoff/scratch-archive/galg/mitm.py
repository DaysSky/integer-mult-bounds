"""Translation-invariant abelian frame model over F_3^{m x m} frames, F_2 payload, r register types.
Word = A_N M_N ... A_1 M_1 A_0, A_k in GL_r(F_2) (bit gates at common frames), M_k = diag(...,w^{eps z_b},...)
(move one component by +-B_b, a rank-1 basis offset).  Need, for all z in F_3^d:  word(z) = w^{mu.z} P  (mu: I = sum mu_b B_b).
Characters evaluated in F_4 = {0,1,w,w^2} (w^2+w+1=0).  Meet in the middle on N = N1+N2 moves.
usage: mitm.py r d N"""
import itertools, sys, numpy as np
r, d, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
# F_4 as ints 0..3: 0,1,w=2,w^2=3 ; addition = xor ; multiplication via log table
LOG = {1: 0, 2: 1, 3: 2}; EXP = [1, 2, 3]
def fmul(a, b):
    if a == 0 or b == 0: return 0
    return EXP[(LOG[a] + LOG[b]) % 3]
MUL = np.array([[fmul(a, b) for b in range(4)] for a in range(4)], dtype=np.int8)
def matmul(X, Y):  # X: (..., r, r) int8 over F_4, broadcast
    out = np.zeros(np.broadcast_shapes(X.shape[:-2], Y.shape[:-2]) + (r, r), dtype=np.int8)
    for k in range(r):
        out ^= MUL[X[..., :, k, None], Y[..., None, k, :]]
    return out
Z = np.array(list(itertools.product(range(3), repeat=d)))          # all z in F_3^d
nz = len(Z)
def wpow(e): return np.array([EXP[x % 3] for x in e], dtype=np.int8)
# GL_r(F_2)
GL = []
for bits in itertools.product((0, 1), repeat=r * r):
    A = np.array(bits, dtype=np.int8).reshape(r, r)
    # invertible over F_2?
    M = A.copy() % 2; rk = 0
    for c in range(r):
        p = next((i for i in range(rk, r) if M[i, c]), None)
        if p is None: continue
        M[[rk, p]] = M[[p, rk]]
        for i in range(r):
            if i != rk and M[i, c]: M[i] ^= M[rk]
        rk += 1
    if rk == r: GL.append(A)
moves = [(c, b, e) for c in range(r) for b in range(d) for e in (1, 2)]
def move_mat(mv):
    c, b, e = mv
    D = np.zeros((nz, r, r), dtype=np.int8)
    for i in range(r): D[:, i, i] = 1
    D[:, c, c] = wpow(e * Z[:, b])
    return D
MOVES = [move_mat(mv) for mv in moves]
GLb = [np.broadcast_to(A, (nz, r, r)) for A in GL]
def words(n):
    """all products M_n A_{n-1} ... A_1 M_1 (gates between moves), as (key, description)."""
    cur = {np.zeros(0).tobytes(): None}
    states = [(MOVES[i], [moves[i]]) for i in range(len(moves))]
    for step in range(1, n):
        new = {}
        for S, desc in states:
            for gi, A in enumerate(GLb):
                SA = matmul(A, S)
                for mi, Mv in enumerate(MOVES):
                    T = matmul(Mv, SA); k = T.tobytes()
                    if k not in new: new[k] = (T, desc + [('g', gi), moves[mi]])
        states = list(new.values())
        print('  half words with', step + 1, 'moves:', len(states), flush=True)
    return states
# targets: for each mu (basis coefficient pattern with I = sum mu_b B_b) and permutation P
mus = [mu for mu in itertools.product(range(3), repeat=d) if sum(1 for x in mu if x) >= 3]
perms = [np.eye(r, dtype=np.int8)[list(p)] for p in itertools.permutations(range(r))]
N1 = N // 2; N2 = N - N1
L = words(N1); R = L if N2 == N1 else words(N2)
# word = A_N * Rw * A_mid * Lw * A_0 ; require = w^{mu z} P  <=>  Rw * A_mid * Lw = A_N^{-1} w^{mu z} P A_0^{-1}
# absorb: P A_0^{-1} and A_N^{-1}: target set T(z) = G1 * w^{mu z} * G2 for G1,G2 in GL; enumerate Lw' = A_mid*Lw*A_0 ... simpler:
# canonical: require Rw * A_mid * Lw * A0 = A_N^{-1} w^{mu z} P.  Build table of X = A_mid * Lw * A0 keyed; check Rw^{-1} A_N^{-1} w^{mu z} P.
def inv_all(S):  # inverse of each (r x r) over F_4 via adjugate for r<=3 using brute Gauss
    out = np.zeros_like(S)
    for i in range(S.shape[0]):
        M = [list(map(int, row)) + [1 if j == k else 0 for k in range(r)] for j, row in enumerate(S[i])]
        for c in range(r):
            p = next(j for j in range(c, r) if M[j][c])
            M[c], M[p] = M[p], M[c]
            invp = [0, 1, 3, 2][M[c][c]]
            M[c] = [fmul(invp, x) for x in M[c]]
            for j in range(r):
                if j != c and M[j][c]:
                    f = M[j][c]; M[j] = [x ^ fmul(f, y) for x, y in zip(M[j], M[c])]
        out[i] = np.array([row[r:] for row in M], dtype=np.int8)
    return out
table = {}
for S, desc in L:
    for gi, A in enumerate(GLb):
        for g0, A0 in enumerate(GLb):
            X = matmul(matmul(A, S), A0); table.setdefault(X.tobytes(), (desc, gi, g0))
print('left table', len(table), flush=True)
found = 0
targets = []
for mu in mus:
    ph = wpow((Z @ np.array(mu)) % 3)
    for P in perms:
        Tz = np.zeros((nz, r, r), dtype=np.int8)
        for i in range(r):
            for j in range(r):
                if P[i, j]: Tz[:, i, j] = ph
        targets.append((mu, P, Tz))
ANinvs = [np.broadcast_to(inv_all(A[:1])[0], (nz, r, r)) for A in GLb]
for S, desc in R:
    Sinv = inv_all(S)
    for gN in range(len(GLb)):
        Y0 = matmul(Sinv, ANinvs[gN])
        for mu, P, Tz in targets:
            k = matmul(Y0, Tz).tobytes()
            if k in table:
                found += 1
                if found <= 5: print('FOUND mu', mu, 'P', P.tolist(), 'right', desc, 'left', table[k], flush=True)
print('r', r, 'd', d, 'N', N, 'solutions found:', found, '(routing cost', 3 * r, ')')
