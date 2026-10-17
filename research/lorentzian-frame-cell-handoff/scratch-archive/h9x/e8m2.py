"""Exact max root-like clique in L = E8 (+) <-2> (signature (8,1), = E7 (+) U): norm-2 vectors (e, m) with
e^2 - 2 m^2 = 2, |m| <= 1: E8 roots (m = 0) and norm-4 E8 vectors (m = +-1).  Lines up to sign; products
(e,m).(e',m') = e.e' - 2 m m' must lie in {0, +-1}.  WLOG one m = 1 line (W(E8) is transitive on norm-4 vectors).
Any clique > 111 must be frame-free (class bounds), so this tests the frame-free h = 9 window inside L."""
import itertools, numpy as np, sys, time
from ortools.sat.python import cp_model
from fractions import Fraction
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 3000
# E8 in doubled coordinates (all entries integers): x in Z^8 all even or all odd, sum = 0 mod 4  (= 2 * E8)
def e8_vectors(norm):
    out = []
    target = 4 * norm  # doubled coords: |2v|^2 = 4 |v|^2
    rng = range(-4, 5)
    def rec(pre, s):
        if len(pre) == 8:
            if s == target and (all(x % 2 == 0 for x in pre) or all(x % 2 for x in pre)) and sum(pre) % 4 == 0:
                out.append(tuple(pre))
            return
        for x in rng:
            if s + x * x <= target: rec(pre + [x], s + x * x)
    rec([], 0); return out
R = e8_vectors(2); N4 = e8_vectors(4)
print('roots', len(R), 'norm-4', len(N4), flush=True)
dot = lambda a, b: sum(x * y for x, y in zip(a, b)) // 4   # true product
lines = []
for e in R:
    if (tuple(-x for x in e), 0) not in lines and e > tuple(-x for x in e): lines.append((e, 0))
for e in N4: lines.append((e, 1))       # (e,1) ~ (-e,-1): all (e, 1) are distinct lines
print('lines in pool', len(lines), flush=True)
def ip(a, b): return dot(a[0], b[0]) - 2 * a[1] * b[1]
u0 = next(i for i, l in enumerate(lines) if l[1] == 1)
ok = lambda i, j: abs(ip(lines[i], lines[j])) <= 1
pool = [i for i in range(len(lines)) if i == u0 or ok(i, u0)]
print('compatible with u0:', len(pool), flush=True)
m = cp_model.CpModel(); y = {i: m.NewBoolVar('') for i in pool}; m.Add(y[u0] == 1)
P = np.array([[ip(lines[i], lines[j]) for j in pool] for i in pool])
bad = np.argwhere(np.triu(np.abs(P) > 1, 1))
for a, b in bad: m.AddBoolOr([y[pool[a]].Not(), y[pool[b]].Not()])
print('conflicts', len(bad), flush=True)
m.Maximize(sum(y.values()))
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 3
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s2): super().__init__(); s2.t0 = time.time()
    def on_solution_callback(s2): print('  sol %d bound %.0f (%.0fs)' % (s2.ObjectiveValue(), s2.BestObjectiveBound(), time.time() - s2.t0), flush=True)
st = s.Solve(m, CB())
print('max lines (genuinely Lorentzian, |m|<=1):', s.StatusName(st), s.ObjectiveValue(), 'bound', s.BestObjectiveBound(), flush=True)
sel = [i for i in pool if s.Value(y[i])]
import collections, pickle; print(collections.Counter(lines[i][1] for i in sel)); pickle.dump([lines[i] for i in sel], open('e8m2_best.pkl', 'wb'))
