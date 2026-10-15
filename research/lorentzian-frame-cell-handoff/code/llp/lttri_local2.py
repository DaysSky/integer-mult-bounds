"""CORRECT local zero-waste test for M11 triangle nodes with three delivered users.
Zero waste needs Y = {P(E)} u (XOR of the three users' transversal sets) inside a hyperplane of the rank-8 node space
(own-A2 terms set to 0 locally, the most permissive choice).  A hyperplane functional phi with phi(P(E)) = 0 is
nonzero iff g(a,b,c) = alpha_a + beta_b + gamma_c is not identically 0 on A x B x C, and the transversal T(a,b,c) lies
in it iff g(a,b,c) = 0.  So the XOR set must lie in the zero set Z(g) of a nonzero additive g.  Transversals whose
three memberships are all forced (pair crossing once for that user) and odd in number MUST be in the XOR set: if no
nonzero additive zero set contains them, every such node needs >= 1 extra register (with 3 delivered users).
Zero sets enumerated over integer alpha, beta in {0}x{-R..R}^2 and gamma in {-2R..2R}^3.  usage: lttri_local2.py R"""
import sys, json, itertools, collections
import numpy as np
R = int(sys.argv[1])
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def mult(X, pair):
    k = 0
    for nj in nodes_of[X]:
        B, C = [T for T in sol[nj] if T != X]
        if (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B): k += 1
    return k
# enumerate zero sets on index grid 3x3x3
rng = range(-R, R + 1); zs = set()
idx = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
for a1, a2 in itertools.product(rng, rng):
    al = (0, a1, a2)
    for b1, b2 in itertools.product(rng, rng):
        be = (0, b1, b2)
        s_ab = np.array([[al[i] + be[j] for j in range(3)] for i in range(3)])
        for g in itertools.product(range(-2 * R, 2 * R + 1), repeat=3):
            m = 0; allzero = True
            for bit, (i, j, k) in enumerate(idx):
                if s_ab[i, j] + g[k] == 0: m |= 1 << bit
                else: allzero = False
            if not allzero: zs.add(m)
zs = sorted(zs, key=lambda m: -bin(m).count('1'))
maxi = []
for m in zs:
    if not any(m & ~q == 0 for q in maxi): maxi.append(m)
print('distinct zero sets', len(zs), 'maximal', len(maxi), 'max size', max(bin(m).count('1') for m in maxi), flush=True)
res = collections.Counter()
for ni, (A, B, C) in enumerate(sol):
    must = 0
    for bit, (i, j, k) in enumerate(idx):
        pts = (A[i], B[j], C[k]); forced = 0; free = 0
        for X in (A, B, C):
            pair = tuple(sorted(p for p in pts if p not in X))
            if mult(X, pair) == 1: forced += 1
            else: free += 1
        if free == 0 and forced % 2 == 1: must |= 1 << bit
    ok = any(must & ~Z == 0 for Z in maxi)
    res[(ok, bin(must).count('1'))] += 1
print('(zero-waste locally possible, #must-odd transversals) histogram:', sorted(res.items()))
