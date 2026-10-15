"""General local RHO-5 test at one M11 triangle node (A,B,C,E) with three delivered users: the node's span S =
span{P_A,P_B,P_C} (all rank 8) can only have a rank-<=5 basis of the form {P_X+P_Y, P_X+P_Z, P_A+P_B+P_C}.  Encode with
CP-SAT: free memberships of transversals (pairs crossing at several of the user's nodes; forced ones fixed), own-A2
flags delta_X in {0,1}, and for each of the three basis vectors a maximal rank-5 closed subset of the node perp
containing its support.  Infeasible => this node needs >= 1 extra register whenever its inputs have rank <= 5.
usage: lttri_rho5local.py node_index ..."""
import sys, json, itertools, collections
from lgeo import *
from lclosed import closed_sets
from ortools.sat.python import cp_model
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def A2(T): return [Ln('P', p) for p in itertools.combinations(T, 2)]
def mult(X, pair):
    k = 0
    for nj in nodes_of[X]:
        B, C = [T for T in sol[nj] if T != X]
        if (pair[0] in B and pair[1] in C) or (pair[0] in C and pair[1] in B): k += 1
    return k
for ni in map(int, sys.argv[1:]):
    A, B, C = sol[ni]; users = (A, B, C)
    E = tuple(x for x in range(11) if x not in A + B + C)
    t = Ln('T', A); F = pp((1 << Ln('T', A)) | (1 << Ln('T', B)) | (1 << Ln('T', C))); perp = pm(F)
    lv = closed_sets(perp, 5)
    maxi = sorted(lv[5], key=pc, reverse=True); mx = []
    for q in maxi:
        if not any(q & ~r == 0 for r in mx): mx.append(q)
    print('node', ni, A, B, C, 'E', E, '| perp', pc(perp), '| maximal rank-5 closed subsets', len(mx), flush=True)
    lines = bits(perp)
    M = cp_model.CpModel()
    # part P_X as indicator over perp lines
    part = {}
    delta = [M.NewBoolVar('') for _ in range(3)]
    for u, X in enumerate(users):
        others = [T for T in users if T != X]
        f = set(A2(others[0]) + A2(others[1]) + [Ln('P', E)])
        for s in lines:
            if s in f: part[(u, s)] = 1
            elif KIND[s] == 'P' and s in A2(X): part[(u, s)] = delta[u]
            elif KIND[s] == 'T' and s != Ln('T', A) and len(set(SUPP[s]) & set(A)) == 1 and len(set(SUPP[s]) & set(B)) == 1 and len(set(SUPP[s]) & set(C)) == 1:
                pair = tuple(sorted(p for p in SUPP[s] if p not in X))
                part[(u, s)] = 1 if mult(X, pair) == 1 else M.NewBoolVar('')
            else: part[(u, s)] = 0
    def xor_lit(vals):
        const = sum(v for v in vals if isinstance(v, int)) % 2; vs = [v for v in vals if not isinstance(v, int)]
        if not vs: return const
        r = M.NewBoolVar(''); k = M.NewIntVar(0, len(vs), '')
        M.Add(sum(vs) + const == 2 * k + r); return r
    ok_any = []
    for p in range(3):
        q, r = [x for x in range(3) if x != p]
        vecs = [[xor_lit([part[(p, s)], part[(q, s)]]) for s in lines],
                [xor_lit([part[(p, s)], part[(r, s)]]) for s in lines],
                [xor_lit([part[(0, s)], part[(1, s)], part[(2, s)]]) for s in lines]]
        o = M.NewBoolVar(''); ok_any.append(o)
        for vec in vecs:
            ch = [M.NewBoolVar('') for _ in mx]; M.Add(sum(ch) == 1).OnlyEnforceIf(o)
            for c, Q in zip(ch, mx):
                for s, v in zip(lines, vec):
                    if Q >> s & 1: continue
                    if isinstance(v, int):
                        if v: M.AddBoolOr([c.Not(), o.Not()])
                    else: M.AddBoolOr([c.Not(), v.Not(), o.Not()])
    M.AddBoolOr(ok_any)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 300; sv.parameters.num_workers = 4
    st = sv.Solve(M)
    print('   general local RHO-5 zero-waste (3 delivered):', sv.StatusName(st), flush=True)
