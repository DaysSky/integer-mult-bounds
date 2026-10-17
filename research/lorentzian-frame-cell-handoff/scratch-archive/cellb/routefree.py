"""ROUTE-LEVEL relaxation, UNRESTRICTED top (a target may receive any register whose node lies in t-perp), for any
3-branch frame-cell source system: cell C = {s,a} has 2 + j_C registers; streams go to nodes N = closure(C + x)
(nondegenerate), at most 1 + j_C carry s+a, at most 2 + j_C in total.  x_u reaches t iff a stream of a cell of u
containing u has N ⊂ t-perp, or t reads that cell in-chain (<= 1 rank-2 read per target).  Minimise sum j_C
(exact lower bound on extra cell registers for this class: R >= 2v + sum j_C).  Symmetry-canonical.
usage: routefree.py SYSTEM(e8|lor) GRAPH(json or 'r420') tl"""
import sys, os, json, collections
from ortools.sat.python import cp_model
SYSTEM, GRAPH, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
if SYSTEM == 'e8':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    V = e8.V; HYP = e8.HYP; bits = e8.bits
    perm = json.load(open('../sec4/coxeter.json'))['perm']
    P = [list(range(V))]; q = perm
    while q != list(range(V)): P.append(q); q = [perm[i] for i in q]
    PERMS = P
    clos = lambda m: e8.closure(m)[0]; nondeg = lambda m: True
    if GRAPH == 'r420': cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
    else:
        adj = json.load(open(GRAPH)); cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
else:
    sys.path.insert(0, '../lcell'); os.environ.setdefault('GRP', '55')
    from lbase import V, HYP, bits, PERMS, nondeg_span, closure as clos
    nondeg = nondeg_span
    Fa = {int(k): v for k, v in json.load(open(GRAPH)).items()}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(Fa[a]) if b != a))
def actp(m, p):
    r = 0
    for s in bits(m): r |= 1 << p[s]
    return r
def canon_tup(tup):
    best = None
    for p in PERMS:
        c = tuple((k, p[v]) if k == 'L' else ((k, actp(v, p)) if k in ('C', 'N') else (k, v)) for k, v in tup)
        if best is None or c < best: best = c
    return best
cellset = set(cells); assert all(actp(C, p) in cellset for C in cells for p in PERMS)
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
CL = {}
def closure(m):
    if m not in CL: CL[m] = clos(m)
    return CL[m]
nodes_of = {}
for C in cells:
    ns = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        if nondeg(N): ns.add(N)
    nodes_of[C] = sorted(ns)
M = cp_model.CpModel(); VV = {}
def var(tup, ub=None):
    c = canon_tup(tup)
    if c not in VV: VV[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return VV[c]
st = lambda C, N, k: var((('C', C), ('N', N), ('k', k)))
jC = lambda C: var((('C', C), ('j', 0)), 3)
seen = set(); reps = []
for C in cells:
    c = canon_tup((('C', C),))
    if c in seen: continue
    seen.add(c); reps.append(C)
    ns = nodes_of[C]
    M.Add(sum(st(C, N, 'sum') for N in ns) <= 1 + jC(C))
    M.Add(sum(st(C, N, k) for N in ns for k in ('sum', 'lo', 'hi')) <= 2 + jC(C))
tseen = set(); treps = []
for t in range(V):
    c = canon_tup((('L', t),))
    if c in tseen: continue
    tseen.add(c); treps.append(t)
for t in treps:
    cr = {C: M.NewBoolVar('') for C in cells if C & ~HYP[t] == 0}
    M.Add(sum(cr.values()) <= 1)
    for u in bits(HYP[t]):
        opts = []
        for C in cells_of[u]:
            if C in cr: opts.append(cr[C])
            lo = min(bits(C))
            for N in nodes_of[C]:
                if N & ~HYP[t] == 0:
                    opts += [st(C, N, 'sum'), st(C, N, 'lo' if u == lo else 'hi')]
        M.AddBoolOr(opts)
def orb(C): return len(set(actp(C, p) for p in PERMS))
J = sum(orb(C) * jC(C) for C in reps)
M.Minimize(J)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 2
r = sol.Solve(M)
print(SYSTEM, GRAPH, 'cells', len(cells), 'reps', len(reps), 'status', sol.StatusName(r), 'min sum j_C',
      sol.ObjectiveValue() if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sol.BestObjectiveBound(), flush=True)
