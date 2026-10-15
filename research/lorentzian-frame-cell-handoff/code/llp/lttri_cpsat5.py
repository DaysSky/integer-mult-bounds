"""CP-SAT for the M11 triangle top's node waste.  Per T line: one in-chain node (its own A2 is taken there: delta = 1
at the in-chain node, 0 elsewhere); for every triple-crossing pair and every a in the line, which of the 3 crossing
nodes delivers T(a,pair) (single-crossing pairs are forced).  A node is ZERO-WASTE only if it has no in-chain user
and the XOR of its three transversal sets lies in the zero set of a nonzero additive g (hyperplane through P(E));
candidate zero sets: the maximal ones (lttri_local2 enumeration) containing the node's forced-odd transversals.
Minimise #non-zero-waste nodes (each costs >= 1 extra register; in-chain nodes cost >= 1 by the identity-hosting
argument).  Lower bound 83 from in-chain hosting.  usage: lttri_cpsat.py R timelimit"""
import sys, json, itertools, collections, time
import numpy as np
from ortools.sat.python import cp_model
R = int(sys.argv[1]); TL = float(sys.argv[2]); t0 = time.time()
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def cross_nodes(X, pair):
    out = []
    for nj in nodes_of[X]:
        B, C = [T for T in sol[nj] if T != X]
        if (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B): out.append(nj)
    return out
idx = [(i, j, k) for i in range(3) for j in range(3) for k in range(3)]
rng = range(-R, R + 1); zs = set()
for a1, a2 in itertools.product(rng, rng):
    al = (0, a1, a2)
    for b1, b2 in itertools.product(rng, rng):
        be = (0, b1, b2)
        for g in itertools.product(range(-2 * R, 2 * R + 1), repeat=3):
            m = 0; allz = True
            for bit, (i, j, k) in enumerate(idx):
                if al[i] + be[j] + g[k] == 0: m |= 1 << bit
                else: allz = False
            if not allz: zs.add(m)
zs = sorted(zs, key=lambda m: -bin(m).count('1')); maxi = []
for m in zs:
    if not any(m & ~q == 0 for q in maxi): maxi.append(m)
print('[%4.0fs] maximal zero sets %d' % (time.time() - t0, len(maxi)), flush=True)
M = cp_model.CpModel()
inch = {}
for X in nodes_of:
    ls = [M.NewBoolVar('') for _ in nodes_of[X]]; M.AddExactlyOne(ls)
    for n, l in zip(nodes_of[X], ls): inch[(X, n)] = l
choice = {}   # (X, pair, x) -> {node: bool}
def member(X, ni, pts):
    """literal / constant for 'user X takes transversal pts (a point in each block) at node ni'"""
    pair = tuple(sorted(p for p in pts if p not in X)); x = [p for p in pts if p in X][0]
    cn = cross_nodes(X, pair)
    if len(cn) == 1: return 1
    key = (X, pair, x)
    if key not in choice:
        vs = {n: M.NewBoolVar('') for n in cn}; M.AddExactlyOne(list(vs.values())); choice[key] = vs
    return choice[key][ni]
zero = []
for ni, (A, B, C) in enumerate(sol):
    users = (A, B, C)
    mem = {}   # (user index, bit) -> 1 or literal
    for bit, (i, j, k) in enumerate(idx):
        pts = (A[i], B[j], C[k])
        for u, X in enumerate(users): mem[(u, bit)] = member(X, ni, pts)
    def eq(x, y, enf):
        """membership x == y under enforcement literal enf"""
        if isinstance(x, int) and isinstance(y, int):
            if x != y: M.AddBoolOr([enf.Not()])
            return
        if isinstance(x, int): x, y = y, x
        if isinstance(y, int): M.Add(x == y).OnlyEnforceIf(enf)
        else: M.Add(x == y).OnlyEnforceIf(enf)
    zn = M.NewBoolVar(''); zero.append(zn)
    for X in users: M.AddImplication(zn, inch[(X, ni)].Not())
    # (i) XOR of the three transversal sets empty: each tau has even membership count
    for bit in range(27):
        lits = [mem[(u, bit)] for u in range(3)]
        const = sum(1 for v in lits if isinstance(v, int)); vs = [v for v in lits if not isinstance(v, int)]
        if not vs:
            if const % 2: M.AddBoolOr([zn.Not()])
            continue
        kk = M.NewIntVar(0, 2, ''); M.Add(sum(vs) + const == 2 * kk).OnlyEnforceIf(zn)
    # (ii)/(iii) pivot user p: P_p + P_q inside A2s + one slice in the third block r, for both q != p
    opts = []
    for p in range(3):
        o = M.NewBoolVar(''); opts.append(o)
        for q in range(3):
            if q == p: continue
            r = 3 - p - q
            sl = [M.NewBoolVar('') for _ in range(3)]; M.AddExactlyOne(sl + [o.Not()]) if False else M.Add(sum(sl) == 1).OnlyEnforceIf(o)
            for v in range(3):
                for bit, ijk in enumerate(idx):
                    if ijk[r] == v: continue
                    both = M.NewBoolVar(''); M.AddBoolAnd([o, sl[v]]).OnlyEnforceIf(both); M.AddBoolOr([o.Not(), sl[v].Not(), both])
                    eq(mem[(p, bit)], mem[(q, bit)], both)
    M.Add(sum(opts) >= 1).OnlyEnforceIf(zn)
print('[%4.0fs] model built; choice vars %d' % (time.time() - t0, len(choice)), flush=True)
# faithful costs (waste = m - d): c = #in-chain users at the node, hp = hyperplane condition
#   c = 0: 1 - hp ;  c = 1: 2 - hp ;  c >= 2: 2 (identical-parts case with cost 1 ignored: optimistic only for c = 2)
costs = []
for ni, node in enumerate(sol):
    c = sum(inch[(X, ni)] for X in node)
    c0 = M.NewBoolVar(''); c1 = M.NewBoolVar(''); c2 = M.NewBoolVar('')
    M.AddExactlyOne([c0, c1, c2])
    M.Add(c == 0).OnlyEnforceIf(c0); M.Add(c == 1).OnlyEnforceIf(c1); M.Add(c >= 2).OnlyEnforceIf(c2)
    w = M.NewIntVar(0, 2, '')
    M.Add(w >= 1 - zero[ni]); M.Add(w >= 2 - zero[ni]).OnlyEnforceIf(c1); M.Add(w >= 2).OnlyEnforceIf(c2)
    costs.append(w)
M.Minimize(sum(costs))
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        print('[%4.0fs] node waste (RHO5 sufficient model) %d  bound %d  aligned nodes %d' % (time.time() - t0, self.ObjectiveValue(), self.BestObjectiveBound(), sum(self.Value(z) for z in zero)), flush=True)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M, CB()); print('[%4.0fs] status' % (time.time() - t0), sv.StatusName(st), 'waste', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sv.BestObjectiveBound(), flush=True)
