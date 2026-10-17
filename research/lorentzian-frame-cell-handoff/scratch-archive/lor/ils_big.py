"""Memory-light ILS for large 0-or-odd vector sets in II_{9,1}; compat rows computed on the fly."""
import numpy as np, itertools, random, sys, time, pickle
maxn = int(sys.argv[1]); iters = int(sys.argv[2]); seed = int(sys.argv[3])
def e8(maxnorm):
    out = []
    for parity in (0, 1):
        vals = [x for x in range(-6, 7) if x % 2 == parity]
        for v in itertools.product(vals, repeat=8):
            s = sum(x * x for x in v)
            if 0 < s <= 4 * maxnorm and sum(v) % 4 == 0: out.append(v)
    return np.array(out)
t0 = time.time()
E = e8(maxn); nrm = (E * E).sum(1) // 4
print('E8 by norm', {k: int((nrm == k).sum()) for k in sorted(set(nrm.tolist()))}, '%.0fs' % (time.time() - t0), flush=True)
vecs = []
for e, nn in zip(E, nrm):
    t = 2 - nn   # need 2ab = t
    if t == 2:
        for a in range(-3, 4):
            vecs.append(list(e) + [a, 0])
            if a: vecs.append(list(e) + [0, a])
    elif t % 2 == 0:
        ab = t // 2
        for a in range(1, abs(ab) + 1):
            if ab % a == 0:
                b = ab // a
                vecs.append(list(e) + [a, b]); vecs.append(list(e) + [-a, -b]); 
                if a != abs(b): vecs.append(list(e) + [b, a]) if False else None
vecs.append([0] * 8 + [1, 1])
V = np.array(vecs, dtype=np.int64)
# canonical lines
key = lambda v: tuple(v) if next(x for x in v if x != 0) > 0 else tuple(-np.array(v))
L = np.array(sorted(set(key(list(v)) for v in V)), dtype=np.int64)
N = len(L); print('lines', N, flush=True)
Ee = L[:, :8]; AB = L[:, 8:]
def row(i):
    p = (Ee @ Ee[i]) // 4 + AB[:, 0] * AB[i, 1] + AB[:, 1] * AB[i, 0]
    c = (p == 0) | (p % 2 != 0); c[i] = False
    return c
rng = random.Random(seed)
inC = np.zeros(N, dtype=bool); miss = np.zeros(N, dtype=np.int64)
cache = {}
def getrow(i):
    if i not in cache:
        if len(cache) > 4000: cache.pop(next(iter(cache)))
        cache[i] = row(i)
    return cache[i]
def add(v):
    inC[v] = True; r = getrow(v); miss[:] += ~r; miss[v] -= 1
def rem(v):
    inC[v] = False; r = getrow(v); miss[:] -= ~r; miss[v] += 1
best = 0; tabu = {}; bestset = []
for it in range(iters):
    free = np.nonzero((~inC) & (miss == 0))[0]
    if len(free): add(int(rng.choice(free)))
    else:
        one = [u for u in np.nonzero((~inC) & (miss == 1))[0] if tabu.get(u, -1) < it]
        if one:
            u = rng.choice(one); w = int(np.nonzero(inC & ~getrow(u))[0][0]); rem(w); tabu[w] = it + 10; add(u)
        else:
            mem = np.nonzero(inC)[0]; w = int(rng.choice(mem)); rem(w); tabu[w] = it + 10
    c = int(inC.sum())
    if c > best:
        best = c; bestset = list(np.nonzero(inC)[0])
        print('it', it, 'clique', c, 'rank', np.linalg.matrix_rank(L[bestset].astype(float)), '%.0fs' % (time.time() - t0), flush=True)
pickle.dump(dict(L=L, best=bestset), open('ilsbig_%d_%d.pkl' % (maxn, seed), 'wb'))
