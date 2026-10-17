"""Flexible greedy growth of S in F2^{2m} (symplectic form w) with an orthogonal representation in C^h of
G_S = {(a,b): w(a,b)=0, a!=b}.  Unit: v=|S|, window h, F2 decoder P = J + w|_S (rank <= 2m+1)."""
import numpy as np, itertools, sys, time, json
from orthrep import solve
m = int(sys.argv[1]); h = int(sys.argv[2]); seed = int(sys.argv[3]); maxtries = int(sys.argv[4])
init = sys.argv[5] if len(sys.argv) > 5 else None
rng = np.random.default_rng(seed)
n2 = 2*m
Jw = np.zeros((n2, n2), dtype=np.int64)
for i in range(m): Jw[2*i, 2*i+1] = Jw[2*i+1, 2*i] = 1
allc = np.array([c for c in itertools.product((0, 1), repeat=n2) if any(c)], dtype=np.int64)
W = (allc @ Jw @ allc.T) % 2          # symplectic form between all classes
N = len(allc)
def pack(R):  # complex (n,h) -> real vector for orthrep (X then Y per row)
    return np.hstack([R.real, R.imag]).reshape(-1)
def unpack(z, n):
    Z = z.reshape(n, 2*h); return Z[:, :h] + 1j*Z[:, h:]
def edges_of(Sidx):
    Sidx = np.array(Sidx); sub = W[np.ix_(Sidx, Sidx)]
    n = len(Sidx)
    return [(i, j) for i in range(n) for j in range(i+1, n) if sub[i, j] == 0]
def resolve(Sidx, R, iters=300):
    E = edges_of(Sidx)
    r, z, t = solve(len(Sidx), E, h, x0=pack(R), iters=iters)
    return r, unpack(z, len(Sidx))
# start: random clique-free small set, solve
if init:
    d = json.load(open(init)); S = d['S']; R = np.array(d['Rre']) + 1j*np.array(d['Rim'])
else:
    S = [int(i) for i in rng.choice(N, size=h, replace=False)]
    R = (rng.standard_normal((h, h)) + 1j*rng.standard_normal((h, h))) / np.sqrt(h)
    r, R = resolve(S, R)
    print('init residual', r)
bad = set()
t0 = time.time()
tries = 0
while tries < maxtries:
    inS = set(S)
    cands = [c for c in range(N) if c not in inS and c not in bad]
    if not cands: break
    # score: smallest singular value of constraint matrix (rows r_b, b in S with w(c,b)=0)
    scores = []
    Sarr = np.array(S)
    for c in cands:
        mask = W[c, Sarr] == 0
        A = R[mask]
        if len(A) < h:
            scores.append((0.0, c)); continue
        s = np.linalg.svd(A, compute_uv=False)
        scores.append((s[-1] / s[0], c))
    scores.sort()
    k = 0 if rng.random() < 0.7 else int(rng.integers(0, min(10, len(scores))))
    sc, c = scores[k]
    mask = W[c, np.array(S)] == 0
    A = R[mask]
    if len(A):
        u, s, vh = np.linalg.svd(A); x = vh[-1].conj()
    else:
        x = rng.standard_normal(h) + 1j*rng.standard_normal(h)
    x = x / np.sqrt(x @ x) if abs(x @ x) > 1e-9 else x
    S2 = S + [c]; R2 = np.vstack([R, x[None, :]])
    r, R3 = resolve(S2, R2, iters=200)
    tries += 1
    if r < 1e-9:
        S, R = S2, R3
        print('size', len(S), 'score %.2e' % sc, 'res %.1e' % r, '%.0fs' % (time.time()-t0), flush=True)
        json.dump(dict(m=m, h=h, S=[int(a) for a in S], Rre=R.real.tolist(), Rim=R.imag.tolist()), open('grow_m%d_h%d_s%d.json' % (m, h, seed), 'w'))
    else:
        bad.add(c)
print('final', len(S))
