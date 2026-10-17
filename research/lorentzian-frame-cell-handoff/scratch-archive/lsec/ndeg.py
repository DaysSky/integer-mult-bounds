"""Nondegeneracy of candidate frames for an I_{11,1} design: sections Q-perp, nodes (Q+Q')-perp: exact rational Gram det
of a basis of span(Q ∪ Q') (perp of a nondegenerate subspace inside the nondegenerate w-perp is nondegenerate)."""
import sys, json
from fractions import Fraction as Fr
from lcommon import *
import numpy as np
DES = sys.argv[1]
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
L = g.L; eta = g.eta
def basis(idx):
    B = []
    for i in idx:
        if np.linalg.matrix_rank(g.LA[B + [i]]) > len(B): B.append(i)
    return B
def det_exact(M):
    M = [[Fr(int(x)) for x in r] for r in M]; n = len(M); d = Fr(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]; M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return d
st = collections.Counter(); seen = {}
reps = []; s_ = set()
for Q in planes:
    c = canon_mask(Q)
    if c not in s_: s_.add(c); reps.append(Q)
for Q in reps:
    for Q2 in planes:
        if Q2 == Q: continue
        B = basis(bits(Q | Q2))
        key = tuple(sorted(B))
        Gm = [[int(G[a, b]) for b in B] for a in B]
        d = det_exact(Gm)
        X = perpmask(Q) & perpmask(Q2)
        st[(len(B), 'deg' if d == 0 else 'nondeg', 'X nonempty' if X else 'X empty')] += 1
for k, n in sorted(st.items()): print(k, n)
