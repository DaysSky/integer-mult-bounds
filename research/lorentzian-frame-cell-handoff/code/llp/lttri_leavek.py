"""Exact (CP-SAT) generalisation of lttri_leave2.py: T(X) keeps 4-k of its M11 triangle nodes and replaces the other
k by k sections (rank-3 frames through t).  The new sections must cover Need = R(t) n (left perps) minus (kept
perps), and a release needs them to cover at least one line lying in exactly one kept perp (the forced memberships
of lttri_rho5_minrel.py are such lines).  Feasible <=> some left set lets T(X) release.  k = 2 cross-checks the
exhaustive lttri_leave2.py; k = 3 keeps a single triangle node.  usage: lttri_leavek.py k target_index ..."""
import sys, json, itertools, collections
from lgeo import *
from ortools.sat.python import cp_model
sol = [tuple(tuple(T) for T in node) for node in json.load(open('lttri_design_z11.json'))]
nodes_of = collections.defaultdict(list)
for ni, node in enumerate(sol):
    for T in node: nodes_of[T].append(ni)
def Ln(k, pts): return IDX[(k, tuple(sorted(pts)))]
targets = sorted(nodes_of); k = int(sys.argv[1])
for xi in map(int, sys.argv[2:]):
    X = targets[xi]; t = Ln('T', X); R = HYP[t]
    nperp = [pm(pp(sum(1 << Ln('T', T) for T in sol[nj]))) & R for nj in nodes_of[X]]
    frames = set()
    for a, b in itertools.combinations([s for s in range(V) if s != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) == 3: frames.add(pp(m))
    frames = sorted(frames); fperp = [pm(F) & R for F in frames]
    res = []
    for left in itertools.combinations(range(4), k):
        kept = [i for i in range(4) if i not in left]
        L = 0
        for i in left: L |= nperp[i]
        K = 0
        for i in kept: K |= nperp[i]
        need = L & ~K
        rel = 0
        for i in kept:
            o = 0
            for j in kept:
                if j != i: o |= nperp[j]
            rel |= nperp[i] & ~o & ~L
        M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in frames]
        M.Add(sum(x) <= k)
        for s in bits(need): M.AddBoolOr([x[f] for f in range(len(frames)) if fperp[f] >> s & 1])
        M.AddBoolOr([x[f] for f in range(len(frames)) if fperp[f] & rel])
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 300; sv.parameters.num_workers = 4
        st = sv.Solve(M); res.append((tuple(nodes_of[X][i] for i in left), pc(need), pc(rel), sv.StatusName(st)))
    print('k', k, '| target', X, '| frames', len(frames), '| (left nodes, |Need|, |release cand|, status):', res, flush=True)
