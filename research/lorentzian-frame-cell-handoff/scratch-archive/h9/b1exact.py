"""B1 class (k=4 and k=5 lines, scaled model (x; z=1) for k=5): the only support structures with crude weight
8|F4| + 10|F5| >= 125 have |F4| = |F5| = 7 (supp.py).  Enumerate them all (F5 = 5-sets pairwise meeting in 3 or 5,
F4 = 4-sets pairwise even, |T n S| even) and solve the exact line-level max clique with CP-SAT."""
import itertools, numpy as np
from ortools.sat.python import cp_model
P = range(8)
S5 = [frozenset(c) for c in itertools.combinations(P, 5)]
S4 = [frozenset(c) for c in itertools.combinations(P, 4)]
# all F5 families of size 7 (5-sets pairwise |n| odd)
def cliques(items, ok, size):
    out = []
    def rec(cur, rest):
        if len(cur) == size: out.append(list(cur)); return
        for i, x in enumerate(rest):
            if all(ok(x, y) for y in cur): rec(cur + [x], rest[i + 1:])
    rec([], items); return out
F5s = cliques(S5, lambda a, b: len(a & b) % 2 == 1, 7)
print('F5 families of size 7:', len(F5s))
structs = []
for F5 in F5s:
    cand4 = [t for t in S4 if all(len(t & s) % 2 == 0 for s in F5)]
    for F4 in cliques(cand4, lambda a, b: len(a & b) % 2 == 0, 7):
        structs.append((F4, F5))
print('structures (|F4|,|F5|) = (7,7):', len(structs))
def lines(F4, F5):
    L = [np.array([2 if j == i else 0 for j in P] + [0]) for i in P]
    for T in F4:
        Tl = sorted(T)
        for sg in itertools.product((1, -1), repeat=3):
            x = [0] * 8; x[Tl[0]] = 1
            for j, s in zip(Tl[1:], sg): x[j] = s
            L.append(np.array(x + [0]))
    for S in F5:
        Sl = sorted(S)
        for sg in itertools.product((1, -1), repeat=5):
            x = [0] * 8
            for j, s in zip(Sl, sg): x[j] = s
            L.append(np.array(x + [1]))
    return np.array(L)
best = 0
for si, (F4, F5) in enumerate(structs):
    V = lines(F4, F5); G = V[:, :8] @ V[:, :8].T - np.outer(V[:, 8], V[:, 8])
    assert (np.diag(G) == 4).all()
    n = len(V); m = cp_model.CpModel(); X = [m.NewBoolVar('x%d' % i) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i, j] not in (0, 2, -2): m.AddBoolOr([X[i].Not(), X[j].Not()])
    m.Maximize(sum(X)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 2
    r = s.Solve(m)
    val = int(s.ObjectiveValue()); bd = int(s.BestObjectiveBound())
    best = max(best, bd)
    print('struct %d: lines %d  max clique %d (bound %d, %s)' % (si, n, val, bd, s.StatusName(r)), flush=True)
print('B1 with (7,7) supports: max total lines <=', best)
