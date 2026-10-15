"""kappa(S): minimum number of SHAREABLE nodes covering all lines of section S (union cover), per plane-section type.
Node = closed line set N inside S; shareable iff #planes inside pm(N) >= ceil(|N|/2) (a node fed by cell registers needs
>= |N|/2 registers and each must leave to a distinct sink to avoid waste).  Also reports kappa with no shareability
filter and with a size cap.  Uses the concrete closed-set enumeration of each section (as in lsecside)."""
import pickle, collections, sys
from lgeo import *
from ortools.sat.python import cp_model
planes = pickle.load(open('planes.pkl', 'rb'))
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
            if c is not None and c not in (a, b): m |= 1 << c
    return m
NPL = {}
def nplanes(N):
    if N not in NPL:
        P = bits(pm(N)); NPL[N] = len(set(plane_of(a, b) for i, a in enumerate(P) for b in P[i + 1:]))
    return NPL[N]
for i, pi0 in enumerate(planes):
    S0 = pm(pi0)
    seen = set(); fr = []
    for u in bits(S0):
        N = pp(1 << u)
        if N not in seen: seen.add(N); fr.append(N)
    while fr:
        nf = []
        for N in fr:
            P = pm(N); done = set()
            for y in bits(S0 & ~N):
                P2 = P & HYP[y]
                if P2 in done: continue
                done.add(P2); N2 = pm(P2)
                if N2 not in seen: seen.add(N2); nf.append(N2)
        fr = nf
    nodes = [N for N in seen if N != S0]
    # keep only maximal-by-inclusion shareable nodes for the cover (any subset of a cover node can be used)
    def shareable(N):
        p = pc(pm(N)); need = (pc(N) + 1) // 2
        if (p - 1) // 2 >= need: return True   # planes through one fixed line of pm(N): >= (p-1)/2 distinct
        return nplanes(N) >= need
    share = [N for N in nodes if shareable(N)]
    res = {}
    for name, cand in (('any proper node', nodes), ('shareable', share)):
        # maximal elements
        cand = sorted(set(cand), key=pc, reverse=True)
        maxi = []
        for N in cand:
            if not any(N & ~M == 0 for M in maxi): maxi.append(N)
        M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in maxi]
        for u in bits(S0):
            M.AddBoolOr([x[k] for k, N in enumerate(maxi) if N >> u & 1])
        M.Minimize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 120; sv.parameters.num_workers = 2
        st = sv.Solve(M)
        res[name] = (int(sv.ObjectiveValue()), int(sv.BestObjectiveBound()), len(maxi), max(pc(N) for N in maxi))
    print('section', pc(pi0), '|', pc(S0), ':', res, flush=True)
