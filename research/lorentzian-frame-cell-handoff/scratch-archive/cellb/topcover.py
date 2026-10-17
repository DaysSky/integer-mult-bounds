"""Minimum number of rank-6 flats P ⊂ t-perp covering R(t), u covered by P iff a source cell of u lies inside P
(route-level top cost); one of them may be a plane-perp read in-chain (free).  Exact ILP per target rep (Z15)."""
import sys, json, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
import numpy as np
from ortools.sat.python import cp_model
V = e8.V
perm = json.load(open('../sec4/coxeter.json'))['perm']
def actp(m, p):
    r = 0
    for s in e8.bits(m): r |= 1 << p[s]
    return r
def perp(mask):
    m = (1 << V) - 1
    for s in e8.bits(mask): m &= e8.HYP[s]
    return m
L = np.array(e8.LINES, dtype=np.int64); n2 = int(L[0] @ L[0])
line_of = {}
for i, x in enumerate(L): line_of[tuple(x)] = i; line_of[tuple(-x)] = i
RP = [[line_of[tuple(L[i] - 2 * (L[i] @ L[r]) * L[r] // n2)] for i in range(V)] for r in range(V)]
to = {0: list(range(V))}; frontier = [0]
while frontier:
    nf = []
    for a in frontier:
        for r in range(V):
            b = RP[r][a]
            if b not in to: to[b] = [RP[r][to[a][i]] for i in range(V)]; nf.append(b)
    frontier = nf
F0 = pickle.load(open('flats6_t0.pkl', 'rb'))
if len(sys.argv) > 1:
    adj = json.load(open(sys.argv[1])); cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
else:
    cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
seen = set(); reps = []
for t in range(V):
    o = {t}; y = perm[t]
    while y != t: o.add(y); y = perm[y]
    k = min(o)
    if k not in seen: seen.add(k); reps.append(t)
res = collections.Counter()
for t in reps:
    Ps = [actp(F, to[t]) for F in F0]
    Qperp = set(perp(e8.closure((1 << t) | (1 << u))[0]) for u in range(V) if u != t)
    M = cp_model.CpModel(); d = [M.NewBoolVar('') for P in Ps]; ic = [M.NewBoolVar('') for P in Ps]
    for P, b in zip(Ps, ic):
        if P not in Qperp: M.Add(b == 0)
    M.Add(sum(ic) <= 1)
    for u in e8.bits(e8.HYP[t]):
        M.AddBoolOr([b for P, b, c in zip(Ps, d, ic) for C in cells_of[u] if C & ~P == 0] +
                    [c for P, b, c in zip(Ps, d, ic) for C in cells_of[u] if C & ~P == 0])
    M.Minimize(sum(d))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 4
    r = s.Solve(M); res[(s.StatusName(r), s.ObjectiveValue())] += 1
    print('target', t, s.StatusName(r), 'min delivered flats', s.ObjectiveValue(), flush=True)
print(dict(res))
