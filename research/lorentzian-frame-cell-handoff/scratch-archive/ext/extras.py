"""All vectors compatible (odd-or-zero products) with every line of I_{n,1} = P(ij) u T(ijk) in w-perp, w = (1^n;3).
P-compatibility forces x to take <= 2 values alpha, beta with alpha - beta odd (or one value).  Enumerate
alpha, beta in [-B, B], |A| = k (by symmetry, then all positions), y from w-perp; keep even nonzero norms."""
import itertools, numpy as np, sys
n = int(sys.argv[1]); Bd = int(sys.argv[2]) if len(sys.argv) > 2 else 8
base = []
for i, j in itertools.combinations(range(n), 2):
    x = [0]*(n+1); x[i], x[j] = 1, -1; base.append(x)
for t in itertools.combinations(range(n), 3):
    x = [0]*(n+1)
    for i in t: x[i] = 1
    x[n] = 1; base.append(x)
base = np.array(base); eta = np.array([1]*n + [-1])
types = {}
for a in range(-Bd, Bd+1):
    for b in range(-Bd, Bd+1):
        for k in range(0, n+1):
            if k not in (0, n) and (a - b) % 2 == 0: continue
            if k in (0, n) and a != b: continue
            s = k*a + (n-k)*b
            if s % 3: continue
            y = s // 3
            x = [a]*k + [b]*(n-k) + [y]
            v = np.array(x); N = int((v*v*eta).sum())
            if N == 0 or N % 2: continue
            g = (base*eta) @ v
            if not (((g % 2) == 1) | (g == 0)).all(): continue
            key = (k, a, b, y)
            # canonical up to sign
            nk = (k, -a, -b, -y)
            if nk in types: continue
            types[key] = N
for key, N in sorted(types.items(), key=lambda t: abs(t[1])):
    print('k=%d alpha=%d beta=%d y=%d norm=%d' % (*key, N))
