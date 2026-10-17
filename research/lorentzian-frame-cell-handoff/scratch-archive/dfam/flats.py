"""Structured flats of I_{11,1}: closures (all lines inside the real span) of generator sets built from point sets.
Canonical up to the cyclic shift Z11.  Saves flats.pkl: list of (rank, frozenset(lines), nondegenerate?)."""
import itertools, numpy as np, pickle
from dfam import LINES, V, eta, IDX, n, v
def closure(idx):
    M = V[list(idx)].astype(float)
    U, s, Wt = np.linalg.svd(M, full_matrices=False); r = int((s > 1e-9).sum()); B = Wt[:r]
    # line l in span iff residual of projection zero
    coef, res, rk, sv = np.linalg.lstsq(B.T, V.T.astype(float), rcond=None)
    resid = np.linalg.norm(B.T @ coef - V.T, axis=0)
    inside = frozenset(np.nonzero(resid < 1e-8)[0].tolist())
    g = (B*eta) @ B.T
    nondeg = abs(np.linalg.det(g)) > 1e-9
    return r, inside, nondeg
def lines_on(S):
    S = set(S); out = []
    for k, (t, pts, _) in enumerate(LINES):
        if set(pts) <= S: out.append(k)
    return out
def shift(fs, a):
    out = set()
    for k in fs:
        t, pts, _ = LINES[k]; out.add(IDX[(t, tuple(sorted((p + a) % n for p in pts)))])
    return frozenset(out)
def canon(fs):
    return min(tuple(sorted(shift(fs, a))) for a in range(n))
if __name__ == '__main__':
    seen = {}
    gens = []
    pts = range(n)
    for k in range(2, 10):
        for S in itertools.combinations(pts, k):
            if S[0] != 0: continue                     # Z11: wlog contains 0 (coarse; canon handles the rest)
            rest = [p for p in pts if p not in S]
            base = lines_on(S)
            gens.append(base)                                           # lines on S
            gens.append([IDX[('P', ij)] for ij in itertools.combinations(S, 2)])   # A_{k-1}(S)
            for p in rest[:]:
                Tp = [IDX[('T', tuple(sorted(ij + (p,))))] for ij in itertools.combinations(S, 2)]
                gens.append([IDX[('P', ij)] for ij in itertools.combinations(S, 2)] + Tp)   # D_k(p, S)
                gens.append(Tp)                                                          # B_p(S)
                gens.append(base + Tp)                                                   # lines on S + B_p(S)
    cnt = 0
    for g in gens:
        if not g: continue
        r, inside, nd = closure(g)
        if r > 9 or not inside: continue
        c = canon(inside)
        if c in seen: continue
        seen[c] = (r, frozenset(c), nd); cnt += 1
    flats = sorted(seen.values(), key=lambda t: (t[0], -len(t[1])))
    from collections import Counter
    print('flats (up to Z11):', len(flats), 'by rank:', dict(Counter(f[0] for f in flats)))
    print('nondegenerate by rank:', dict(Counter(f[0] for f in flats if f[2])))
    for r in range(1, 10):
        sizes = sorted(set(len(f[1]) for f in flats if f[0] == r), reverse=True)[:6]
        print(' rank', r, 'largest line counts', sizes)
    pickle.dump(flats, open('flats.pkl', 'wb'))
