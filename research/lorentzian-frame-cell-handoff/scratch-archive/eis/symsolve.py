"""H-invariant linear-over-F2 decoder search with CP-SAT (flat-pair rectangles)."""
import pickle, sys, time, numpy as np
from ortools.sat.python import cp_model
from sympy.combinatorics import Permutation, PermutationGroup
d = pickle.load(open('eis.pkl','rb'))
n = 40; fl = d['flat_list']; C = d['cost'].astype(int); nonorth = d['nonorth']
nf = len(fl); fidx = {f: i for i, f in enumerate(fl)}
sub = pickle.load(open('subgroups.pkl','rb'))
name = sys.argv[1]; budget = int(sys.argv[2]); tlimit = float(sys.argv[3]) if len(sys.argv) > 3 else 600
if name.startswith('nsyl'):
    H = PermutationGroup([Permutation(g) for g in sub[name]])
else:
    H = PermutationGroup([Permutation(g) for g in sub[name]])
els = [np.array(g.array_form) for g in H.generate_schreier_sims()]
print('H', name, 'order', len(els), flush=True)
def img_flat(f, g):
    m = 0
    x = f
    while x:
        b = x & -x; t = b.bit_length() - 1; x ^= b
        m |= 1 << int(g[t])
    return fidx[m]
fimg = np.array([[img_flat(f, g) for f in fl] for g in els])  # |H| x nf
# orbits of flat pairs with cost>=1 and |O|*c <= budget
seen = np.zeros((nf, nf), dtype=bool)
orbs = []
for a in range(nf):
    if not fl[a]: continue
    for b in range(nf):
        if not fl[b] or seen[a, b] or C[a, b] == 0: continue
        O = set(zip(fimg[:, a].tolist(), fimg[:, b].tolist()))
        for x, y in O: seen[x, y] = True
        c = int(C[a, b])
        if len(O) * c <= budget:
            orbs.append((sorted(O), c))
print('usable orbits', len(orbs), flush=True)
# constraint entries and their orbits
cons = [(t, t, 1) for t in range(n)] + [(t, s, 0) for t in range(n) for s in range(n) if (nonorth[t] >> s) & 1]
cseen = set(); creps = []
for t, s, v in cons:
    if (t, s) in cseen: continue
    O = set((int(g[t]), int(g[s])) for g in els)
    cseen |= O; creps.append((t, s, v))
print('constraint orbits', len(creps), flush=True)
mem = [[(f >> t) & 1 for t in range(n)] for f in fl]
model = cp_model.CpModel()
x = [model.NewBoolVar('x%d' % i) for i in range(len(orbs))]
for t, s, v in creps:
    lits = []
    for i, (O, c) in enumerate(orbs):
        k = sum(mem[a][t] & mem[b][s] for a, b in O)
        if k & 1: lits.append(x[i])
    if v == 1:
        model.AddBoolXOr(lits if lits else [model.NewConstant(0)])  # xor = true
    else:
        if lits:
            model.AddBoolXOr(lits + [model.NewConstant(1)])  # xor(lits) = 0
cost = sum(len(O) * c * x[i] for i, (O, c) in enumerate(orbs))
model.Add(cost <= budget)
model.Minimize(cost)
solver = cp_model.CpSolver(); solver.parameters.max_time_in_seconds = tlimit; solver.parameters.num_workers = 1
t0 = time.time(); st = solver.Solve(model)
print('status', solver.StatusName(st), 'time %.1f' % (time.time() - t0), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = [orbs[i] for i in range(len(orbs)) if solver.Value(x[i])]
    print('cost', solver.ObjectiveValue(), 'orbits', [(len(O), c) for O, c in chosen])
    rects = [(a, b, c) for O, c in chosen for a, b in O]
    # verify
    B = np.zeros((n, n), dtype=np.uint8)
    for a, b, c in rects:
        for t in range(n):
            if mem[a][t]:
                for s in range(n):
                    if mem[b][s]: B[t, s] ^= 1
    ok = all(B[t, t] for t in range(n)) and not any(B[t, s] for t in range(n) for s in range(n) if (nonorth[t] >> s) & 1)
    print('verify', ok, 'total cost', sum(c for a, b, c in rects))
    pickle.dump(rects, open('sym_%s_%d.pkl' % (name, int(solver.ObjectiveValue())), 'wb'))
