"""Exact top-cover numbers for Lorentzian odd-or-zero units (bit side: char-0 labels).
Readers of s: R(s) = {t != s : Q(s,t) = 0}.  cover 1 iff rank R(s) <= h-2 (h = rank of all labels).
cover <= 2 iff some product l1*l2 of functionals on s^perp vanishes on R(s); necessary: the space K of quadratic
forms on span R(s) vanishing on R(s) is nonzero.  dim K is computed exactly (rank mod two primes; full column rank
mod p certifies K = 0 over Q).  When K != 0 we test factorable members exhaustively via reader-spanned hyperplanes."""
import json, sys, itertools, collections
import numpy as np
from fractions import Fraction as Fr

def rank_mod(M, p):
    M = [[x % p for x in row] for row in M]
    r = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r

def qrank(rows):
    return np.linalg.matrix_rank(np.array(rows, dtype=float), tol=1e-8) if len(rows) else 0

def coords_basis(rows, d):
    """greedy coordinate subset of size d on which rows have rank d"""
    A = np.array(rows, dtype=float); cols = []
    for j in range(A.shape[1]):
        if qrank(A[:, cols + [j]]) > len(cols): cols.append(j)
        if len(cols) == d: break
    return cols

def hyperplane_cover2(Y, d):
    """exhaustive: R subset H1 u H2 for hyperplanes of span (dim d).  WLOG H1 spanned by readers in it, or H1 contains
    a rank < d-1 reader set A and then B = R\\A has rank <= d-1 (so H2 is spanned by its readers if rank d-1, else
    everything is in two lower flats -> also caught by enumerating H2 spanned).  If both A,B have rank < d-1 then
    rank R <= 2(d-2) ... still possible; we handle the general case by enumerating flats of rank d-1 spanned by readers
    (normals) and testing whether the complement has rank <= d-1."""
    n = len(Y); Yf = np.array(Y, dtype=float)
    seen = set()
    # enumerate normals of hyperplanes spanned by d-1 independent readers, via incremental flats (BFS on closures)
    # closure-based enumeration of all rank-(d-1) flats: extend independent sets in lexicographic order with pruning
    flats = set()
    def closure(idx):
        B = Yf[list(idx)]
        r = qrank(B)
        out = [i for i in range(n) if qrank(np.vstack([B, Yf[i]])) == r]
        return frozenset(out)
    # build flats level by level (rank k flats from rank k-1 flats + one reader outside)
    level = {frozenset([i]) for i in range(n)}
    level = {closure(f) for f in level}
    for k in range(2, d):
        nxt = set()
        for F in level:
            for i in range(n):
                if i not in F and i > min(F) - 10**9:
                    nxt.add(closure(list(F) + [i]))
        level = nxt
        if len(level) > 200000: return None, len(level)
    for F in level:          # rank d-1 flats
        rest = [i for i in range(n) if i not in F]
        if not rest or qrank(Yf[rest]) <= d - 1:
            return True, len(level)
    # also the degenerate case where both parts have rank < d-1: then each lies in some hyperplane; the part A
    # of rank < d-1 extends to a reader flat of rank d-1 unless all readers outside A lie in B ... covered since the
    # flat containing A only grows A and shrinks B (B's rank cannot increase).  If A cannot be extended inside the
    # reader flats (A is itself closed of rank < d-1 and every extension is a rank-(d-1) flat F containing A), then
    # R \\ F subset B still has rank <= d-1 -> found above.
    return False, len(level)

def analyse(path, maxsrc=None):
    d0 = json.load(open(path)); eta = np.array(d0['eta']); R = np.array(d0['R'])
    G = R @ eta @ R.T
    Gi = np.rint(G).astype(np.int64); assert np.allclose(G, Gi)
    v = len(R); h = qrank(R)
    # integer labels: scale to integers
    Ri = np.rint(R * 2).astype(np.int64) if not np.allclose(R, np.rint(R)) else np.rint(R).astype(np.int64)
    res = collections.Counter(); kd = collections.Counter(); nread = collections.Counter()
    for s in range(v if maxsrc is None else maxsrc):
        rd = [t for t in range(v) if t != s and Gi[s, t] == 0]
        nread[len(rd)] += 1
        Y = [list(Ri[t]) for t in rd]
        d = qrank(Y)
        if d <= h - 2:
            res[1] += 1; continue
        cols = coords_basis(Y, d)
        Yc = [[row[j] for j in cols] for row in Y]
        mons = list(itertools.combinations_with_replacement(range(d), 2))
        M = [[int(y[i]) * int(y[j]) for (i, j) in mons] for y in Yc]
        r1 = rank_mod(M, 1000003); r2 = rank_mod(M, 998244353)
        rk = max(r1, r2); kdim = len(mons) - rk
        kd[kdim] += 1
        if kdim == 0:
            res['>=3 (K=0)'] += 1; continue
        ok, nf = hyperplane_cover2(Yc, d)
        res[2 if ok else ('>=3' if ok is False else 'undecided')] += 1
    print(path, 'v', v, 'h', h, 'readers/src', dict(nread), 'dim K', dict(kd), 'cover', dict(res), flush=True)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        analyse(p)
