"""S11-orbit representatives of all flats (closed line sets L(span)) of I_{11,1}, by rank.
Closure: exact rank mod p = 2^31 - 1 (coordinates are 0/+-1 and 12-dimensional, so every nonzero minor has
|det| <= 12^6 < p and ranks/memberships mod p equal those over Q).
Orbits: canonical form = lexicographically least relabelled line list over the leaves of an individualisation-
refinement search on the 11 points, with branches pruned by point transpositions that preserve the line set
(these are automorphisms fixing the current partition, so pruned subtrees give the same encodings).
usage: flats.py MAXRANK"""
import sys, pickle, time, collections
import numpy as np
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
NPT = 11; PR = 2147483647
LINES = [tuple(sorted(g.supp[x])) for x in range(V)]
def coord(x):
    v = [0] * 12; s = g.supp[x]
    if g.kind[x] == 'P': v[s[0]] = 1; v[s[1]] = -1
    else:
        v[11] = 1
        for i in s: v[i] = 1
    return v
C = np.array([coord(x) for x in range(V)], dtype=object)
def rref_modp(rows):
    A = [list(r) for r in rows]; piv = []; r = 0
    for c in range(12):
        p = next((i for i in range(r, len(A)) if A[i][c] % PR), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        inv = pow(A[r][c] % PR, PR - 2, PR); A[r] = [(x * inv) % PR for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % PR:
                f = A[i][c]; A[i] = [(a - f * b) % PR for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    return A[:r], piv
def closure(idx):
    B, piv = rref_modp([C[i] for i in idx])
    r = len(B)
    if r == 12: return tuple(range(V)), r
    free = [c for c in range(12) if c not in piv]
    # kernel basis of B (B k = 0): for each free column f, k_f = e_f - sum_i B[i][f] e_{piv i}
    K = []
    for f in free:
        k = [0] * 12; k[f] = 1
        for i, pc in enumerate(piv): k[pc] = (-B[i][f]) % PR
        K.append(k)
    K = np.array(K, dtype=object)
    vals = C.dot(K.T) % PR
    inside = [i for i in range(V) if not any(vals[i])]
    return tuple(inside), r
def refine(lines, col):
    for _ in range(NPT + 1):
        sig = []
        for q in range(NPT):
            ms = sorted((len(l), tuple(sorted(col[r] for r in l if r != q))) for l in lines if q in l)
            sig.append((col[q], tuple(ms)))
        ks = sorted(set(sig)); new = [ks.index(s) for s in sig]
        if new == col: return col
        col = new
    return col
def canon(idx):
    lines = [LINES[i] for i in idx]; lset = set(lines)
    def is_aut_transposition(a, b):
        def sw(q): return b if q == a else a if q == b else q
        return all(tuple(sorted(sw(q) for q in l)) in lset for l in lines)
    best = [None]
    def search(col):
        cells = collections.defaultdict(list)
        for p in range(NPT): cells[col[p]].append(p)
        keys = sorted(cells)
        target = next((k for k in keys if len(cells[k]) > 1), None)
        if target is None:
            perm = [0] * NPT
            for rk, k in enumerate(keys): perm[cells[k][0]] = rk
            e = tuple(sorted(tuple(sorted(perm[q] for q in l)) for l in lines))
            if best[0] is None or e < best[0]: best[0] = e
            return
        X = cells[target]; x0 = X[0]
        branches = [x0] + [x for x in X[1:] if not is_aut_transposition(x0, x)]
        for p in branches:
            c2 = [2 * c for c in col]; c2[p] -= 1
            search(refine(lines, c2))
    search(refine(lines, [0] * NPT))
    return best[0]
if __name__ == '__main__':
    MAXR = int(sys.argv[1])
    t0 = time.time()
    reps = {1: {}}
    for x in (0, 55):
        cl, r = closure([x]); reps[1][canon(cl)] = cl
    print('rank 1 orbits', len(reps[1]), flush=True)
    for r in range(1, MAXR):
        nxt = {}
        for key, cl in reps[r].items():
            S = set(cl); seen = set()
            for s in range(V):
                if s in S: continue
                c2, rr = closure(list(cl) + [s])
                if rr != r + 1 or c2 in seen: continue
                seen.add(c2)
                k2 = canon(c2)
                if k2 not in nxt: nxt[k2] = c2
        reps[r + 1] = nxt
        sizes = collections.Counter(len(c) for c in nxt.values())
        print('rank %d orbits %d (largest line counts %s) %.0fs' % (r + 1, len(nxt), sorted(sizes.items())[-5:], time.time() - t0), flush=True)
        pickle.dump(reps, open('/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/declp/flats_reps.pkl', 'wb'))
