"""Flexible growth from a given configuration with a custom alternating form G0 on F2^n2 (classes as ints)."""
import numpy as np, itertools, sys, time, json
from orthrep import solve
d = json.load(open(sys.argv[1])); seed = int(sys.argv[2]); maxtries = int(sys.argv[3]); out = sys.argv[4]
G0 = np.array(d['G0']) % 2; n2 = len(G0)
rng = np.random.default_rng(seed)
allc = np.array([c for c in itertools.product((0, 1), repeat=n2) if any(c)], dtype=np.int64)
W = (allc @ G0 @ allc.T) % 2
N = len(allc)
S = [s - 1 for s in d['S']]
R = np.array(d['Rre']) + 1j*np.array(d['Rim']); h = R.shape[1]
def pack(R): return np.hstack([R.real, R.imag]).reshape(-1)
def unpack(z, n):
    Z = z.reshape(n, 2*h); return Z[:, :h] + 1j*Z[:, h:]
def edges_of(Sidx):
    Sidx = np.array(Sidx); sub = W[np.ix_(Sidx, Sidx)]; n = len(Sidx)
    iu = np.triu_indices(n, 1); m = sub[iu] == 0
    return list(zip(iu[0][m], iu[1][m]))
def resolve(Sidx, R, iters=300):
    r, z, t = solve(len(Sidx), edges_of(Sidx), h, x0=pack(R), iters=iters)
    return r, unpack(z, len(Sidx))
r0, R = resolve(S, R, 50); print('initial', len(S), 'residual %.2e' % r0, flush=True)
bad = set(); tries = 0; t0 = time.time()
while tries < maxtries:
    inS = set(S); Sarr = np.array(S)
    cands = [c for c in range(N) if c not in inS and c not in bad]
    if not cands: break
    scores = []
    for c in cands:
        A = R[W[c, Sarr] == 0]
        if len(A) < h: scores.append((0.0, c)); continue
        s = np.linalg.svd(A, compute_uv=False); scores.append((s[-1]/s[0], c))
    scores.sort()
    k = 0 if rng.random() < 0.6 else int(rng.integers(0, min(15, len(scores))))
    sc, c = scores[k]
    A = R[W[c, Sarr] == 0]
    if len(A): x = np.linalg.svd(A)[2][-1].conj()
    else: x = rng.standard_normal(h) + 1j*rng.standard_normal(h)
    if abs(x @ x) > 1e-9: x = x/np.sqrt(x @ x)
    r, R3 = resolve(S + [c], np.vstack([R, x[None, :]]), iters=150)
    tries += 1
    if r < 1e-9:
        S = S + [c]; R = R3
        print('size', len(S), 'score %.2e' % sc, '%.0fs' % (time.time()-t0), flush=True)
        json.dump(dict(G0=G0.tolist(), S=[int(a)+1 for a in S], Rre=R.real.tolist(), Rim=R.imag.tolist()), open(out, 'w'))
    else:
        bad.add(c)
print('final', len(S), 'tries', tries)
