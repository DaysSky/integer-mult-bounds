"""Generalized stage-0 routing for the 4-plane design with R = 360 (480 registers, 4 per line), Z15-canonical variables.
Registers start at lines (4 each) and flow through cells (design planes), multi-section nodes (flats of rank 3..5 that
lie in the perp of >= 2 design sections; nested node->node edges allowed) into sections (exactly |Q| arrivals each).
Edges: line->cell, line->node, line->section, cell->node, cell->section, node->node (strict containment), node->section.
Reachability av(s, N): line s's content can be present at N.  Coverage: for every rep target t and s in R(t)
(optionally excluding t's complement block, which an in-chain block-total read can supply), av(s, Q) for some Q ∋ t.
argv: tl  exclude_comp(0/1)  [maxnodes_rank]"""
import sys, pickle
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); excl = int(sys.argv[2])
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
flats = pickle.load(open('flats.pkl', 'rb'))
nodes = [F for F, r, c, s in flats if len(s) >= 2]
nodeset = set(nodes)
Qperp = {Q: perpmask(Q) for Q in planes}
secs_of = {F: [Q for Q in planes if F & ~Qperp[Q] == 0] for F in nodes}
print('nodes', len(nodes), flush=True)
nodes_by_line = collections.defaultdict(list)
for G in nodes:
    for s in e8.bits(G): nodes_by_line[s].append(G)
cells_in_rev = collections.defaultdict(list)
for F, r, c, s in flats:
    if len(s) >= 2:
        for P in c: cells_in_rev[P].append(F)
def g(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else (k, act(v))
def canon(tup):
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel()
fv = {}; uv = {}
def edge(a, b):
    c = canon((a, b))
    if c not in fv:
        fv[c] = M.NewIntVar(0, 12, ''); uv[c] = M.NewBoolVar('')
        M.Add(fv[c] >= 1).OnlyEnforceIf(uv[c]); M.Add(fv[c] == 0).OnlyEnforceIf(uv[c].Not())
    return c
avv = {}
def av(s, N):
    c = canon((('L', s), N))
    if c not in avv: avv[c] = M.NewBoolVar('')
    return avv[c]
# adjacency
ins = collections.defaultdict(list); outs = collections.defaultdict(list)
def add(a, b):
    ins[b].append(a); outs[a].append(b)
for s in range(V):
    for P in planes:
        if P >> s & 1: add(('L', s), ('C', P))
    for G in nodes_by_line[s]: add(('L', s), ('G', G))
    for Q in planes:
        if Qperp[Q] >> s & 1: add(('L', s), ('S', Q))
for P in planes:
    for G in cells_in_rev[P]: add(('C', P), ('G', G))
    for Q in planes:
        if P & ~Qperp[Q] == 0: add(('C', P), ('S', Q))
bylen = sorted(nodes, key=lambda F: e8.dim(F))
rk = {F: e8.dim(F) for F in nodes}
nidx = {G: i for i, G in enumerate(nodes)}
byline = [0] * V
for i, G in enumerate(nodes):
    for s in e8.bits(G): byline[s] |= 1 << i
for G1 in nodes:
    m = (1 << len(nodes)) - 1
    for s in e8.bits(G1): m &= byline[s]
    while m:
        b = m & -m; i = b.bit_length() - 1; m ^= b
        G2 = nodes[i]
        if G2 != G1 and rk[G1] < rk[G2]: add(('G', G1), ('G', G2))
    for Q in secs_of[G1]: add(('G', G1), ('S', Q))
print('edges', sum(len(v) for v in outs.values()), flush=True)
def orbit_reps(objs):
    seen = set(); reps_ = []
    for o in objs:
        c = canon((o,))
        if c in seen: continue
        seen.add(c); reps_.append(o)
    return reps_
Lr = orbit_reps([('L', s) for s in range(V)]); Cr = orbit_reps([('C', P) for P in planes])
Gr = orbit_reps([('G', G) for G in nodes]); Sr = orbit_reps([('S', Q) for Q in planes])
for o in Lr: M.Add(sum(fv[edge(o, b)] for b in outs[o]) == 4)
for o in Cr + Gr: M.Add(sum(fv[edge(a, o)] for a in ins[o]) == sum(fv[edge(o, b)] for b in outs[o]))
for o in Sr: M.Add(sum(fv[edge(a, o)] for a in ins[o]) == pc(o[1]))
# reachability, for every rep of (line, node/section) pairs
aux = 0
done = set()
for o in Cr + Gr + Sr:
    N = o
    lines = e8.bits(N[1]) if N[0] != 'S' else e8.bits(Qperp[N[1]])
    for s in lines:
        c = canon((('L', s), N))
        if c in done: continue
        done.add(c)
        terms = []
        for a in ins[N]:
            e = edge(a, N)
            if a == ('L', s): terms.append(uv[e])
            elif a[0] != 'L' and ((a[0] == 'C' and a[1] >> s & 1) or (a[0] == 'G' and a[1] >> s & 1)):
                x = M.NewBoolVar(''); aux += 1
                M.AddImplication(x, uv[e]); M.AddImplication(x, av(s, a)); terms.append(x)
        M.AddBoolOr(terms + [av(s, N).Not()])
print('aux', aux, 'avail', len(avv), 'edge vars', len(fv), flush=True)
cov = []
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    for s in e8.bits(e8.HYP[t]):
        if excl and blk[s] == comp[blk[t]]: continue
        c = M.NewBoolVar(''); cov.append(c)
        M.AddBoolOr([av(s, ('S', Q)) for Q in mine]).OnlyEnforceIf(c)
M.Maximize(sum(cov))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r), 'covered', sum(sol.Value(c) for c in cov) if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
      'of', len(cov), 'bound', sol.BestObjectiveBound(), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    used = [(str(k), sol.Value(fv[k])) for k in fv if sol.Value(fv[k])]
    json.dump(used, open('route3_ex%d.json' % excl, 'w'))
