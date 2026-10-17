"""Free-top cell bottleneck for frame graphs that are NOT D4 partitions: generate Z15-invariant 3-regular frame graphs
(closed neighbourhoods = orthogonal 4-frames) with a bounded number of triangles, then per cell C: doubly forced
targets T_C (t ⊥ s,e; no other cell of s or of e inside t-perp) and k_C.  Counting bound: cells with j_C = 0 need k_C
distinct cell readers (<= 120 in total) -> sum j_C >= 180 - (max #cells coverable)."""
import sys, json, random, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V
ORTH = [set(e8.ORTH[a]) for a in range(V)]
perm = json.load(open('../sec4/coxeter.json'))['perm']
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
def kfree(adj):
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
    cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
    out = []
    for C in cells:
        s, e = e8.bits(C)
        T = [t for t in range(V) if C & ~e8.HYP[t] == 0
             and not any(c != C and c & ~e8.HYP[t] == 0 for c in cells_of[s] + cells_of[e])]
        best = 0
        for x in range(V):
            if C >> x & 1: continue
            N = closure(C | (1 << x))
            best = max(best, sum(1 for t in T if N & ~e8.HYP[t] == 0))
        out.append((len(T), len(T) - best))
    return out
seed = int(sys.argv[1]); maxtri = int(sys.argv[2]); n = int(sys.argv[3]); random.seed(seed)
M = cp_model.CpModel(); X = {}
def key(a, b): return (min(a, b), max(a, b))
for a in range(V):
    for b in ORTH[a]:
        if a < b: X[(a, b)] = M.NewBoolVar('')
x = lambda a, b: X[key(a, b)]
for (a, b), v in X.items():           # Z15 invariance
    M.Add(v == x(perm[a], perm[b]))
for a in range(V):
    M.Add(sum(x(a, b) for b in ORTH[a]) == 3)
    nb_ = sorted(ORTH[a])
    for i, b in enumerate(nb_):
        for c in nb_[i + 1:]:
            if c not in ORTH[b]: M.AddBoolOr([x(a, b).Not(), x(a, c).Not()])
tri = []
for a in range(V):
    for b in ORTH[a]:
        if b <= a: continue
        for c in ORTH[a] & ORTH[b]:
            if c <= b: continue
            t = M.NewBoolVar(''); M.AddBoolOr([x(a, b).Not(), x(a, c).Not(), x(b, c).Not(), t]); tri.append(t)
M.Add(sum(tri) <= maxtri)
for k in range(n):
    M.Maximize(sum(random.randint(0, 100) * v for v in X.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 120; sol.parameters.num_workers = 4
    sol.parameters.random_seed = seed * 100 + k
    r = sol.Solve(M)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no graph', sol.StatusName(r)); break
    adj = [[b for b in ORTH[a] if sol.Value(x(a, b))] for a in range(V)]
    res = kfree(adj)
    hT = collections.Counter(a for a, b in res); hk = collections.Counter(b for a, b in res)
    # greedy upper bound on # j=0 cells: cells with k_C = 0 are free; others need k_C readers from a pool of 120
    free0 = sum(1 for a, b in res if b == 0)
    ks = sorted(b for a, b in res if b > 0); pool = 120; cnt = 0
    for kk in ks:
        if pool >= kk: pool -= kk; cnt += 1
    print('graph', k, 'triangles', sum(sol.Value(t) for t in tri), '|T_C|', dict(hT), 'k_C', dict(hk),
          ' max j=0 cells <=', free0 + cnt, ' => sum j_C >=', 180 - free0 - cnt, flush=True)
    json.dump(adj, open('fg_%d_%d_%d.json' % (seed, maxtri, k), 'w'))
