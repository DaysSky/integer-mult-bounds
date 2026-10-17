"""Per-line pool cover with arbitrary vectors w: rank-2 pools <u,w> with w in S_E for every demand E containing u.
Random intersections of 4-6 demand frames give candidate w; then exact set cover (CP-SAT) over candidates + lines."""
from part13 import *
import numpy as np, random
from fractions import Fraction as Fr
from math import gcd, lcm
from ortools.sat.python import cp_model
random.seed(2)
L = g.L.astype(np.int64); eta = g.eta
dem_u = collections.defaultdict(list)
for k, d in enumerate(DEM):
    for u in bits(d[2]): dem_u[u].append(k)
def perp_constraints(k):
    """S_E as {w : w . eta . y = 0 for y in Y_k}; Y = frame pair (t,e) or the 4 frame lines for Q"""
    kind, S, E, fi, users = DEM[k]
    return list(users) if kind == 'E' else list(part[fi])
W0 = np.array([1]*13 + [-3], dtype=np.int64)   # eta-dual of w0 = sum e + 3f: w.eta.w0 = sum w_i - 3 w_f... use plain constraint rows
def nullspace(rows):
    n = L.shape[1]
    M = [[Fr(int(x)) for x in (L[y] @ eta)] for y in rows] + [[Fr(int(x)) for x in W0]]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; iv = 1 / M[r][c]; M[r] = [x * iv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(n) if c not in piv]
    out = []
    for fc in free:
        v = [Fr(0)] * n; v[fc] = Fr(1)
        for i, pc_ in enumerate(piv): v[pc_] = -M[i][fc]
        out.append(v)
    return out
def contains(k, w):
    return all(int(L[y] @ eta @ w) == 0 for y in perp_constraints(k))
for u in (0, 26, 78, 200):
    Ds = dem_u[u]
    cands = {}
    for trial in range(400):
        sub = random.sample(Ds, random.choice([4, 5, 6]))
        rows = sorted(set(y for k in sub for y in perp_constraints(k)))
        ns = nullspace(rows)
        for b in ns:
            den = 1
            for x in b: den = lcm(den, x.denominator)
            bv = np.array([int(x * den) for x in b], dtype=np.int64)
            if np.linalg.matrix_rank(np.vstack([bv, L[u]])) == 2:
                key = tuple(bv // np.gcd.reduce(bv[bv != 0]) if (bv != 0).any() else bv)
                cands[key] = bv
    cov = {key: frozenset(k for k in Ds if contains(k, w)) for key, w in cands.items()}
    for w in range(V):
        if w != u: cov[('line', w)] = frozenset(k for k in Ds if DEM[k][1] >> w & 1)
    best = max(len(c) for c in cov.values()); bestline = max(len(c) for key, c in cov.items() if key[0] == 'line')
    m = cp_model.CpModel(); x = {key: m.NewBoolVar(str(i)) for i, key in enumerate(cov)}
    for k in Ds: m.AddBoolOr([x[key] for key, c in cov.items() if k in c])
    m.Minimize(sum(x.values())); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 30; s.parameters.num_workers = 4
    s.Solve(m)
    chosen = [key for key in cov if s.Value(x[key])]
    print(g.kind[u], g.supp[u], 'demands', len(Ds), 'cands', len(cands), 'max group (any/line)', best, bestline,
          'cover', int(s.ObjectiveValue()), 'lb', int(s.BestObjectiveBound()), 'chosen kinds', [('L' if k[0] == 'line' else 'v') for k in chosen], flush=True)
