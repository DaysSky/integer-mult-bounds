"""Star-structured aligned partition of I_{13,1} (apex x = 12; P(12,.) punctured).
Stage 1 (exact, CP-SAT): 33 pairwise compatible star frames {P(ab),P(cd),T(ab12),T(cd12)} partitioning the 66 P lines
on points 0..11 (equivalently the 66 T lines through 12).  Stage 2: for a stage-1 solution, TTTT frames on 0..11
compatible with all 33 star frames; exact cover of the 220 triples with pairwise compatibility (CP-SAT, lazy clauses);
T punctures allowed with minimisation."""
import sys, pickle, numpy as np, itertools, time
from ortools.sat.python import cp_model
frames, comp_lists, kinds = pickle.load(open('compat13.pkl', 'rb'))
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lword')
from geom import Geom
g = Geom(13); V = g.V
F = np.array(frames); nf = len(F)
def is_comp(a, b):
    arr = comp_lists[a]; k = np.searchsorted(arr, b); return k < len(arr) and arr[k] == b
supp = lambda l: g.supp[l]
star = [j for j in range(nf) if kinds[j] == 'PPTT' and all(12 in supp(l) for l in F[j] if g.kind[l] == 'T')]
print('star frames with apex 12:', len(star), flush=True)
Plines = [l for l in range(V) if g.kind[l] == 'P' and 12 not in supp(l)]
m = cp_model.CpModel(); x = {j: m.NewBoolVar('s%d' % j) for j in star}
for l in Plines: m.AddExactlyOne([x[j] for j in star if l in F[j]])
npair = 0
for i, a in enumerate(star):
    for b in star[i+1:]:
        if set(F[a]) & set(F[b]): continue
        if not is_comp(a, b): m.AddBoolOr([x[a].Not(), x[b].Not()]); npair += 1
print('incompatible disjoint star pairs', npair, flush=True)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 1800; s.parameters.num_workers = 3
st = s.Solve(m); print('stage 1:', s.StatusName(st), flush=True)
if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): sys.exit()
S1 = [j for j in star if s.Value(x[j])]
print('stage-1 solution:', [[supp(l) for l in F[j] if g.kind[l] == 'P'] for j in S1], flush=True)
pickle.dump(S1, open('star13_stage1.pkl', 'wb'))
# stage 2
tt = [j for j in range(nf) if kinds[j] == 'TTTT' and all(12 not in supp(l) for l in F[j]) and all(is_comp(j, a) for a in S1)]
print('TTTT frames on 0..11 compatible with all star frames:', len(tt), flush=True)
Tl = [l for l in range(V) if g.kind[l] == 'T' and 12 not in supp(l)]
clauses = set(); it = 0; t0 = time.time()
while True:
    it += 1
    m = cp_model.CpModel(); y = {j: m.NewBoolVar('t%d' % j) for j in tt}; p = {l: m.NewBoolVar('p%d' % l) for l in Tl}
    for l in Tl: m.Add(sum(y[j] for j in tt if l in F[j]) + p[l] == 1)
    for a, b in clauses: m.AddBoolOr([y[a].Not(), y[b].Not()])
    m.Minimize(sum(p.values()))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 3
    st = s.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('stage 2 iter', it, s.StatusName(st)); break
    sol = [j for j in tt if s.Value(y[j])]
    viol = [(a, b) for i, a in enumerate(sol) for b in sol[i+1:] if not is_comp(a, b)]
    print('stage 2 iter %d: %s T-punctures %d (lower bound %.0f), frames %d, violated %d, clauses %d (%.0fs)' % (
        it, s.StatusName(st), s.ObjectiveValue(), s.BestObjectiveBound(), len(sol), len(viol), len(clauses), time.time() - t0), flush=True)
    if not viol:
        print('STAR ALIGNED PARTITION: 12 P punctures +', int(s.ObjectiveValue()), 'T punctures')
        pickle.dump((S1, sol, [l for l in Tl if s.Value(p[l])]), open('star13_solution.pkl', 'wb')); break
    for a, b in viol: clauses.add((min(a, b), max(a, b)))
    if it > 400: print('iteration cap'); break
