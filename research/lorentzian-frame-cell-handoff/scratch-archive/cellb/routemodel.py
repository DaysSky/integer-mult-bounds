"""ROUTE-LEVEL LOWER-BOUND MODEL (relaxation of any E8 word whose sources have exactly 3 branches first-mixing at the
R420 cells): each cell C={s,e} has 2 + j_C registers; its output streams (next frame N ⊋ C, WLOG minimal N =
closure(C+x)) carry s+e (at most 1 + j_C of them), s or e.  Target t reads inside its chosen sections (planes ∋ t,
perps); x_u reaches t iff some stream of a cell of u containing u has its node inside a chosen section perp of t, or t
reads that cell in-chain (<= 1 rank-2 read per target).  Registers >= sum_C (2 + j_C) and >= sum_t (#sections - 1).
MODE frame: sections fixed = the 3 frame D6s.  MODE free: each target picks sections among all planes through it,
<= MAXSEC of them.  Z15-canonical.  Objective: minimise sum j_C (frame) / max(cells, arrivals) (free)."""
import sys, json, os, collections, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V; pc = lambda m: bin(m).count('1')
MODE = sys.argv[1]; MAXSEC = int(sys.argv[2]); tl = float(sys.argv[3]); SYM = int(sys.argv[4]) if len(sys.argv) > 4 else 1
perm = json.load(open('../sec4/coxeter.json'))['perm']
def act(m):
    r = 0
    for s in e8.bits(m): r |= 1 << perm[s]
    return r
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
CL = {}
def closure(m):
    if m not in CL: CL[m] = e8.closure(m)[0]
    return CL[m]
if os.environ.get('GRAPH'):
    _adj = json.load(open(os.environ['GRAPH'])); cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in _adj[a]))
else:
    cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
cellset = set(cells)
assert all(act(C) in cellset for C in cells)
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
def g_(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else ((k, act(v)) if k in ('C', 'N', 'S') else o)
def canon(tup):
    if not SYM: return tup
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g_(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel(); VV = {}
def var(tup, ub=None):
    c = canon(tup)
    if c not in VV: VV[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return VV[c]
# nodes per cell
nodes_of = {C: sorted(set(closure(C | (1 << x)) for x in range(V) if not C >> x & 1)) for C in cells}
print('nodes per cell', collections.Counter(len(v) for v in nodes_of.values()), flush=True)
st = lambda C, N, k: var((('C', C), ('N', N), ('k', k)))          # k in 'sum','s','e' (s = lower line)
jC = lambda C: var((('C', C), ('j', 0)), 2)
seen = set(); cell_reps = []
for C in cells:
    c = canon((('C', C),))
    if c in seen: continue
    seen.add(c); cell_reps.append(C)
    ns = nodes_of[C]
    M.Add(sum(st(C, N, 'sum') for N in ns) <= 1 + jC(C))
    M.Add(sum(st(C, N, k) for N in ns for k in ('sum', 's', 'e')) <= 2 + jC(C))
def stream_has(C, N, u):
    s, e = e8.bits(C)
    return [st(C, N, 'sum'), st(C, N, 's' if u == s else 'e')]
# targets
tseen = set(); t_reps = []
for t in range(V):
    c = canon((('L', t),))
    if c in tseen: continue
    tseen.add(c); t_reps.append(t)
planes_t = {}
for t in t_reps:
    ps = set()
    for u in range(V):
        if u != t: ps.add(closure((1 << t) | (1 << u)))
    planes_t[t] = sorted(ps)
frameD6 = {t: [C for C in cells_of[t]] for t in range(V)}   # sections = these cells' perps
arr_terms = []
for t in t_reps:
    if MODE == 'frame':
        secs = [(Q, 1) for Q in frameD6[t]]
    else:
        secs = [(Q, var((('L', t), ('S', Q)))) for Q in planes_t[t]]
        M.Add(sum(b for Q, b in secs) <= MAXSEC); M.Add(sum(b for Q, b in secs) >= 3)
        arr_terms.append(sum(b for Q, b in secs) - 1)
    Sperp = [(perp(Q), b) for Q, b in secs]
    usable = {}
    def use(N):
        if N not in usable:
            lits = [b for P, b in Sperp if N & ~P == 0]
            if not lits: usable[N] = None
            elif any(isinstance(l, int) for l in lits): usable[N] = 1
            else:
                y = M.NewBoolVar(''); M.AddBoolOr([y.Not()] + lits); usable[N] = y
        return usable[N]
    creads = {}
    for C in cells:
        if C & ~e8.HYP[t] == 0: creads[C] = M.NewBoolVar('')
    M.Add(sum(creads.values()) <= 1)
    for u in e8.bits(e8.HYP[t]):
        opts = []
        for C in cells_of[u]:
            if C in creads: opts.append(creads[C])
            for N in nodes_of[C]:
                uN = use(N)
                if uN is None: continue
                for lit in stream_has(C, N, u):
                    if isinstance(uN, int): opts.append(lit)
                    else:
                        z = M.NewBoolVar(''); M.AddImplication(z, uN); M.AddImplication(z, lit); opts.append(z)
        if not opts: print('NO ROUTE possible for', t, u); M.AddBoolOr([])
        else: M.AddBoolOr(opts)
J = sum(jC(C) * len(set(act(C) for _ in [0]) | set()) for C in cell_reps)
# orbit sizes for objective
def orb(m):
    o = {m}; y = act(m)
    while y != m: o.add(y); y = act(y)
    return len(o) if SYM else 1
J = sum(orb(C) * jC(C) for C in cell_reps)
if MODE == 'frame':
    M.Minimize(J)
else:
    A = sum(orb(1 << t) * a for t, a in zip(t_reps, arr_terms))
    Z = M.NewIntVar(0, 2000, ''); M.Add(Z >= 360 + J); M.Add(Z >= A); M.Minimize(Z)
print('built; vars', len(VV), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print(os.environ.get('GRAPH','r420'), MODE, MAXSEC, 'status', sol.StatusName(r), 'obj', sol.ObjectiveValue() if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
      'bound', sol.BestObjectiveBound(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print('sum j_C =', sol.Value(J))
