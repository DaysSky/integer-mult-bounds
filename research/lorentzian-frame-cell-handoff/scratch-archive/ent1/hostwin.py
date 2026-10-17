"""Window-aware whole-residual hosting for the nine-stage B_K template (K = 4, a = 7), exact MILP.
Slot types (per port copy; 2v copies per replica): (pair, capacity, window of calls whose residuals may sit there).
Each call has R residuals: R - n7 of width 8 and n7 of width 7.  Choose, per slot type, how many of its 2v copies use
each filling (a8, a7) and route residuals of calls in the window to them; minimise sum f(remainder) at q, iterate q
to the fixed point of the exact root (pricer.root).  No banks (the selected word has none)."""
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
from ortools.linear_solver import pywraplp
a = 7; K = 4; L = 9; v = 111; T = 32; m = 1 + L * a; W = 2 * K * v * T
# slot types: (name, capacity, window calls)
SLOTS = [('p0post', 42, range(3, 9)), ('p1pre', 14, range(0, 2)), ('p1one', 7, [2]), ('p1post', 28, range(5, 9)),
         ('p2pre', 28, range(0, 4)), ('p2one', 7, [4]), ('p2post', 14, range(7, 9)), ('p3pre', 42, range(0, 6)), ('p3one', 7, [6])]
def solve(local, R, n7, q):
    f = lambda r: 0.0 if r == 0 else float(mpf(r) * ((mpf(m) / r) ** q - 1))
    sv = pywraplp.Solver.CreateSolver('SCIP')
    N = 2 * v
    pats = {}; x = {}; y = {}
    obj = []
    for s, (nm, cap, win) in enumerate(SLOTS):
        for a8 in range(cap // 8 + 1):
            for a7 in range((cap - 8 * a8) // 7 + 1):
                x[s, a8, a7] = sv.IntVar(0, N, 'x')
                obj.append(f(cap - 8 * a8 - 7 * a7) * x[s, a8, a7])
        sv.Add(sum(x[s, a8, a7] for (ss, a8, a7) in x if ss == s) == N)
        for call in win:
            for wd in (7, 8):
                y[s, call, wd] = sv.IntVar(0, 10 ** 6, 'y')
        for wd in (7, 8):
            sv.Add(sum(y[s, c, wd] for c in win) == sum((a8 if wd == 8 else a7) * x[s, a8, a7] for (ss, a8, a7) in x if ss == s))
    for call in range(L):
        for wd, dem in ((8, R - n7), (7, n7)):
            sv.Add(sum(y[s, call, wd] for s, (nm, cap, win) in enumerate(SLOTS) if call in win) == dem)
    sv.Minimize(sum(obj))
    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE): return None
    rem = {}
    for (s, a8, a7), var in x.items():
        k = int(round(var.solution_value()))
        r = SLOTS[s][1] - 8 * a8 - 7 * a7
        if k and r: rem[r] = rem.get(r, 0) + k
    return rem, st == pywraplp.Solver.OPTIMAL
def price(local, R, n7):
    q = mpf('0.0017334')
    for it in range(12):
        out = solve(local, R, n7, q)
        if out is None: return None
        rem, opt = out
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = P.root(prof, m, W)
        if abs(q2 - q) < mpf(10) ** -26: break
        q = q2
    return q2, rem, opt
if __name__ == '__main__':
    ref = mpf('0.001733427039589844')
    base = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
    c0, rem0, o0 = price(base, 439, 0)
    print('control P111-tuned (all width 8):', float(c0), 'vs published', float(ref), 'remainders', rem0, 'optimal', o0)
    e1 = dict(base); e1[1] -= 1
    c1, rem1, o1 = price(e1, 439, 1)
    print('E1 (helper 248 width 7, one rank-1 child removed):', float(c1), '%+.4f%%' % float((c1 / ref - 1) * 100), 'remainders', rem1, 'optimal', o1)
