"""(env ONEUSER=u: feasibility with only user u releasing.)  (env RELA2=1: A2(other) lines are releasable memberships too.)  (env OBJ=users: minimise 100*#releasing users + #releases.)  MIN-RELEASE probe: the minimum number of coverage-forced (multiplicity-1) transversal memberships that must be
released (covered elsewhere, as in a mixed design) for the node to admit a rank-5 basis.  Released = forced line set to 0.
RELAX may still contain pe / a2.  Original header of lttri_rho5_relax.py follows.
  env RELAX (comma list) frees, per user:
  pe = P(E); trans = the multiplicity-1 transversals; a2 = the A2(other) lines.  Otherwise as lttri_rho5_pe.py.
  General local RHO-5 test at one M11 triangle node, decomposed: for every own-A2 pattern delta in {0,1}^3 and
pivot p, the basis {P_p+P_q, P_p+P_r, P_A+P_B+P_C} must consist of rank-<=5 vectors.  Lines of each vector that
are constant 1 (forced) prune the candidate maximal rank-5 closed subsets; a small CP-SAT then decides the free
transversal memberships.  All sub-problems infeasible => the node needs >= 1 extra register with inputs of rank
<= 5 when all three users are delivered.  usage: lttri_rho5local2.py node_index ..."""
import sys, os, json, itertools, collections
from lgeo import *
from lclosed import closed_sets
from ortools.sat.python import cp_model
RELAX = set(os.environ.get('RELAX', 'pe').split(','))
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
            part = {}; rel = []; relu = {0: [], 1: [], 2: []}
            pe = [M.NewBoolVar('') for _ in range(3)]   # P(E) optional per user (mixed covers)
            for u, X in enumerate(users):
                others = [T for T in users if T != X]
                f = set(A2(others[0]) + A2(others[1]))
                for s in lines:
                    if s == Ln('P', E): part[(u, s)] = pe[u] if 'pe' in RELAX else 1
                    elif s in f:
                        if os.environ.get('RELA2'):   # A2(other) memberships releasable too, counted as releases
                            v = M.NewBoolVar(''); part[(u, s)] = v; rel.append(v); relu[u].append(v)
                        else: part[(u, s)] = M.NewBoolVar('') if 'a2' in RELAX else 1
                    elif KIND[s] == 'P' and s in A2(X): part[(u, s)] = dl[u]
                    elif s in trans:
                        pair = tuple(sorted(x for x in SUPP[s] if x not in X))
                        if mult(X, pair) == 1:
                            v = M.NewBoolVar(''); part[(u, s)] = v; rel.append(v); relu[u].append(v)
                        else: part[(u, s)] = M.NewBoolVar('')
                    else: part[(u, s)] = 0
            def xr(vals):
                const = sum(v for v in vals if isinstance(v, int)) % 2; vs = [v for v in vals if not isinstance(v, int)]
                if not vs: return const
                rr = M.NewBoolVar(''); k = M.NewIntVar(0, len(vs), ''); M.Add(sum(vs) + const == 2 * k + rr); return rr
            vecs = [[xr([part[(p, s)], part[(q, s)]]) for s in lines], [xr([part[(p, s)], part[(r, s)]]) for s in lines],
                    [xr([part[(0, s)], part[(1, s)], part[(2, s)]]) for s in lines]]
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
            if os.environ.get('ONEUSER'):   # feasibility: only user ONEUSER may release (A2 too if RELA2); others fully forced
                ou = int(os.environ['ONEUSER'])
                for w in range(3):
                    if w != ou:
                        for v in relu[w]: M.Add(v == 1)
            elif os.environ.get('OBJ') == 'users':   # minimise #users with >= 1 release, then #releases
                ru = [M.NewBoolVar('') for _ in range(3)]
                for u in range(3):
                    for v in relu[u]: M.AddImplication(v.Not(), ru[u])
                M.Minimize(100 * sum(ru) + len(rel) - sum(rel))
            elif not os.environ.get('ONEUSER'): M.Minimize(len(rel) - sum(rel))
            sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = float(os.environ.get("TL", "60")); sv.parameters.num_workers = 4
            st = sv.Solve(M)
            if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                feasible.append((dl, p, 'SAT') if os.environ.get('ONEUSER') else (dl, p, int(sv.ObjectiveValue()), int(sv.BestObjectiveBound()), 'OPT' if st == cp_model.OPTIMAL else 'FEAS', len(rel)))
            else: feasible.append((dl, p, sv.StatusName(st)))
    print('node', ni, '| maximal rank-5 subsets', len(mx), '| (delta, pivot, min released, bound, status, #forced):', feasible if feasible else 'NONE', '| RELAX', sorted(RELAX), flush=True)
