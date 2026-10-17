"""Inertia bound for root-like line systems (norm 2, products in {0,+-1}) in R^{p,q}.
Phi(a,b) = <a,b> - (1/4)<Ta,Tb> on Sym^3(V), T = metric contraction; Phi(u^3, w^3) = <u,w>^3 - <u,w>.
For a root-like system [Phi(u_i^3,u_j^3)] = 6 I, so v <= positive index of Phi.  Numerical check of the index and of
the 6I identity on I_{n,1} (p = n - 1 + ... see below)."""
import itertools, numpy as np, sys
from math import comb
def sym3_basis(h):
    return list(itertools.combinations_with_replacement(range(h), 3))
def phi_matrix(eta):
    h = len(eta); B = sym3_basis(h); idx = {m: i for i, m in enumerate(B)}
    # represent symmetric tensors in the monomial basis via the full tensor; Gram of monomials under induced form.
    # monomial m = sym(e_a e_b e_c) as full tensor = average over distinct permutations
    def full(m):
        t = np.zeros((h, h, h))
        perms = set(itertools.permutations(m))
        for p in perms: t[p] += 1.0/len(perms)
        return t
    F = [full(m) for m in B]
    E = np.array(eta, float)
    def ip(s, t): return np.einsum('abc,abc,a,b,c->', s, t, E, E, E)
    def T(s): return np.einsum('aac,a->c', s, E)
    N = len(B); P = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            P[i, j] = P[j, i] = ip(F[i], F[j]) - 0.25*np.dot(T(F[i])*E, T(F[j]))
    return P, F, B
def tensor3(u):
    return np.einsum('a,b,c->abc', u, u, u)
for (p, q) in [(8, 1), (9, 1), (10, 1), (11, 1), (8, 0), (9, 0), (10, 0)]:
    eta = [1]*p + [-1]*q
    P, F, B = phi_matrix(eta)
    ev = np.linalg.eigvalsh(P)
    pos = int((ev > 1e-9).sum()); neg = int((ev < -1e-9).sum()); zer = len(ev) - pos - neg
    h = p + q
    pred = (comb(p+2, 3) + (p if h < 10 else 0 if h == 10 else q)) if q == 1 else None
    print('sig (%d,%d) h=%d: Phi index pos %d neg %d zero %d ; predicted pos %s' % (p, q, h, pos, neg, zer, pred), flush=True)
