import json, sys, numpy as np, itertools
d = json.load(open(sys.argv[1])); eta = np.array(d['eta']); R = np.array(d['R']); S = [tuple(s) for s in d['S']]
n1 = len(eta); v = len(S)
# class reps: any integer vector with given parity in L; Bbar via rep inner products -> recompute from base reps
# here we use: Bbar(a,b) = <rep_a, rep_b> mod 2 with rep = parity vector lifted (x parity, y parity) adjusted to L later;
# parity-only formula: <p,q> mod 2 = sum_i p_i q_i - p_y q_y mod 2 = sum p_i q_i + p_y q_y (mod 2) is NOT valid for lifts with
# +-2 shifts? shifts change <.,.> by even amounts only (2k*q) -> valid.
P = np.array(S, dtype=np.int64)
Bm = (P @ P.T) % 2       # eta = diag(1,...,-1): -1 = 1 mod 2
Pdec = (1 + Bm) % 2
G = R @ eta @ R.T
viol = [(i, j) for i in range(v) for j in range(i+1, v) if Pdec[i, j] and abs(G[i, j]) > 1e-7 * np.sqrt(abs(G[i, i] * G[j, j]))]
def rank2(M):
    M = M.copy() % 2; r = 0
    for c in range(M.shape[1]):
        p = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
c = rank2(Pdec); h = np.linalg.matrix_rank(R, tol=1e-8)
print('v', v, 'violations', len(viol), 'min |norm|', np.abs(np.diag(G)).min(), 'c', c, 'window', h,
      'x_proxy c*h/v = %.3f, c*(h-1)/v = %.3f' % (c*h/v, c*(h-1)/v))
