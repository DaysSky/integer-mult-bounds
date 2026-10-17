"""Exact (rational) check: in the triple family T_h (form I - J/9 on Q^h), every source s = t_{abc} has its readers
R(s) = {t_T : |T cap s| = 1} covered by two NONDEGENERATE hyperplanes of s^perp:
  H1 = s^perp cap {x_a = 0}      (contains G_b u G_c),
  H2 = a hyperplane of s^perp containing span(G_a), chosen nondegenerate from the pencil.
A hyperplane H of s^perp is nondegenerate iff its 2-dim orthogonal complement (in Q^h) is nondegenerate.
By S_h symmetry one source per h suffices (all sources are equivalent)."""
import itertools, sys
import sympy as sp
def run(h):
    B = sp.eye(h) - sp.ones(h, h) / 9
    tri = list(itertools.combinations(range(h), 3))
    vec = lambda T: sp.Matrix([1 if i in T else 0 for i in range(h)])
    s = (0, 1, 2); a, b, c = s; vs = vec(s)
    ip = lambda x, y: (x.T * B * y)[0]
    R = [T for T in tri if len(set(T) & set(s)) == 1]
    assert all(ip(vec(T), vs) == 0 for T in R)
    # H1 = s^perp cap {x_a = 0}: normal functionals (as vectors via the form): s and z with <z, x> = x_a, z = B^-1 e_a
    Binv = B.inv()
    za = Binv * sp.Matrix([1 if i == a else 0 for i in range(h)])
    def comp_nondeg(n1, n2):
        G = sp.Matrix([[ip(n1, n1), ip(n1, n2)], [ip(n2, n1), ip(n2, n2)]])
        return G.det()
    d1 = comp_nondeg(vs, za)
    G1 = [T for T in R if T[0] != a and a not in T]       # readers with x_a = 0
    cov1 = set(T for T in R if a not in T)
    # H2: hyperplanes of s^perp containing span(G_a) -> normals in span(G_a u {s})^perp (2-dim, contains s's dual
    # direction); pick n = combination of a basis of that complement, not parallel to s, with nondegenerate <s, n>
    Ga = [vec(T) for T in R if a in T]
    M = sp.Matrix.hstack(*Ga, vs).T * B          # rows: functionals <g, .>
    ns = M.nullspace()                            # vectors y with <g, y> = 0 for all g in G_a and <s, y> = 0
    assert len(ns) >= 1
    best = None
    for coeffs in [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1)][: (6 if len(ns) > 1 else 1)]:
        n = sum((cf * ns[i] for i, cf in enumerate(coeffs[:len(ns)])), sp.zeros(h, 1))
        if n == sp.zeros(h, 1): continue
        d2 = comp_nondeg(vs, n)
        if d2 != 0:
            best = (coeffs, d2); break
    cov2 = set(T for T in R if a in T)
    covered = cov1 | cov2
    print('h=%2d readers %4d | H1 complement det %s (%s) covers %d | H2 complement det %s covers %d | all covered: %s'
          % (h, len(R), d1, 'nondeg' if d1 != 0 else 'DEGENERATE', len(cov1), best[1] if best else None, len(cov2),
             covered == set(R)), flush=True)
    # sanity: H1 really contains its claimed readers: <z_a, t_T> = x_a(T) = 0 for T not containing a
    assert all(ip(za, vec(T)) == 0 for T in cov1)
for h in map(int, sys.argv[1:]):
    run(h)
