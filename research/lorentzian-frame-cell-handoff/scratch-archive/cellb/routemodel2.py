"""ROUTE-LEVEL LOWER-BOUND MODEL, FREE TOP (relaxation for any E8 word whose sources have exactly 3 branches
first-mixing at the R420 cells, with ANY top): target t chooses delivered registers, each with a last frame P = a
rank-6 closed flat inside t-perp (cost 1 register each; WLOG maximal), plus at most one in-chain plane-perp section
(cost 0) and at most one in-chain cell read.  x_u reaches t iff a stream of a cell of u containing u has its node
inside a chosen P or the in-chain section, or t reads that cell.  Cells: 2 + j_C registers, <= 1 + j_C sum-streams.
Registers >= 360 + sum j_C and >= total delivered.  Minimise Z = max of the two.  Z15-canonical (SYM=1) or none."""
import sys, json, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
from ortools.sat.python import cp_model
V = e8.V; pc = lambda m: bin(m).count('1')
tl = float(sys.argv[1]); SYM = int(sys.argv[2]); MAXDEL = int(sys.argv[3]) if len(sys.argv) > 3 else 3
perm = json.load(open('../sec4/coxeter.json'))['perm']
def actp(m, p):
    r = 0
    for s in e8.bits(m): r |= 1 << p[s]
    return r
act = lambda m: actp(m, perm)
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
L = np.array(e8.LINES, dtype=np.int64); n2 = int(L[0] @ L[0])
line_of = {}
for i, x in enumerate(L): line_of[tuple(x)] = i; line_of[tuple(-x)] = i
RP = [[line_of[tuple(L[i] - 2 * (L[i] @ L[r]) * L[r] // n2)] for i in range(V)] for r in range(V)]
# Weyl elements mapping line 0 to every line (BFS over reflections)
to = {0: list(range(V))}; frontier = [0]
while frontier:
    nf = []
    for a in frontier:
        for r in range(V):
            b = RP[r][a]
            if b not in to:
                to[b] = [RP[r][to[a][i]] for i in range(V)]; nf.append(b)
    frontier = nf
assert len(to) == V and all(to[b][0] == b for b in to)
F0 = pickle.load(open('flats6_t0.pkl', 'rb'))
if len(sys.argv) > 4:
    adj = json.load(open(sys.argv[4]))
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
else:
    cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
assert len(cells) == 180 and all(act(C) in set(cells) for C in cells)
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def g_(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else ((k, act(v)) if k in ('C', 'N', 'P', 'Q') else o)
def canon(tup):
    if not SYM: return tup
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g_(o) for o in cur)
        if cur < best: best = cur
    return best
def orb(m):
    if not SYM: return 1
    o = {m}; y = act(m)
    while y != m: o.add(y); y = act(y)
    return len(o)
M = cp_model.CpModel(); VV = {}
def var(tup, ub=None):
    c = canon(tup)
    if c not in VV: VV[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return VV[c]
nodes_of = {C: sorted(set(closure(C | (1 << x)) for x in range(V) if not C >> x & 1)) for C in cells}
st = lambda C, N, k: var((('C', C), ('N', N), ('k', k)))
jC = lambda C: var((('C', C), ('j', 0)), 2)
seen = set(); cell_reps = []
for C in cells:
    c = canon((('C', C),))
    if c in seen: continue
    seen.add(c); cell_reps.append(C)
    ns = nodes_of[C]
    M.Add(sum(st(C, N, 'sum') for N in ns) <= 1 + jC(C))
    M.Add(sum(st(C, N, k) for N in ns for k in ('sum', 's', 'e')) <= 2 + jC(C))
tseen = set(); t_reps = []
for t in range(V):
    c = canon((('L', t),))
    if c in tseen: continue
    tseen.add(c); t_reps.append(t)
arr = []
for t in t_reps:
    g = to[t]
    Ps = [actp(F, g) for F in F0]
    assert all(P & ~e8.HYP[t] == 0 for P in Ps)
    dvars = [(P, var((('L', t), ('P', P)))) for P in Ps]
    M.Add(sum(b for P, b in dvars) <= MAXDEL)
    arr.append(orb(1 << t) * sum(b for P, b in dvars))
    Qs = sorted(set(closure((1 << t) | (1 << u)) for u in range(V) if u != t))
    ivars = [(perp(Q), var((('L', t), ('Q', Q)))) for Q in Qs]
    M.Add(sum(b for P, b in ivars) <= 1)
    allv = dvars + ivars
    usable = {}
    def use(N):
        if N not in usable:
            lits = [b for P, b in allv if N & ~P == 0]
            if not lits: usable[N] = None
            else:
                y = M.NewBoolVar(''); M.AddBoolOr([y.Not()] + lits); usable[N] = y
        return usable[N]
    creads = {C: M.NewBoolVar('') for C in cells if C & ~e8.HYP[t] == 0}
    M.Add(sum(creads.values()) <= 1)
    for u in e8.bits(e8.HYP[t]):
        opts = []
        s_e = None
        for C in cells_of[u]:
            if C in creads: opts.append(creads[C])
            s, e = e8.bits(C)
            for N in nodes_of[C]:
                uN = use(N)
                if uN is None: continue
                for lit in (st(C, N, 'sum'), st(C, N, 's' if u == s else 'e')):
                    z = M.NewBoolVar(''); M.AddImplication(z, uN); M.AddImplication(z, lit); opts.append(z)
        M.AddBoolOr(opts)
J = sum(orb(C) * jC(C) for C in cell_reps)
Z = M.NewIntVar(0, 3000, ''); M.Add(Z >= 360 + J); M.Add(Z >= sum(arr)); M.Minimize(Z)
print('built; vars', len(VV), 'targets', len(t_reps), 'flats per target', len(F0), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
ok = r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
print('free top cells', sys.argv[4] if len(sys.argv) > 4 else 'r420', 'MAXDEL', MAXDEL, 'SYM', SYM, 'status', sol.StatusName(r), 'Z', sol.ObjectiveValue() if ok else None,
      'bound', sol.BestObjectiveBound(), flush=True)
if ok: print('sum j_C', sol.Value(J), 'delivered', sol.Value(sum(arr)))
