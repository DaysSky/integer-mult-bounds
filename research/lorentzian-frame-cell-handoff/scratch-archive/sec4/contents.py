"""Stage 1: given design.json (planes) and routing.json (cell->quad Y edges, quad->section Z edges), solve for the
Z15-equivariant contents with CP-SAT:
  cell outputs c[P,W] in F2^P (basis per cell), quad mixing mu[W,Q,P] (invertible per quad: unit lower triangular
  in a fixed order, or checked afterwards), section mixing lam[t,Q,W] (invertible per section), and the target
  equations  sum_{Q∋t} sum_{W->Q} lam[t,Q,W] sum_{P->W} mu[W,Q,P] c[P,W][s] = 1  for every s in R(t)."""
import sys, json, itertools, collections
from common import *
from ortools.sat.python import cp_model
rt = json.load(open('routing.json'))
Y = [(int(P, 16), int(W, 16)) for P, W in rt['Y']]
Z = [(int(W, 16), int(Q, 16)) for W, Q in rt['Z']]
ins = collections.defaultdict(list); outs = collections.defaultdict(list); feed = collections.defaultdict(list)
cell_out = collections.defaultdict(list)
for P, W in Y: ins[W].append(P); cell_out[P].append(W)
for W, Q in Z: outs[W].append(Q); feed[Q].append(W)
for W in ins: assert len(ins[W]) == len(outs[W]), 'quad imbalance'
def rot(x, k):
    for _ in range(k):
        x = act(x) if isinstance(x, int) and x >= 256 or (isinstance(x, int) and pc(x) > 1) else x
    return x
def g(obj):   # act on a tagged object
    kind, val = obj
    if kind == 'line': return (kind, perm[val])
    return (kind, act(val))
def canon(tup):
    best = None; cur = tup
    for k in range(15):
        if best is None or cur < best: best = cur
        cur = tuple(g(o) for o in cur)
    return best
M = cp_model.CpModel()
vars_ = {}
def var(tup):
    c = canon(tup)
    if c not in vars_: vars_[c] = M.NewBoolVar(str(len(vars_)))
    return vars_[c]
def cbit(P, W, s): return var((('cell', P), ('quad', W), ('line', s)))
def mu(W, Q, P): return var((('quad', W), ('sec', Q), ('cell', P)))
def lam(t, Q, W): return var((('line', t), ('sec', Q), ('quad', W)))
# cell bases
done = set()
for P, Ws in cell_out.items():
    key = canon((('cell', P),))
    if key in done: continue
    done.add(key)
    lines = e8.bits(P)
    vecs = [[cbit(P, W, s) for s in lines] for W in Ws]
    n = len(lines); assert len(Ws) == n
    allowed = []
    for combo in itertools.product(range(1, 2 ** n), repeat=n):
        # independence over F2
        rows = list(combo); r = 0; b = []
        for v in rows:
            for x in b:
                if v ^ x < v: v ^= x
            if v: b.append(v); b.sort(reverse=True); r += 1
        if r == n: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)])
    M.AddAllowedAssignments([x for row in vecs for x in row], allowed)
# section invertibility
done = set()
for Q, Ws in feed.items():
    key = canon((('sec', Q),))
    if key in done: continue
    done.add(key)
    users = e8.bits(Q); n = len(users); assert len(Ws) == n
    allowed = []
    for combo in itertools.product(range(1, 2 ** n), repeat=n):
        rows = list(combo); b = []
        for v in rows:
            for x in b:
                if v ^ x < v: v ^= x
            if v: b.append(v); b.sort(reverse=True)
        if len(b) == n: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)])
    M.AddAllowedAssignments([lam(t, Q, W) for t in users for W in Ws], allowed)
# quad invertibility: unit lower triangular in fixed orders (sufficient)
done = set()
for W in ins:
    key = canon((('quad', W),))
    if key in done: continue
    done.add(key)
    Qs = sorted(outs[W]); Ps = sorted(ins[W])
    for i, Q in enumerate(Qs):
        for j, P in enumerate(Ps):
            if j == i: M.Add(mu(W, Q, P) == 1)
            elif j > i: M.Add(mu(W, Q, P) == 0)
# target equations for representative targets
nterms = 0
for t in reps:
    mine = [Q for Q in feed if Q >> t & 1]
    assert len(mine) == 4, (t, len(mine))
    for s in e8.bits(e8.HYP[t]):
        terms = []
        for Q in mine:
            for W in feed[Q]:
                for P in ins[W]:
                    if not (P >> s & 1): continue
                    a = M.NewBoolVar('')
                    lits = [lam(t, Q, W), mu(W, Q, P), cbit(P, W, s)]
                    M.AddBoolAnd(lits).OnlyEnforceIf(a)
                    M.AddBoolOr([x.Not() for x in lits]).OnlyEnforceIf(a.Not())
                    terms.append(a)
        nterms += len(terms)
        if not terms: print('no path for', t, s); sys.exit(1)
        M.AddBoolXOr(terms + [M.NewConstant(0)] if False else terms)
print('vars', len(vars_), 'product terms', nterms, flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    json.dump({str(k): int(sol.Value(v)) for k, v in vars_.items()}, open('contents.json', 'w'))
