"""Candidate even-norm vectors of II_{9,1} = E8 + U, stored in doubled E8 coords (X=2x) plus (p,q) for U.
Inner product <(X,p,q),(X',p',q')> = X.X'/4 + p q' + q p'.  Norm = X.X/4 + 2pq."""
import itertools, numpy as np, sys
def e8_vectors(maxnorm):
    out = []
    vals = np.array([-4, -2, 0, 2, 4])
    for t in itertools.product(range(5), repeat=8):
        X = vals[list(t)]
        n4 = int((X*X).sum())
        if n4 > 4*maxnorm: continue
        if (X.sum() // 2) % 2: continue   # sum of x even  -> sum X = 0 mod 4
        out.append(tuple(X))
    vals = np.array([-5, -3, -1, 1, 3, 5])
    for t in itertools.product(range(6), repeat=8):
        X = vals[list(t)]
        n4 = int((X*X).sum())
        if n4 > 4*maxnorm: continue
        if X.sum() % 4: continue
        out.append(tuple(X))
    return np.array(out, dtype=np.int64)
if __name__ == '__main__':
    maxn = int(sys.argv[1]); R = int(sys.argv[2]); norms = [int(a) for a in sys.argv[3].split(',')]
    E = e8_vectors(maxn)
    n8 = (E*E).sum(1)//4
    print('E8 vectors', len(E), {k: int((n8 == k).sum()) for k in sorted(set(n8.tolist()))})
    vecs = []
    for p in range(-R, R+1):
        for q in range(-R, R+1):
            for i in range(len(E)):
                N = n8[i] + 2*p*q
                if N in norms:
                    vecs.append(tuple(E[i]) + (p, q))
    V = np.array(vecs, dtype=np.int64)
    # lines: identify v ~ -v (primitive assumed: check gcd later); keep canonical sign
    key = {}
    for v in V:
        t = tuple(v); nt = tuple(-v)
        k = max(t, nt)
        key[k] = 1
    L = np.array(sorted(key), dtype=np.int64)
    np.save('cand_%d_%d_%s.npy' % (maxn, R, '_'.join(map(str, norms))), L)
    print('lines', len(L))
