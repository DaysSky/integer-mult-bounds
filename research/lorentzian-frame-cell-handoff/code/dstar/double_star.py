"""Double-star decoders on punctured E8 (exact; geometry of the R420/P111 skeleton, research/e8-bit-carrier-skeleton).

B0 = (J + G) mod 2.  For centres p_1..p_9 with affinely independent classes, the decoder rows (1 + B(t,.)) of every
target are XORs of the stars N[p_j]; the coefficient of N[p_j] in row t is Q_j(t), an affine function of the class
of t (the dual basis).  Q_j equals N[p'_j] for a line p'_j iff p'_j _|_ p_j and p'_j is non-orthogonal to every other
centre.  This happens for all nine j iff the centre classes sum to 0 and every B-dual vector is nonsingular.
Puncturing centres and partners gives B0|live = sum_j N[p'_j]|live (x) N[p_j]|live with sources in p_j-perp and
readers in p'_j-perp.  The pairing rank (#446 Theorem C) is 6 per piece, so the decoder floor is 54 on 102 lines
(x = 54/102).  In the bitE8/1 format (targets at frame 0 at the scatter) each copy still costs its frame dimension 7;
the saving needs the copy read at the cut <p'_j>.
Also checks P111's punctured set: piece 66 has partner 87 (P110: pairing rank 6, 62 readers, all orthogonal to 87).
usage: python3 double_star.py [seed]"""
import itertools, os, random, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'e8-bit-carrier-skeleton', 'code', 'skeleton'))
import e8  # noqa: E402
GI = np.array(e8.GI); V = 120
w_, U_ = np.linalg.eigh(GI.astype(float)); X = U_[:, w_ > 1e-9] * np.sqrt(w_[w_ > 1e-9])   # real line vectors
assert np.allclose(X @ X.T, GI)
N = ((GI == 0) | np.eye(V, dtype=bool)).astype(np.uint8)        # rows of B0
ROW = {N[t].tobytes(): t for t in range(V)}
def f2rank(M):
    M = (np.array(M) % 2).astype(np.uint8).copy(); r = 0
    for c in range(M.shape[1]):
        p = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not p: continue
        M[[r, p[0]]] = M[[p[0], r]]
        for i in range(M.shape[0]):
            if i != r and M[i, c]: M[i] ^= M[r]
        r += 1
    return r
def prk(a, b):
    return int(np.linalg.matrix_rank(X[list(a)] @ X[list(b)].T, tol=1e-8)) if len(a) and len(b) else 0
def duals(P):
    """Q_j as 0/1 vectors on all lines: the unique combination of the stars N[p_k] with Q_j(p_l) = delta_jl."""
    out = []
    for j in range(9):
        for c in itertools.product((0, 1), repeat=9):
            Q = np.zeros(V, np.uint8)
            for k in range(9):
                if c[k]: Q ^= N[P[k]]
            if all(Q[P[l]] == (l == j) for l in range(9)):
                out.append(Q); break
    return out
def check(P, Pp, label):
    punct = set(P) | set(Pp); live = [t for t in range(V) if t not in punct]
    S = np.zeros((V, V), np.uint8)
    for p, q in zip(P, Pp): S ^= np.outer(N[q], N[p]).astype(np.uint8)
    ok = (S[np.ix_(live, live)] == N[np.ix_(live, live)]).all()
    costs = [prk([t for t in live if N[q, t]], [s for s in live if N[p, s]]) for p, q in zip(P, Pp)]
    src = [np.linalg.matrix_rank(X[[s for s in live if N[p, s]]], tol=1e-8) for p in P]
    print('%s: live %d, B0|live = sum N[p\'] x N[p]: %s, pairing ranks %s (sum %d), source spans %s, value 8v - 9cst = %d'
          % (label, len(live), ok, costs, sum(costs), src, 8 * len(live) - 9 * sum(costs)))
    return ok, len(live), sum(costs)
if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    found = None
    for it in range(400000):
        Z = rng.sample(range(V), 8)
        acc = np.ones(V, np.uint8)
        for z in Z: acc ^= N[z]
        x = ROW.get(acc.tobytes())                        # the line whose class is the sum of the 8 classes
        if x is None or x in Z: continue
        P = Z + [x]
        if f2rank(N[P]) != 9: continue                    # affinely independent
        Qs = duals(P); Pp = [ROW.get(Q.tobytes()) for Q in Qs]
        if any(q is None for q in Pp): continue
        if any(q == p or GI[p, q] != 0 for p, q in zip(P, Pp)): continue   # partner must be a new, orthogonal line
        found = (sorted(P), [Pp[P.index(p)] for p in sorted(P)]); break
    assert found, 'no double-star set found'
    P, Pp = found
    print('centres', P, 'partners', Pp)
    for p, q in zip(P, Pp):
        assert GI[p, q] == 0 and all(GI[q, r] != 0 for r in P if r != p)
    check(P, Pp, 'double star (18 punctures)')
    # P111's punctured set (research/e8-bit-p111-tuned/data/punct.json) and its partners
    P111 = [10, 15, 51, 53, 56, 66, 72, 89, 111]
    Qs = duals(P111)
    for p, Q in zip(P111, Qs):
        q = ROW.get(Q.tobytes())
        if q is not None:
            live = [t for t in range(V) if t not in P111 and t != q]
            rd = [t for t in live if Q[t]]
            print('P111 centre %d: partner %d (orthogonal %s); with %d punctured: %d readers, all orthogonal to %d: %s, '
                  'pairing rank %d' % (p, q, GI[p, q] == 0, q, len(rd), q, all(GI[q, t] == 0 for t in rd),
                                       prk(rd, [s for s in live if N[p, s]])))
