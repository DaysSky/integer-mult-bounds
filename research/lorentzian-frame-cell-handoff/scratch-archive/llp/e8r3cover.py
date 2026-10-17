"""E8 analogue of the rank-8 frame sections: sections F-perp for rank-3 frames F through t (rank 5 in E8).
Min cover of R(t) (63 lines) by such perps (CP-SAT), and the distribution of frame sizes / perp sizes."""
import sys, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
t = 0; R = HYP[t] & ~(1 << t)
print('E8 lines', V, '|R(t)|', pc(R))
fr = {}
for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
    F, r = e8.closure((1 << t) | (1 << a) | (1 << b))
    if r != 3: continue
    if F not in fr: fr[F] = pm(F) & R
st = collections.Counter((pc(F), pc(P)) for F, P in fr.items())
print('rank-3 frames through t', len(fr), '(lines, perp) hist', sorted(st.items()))
sets = sorted(set(fr.values()), key=pc, reverse=True)
M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in sets]
for w in bits(R): M.AddBoolOr([x[i] for i, s_ in enumerate(sets) if s_ >> w & 1])
M.Minimize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 1
st_ = sv.Solve(M); print('min cover by rank-3-frame perps:', int(sv.ObjectiveValue()), sv.StatusName(st_), 'bound', sv.BestObjectiveBound())
