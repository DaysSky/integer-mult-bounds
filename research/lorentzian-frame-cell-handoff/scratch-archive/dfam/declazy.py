"""Non-symmetric search for an I_{11,1} decoder cheaper than B0 (110): lazy-cut ILP over the structured-flat pool
(Z11 orbits of the 1,390 canonical flats, nondegenerate, plus the 11 D10's).  A family serves target t iff e_t|N'(t)
lies in the F2 span of the restricted piece indicators; when it fails, a certificate y (y_t = 1, y orthogonal to all
chosen restrictions) gives the valid cut  sum_{S : |S n Y| odd} x_S >= 1.  Objective: min sum rank, with cost <= C."""
import pickle, sys, time, itertools, numpy as np
from ortools.sat.python import cp_model
from dfam import LINES, NO, v, n, IDX, f2_solve
from flats import shift
C = int(sys.argv[1]) if len(sys.argv) > 1 else 109
fl = pickle.load(open('flats.pkl', 'rb'))
pool = {}
for r, S, nd in fl:
    if not nd: continue
    for a in range(n):
        T = shift(S, a)
        pool[T] = r
for p in range(n):   # D10(p)
    S = frozenset(IDX[('P', ij)] for ij in itertools.combinations([q for q in range(n) if q != p], 2)) | \
        frozenset(IDX[('T', tuple(sorted(ij + (p,))))] for ij in itertools.combinations([q for q in range(n) if q != p], 2))
    pool[S] = 10
cands = list(pool.items()); print('candidate pieces', len(cands), flush=True)
memb = np.zeros((len(cands), v), np.uint8)
for j, (S, r) in enumerate(cands): memb[j, list(S)] = 1
cost = [r for S, r in cands]
Np = [[t] + list(np.nonzero(NO[t])[0]) for t in range(v)]
cuts = []
# initial cuts: Y = {t}
for t in range(v): cuts.append(np.nonzero(memb[:, t])[0].tolist())
def certificate(chosen, t):
    A = memb[chosen][:, Np[t]]           # k x m
    # need y (length m) with y_0 = 1, A y = 0 over F2: solve [A; e0] y = [0; 1]
    M = np.concatenate([A, np.eye(1, A.shape[1], 0, dtype=np.uint8)], 0)
    b = np.zeros(M.shape[0], np.uint8); b[-1] = 1
    y, null = f2_solve(M, b)
    if y is None: return None
    return [Np[t][i] for i in np.nonzero(y)[0]]
it = 0; t0 = time.time()
while True:
    it += 1
    m = cp_model.CpModel(); x = [m.NewBoolVar('') for _ in cands]
    for c in cuts: m.AddBoolOr([x[j] for j in c])
    m.Add(sum(cost[j] * x[j] for j in range(len(cands))) <= C)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 3
    st = s.Solve(m)
    if st == cp_model.INFEASIBLE:
        print('iter %d: INFEASIBLE with %d cuts -> no decoder of cost <= %d in this pool (%.0fs)' % (it, len(cuts), C, time.time() - t0), flush=True); break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print('iter %d: %s (%d cuts) -- undecided' % (it, s.StatusName(st), len(cuts)), flush=True); break
    chosen = [j for j in range(len(cands)) if s.Value(x[j])]
    new = 0
    for t in range(v):
        Y = certificate(chosen, t)
        if Y is not None:
            Ys = np.zeros(v, np.uint8); Ys[Y] = 1
            cut = np.nonzero((memb @ Ys) % 2)[0].tolist()
            cuts.append(cut); new += 1
    print('iter %d: cost %d, pieces %d, unserved targets %d, cuts %d (%.0fs)' % (it, sum(cost[j] for j in chosen), len(chosen), new, len(cuts), time.time() - t0), flush=True)
    if new == 0:
        print('FOUND decoder of cost', sum(cost[j] for j in chosen)); pickle.dump([cands[j] for j in chosen], open('declazy_found.pkl', 'wb')); break
