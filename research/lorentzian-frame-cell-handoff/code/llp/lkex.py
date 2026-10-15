"""kappa_any(E): minimum number of proper closed nodes inside section S covering S's exclusive part E (union cover),
for every section of every 3-section top (frame triples, defect-1 triples) of the representative targets.  Maximal
proper closed subsets of S are S & HYP[x] (x a line not in the plane), so the cover uses those.  Exact (CP-SAT).
Also kappa for 2-user/3-user common exclusive parts is not needed for the lower bound."""
import itertools, collections
from lgeo import *
from ortools.sat.python import cp_model
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
CACHE = {}
def kappa(S, E, p):
    key = (S, E)
    if key in CACHE: return CACHE[key]
    cands = set()
    for x in range(V):
        if p >> x & 1: continue
        N = S & HYP[x]
        if N != S and N & E: cands.add(N & E)
    cands = sorted(cands, key=pc, reverse=True)
    maxi = []
    for c in cands:
        if not any(c & ~d == 0 for d in maxi): maxi.append(c)
    M = cp_model.CpModel(); xs = [M.NewBoolVar('') for _ in maxi]
    for u in bits(E): M.AddBoolOr([xs[k] for k, c in enumerate(maxi) if c >> u & 1])
    M.Minimize(sum(xs)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 30; sv.parameters.num_workers = 2
    st = sv.Solve(M)
    r = (int(sv.ObjectiveValue()), int(sv.BestObjectiveBound()), max(pc(c) for c in maxi))
    CACHE[key] = r; return r
for t in (0, 100):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = {p: pm(p) for p in pl}
    stat = collections.Counter()
    for i, j, k in itertools.combinations(pl, 3):
        D = S[i] ^ S[j] ^ S[k] ^ R; d = pc(D)
        if not (d == 1 or (d == 3 and all(G[x][y] == 0 for x, y in itertools.combinations(bits(D) + [t], 2)))): continue
        for a, b, c in ((i, j, k), (j, i, k), (k, i, j)):
            E = S[a] & ~S[b] & ~S[c]
            kv = kappa(S[a], E, a)
            stat[(d, pc(a), pc(S[a]), pc(E), kv)] += 1
    print('target', KIND[t], flush=True)
    for key, v in sorted(stat.items()): print('   (defect, plane, |S|, |E|, (kappa, bound, max piece)):', key, 'x', v, flush=True)
