"""Exact inertia bound for root-like line systems (session 6g).

A root-like system is a set of v vectors u_i in a real quadratic space V of signature (p, q), h = p + q, with
<u_i, u_i> = 2 and <u_i, u_j> in {0, +1, -1} for i != j.

Claim: v <= pi(h; p, q), the positive index of inertia of the symmetric form
    Phi(a, b) = <a, b> - (1/4) <T a, T b>     on Sym^3(V),
where <,> is the induced form and T : Sym^3(V) -> V is the metric contraction (T(u^3) = <u, u> u).
Proof: Phi(u^3, w^3) = <u, w>^3 - (1/4)<u,u><w,w><u,w> = <u, w>^3 - <u, w>, which is 6 on the diagonal and 0 for
products in {0, +-1}.  So the u_i^3 span a Phi-positive-definite subspace of dimension v.
Closed form (Sym^3 = ker T  (+)  im T*, T T* = (h+2)/3, Phi = kappa (1 - kappa/4) <,> on im T*, kappa = (h+2)/3):
    q = 1 (Lorentzian, p = h - 1):  pi = C(h+1, 3) + (h - 1 if h < 10, 0 if h = 10, 1 if h > 10).
    q = 0 (Euclidean):              pi = C(h+2, 3) (h < 10), C(12,3) - 10 (h = 10), C(h+2, 3) - h (h > 10).
So h = 9: 128, h = 10: 165 (attained by I_{10,1}), h = 11: 221 (I_{11,1}: 220), h = 12: 287, h = 13: 365, h = 16: 681;
E8 (h = 8, Euclidean): 120, attained.

This script checks the closed form EXACTLY (rational Gram matrix of Phi in the monomial basis of Sym^3, inertia by
exact symmetric elimination; Sylvester's law), and checks Phi(u_i^3, u_j^3) = 6 delta_ij on the I_{n,1} systems
(n = 10, 11) and on E8 (as I_{8,1} w-perp).  usage: python3 inertia_bound.py    (about 1-3 min)"""
import itertools
from fractions import Fraction as Fr
from math import comb, factorial
from collections import Counter

def monomials(h):
    return list(itertools.combinations_with_replacement(range(h), 3))

def gram_phi(eta):
    """Exact Gram of Phi on the basis of symmetrised monomials s_m = sym(e_a e_b e_c) (orthogonal basis e, eta = +-1)."""
    h = len(eta); B = monomials(h)
    # <s_m, s_m'> = 0 unless m = m' (as multisets); <s_m, s_m> = prod(eta) * (prod mult!)/3!
    def ip(m):
        c = Counter(m); w = Fr(1)
        for a, k in c.items(): w *= Fr(factorial(k)) * eta[a]**k
        return w / 6
    # T(s_m) = metric contraction of a symmetrised monomial: average over the 3 choices of the free slot
    def T(m):
        out = Counter()
        for free in range(3):
            pair = [m[i] for i in range(3) if i != free]
            if pair[0] == pair[1]:
                out[m[free]] += Fr(eta[pair[0]], 3)
        return out
    Ts = [T(m) for m in B]
    N = len(B); G = [[Fr(0)]*N for _ in range(N)]
    for i in range(N):
        G[i][i] += ip(B[i])
    for i in range(N):
        for j in range(N):
            s = sum(c * Ts[j].get(a, 0) * eta[a] for a, c in Ts[i].items())
            if s: G[i][j] -= s / 4
    return G

def inertia(G):
    """Exact (pos, neg, zero) of a rational symmetric matrix by symmetric Gaussian elimination with 2x2 pivots."""
    A = [row[:] for row in G]; n = len(A); pos = neg = 0; alive = list(range(n))
    while alive:
        k = next((i for i in alive if A[i][i] != 0), None)
        if k is not None:
            d = A[k][k]
            if d > 0: pos += 1
            else: neg += 1
            rest = [i for i in alive if i != k]
            for i in rest:
                if A[i][k]:
                    f = A[i][k] / d
                    for j in rest: A[i][j] -= f * A[k][j]
            alive = rest; continue
        pair = next(((i, j) for i in alive for j in alive if i < j and A[i][j] != 0), None)
        if pair is None: break                     # remaining block is zero
        i, j = pair                                 # diagonal zero, A[i][j] != 0: replace e_i by e_i + e_j
        for r in alive: A[r][i] += A[r][j]
        for c in alive: A[i][c] += A[j][c]
    return pos, neg, n - pos - neg

def closed_form(p, q):
    h = p + q
    if q == 1: return comb(h + 1, 3) + (h - 1 if h < 10 else 0 if h == 10 else 1)
    if q == 0: return comb(h + 2, 3) if h < 10 else comb(12, 3) - 10 if h == 10 else comb(h + 2, 3) - h

def phi_on_lines(L, eta):
    ip = lambda u, w: sum(a*b*e for a, b, e in zip(u, w, eta))
    bad = 0
    for i, u in enumerate(L):
        for j, w in enumerate(L):
            g = ip(u, w); val = g**3 - Fr(ip(u, u) * ip(w, w), 4) * g
            bad += val != (6 if i == j else 0)
    return bad

def inl(n):
    L = []
    for i, j in itertools.combinations(range(n), 2):
        x = [0]*(n+1); x[i], x[j] = 1, -1; L.append(x)
    for t in itertools.combinations(range(n), 3):
        x = [0]*(n+1)
        for i in t: x[i] = 1
        x[n] = 1; L.append(x)
    return L

def e8_in_i81():
    """All norm-2 vectors (x; y) of I_{8,1} with sum x = 3y (w = (1^8; 3), w^2 = -1, w-perp = E8), up to sign."""
    out = set()
    for y in range(0, 4):
        for x in itertools.product(range(-3, 4), repeat=8):
            if sum(x) == 3*y and sum(a*a for a in x) - y*y == 2:
                v = tuple(x) + (y,); nv = tuple(-a for a in v); out.add(max(v, nv))
    return [list(v) for v in sorted(out)]

if __name__ == '__main__':
    for p, q in [(7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (8, 0), (9, 0), (10, 0)]:
        G = gram_phi([1]*p + [-1]*q)
        ps, ng, z = inertia(G)
        cf = closed_form(p, q)
        print('signature (%d,%d), h = %2d: dim Sym^3 = %3d, Phi inertia (+%d, -%d, 0:%d); closed form %d %s'
              % (p, q, p + q, len(G), ps, ng, z, cf, 'OK' if cf == ps else 'MISMATCH'), flush=True)
        assert cf == ps
    for n in (10, 11):
        L = inl(n); bad = phi_on_lines(L, [1]*n + [-1])
        print('I_{%d,1}: %d lines, Phi(u_i^3, u_j^3) = 6 delta_ij violations: %d; bound %d' % (n, len(L), bad, closed_form(n - 1, 1) if n != 10 else closed_form(9, 1)))
        assert bad == 0
    L = e8_in_i81(); bad = phi_on_lines(L, [1]*8 + [-1])
    print('E8 = w-perp in I_{8,1}: %d lines, violations %d; Euclidean bound (h = 8) %d' % (len(L), bad, closed_form(8, 0)))
    assert bad == 0 and len(L) == 120
    print('PASS')
