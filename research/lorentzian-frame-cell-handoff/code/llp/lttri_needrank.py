"""Necessary condition for releasing a target from the M11 triangle design.  Every target sits in exactly 4 triangle
nodes, so if T(X) leaves node n0 its replacement section F'-perp (rank 8, F' a rank-3 frame through T(X)) must contain
every line of R(T(X)) covered ONLY by n0 among X's 4 nodes: A2(B0) + A2(C0) + P(E0) (each within-block pair outside
X is covered exactly once, 4 x 7 = 28) and the multiplicity-1 transversals of n0.  If that set spans n0-perp (rank 8),
then F'-perp = n0-perp, F' = n0's frame, and F'-perp holds no transversal released at another node (a released
transversal at node n is split only by n, so it is not in n0-perp).  Reports the rank for every (node, user).
usage: lttri_needrank.py"""
import json, itertools, collections
from lgeo import *
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def A2(T): return [Ln('P', p) for p in itertools.combinations(T, 2)]
def splits(nj, X, pair):
    B, C = [T for T in sol[nj] if T != X]
    return (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B)
cnt = collections.Counter(); bad = []
for ni, node in enumerate(sol):
    F = pp(sum(1 << Ln('T', T) for T in node)); perp = pm(F)
    for X in node:
        B, C = [T for T in node if T != X]
        E = tuple(x for x in range(11) if x not in X + B + C)
        need = sum(1 << s for s in A2(B) + A2(C)) | (1 << Ln('P', E))
        for s in bits(perp):
            if KIND[s] != 'T': continue
            pair = tuple(sorted(x for x in SUPP[s] if x not in X))
            if len(pair) == 2 and sum(splits(nj, X, pair) for nj in nodes_of[X]) == 1: need |= 1 << s
        assert need & ~perp == 0
        r = rank(need); cnt[(r, pc(need))] += 1
        if r < rank(perp): bad.append((ni, X, r))
print('perp rank', rank(perp), '| (rank, #lines) of the n0-only set over all (node, user):', dict(cnt))
print('pairs with rank < perp rank (release possible in principle):', len(bad), bad[:10])
