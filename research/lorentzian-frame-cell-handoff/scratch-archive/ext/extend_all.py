"""All primitive lines compatible with I_{n,1} (two-value vectors, |entries| <= B), pairwise compatibility among them,
max cliques (CP-SAT), and exact decoder cost of I_{n,1} + clique (matroid greedy over codewords)."""
import itertools, sys, numpy as np
from math import gcd
from functools import reduce
from ortools.sat.python import cp_model
n = int(sys.argv[1]); Bd = int(sys.argv[2]) if len(sys.argv) > 2 else 9
base = []
for i, j in itertools.combinations(range(n), 2):
    x = [0]*(n+1); x[i], x[j] = 1, -1; base.append(x)
for t in itertools.combinations(range(n), 3):
    x = [0]*(n+1)
    for i in t: x[i] = 1
    x[n] = 1; base.append(x)
base = np.array(base); eta = np.array([1]*n + [-1])
ext = set()
for a in range(-Bd, Bd+1):
    for b in range(-Bd, Bd+1):
        for k in range(0, n+1):
            if k not in (0, n) and (a - b) % 2 == 0: continue
            if k in (0, n) and a != b: continue
            s = k*a + (n-k)*b
            if s % 3: continue
            y = s // 3
            proto = [a]*k + [b]*(n-k) + [y]
            if reduce(gcd, [abs(t) for t in proto]) != 1: continue
            v0 = np.array(proto); N = int((v0*v0*eta).sum())
            if N == 0 or N % 2: continue
            g = (base*eta) @ v0
            if not (((g % 2) == 1) | (g == 0)).all(): continue
            for A in itertools.combinations(range(n), k):
                x = [b]*n
                for i in A: x[i] = a
                v = tuple(x) + (y,); nv = tuple(-t for t in v); ext.add(max(v, nv))
E = np.array(sorted(ext)); m = len(E)
from collections import Counter
print('n', n, 'base', len(base), 'extras', m, 'norms', dict(Counter((E*E*eta).sum(1).tolist())))
if m == 0: sys.exit()
GE = (E*eta) @ E.T
comp = ((GE % 2) == 1) | (GE == 0); np.fill_diagonal(comp, True)
md = cp_model.CpModel(); xs = [md.NewBoolVar('x%d' % i) for i in range(m)]
for i in range(m):
    for j in range(i+1, m):
        if not comp[i, j]: md.AddBoolOr([xs[i].Not(), xs[j].Not()])
md.Maximize(sum(xs)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 4
st = sv.Solve(md)
sel = [i for i in range(m) if sv.Value(xs[i])]
print('max compatible extras:', len(sel), sv.StatusName(st), 'norms', dict(Counter((E[sel]*E[sel]*eta).sum(1).tolist())))
np.save('ext_n%d.npy' % n, np.vstack([base, E[sel]]))
