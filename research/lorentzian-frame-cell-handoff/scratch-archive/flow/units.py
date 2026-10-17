"""Root-system units: lines, Gram, F2 fitting decoder via J + B (mod 2) when valid, else SAT minrank."""
import itertools, numpy as np
def roots_D(n):
    R = []
    for i, j in itertools.combinations(range(n), 2):
        for a, b in ((1, 1), (1, -1)):
            r = [0] * n; r[i] = a; r[j] = b; R.append(r)
    return np.array(R)
def roots_E8():
    R = [list(r) for r in roots_D(8)]
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0 and s[0] == 1:
            R.append([x / 2 for x in s])
    return np.array(R)
def roots_E7():
    E = roots_E8(); w = np.ones(8) / 2  # E7 = roots orthogonal to a fixed root
    a = E[0]
    return np.array([r for r in E if abs(r @ a) < 1e-9])
def roots_E6():
    E = roots_E8(); a, b = E[0], None
    for r in E:
        if abs(abs(r @ a) - 1) < 1e-9: b = r; break   # A2 pair
    return np.array([r for r in E if abs(r @ a) < 1e-9 and abs(r @ b) < 1e-9])
def roots_F4():
    R = [list(r) for r in roots_D(4)]
    for i in range(4):
        r = [0] * 4; r[i] = 1; R.append(r)
    for s in itertools.product((1, -1), repeat=4):
        if s[0] == 1: R.append([x / 2 for x in s])
    return np.array(R, dtype=float)
UNITS = {'D4': roots_D(4), 'D5': roots_D(5), 'F4': roots_F4(), 'E6': roots_E6(), 'E7': roots_E7(), 'E8': roots_E8()}
