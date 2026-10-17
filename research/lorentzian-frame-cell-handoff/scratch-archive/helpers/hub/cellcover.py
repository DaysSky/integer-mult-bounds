"""Cell cover numbers (E8 skeleton analogue of the source-branch count).
A source s branches into cells {s, e} (e a line orthogonal to s); a branch at frame span{s, e} can be read by exactly
the targets t orthogonal to both s and e.  The cell cover number b(s) is the least number of such e covering every
reader t of s (t orthogonal to s, t != s), where t is covered by e when t is orthogonal to e and t != e.
E8 control: b = 3 (the 4-frame, #463's carrier bound).  CP-SAT, exact optimum (OPTIMAL status reported).
Also reports whether an optimal cover can be chosen pairwise orthogonal (a frame), and the target-side analogue is
the same number because the reader relation is symmetric.  Usage: python cellcover.py n"""
import sys, itertools
import numpy as np
from ortools.sat.python import cp_model
sys.dont_write_bytecode = True
import units as U


def lines(n):
    return list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 2))


def cover(G, s, frame=False, tl=600):
    v = len(G)
    R = [t for t in range(v) if t != s and G[s, t] == 0]
    m = cp_model.CpModel()
    x = {e: m.NewBoolVar('x%d' % e) for e in R}
    for t in R:
        m.AddBoolOr([x[e] for e in R if e != t and G[t, e] == 0])
    if frame:
        for e, f in itertools.combinations(R, 2):
            if G[e, f] != 0:
                m.AddBoolOr([x[e].Not(), x[f].Not()])
    m.Minimize(sum(x.values()))
    so = cp_model.CpSolver(); so.parameters.max_time_in_seconds = tl; so.parameters.num_workers = 4
    st = so.Solve(m)
    return so.StatusName(st), int(so.ObjectiveValue()), int(so.BestObjectiveBound()), [e for e in R if so.Value(x[e])], len(R)


if __name__ == '__main__':
    n = int(sys.argv[1])
    if n == 8:
        sys.path.insert(0, '.')
        L = U.roots_E8(); G = U.gram_doubled(L); reps = [('E8 root', 0)]
    else:
        L, G, lab = U.lorentz_family(n)
        LN = lines(n)
        reps = [('triple', 0), ('pair', LN.index((0, 1)))]
    for name, s in reps:
        for fr in (False, True):
            st, val, bd, sol, z = cover(G, s, fr)
            assert st == 'OPTIMAL' and val == bd
            print('n=%s %s source (readers %d) pairwise-orthogonal=%s: cell cover number %d (OPTIMAL)' % (
                n, name, z, fr, val), flush=True)
