"""Minimum number of cell partners of a line s (partners orthogonal to s) such that every target t orthogonal to s
has a partner (other than t) inside t-perp.  Lower bound on the degree of any cell graph in which s is never an
isolated vertex of H[t-perp].  Exact CP-SAT for one P line and one T line of I_{11,1}; E8 control via E8(M)."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/lmid')
from lw import g, V
from ortools.sat.python import cp_model
G = g.G
def minpartners(lines, s):
    P = [x for x in lines if x != s and G[s, x] == 0]
    m = cp_model.CpModel(); x = {u: m.NewBoolVar('') for u in P}
    for t in P:      # t is a target orthogonal to s
        cand = [u for u in P if u != t and G[t, u] == 0]
        m.AddBoolOr([x[u] for u in cand])
    m.Minimize(sum(x.values()))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 300; sv.parameters.num_workers = 4
    st = sv.Solve(m)
    return sv.StatusName(st), sv.ObjectiveValue(), sv.BestObjectiveBound(), len(P)
allL = list(range(V))
for s in (0, 55):
    print('I11 %s %s: (status, min partners, bound, |s-perp|) =' % (g.kind[s], tuple(g.supp[s])), minpartners(allL, s), flush=True)
M = [x for x in range(V) if 9 not in g.supp[x] and 10 not in g.supp[x]]     # E8(M) on points 0..8 (control)
for s in (M[0], M[-1]):
    print('E8(M) control %s %s:' % (g.kind[s], tuple(g.supp[s])), minpartners(M, s), flush=True)
