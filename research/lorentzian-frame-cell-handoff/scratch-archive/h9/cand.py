"""Lines in R^{8,1} (norm 2, products in {0,+-1}) containing an orthogonal 8-frame e_1..e_8.
Every other line u has x_i = <u,e_i> in {0,+-1}, support k in {4..8} and n-part beta^2 = k/2 - 2 (n norm -1).
Products are rational only inside one class: A k in {4,6}, B k in {4,5,8}, C k in {4,7}.
Scaled integer model per class (vector (x; z), scaled product Sxx' - m zz', scaled norm 4, products in {0,+-2}):
  A: m = 2, z = 0 (k=4), +-1 (k=6);  B: m = 1, z = 0, +-1 (k=5), +-2 (k=8);  C: m = 3, z = 0, +-1 (k=7).
Frame lines: x = 2 e_i, z = 0.  Lines up to sign."""
import itertools, numpy as np
def cands(case):
    m = {'A': 2, 'B': 1, 'C': 3}[case]
    V = [tuple([2 if j == i else 0 for j in range(8)]) + (0,) for i in range(8)]
    for x in itertools.product((-1, 0, 1), repeat=8):
        k = sum(1 for a in x if a)
        if k < 4: continue
        r = k - 4
        if r % m: continue
        z2 = r // m; z = int(round(z2 ** 0.5))
        if z * z != z2: continue
        for zz in ({0} if z == 0 else {z, -z}):
            vec = x + (zz,)
            # canonical sign: first nonzero coordinate positive
            fn = next(a for a in vec if a)
            if fn < 0: continue
            V.append(vec)
    return np.array(V), m
def gram(V, m):
    X = V[:, :8]; Z = V[:, 8]
    return X @ X.T - m * np.outer(Z, Z)
if __name__ == '__main__':
    for case in 'ABC':
        V, m = cands(case); G = gram(V, m)
        assert (np.diag(G) == 4).all()
        ok = np.isin(G, (0, 2, -2)); np.fill_diagonal(ok, False)
        print(case, 'lines', len(V), 'compat density %.3f' % ok.mean(), 'k counts', np.unique((V[:, :8] != 0).sum(1), return_counts=True))
