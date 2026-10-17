"""Double-star decoders on punctured E8: centres p_1..p_9 (affinely independent classes) with partners p'_j such that
p'_j _|_ p_j and p'_j non-orth p_k (k != j).  Then B0|live = sum_j N[p'_j]|live (x) N[p_j]|live, piece j has sources in
p_j-perp and readers in p'_j-perp, so cost <= 6 when p_j _|_ p'_j and both are punctured.  Search and price."""
import sys, random, itertools, numpy as np
from e8dec import G, v, A
NONO = (G != 0) & ~np.eye(v, dtype=bool)          # non-orthogonal
ORTH = (G == 0)
N = ((G == 0) | np.eye(v, dtype=bool)).astype(np.uint8)
def aff_indep(Z):
    M = N[Z].astype(np.uint8).copy(); r = 0
    for c in range(v):
        p = [i for i in range(r, len(Z)) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(len(Z)):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r == len(Z)
def partners(Z):
    out = []
    for j, pj in enumerate(Z):
        cand = [x for x in range(v) if ORTH[x, pj] and x != pj and all(NONO[x, pk] for k, pk in enumerate(Z) if k != j)]
        out.append(cand)
    return out
def prk(a, b):
    return int(np.linalg.matrix_rank(A[a] @ A[b].T)) if len(a) and len(b) else 0
def evaluate(Z, Pp):
    punct = set(Z) | set(Pp); live = [t for t in range(v) if t not in punct]
    # verify decomposition on live x live: B0 = sum_j N[p'_j] (x) N[p_j]
    Bsum = np.zeros((v, v), np.uint8)
    for pj, qj in zip(Z, Pp): Bsum ^= np.outer(N[qj], N[pj]).astype(np.uint8)
    ok = (Bsum[np.ix_(live, live)] == N[np.ix_(live, live)]).all()
    costs = [prk([s for s in live if N[pj, s]], [t for t in live if N[qj, t]]) for pj, qj in zip(Z, Pp)]
    return ok, len(live), costs
rng = random.Random(int(sys.argv[1])); found = 0; tries = 0
best = None
while tries < int(sys.argv[2]):
    tries += 1
    Z = rng.sample(range(v), 9)
    if not aff_indep(Z): continue
    cand = partners(Z)
    if any(len(c) == 0 for c in cand): continue
    # choose partners to minimise punctures (prefer partners that coincide / are among Z? they cannot be in Z)
    Pp = [c[0] for c in cand]
    ok, nl, costs = evaluate(Z, Pp)
    val = 8 * nl - 9 * sum(costs)
    found += 1
    if best is None or val > best[0]:
        best = (val, nl, sum(costs), costs, ok, Z, Pp)
        print('found: live %d cost %d (pieces %s) decomposition ok %s value 8v-9cst = %d (P111 321)' % (nl, sum(costs), costs, ok, val), flush=True)
print('tries', tries, 'double-star sets found', found)
