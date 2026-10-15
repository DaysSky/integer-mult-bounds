"""Evaluate a consistent A3 design (line -> A3): sections = used planes; per section the users, the union of the users'
exclusive parts, the exact minimum number of proper nodes covering that union (kappa_U), its best 2-or-more cover
shareability, routability of every line of the section by design cells inside it, and an estimated register count
   sum over sections [kappa_eff(union) + (users - 1)]  (pieces + differentiators).
usage: e11eval.py design.json"""
import sys, json, itertools, collections
from lgeo import *
from ortools.sat.python import cp_model
sol = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def third(a, b):
    out = []
    if G[a][b] == 0: return out
    for sg in (1, -1):
        c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
        if c is not None and c not in (a, b): out.append(c)
    return out
def planes_through(X, t):
    tris = set()
    for a in bits(X):
        if a == t: continue
        for c in third(t, a):
            if X >> c & 1: tris.add((1 << t) | (1 << a) | (1 << c))
    tris = sorted(tris)
    opp = [e for e in bits(X) if e != t and not any(T >> e & 1 for T in tris)]
    return tris[0], tris[1], (1 << t) | (1 << opp[0])
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    for c in third(a, b): m |= 1 << c
    return m
top = {s: tuple(int(h, 16) for h in sol[s]) if isinstance(sol[s], list) else planes_through(int(sol[s], 16), s) for s in range(V)}
users = collections.defaultdict(list)
for s in range(V):
    for p in top[s]: users[p].append(s)
cells = set(users)                           # self-dual: source cells = used planes
bad = [p for p in users if sorted(users[p]) != sorted(bits(p))]
print('sections', len(users), 'inconsistent planes', len(bad), 'by size', collections.Counter(pc(p) for p in users))
cells_of = collections.defaultdict(list)
for c in cells:
    for s in bits(c): cells_of[s].append(c)
NS = {}
def sinks(N):
    if N not in NS:
        P = bits(pm(N)); NS[N] = len(set(plane_of(a, b) for i, a in enumerate(P) for b in P[i + 1:]))
    return NS[N]
def kappa_cover(S, E, p):
    parts = set()
    for x in range(V):
        if p >> x & 1: continue
        P_ = E & HYP[x]
        if P_: parts.add(P_)
    parts = sorted(parts, key=pc, reverse=True)
    maxi = []
    for c in parts:
        if not any(c & ~d == 0 for d in maxi): maxi.append(c)
    M = cp_model.CpModel(); xv = [M.NewBoolVar('') for _ in maxi]
    for u in bits(E): M.AddBoolOr([xv[k] for k, c in enumerate(maxi) if c >> u & 1])
    M.Minimize(sum(xv)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; sv.parameters.num_workers = 2
    sv.Solve(M)
    chosen = [maxi[k] for k in range(len(maxi)) if sv.Value(xv[k])]
    # shareability of the chosen cover (assign each line to the first piece containing it)
    rem = E; worst = 99.0
    for c in chosen:
        piece = c & rem; rem &= ~c
        if piece: worst = min(worst, sinks(pp(piece)) / ((pc(piece) + 1) // 2))
    return len(chosen), worst
est = 0.0; unr = 0; stats = collections.Counter()
for p, us in users.items():
    S = pm(p)
    E = 0
    for u in us:
        o = [q for q in top[u] if q != p]
        E |= S & ~pm(o[0]) & ~pm(o[1])
    k, ratio = kappa_cover(S, E, p)
    keff = k / min(1.0, ratio)
    est += keff + (len(us) - 1)
    stats[(pc(p), pc(S), len(us), pc(E), k, round(min(ratio, 9), 2))] += 1
    for u in bits(S):
        if not any(c & ~S == 0 for c in cells_of[u]): unr += 1
print('estimated registers %.1f -> R ~ %.1f ; unroutable (section,line) %d' % (est, est - 220, unr))
for k, v in sorted(stats.items()): print('   (plane, |S|, users, |E union|, kappa, worst sinks/need):', k, 'x', v)
