"""Window-aware whole-residual hosting for the nine-stage B_K template (K = 4, a = 7), exact MILP, any residual widths.
Slot types (per port copy; 2v copies per replica): (pair, capacity, window of calls whose residuals may sit there).
Each call has R residuals with a given width multiset.  Choose, per slot type, how many of its 2v copies use each filling
and route the residuals of calls in the window to them; minimise sum f(remainder) at q, and iterate q to the fixed
point of the exact root (pricer.root).  No banks (neither word has any).  Not run by verify.sh; needs ortools, mpmath."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lorentzian-frame-cell-handoff', 'code', 'price'))
import pricer as P
from mpmath import mpf
from ortools.linear_solver import pywraplp
a = 7; K = 4; L = 9; v = 111; T = 32; m = 1 + L * a; W = 2 * K * v * T
# slot types: (name, capacity, window calls)
SLOTS = [('p0post', 42, range(3, 9)), ('p1pre', 14, range(0, 2)), ('p1one', 7, [2]), ('p1post', 28, range(5, 9)),
         ('p2pre', 28, range(0, 4)), ('p2one', 7, [4]), ('p2post', 14, range(7, 9)), ('p3pre', 42, range(0, 6)), ('p3one', 7, [6])]


def fillings(cap, widths):
    out = []
    def rec(i, rem, cnt):
        if i == len(widths): out.append(tuple(cnt)); return
        for k in range(rem // widths[i] + 1): rec(i + 1, rem - k * widths[i], cnt + [k])
    rec(0, cap, []); return out


def solve(widthcount, q):
    widths = sorted(widthcount)
    f = lambda r: 0.0 if r == 0 else float(mpf(r) * ((mpf(m) / r) ** q - 1))
    sv = pywraplp.Solver.CreateSolver('SCIP')
    N = 2 * v; x = {}; y = {}; obj = []
    for s, (nm, cap, win) in enumerate(SLOTS):
        for pt in fillings(cap, widths):
            x[s, pt] = sv.IntVar(0, N, 'x')
            obj.append(f(cap - sum(k * wd for k, wd in zip(pt, widths))) * x[s, pt])
        sv.Add(sum(x[s, pt] for (ss, pt) in x if ss == s) == N)
        for c in win:
            for wd in widths: y[s, c, wd] = sv.IntVar(0, 10 ** 6, 'y')
        for i, wd in enumerate(widths):
            sv.Add(sum(y[s, c, wd] for c in win) == sum(pt[i] * x[s, pt] for (ss, pt) in x if ss == s))
    for c in range(L):
        for wd in widths:
            sv.Add(sum(y[s, c, wd] for s, (nm, cap, win) in enumerate(SLOTS) if c in win) == widthcount[wd])
    sv.Minimize(sum(obj))
    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE): return None
    rem = {}
    for (s, pt), var in x.items():
        k = int(round(var.solution_value())); r = SLOTS[s][1] - sum(kk * wd for kk, wd in zip(pt, widths))
        if k and r: rem[r] = rem.get(r, 0) + k
    return rem, st == pywraplp.Solver.OPTIMAL


def price(local, widthcount):
    q = mpf('0.0017334')
    for it in range(12):
        out = solve(widthcount, q)
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
    c0, rem0, o0 = price(base, {8: 439})
    print('control P111-tuned (all width 8):', float(c0), 'vs published', float(ref), 'remainders', rem0, 'optimal', o0)
    e1 = {1: 1321, 2: 1344, 3: 78, 4: 44, 5: 102, 6: 12, 7: 18}   # E1's local paid profile (exact replay)
    c1, rem1, o1 = price(e1, {8: 438, 6: 1})
    print('E1 (helper 248 entrance rank 2, width 6):', float(c1), '%+.4f%%' % float((c1 / ref - 1) * 100), 'remainders', rem1, 'optimal', o1)
