# For plane sections H = {t,u}-perp (all orbit types of u relative to a representative t) and A3-perps:
# is lines(H) covered by 2 hyperplanes of span(H)?  (kappa = 2 iff some product of two linear forms on H vanishes
# on every line of H.)  Exact via the space of quadratic forms vanishing on lines(H) + decomposability search.
import sys, itertools, numpy as np
from fractions import Fraction
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V, bits, closure, dim, nondegenerate
import sympy as sp
P, T = g.P, g.T
L = g.L
def basis_coords(ls):
    M = sp.Matrix([list(L[u]) for u in ls])
    rref, piv = M.T.rref()           # columns = lines
    B = [ls[i] for i in piv]
    Bm = sp.Matrix([list(L[u]) for u in B]).T
    coords = {}
    for u in ls:
        sol = Bm.solve_least_squares(sp.Matrix(list(L[u]))) if False else None
    # solve exactly
    pinv = (Bm.T * Bm).inv() * Bm.T
    for u in ls:
        c = pinv * sp.Matrix(list(L[u]))
        assert Bm * c == sp.Matrix(list(L[u]))
        coords[u] = [sp.nsimplify(x) for x in c]
    return B, coords
def two_cover(ls):
    B, C = basis_coords(ls); r = len(B)
    mons = list(itertools.combinations_with_replacement(range(r), 2))
    rows = [[C[u][i] * C[u][j] for (i, j) in mons] for u in ls]
    N = sp.Matrix(rows).nullspace()
    if not N: return r, 0, None
    # decomposable check: a rank<=2 symmetric matrix in span(N).  Try products l1*l2 with l1 from hyperplanes spanned by lines
    # cheap sufficient search: for each pair of disjoint line subsets given by candidate hyperplanes through r-1 lines (greedy)
    return r, len(N), N
def sect(ls_perp):
    m = (1 << V) - 1
    for u in ls_perp: m &= g.HYP[u]
    return bits(m)
t = T(0, 1, 2)
reps = {}
for u in range(V):
    if u == t: continue
    key = (g.kind[u], len(set(g.supp[u]) & {0, 1, 2}), int(round(g.G[t, u])))
    reps.setdefault(key, u)
for key, u in sorted(reps.items()):
    H = sect([t, u])
    r, nd, N = two_cover(H)
    print('T-target section {T012,', g.kind[u], g.supp[u], '} inner', key[2], '| lines', len(H), '| rank', r, '| quadric null dim', nd, flush=True)
t = P(0, 1); reps = {}
for u in range(V):
    if u == t: continue
    key = (g.kind[u], len(set(g.supp[u]) & {0, 1}), int(round(g.G[t, u])))
    reps.setdefault(key, u)
for key, u in sorted(reps.items()):
    H = sect([t, u])
    r, nd, N = two_cover(H)
    print('P-target section {P01,', g.kind[u], g.supp[u], '} inner', key[2], '| lines', len(H), '| rank', r, '| quadric null dim', nd, flush=True)
