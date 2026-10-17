"""Lower bound (exact when it terminates) on the minimum number of punctured lines for an aligned good-frame partition
of I_{13,1}, f0 (a PPTT frame, WLOG) included.  Model: x_j (frames compatible with f0, disjoint from it), p_u (line u
punctured); every line other than f0's lines is covered exactly once or punctured; minimise sum p.  Incompatible-pair
clauses are added lazily: each iteration solves to optimality (its optimum is a valid LOWER bound), checks pairwise
compatibility of the chosen frames, adds clauses for violated pairs, repeats.  Ends when a solution is compatible."""
import sys, pickle, numpy as np, time
from ortools.sat.python import cp_model
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
F = np.array(frames); nf = len(F); V = 364
f0 = next(i for i in range(nf) if kinds[i] == 'PPTT')
f0set = set(F[f0].tolist())
cand = [int(j) for j in comp_lists[f0] if not (set(F[j].tolist()) & f0set)]
cset = set(cand)
compsets = {}
def is_comp(a, b):
    arr = comp_lists[a]; k = np.searchsorted(arr, b); return k < len(arr) and arr[k] == b
print('candidates', len(cand), flush=True)
clauses = set()
t0 = time.time(); it = 0
TL = float(sys.argv[1]) if len(sys.argv) > 1 else 600
while True:
    it += 1
    m = cp_model.CpModel()
    x = {j: m.NewBoolVar('x%d' % j) for j in cand}
    p = {u: m.NewBoolVar('p%d' % u) for u in range(V) if u not in f0set}
    inc = {u: [] for u in p}
    for j in cand:
        for u in F[j]: inc[int(u)].append(x[j])
    for u in p: m.Add(sum(inc[u]) + p[u] == 1)
    for a, b in clauses: m.AddBoolOr([x[a].Not(), x[b].Not()])
    m.Minimize(sum(p.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_workers = 4
    st = s.Solve(m)
    lb = s.BestObjectiveBound()
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('iter %d: status %s, lower bound %s' % (it, s.StatusName(st), lb), flush=True); break
    sol = [j for j in cand if s.Value(x[j])]
    viol = [(a, b) for i, a in enumerate(sol) for b in sol[i+1:] if not is_comp(a, b)]
    print('iter %d: %s obj %d lower-bound %.0f, frames %d, violated pairs %d, clauses %d (%.0fs)' % (
        it, s.StatusName(st), s.ObjectiveValue(), lb, len(sol), len(viol), len(clauses), time.time() - t0), flush=True)
    if not viol:
        print('COMPATIBLE SOLUTION: punctures', int(s.ObjectiveValue()), '(optimal)' if st == cp_model.OPTIMAL else '(not proven optimal)')
        pickle.dump(([f0] + sol, [u for u in p if s.Value(p[u])]), open('lazy13_solution.pkl', 'wb'))
        break
    for a, b in viol: clauses.add((min(a, b), max(a, b)))
    # also add, for each violated frame, its incompatibilities with frames sharing its most-constrained lines (strengthening)
    if it % 5 == 0: pickle.dump(clauses, open('lazy13_clauses.pkl', 'wb'))
