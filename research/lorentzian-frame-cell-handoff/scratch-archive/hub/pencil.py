# Exact 2-hyperplane covers of a section whose vanishing-quadric space is a pencil (dim 2).
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
import sympy as sp
P, T = g.P, g.T
def sect(lp):
    m = (1 << V) - 1
    for u in lp: m &= g.HYP[u]
    return bits(m)
def coords(H):
    M = sp.Matrix([list(map(int, g.L[u])) for u in H])
    _, piv = M.T.rref(); B = [H[i] for i in piv]
    Bm = sp.Matrix([list(map(int, g.L[u])) for u in B]).T
    pinv = (Bm.T * Bm).inv() * Bm.T
    return B, {u: list(pinv * sp.Matrix(list(map(int, g.L[u])))) for u in H}
def covers(H):
    B, C = coords(H); r = len(B)
    mons = list(itertools.combinations_with_replacement(range(r), 2))
    A = sp.Matrix([[C[u][i] * C[u][j] for (i, j) in mons] for u in H])
    N = A.nullspace()
    def symm(vec):
        S = sp.zeros(r, r)
        for k, (i, j) in enumerate(mons):
            if i == j: S[i, i] = vec[k]
            else: S[i, j] = S[j, i] = vec[k] / 2
        return S
    out = []
    if len(N) == 2:
        lam = sp.symbols('lam')
        cand = []
        for Q in (symm(N[1]), symm(N[0] + lam * N[1])):
            if not Q.has(lam):
                if Q.rank() <= 2: cand.append(Q)
                continue
            # rank<=2: all 3x3 minors vanish; take gcd of a few minors' numerators
            polys = []
            idx = list(itertools.combinations(range(r), 3))
            for (a, b, c) in idx[:60]:
                for (d, e, f) in idx[:60:7]:
                    m = sp.together(Q.extract([a, b, c], [d, e, f]).det())
                    p = sp.Poly(sp.numer(m), lam)
                    if not p.is_zero: polys.append(p)
                if len(polys) > 40: break
            gpol = polys[0]
            for p in polys[1:]: gpol = sp.gcd(gpol, p)
            for rt in sp.roots(gpol, lam):
                Qr = Q.subs(lam, rt)
                if Qr.rank() <= 2: cand.append(Qr)
        for Q in cand:
            # factor Q = (l1 l2^T + l2 l1^T)/2 : kernels give the two hyperplanes
            ev = Q.eigenvects()
            vals = [(v, m, vecs) for v, m, vecs in ev if v != 0]
            # build lines per hyperplane by testing products
            # find l1,l2 from the nonzero eigenpairs: Q = s1 v1 v1^T + s2 v2 v2^T with s1 s2 < 0
            (s1, _, v1), (s2, _, v2) = vals[0], vals[1]
            v1, v2 = v1[0], v2[0]
            v1 = v1 / sp.sqrt((v1.T * v1)[0]); v2 = v2 / sp.sqrt((v2.T * v2)[0])
            a, b = sp.sqrt(sp.Abs(s1)), sp.sqrt(sp.Abs(s2))
            l1 = a * v1 + b * v2; l2 = a * v1 - b * v2
            Fa = [u for u in H if sp.simplify((sp.Matrix(C[u]).T * l1)[0]) == 0]
            Fb = [u for u in H if sp.simplify((sp.Matrix(C[u]).T * l2)[0]) == 0]
            assert set(Fa) | set(Fb) == set(H)
            out.append((Fa, Fb))
    return len(N), out
if __name__ == '__main__':
    t = T(0, 1, 2)
    H = sect([t, T(0, 1, 3)])
    nd, cov = covers(H)
    print('null dim', nd, '| covers', [(len(a), len(b), len(set(a) & set(b))) for a, b in cov])
