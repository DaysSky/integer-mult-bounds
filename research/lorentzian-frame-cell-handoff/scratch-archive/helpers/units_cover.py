import numpy as np, itertools, sys
sys.path.insert(0, '../smallh')
from cover2 import cover_number
def roots_E8():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for a in (1, -1):
            for b in (1, -1):
                v = [0]*8; v[i] = 2*a; v[j] = 2*b; R.append(v)
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0: R.append(list(s))
    R = np.array(R)
    L = {}
    for r in R:
        k = tuple(r) if tuple(r) > tuple(-r) else tuple(-r); L[k] = 1
    return np.array(list(L))
def subsystem(L, normals):
    return np.array([l for l in L if all(abs(l @ n) < 1e-9 for n in normals)])
def report(name, L, F=None):
    F = np.eye(L.shape[1]) if F is None else F
    G = L @ F @ L.T
    h = np.linalg.matrix_rank(L.astype(float))
    covs = []
    for s in range(len(L)):
        R = [L[t] for t in range(len(L)) if t != s and abs(G[s, t]) < 1e-9]
        # cover inside s^perp: ambient for the test is span(L) dimension h
        covs.append(cover_number(R, h))
    from collections import Counter
    print('%-12s v=%d h=%d readers/source %s cover numbers %s' % (name, len(L), h,
          sorted(set(int(sum(1 for t in range(len(L)) if t != s and abs(G[s, t]) < 1e-9)) for s in range(len(L)))), dict(Counter(covs))), flush=True)
E8 = roots_E8()
report('E8', E8)
E7 = subsystem(E8, [E8[0]]); report('E7', E7)
E6 = subsystem(E8, [E8[0], [l for l in E8 if abs(l @ E8[0] - 4) < 1e-9 or abs(l @ E8[0] + 4) < 1e-9][0]]) if False else None
# D8 roots (integral part of E8): lines with two nonzero coords
D8 = np.array([l for l in E8 if (l != 0).sum() == 2]); report('D8', D8)
