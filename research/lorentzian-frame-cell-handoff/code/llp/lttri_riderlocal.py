"""RIDER VARIANT: an extra register r (P(E)'s part at its T-node, any subset of the hub M_n = node perp minus P(E))
stops at M_n; zero waste then needs span{P_p+P_q, P_p+P_r, r} to have a basis of three rank-<=5 vectors (any three
independent combinations are allowed: we require c1, c2 and r each rank <= 5 OR c1, r and c1+... -- simplified to
c1 = P_p+P_q and c2 = P_p+P_r each in span of rank-5 vectors {r, s1, s2}: here we test the sufficient pattern
{c1 + r, c2 + r, r} or {c1, c2 + r, r} etc. all rank <= 5) and the triple sum rank <= 5.
Original: General local RHO-5 test at one M11 triangle node, decomposed: for every own-A2 pattern delta in {0,1}^3 and
pivot p, the basis {P_p+P_q, P_p+P_r, P_A+P_B+P_C} must consist of rank-<=5 vectors.  Lines of each vector that
are constant 1 (forced) prune the candidate maximal rank-5 closed subsets; a small CP-SAT then decides the free
transversal memberships.  All sub-problems infeasible => the node needs >= 1 extra register with inputs of rank
<= 5 when all three users are delivered.  usage: lttri_rho5local2.py node_index ..."""
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
    F = pp((1 << Ln('T', A)) | (1 << Ln('T', B)) | (1 << Ln('T', C))); perp = pm(F)
    lv = closed_sets(perp, 5)
    allq = sorted(lv[5], key=pc, reverse=True); mx = []
    for q in allq:
        if not any(q & ~r == 0 for r in mx): mx.append(q)
    lines = bits(perp)
    trans = [s for s in lines if KIND[s] == 'T']
    feasible = []
    for dl in itertools.product((0, 1), repeat=3):
        for p in range(3):
            q, r = [x for x in range(3) if x != p]
            M = cp_model.CpModel()
            part = {}
            for u, X in enumerate(users):
                others = [T for T in users if T != X]
                f = set(A2(others[0]) + A2(others[1]) + [Ln('P', E)])
                for s in lines:
                    if s in f: part[(u, s)] = 1
                    elif KIND[s] == 'P' and s in A2(X): part[(u, s)] = dl[u]
                    elif s in trans:
                        pair = tuple(sorted(x for x in SUPP[s] if x not in X))
                        part[(u, s)] = 1 if mult(X, pair) == 1 else M.NewBoolVar('')
                    else: part[(u, s)] = 0
            def xr(vals):
                const = sum(v for v in vals if isinstance(v, int)) % 2; vs = [v for v in vals if not isinstance(v, int)]
                if not vs: return const
                rr = M.NewBoolVar(''); k = M.NewIntVar(0, len(vs), ''); M.Add(sum(vs) + const == 2 * k + rr); return rr
            hub = [s for s in lines if not (KIND[s] == 'P' and s == Ln('P', E))]
            rv = {s: (M.NewBoolVar('') if s in hub else 0) for s in lines}
            pat = (p + dl[0]) % 4          # cycle through combination patterns cheaply
            c1 = [xr([part[(p, s)], part[(q, s)]]) for s in lines]; c2 = [xr([part[(p, s)], part[(r, s)]]) for s in lines]
            rr_ = [rv[s] for s in lines]
            tw = lambda X, Y: [xr([x, y]) for x, y in zip(X, Y)]
            vecs = [tw(c1, rr_), tw(c2, rr_), rr_, [xr([part[(0, s)], part[(1, s)], part[(2, s)]]) for s in lines]]
            dead = False
            for vec in vecs:
                forced = 0
                for s, v in zip(lines, vec):
                    if isinstance(v, int) and v == 1: forced |= 1 << s
                cands = [Q for Q in mx if forced & ~Q == 0]
                if not cands: dead = True; break
                ch = [M.NewBoolVar('') for _ in cands]; M.AddExactlyOne(ch)
                for c, Q in zip(ch, cands):
                    for s, v in zip(lines, vec):
                        if Q >> s & 1 or isinstance(v, int): continue
                        M.AddImplication(c, v.Not())
            if dead: continue
            sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 4
            st = sv.Solve(M)
            if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): feasible.append((dl, p)); break
            if st == cp_model.UNKNOWN: feasible.append((dl, p, 'UNKNOWN'))
    print('node', ni, '| maximal rank-5 subsets', len(mx), '| feasible (delta, pivot) sub-problems:', feasible if feasible else 'NONE (rider pattern {c1+r, c2+r, r} + triple sum infeasible)', flush=True)
