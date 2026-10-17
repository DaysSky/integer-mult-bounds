"""Randomised greedy min-cost decoder on I_{11,1}: pieces = all structured flats (all Z11 shifts) + the 11 D10(p).
Served(t) is monotone in the family; greedy adds the piece with max (newly served targets)/cost (random tie-breaks,
noise), then prunes redundant pieces.  Exact incremental F2 bookkeeping per target with numpy bit-matrices."""
import pickle, sys, numpy as np, time
from dfam import LINES, IDX, NO, n, v, check, rank_of
from flats import shift
flats = pickle.load(open('flats.pkl', 'rb'))
pcs = {}; cst = {}
for f in flats:
    c = f[0] + (0 if f[2] else 1)
    for a in range(n):
        p = tuple(sorted(shift(f[1], a))); pcs[p] = c
D10 = [tuple(sorted(k for k, l in enumerate(LINES) if (l[0] == 'P' and q not in l[1]) or (l[0] == 'T' and q in l[1]))) for q in range(n)]
for p in D10: pcs[p] = 10
P = list(pcs.keys()); C = np.array([pcs[p] for p in P], float); J = len(P)
Np = [[t] + list(np.nonzero(NO[t])[0]) for t in range(v)]
# restricted piece vectors per target as boolean matrices (J x |N'(t)|)
M = np.zeros((J, v), np.uint8)
for j, p in enumerate(P): M[j, list(p)] = 1
R = [M[:, Np[t]].astype(bool) for t in range(v)]
def run(seed, noise):
    rng = np.random.default_rng(seed)
    # per target: basis rows (bool vectors) with pivots; residual of e_t
    basis = [[] for _ in range(v)]; piv = [[] for _ in range(v)]
    e = [np.eye(len(Np[t]), dtype=bool)[0] for t in range(v)]
    served = np.zeros(v, bool); chosen = []
    def reduce_vecs(t, X):
        X = X.copy()
        for b, p in zip(basis[t], piv[t]):
            mask = X[:, p]
            if mask.any(): X[mask] ^= b
        return X
    while not served.all():
        gain = np.zeros(J)
        for t in np.nonzero(~served)[0]:
            Xr = reduce_vecs(t, R[t]); er = reduce_vecs(t, e[t][None, :])[0]
            gain += (Xr == er).all(1) & Xr.any(1)
        score = gain / C * (1 + noise * rng.random(J))
        score[chosen] = -1
        j = int(np.argmax(score))
        if gain[j] == 0:   # no single piece serves a new target: add the cheapest piece touching an unserved target
            t = int(np.nonzero(~served)[0][0]); j = int(np.argmin(np.where(R[t][:, 0], C, 1e9)))
        chosen.append(j)
        for t in range(v):
            x = reduce_vecs(t, R[t][j][None, :])[0]
            if x.any():
                p = int(np.argmax(x)); basis[t].append(x); piv[t].append(p)
                if served[t]: continue
                er = reduce_vecs(t, e[t][None, :])[0]
                if not er.any(): served[t] = True
    # prune
    fam = list(chosen)
    for j in sorted(fam, key=lambda j: -C[j]):
        trial = [k for k in fam if k != j]
        ok, _, _ = check([P[k] for k in trial], want_rows=False)
        if ok: fam = trial
    return fam
if __name__ == '__main__':
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    best = None
    for s in range(seeds):
        t0 = time.time(); fam = run(s, 0.3 if s else 0.0)
        cost = int(sum(C[j] for j in fam))
        ok, bad, rows = check([P[k] for k in fam])
        from collections import Counter
        print('seed %d: cost %d, pieces %d, ranks %s, valid %s, avg row %.1f (%.0fs)' % (s, cost, len(fam), dict(Counter(int(C[j]) for j in fam)), ok, sum(rows)/len(rows), time.time()-t0), flush=True)
