"""Z15-invariant D4-FRAME GRAPHS: every line a picks one D4 frame F_a ∋ a; adjacency a~b iff b ∈ F_a; must be
symmetric.  MAXSAME bounds the number of lines whose 3 neighbours all pick the same frame (partition-like).
For each graph: free-top doubly forced sets / k_C (kfree), saved as fgd4_<seed>_<k>.json (adjacency)."""
import sys, json, pickle, random, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V
perm = json.load(open('../sec4/coxeter.json'))['perm']
def act(m):
    r = 0
    for s in e8.bits(m): r |= 1 << perm[s]
    return r
frames = pickle.load(open('d4frames.pkl', 'rb'))
fr_of = {a: [F for F in frames if F >> a & 1] for a in range(V)}
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
seed = int(sys.argv[1]); n = int(sys.argv[2]); MAXSAME = int(sys.argv[3]); random.seed(seed)
M = cp_model.CpModel()
Y = {(a, F): M.NewBoolVar('') for a in range(V) for F in fr_of[a]}
for a in range(V):
    M.AddExactlyOne([Y[(a, F)] for F in fr_of[a]])
    for F in fr_of[a]: M.Add(Y[(a, F)] == Y[(perm[a], act(F))])
X = {}
for a in range(V):
    for b in e8.ORTH[a]:
        X[(a, b)] = sum(Y[(a, F)] for F in fr_of[a] if F >> b & 1)
for a in range(V):
    for b in e8.ORTH[a]:
        if a < b: M.Add(X[(a, b)] == X[(b, a)])
same = []
for a in range(V):
    for F in fr_of[a]:
        z = M.NewBoolVar('')
        others = [b for b in e8.bits(F) if b != a]
        M.AddBoolOr([Y[(a, F)].Not()] + [Y[(b, F)].Not() for b in others] + [z])
        same.append(z)
M.Add(sum(same) <= MAXSAME)
for k in range(n):
    M.Maximize(sum(random.randint(0, 100) * v for v in Y.values()))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 120; sol.parameters.num_workers = 4
    sol.parameters.random_seed = seed * 100 + k
    r = sol.Solve(M)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('no graph', sol.StatusName(r), flush=True); break
    Fa = {a: next(F for F in fr_of[a] if sol.Value(Y[(a, F)])) for a in range(V)}
    adj = [[b for b in e8.bits(Fa[a]) if b != a] for a in range(V)]
    nsame = sum(1 for a in range(V) if all(Fa[b] == Fa[a] for b in adj[a]))
    res = kfree(adj)
    hT = collections.Counter(x for x, y in res); hk = collections.Counter(y for x, y in res)
    free0 = sum(1 for x, y in res if y == 0)
    ks = sorted(y for x, y in res if y > 0); pool = 120; cnt = 0
    for kk in ks:
        if pool >= kk: pool -= kk; cnt += 1
    print('graph', k, 'partition-like lines', nsame, '|T_C|', dict(hT), 'k_C', dict(hk), '=> sum j_C >=', 180 - free0 - cnt, flush=True)
    json.dump(adj, open('fgd4_%d_%d.json' % (seed, k), 'w'))
