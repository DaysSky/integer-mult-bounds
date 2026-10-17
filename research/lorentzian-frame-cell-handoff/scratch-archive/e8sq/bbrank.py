"""F2 rank of W(E8)xW(E8)-invariant decoders on the 28800 root-pair lines (r,s) of E8+E8 (norm-4 vectors).
Lifted to root pairs: M = I(x)I + A(x)A + c0 E0(x)E0 + c1 (E1(x)AE1 + AE1(x)E1) + c2 (I(x)A + A(x)I), A = antipodal,
E_a = [r.r' = a].  rank(M) = dim span{ sum_k Y_k Z X_k^T : Z } computed from random Z until the rank stabilises.
Pattern check: M must vanish on non-orthogonal pairs (r.r'+s.s' != 0) -- true by construction."""
import itertools, sys, numpy as np
R = []
for i, j in itertools.combinations(range(8), 2):
    for a, b in itertools.product((1, -1), repeat=2):
        v = [0] * 8; v[i] = a; v[j] = b; R.append(v)
for s in itertools.product((0.5, -0.5), repeat=8):
    if sum(1 for x in s if x < 0) % 2 == 0: R.append(list(s))
R = np.array(R); G = np.rint(R @ R.T).astype(int); n = 240
E = {a: (G == a).astype(np.float32) for a in (-2, -1, 0, 1, 2)}
I = E[2]; A = E[-2]; E0 = E[0]; E1 = E[1]; AE1 = (A @ E1) % 2
assert np.array_equal(AE1, E[-1])
def terms(c0, c1, c2):
    T = [(I, I), (A, A)]
    if c0: T.append((E0, E0))
    if c1: T += [(E1, AE1), (AE1, E1)]
    if c2: T += [(I, A), (A, I)]
    return T
def f2rank_rows(rows_bits):
    M = np.packbits(rows_bits.astype(np.uint8), axis=1)
    r = 0; nrow, ncol = M.shape[0], rows_bits.shape[1]
    M = M.copy()
    for c in range(ncol):
        byte, bit = divmod(c, 8); mask = np.uint8(1 << (7 - bit))
        col = (M[r:, byte] & mask) != 0
        idx = np.nonzero(col)[0]
        if len(idx) == 0: continue
        p = r + idx[0]
        if p != r: M[[r, p]] = M[[p, r]]
        others = np.nonzero((M[:, byte] & mask) != 0)[0]; others = others[others != r]
        M[others] ^= M[r]; r += 1
        if r == nrow: break
    return r
rng = np.random.default_rng(0)
def rank_of(c, maxs=4000, step=400):
    T = terms(*c); imgs = []; last = -1
    while len(imgs) < maxs:
        for _ in range(step):
            Z = rng.integers(0, 2, (n, n)).astype(np.float32)
            Y = np.zeros((n, n), np.float32)
            for X, W in T: Y += W @ Z @ X.T
            imgs.append((np.rint(Y).astype(np.int64) % 2).ravel())
        rk = f2rank_rows(np.array(imgs))
        if rk < len(imgs) - 50: return rk
        last = rk
    return '>= %d' % last
for c in itertools.product((0, 1), repeat=3):
    print('c0,c1,c2 =', c, ' rank on root pairs (= rank on the 28800 lines):', rank_of(c), flush=True)
