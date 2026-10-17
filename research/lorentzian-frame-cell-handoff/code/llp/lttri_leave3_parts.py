"""Leave-3 cost probe.  T(X) keeps one M11 triangle node n_k and replaces the other three by sections F1, F2, F3 (rank-3
frames through t).  Enumerates ALL frame triples covering Need = R(t) n (left perps) minus n_k-perp (CP-SAT, all
solutions), and for each triple the lines forced into each new part (Need lines in exactly one F_i-perp), their rank,
and |F_i-perp|.  A new section whose only user is T(X) and whose part has rank 8 (= node rank) costs >= 1 at any
RHO <= 7 (no good vector spans it).  usage: lttri_leave3_parts.py target_index kept_slot"""
import sys, json, itertools, collections
from lgeo import *
from ortools.sat.python import cp_model
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
def nm(s): return KIND[s] + ''.join(map(str, SUPP[s]))
targets = sorted(nodes_of); X = targets[int(sys.argv[1])]; ks = int(sys.argv[2])
t = Ln('T', X); R = HYP[t]
nfr = [pp(sum(1 << Ln('T', T) for T in sol[nj])) for nj in nodes_of[X]]
nperp = [pm(F) & R for F in nfr]
frames = set()
for a, b in itertools.combinations([s for s in range(V) if s != t], 2):
    m = (1 << t) | (1 << a) | (1 << b)
    if rank(m) == 3: frames.add(pp(m))
frames = sorted(frames); fperp = [pm(F) & R for F in frames]
L = 0
for i in range(4):
    if i != ks: L |= nperp[i]
need = L & ~nperp[ks]
print('target', X, 'kept node', nodes_of[X][ks], '| |Need|', pc(need), 'rank', rank(need), flush=True)
M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in frames]
M.Add(sum(x) <= 3)
for s in bits(need): M.AddBoolOr([x[f] for f in range(len(frames)) if fperp[f] >> s & 1])
class CB(cp_model.CpSolverSolutionCallback):
    def __init__(s): super().__init__(); s.sols = []
    def on_solution_callback(s): s.sols.append(tuple(f for f in range(len(frames)) if s.Value(x[f])))
cb = CB(); sv = cp_model.CpSolver(); sv.parameters.enumerate_all_solutions = True; sv.parameters.max_time_in_seconds = 600
st = sv.Solve(M, cb)
sols = sorted(set(cb.sols)); print('status', sv.StatusName(st), '| covering frame sets (size <= 3):', len(sols), flush=True)
hist = collections.Counter()
for S in sols:
    row = []
    for f in S:
        others = 0
        for g in S:
            if g != f: others |= fperp[g]
        forced = need & fperp[f] & ~others
        row.append((rank(forced), pc(forced), pc(fperp[f]), frames[f] in nfr))
    hist[tuple(sorted(row))] += 1
for k, v in sorted(hist.items(), key=lambda kv: -kv[1])[:15]:
    print(' ', v, 'x  per frame (forced rank, #forced, |F-perp n R|, is original frame):', k)
