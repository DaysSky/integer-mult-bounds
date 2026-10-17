"""SAT search for an F2 decoder of rank r for a line system: B = W U^T (labels in F2^r) with B_tt = 1 and B_ts = 0
whenever s, t are non-orthogonal.  Symmetry breaking: a max pairwise-non-orthogonal clique K gets u = e_1..e_|K|
(B restricted to K is the identity), w_K = e_i + free combination of coordinates > |K|."""
import sys, numpy as np, itertools, time
from ortools.sat.python import cp_model
V = np.load(sys.argv[1]); n = V.shape[1] - 1; r = int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
eta = np.array([1]*n + [-1]); G = (V*eta) @ V.T; v = len(V)
NO = (G % 2 == 1)
# clique
m0 = cp_model.CpModel(); xx = [m0.NewBoolVar('') for _ in range(v)]
for i in range(v):
    for j in range(i+1, v):
        if not NO[i, j]: m0.AddBoolOr([xx[i].Not(), xx[j].Not()])
m0.Maximize(sum(xx)); s0 = cp_model.CpSolver(); s0.parameters.max_time_in_seconds = 60; s0.Solve(m0)
K = [i for i in range(v) if s0.Value(xx[i])]; k = len(K); print('clique', k, flush=True)
assert k <= r
m = cp_model.CpModel()
u = [[m.NewBoolVar('u%d_%d' % (s, j)) for j in range(r)] for s in range(v)]
w = [[m.NewBoolVar('w%d_%d' % (t, j)) for j in range(r)] for t in range(v)]
for idx, s in enumerate(K):
    for j in range(r):
        m.Add(u[s][j] == (1 if j == idx else 0))
        if j < k: m.Add(w[s][j] == (1 if j == idx else 0))
def dotvar(t, s):
    terms = []
    for j in range(r):
        p = m.NewBoolVar('')
        m.AddMultiplicationEquality(p, [w[t][j], u[s][j]])
        terms.append(p)
    return terms
nc = 0
for t in range(v):
    m.AddBoolXOr(dotvar(t, t) + [m.NewConstant(0)] + []) if False else None
    terms = dotvar(t, t); m.AddBoolXOr(terms)          # XOR = 1
    for s in np.nonzero(NO[t])[0]:
        terms = dotvar(t, int(s)); m.AddBoolXOr(terms + [m.NewConstant(1)])   # XOR(terms) = 0
        nc += 1
print('constraints', nc, flush=True)
ORTH = (~NO) & ~np.eye(v, dtype=bool)
obj = []
import random
random.seed(0)
pairs = [(t, int(q)) for t in range(v) for q in np.nonzero(ORTH[t])[0]]
for (t, q) in pairs:
    terms = dotvar(t, q); b = m.NewBoolVar('')
    m.AddBoolXOr(terms + [b.Not()])   # b = XOR(terms)
    obj.append(b)
m.Add(sum(obj) <= len(obj) - 1)
print('orthogonal pairs in objective', len(pairs), flush=True)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
t0 = time.time(); st = s.Solve(m)
print('rank %d decoder: %s (%.0fs)' % (r, s.StatusName(st), time.time() - t0), flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    U = np.array([[s.Value(u[a][j]) for j in range(r)] for a in range(v)]); W = np.array([[s.Value(w[a][j]) for j in range(r)] for a in range(v)])
    B = (W @ U.T) % 2
    assert all(B[t, t] == 1 for t in range(v)) and not (B[NO] == 1).any()
    np.save(sys.argv[1].replace('.npy', '_U%d.npy' % r), U); np.save(sys.argv[1].replace('.npy', '_W%d.npy' % r), W)
    print('verified; row weights', np.bincount(B.sum(1)).nonzero()[0][:10], 'mean', B.sum(1).mean())
