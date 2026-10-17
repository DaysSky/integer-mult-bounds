"""Symmetry group of the 40 Eisenstein lines via order-3 complex reflections."""
import pickle, numpy as np
from fractions import Fraction
from geometry798 import geometry
from sympy.combinatorics import Permutation, PermutationGroup
reps, images, adjacent, pairs, orbits = geometry()
roots = [r for orb in orbits for r in orb]
line_of = {}
for li, orb in enumerate(orbits):
    for r in orb: line_of[tuple(r)] = li
# J as rational matrix: J r = images; build from basis via solving
R = np.array(reps[:8] + [], dtype=float)
# solve J on a basis of Q^8 using roots and their rotations
X = []; Y = []
for orb_i, orb in enumerate(orbits):
    X.append(reps[orb_i]); Y.append(images[orb_i])
X = np.array(X, dtype=float); Y = np.array(Y, dtype=float)
J = np.linalg.lstsq(X, Y, rcond=None)[0].T   # J x = y  => X J^T = Y
assert np.allclose(J @ X.T, Y.T)
gens = []
for li in range(40):
    P = np.array([reps[li], images[li]], dtype=float)  # 2x8 basis of the plane
    G = P @ P.T
    Pi = P.T @ np.linalg.inv(G) @ P   # orthogonal projection onto plane
    Rm = (np.eye(8) - Pi) + J @ Pi
    perm = []
    for li2 in range(40):
        v = Rm @ np.array(reps[li2], dtype=float)
        vr = tuple(int(round(x)) for x in v)
        assert np.allclose(v, vr), 'non-integral'
        perm.append(line_of[vr])
    assert sorted(perm) == list(range(40))
    gens.append(Permutation(perm))
G = PermutationGroup(gens)
print('group order', G.order(), 'transitive', G.is_transitive())
pickle.dump([g.array_form for g in gens], open('eis_gens.pkl', 'wb'))
