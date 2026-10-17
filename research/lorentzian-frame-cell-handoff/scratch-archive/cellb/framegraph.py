"""Random 3-regular FRAME GRAPHS on the E8 lines (closed neighbourhoods = orthogonal 4-frames, symmetric cells), not
necessarily D4 partitions.  For each: count K4 components, (t,u) pairs without a route under the matched frame top,
and bad cells (cell bottleneck screen).  CP-SAT with a random objective."""
import sys, json, random, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V
ORTH = [set(e8.ORTH[a]) for a in range(V)]
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
def analyse(adj):
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    D6s_of = {t: [perp(C) for C in cells_of[t]] for t in range(V)}
    k4 = sum(1 for a in range(V) if all(set(adj[b]) | {b} == set(adj[a]) | {a} for b in adj[a])) // 4
    nor = sum(1 for t in range(V) for u in e8.bits(e8.HYP[t]) if not any(c & ~D == 0 for D in D6s_of[t] for c in cells_of[u]))
    nb = 0
    for C in cells:
        s, e = e8.bits(C); T = []
        for t in range(V):
            if not (e8.HYP[t] >> s & 1 and e8.HYP[t] >> e & 1): continue
            rs = [(D, c) for D in D6s_of[t] for c in cells_of[s] if c & ~D == 0]
            re = [(D, c) for D in D6s_of[t] for c in cells_of[e] if c & ~D == 0]
            if rs and re and all(c == C for _, c in rs) and all(c == C for _, c in re): T.append([D for D, _ in rs])
        if not T: continue
        if not any(all(any(closure(C | (1 << x)) & ~D == 0 for D in Ds) for Ds in T) for x in range(V) if not C >> x & 1): nb += 1
    return len(cells), k4, nor, nb
seed = int(sys.argv[1]); random.seed(seed); n = int(sys.argv[2])
M = cp_model.CpModel(); X = {}
for a in range(V):
    for b in ORTH[a]:
        if a < b: X[(a, b)] = M.NewBoolVar('')
x = lambda a, b: X[(min(a, b), max(a, b))]
for a in range(V):
    M.Add(sum(x(a, b) for b in ORTH[a]) == 3)
    nb_ = sorted(ORTH[a])
    for i, b in enumerate(nb_):
        for c in nb_[i + 1:]:
            if c not in ORTH[b]: M.AddBoolOr([x(a, b).Not(), x(a, c).Not()])
maxk4 = int(sys.argv[3]) if len(sys.argv) > 3 else 30
# limit K4 components: z_a = 1 if a's closed nbhd is a K4 (all 6 edges) -- approximate via triangles: count triangles
tri = []
for a in range(V):
    for b in ORTH[a]:
        if b <= a: continue
        for c in ORTH[a] & ORTH[b]:
            if c <= b: continue
            t = M.NewBoolVar(''); M.AddBoolAnd([x(a, b), x(a, c), x(b, c)]).OnlyEnforceIf(t)
            M.AddBoolOr([x(a, b).Not(), x(a, c).Not(), x(b, c).Not(), t]); tri.append(t)
M.Add(sum(tri) <= 4 * maxk4 + int(sys.argv[4]) if len(sys.argv) > 4 else 4 * maxk4)
for k in range(n):
    M.Maximize(sum(random.randint(0, 100) * v for v in X.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 60; sol.parameters.num_workers = 4
    sol.parameters.random_seed = seed * 100 + k
    r = sol.Solve(M)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no graph', sol.StatusName(r)); break
    adj = [[b for b in ORTH[a] if sol.Value(x(a, b))] for a in range(V)]
    ntri = sum(sol.Value(t) for t in tri)
    print('graph', k, 'triangles', ntri, 'cells, K4 comps, no-route pairs, bad cells:', analyse(adj), flush=True)
