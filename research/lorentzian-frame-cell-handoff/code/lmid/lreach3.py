"""Refined RIGOROUS one-level per-cell value.  A register at node N reaches the lines of ONE plane Q inside perp(N)
(its section Q-perp has users = lines of Q: 3 for an A2 plane, 2 for an orthogonal pair).  k registers reach at most
reach(k) <= min(b, 2k + min(k, alpha)) targets, alpha = max number of pairwise DISJOINT A2 planes inside perp(N) (a plane
adding 3 new lines is disjoint from all earlier ones).  Lines fed <= min(a, 2k).  So
   incidences(N) <= k * g(N),  g(N) = max_k min(a, 2k) * min(b, 2k + min(k, alpha)) / k.
DFS over N = pp(system cells) as in lreach2 (prune 2b <= best, since g <= min(3a, 2b)).
usage: lreach3.py SYSTEM.json"""
import sys, os, json, collections, time, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, g as geo
from ortools.sat.python import cp_model
pc = lambda m: bin(m).count('1')
G = geo.G
cov = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
PM = {}
def pm(m):
    r = PM.get(m)
    if r is None:
        r = (1 << V) - 1
        for s in bits(m): r &= HYP[s]
        PM[m] = r
    return r
# A2 planes: triples of lines {x, y, z} pairwise non-orthogonal and dependent (z = +-x +- y)
A2 = []
L = geo.L
for x in range(V):
    for y in range(x + 1, V):
        if G[x, y] == 0: continue
        for z in range(y + 1, V):
            if G[x, z] == 0 or G[y, z] == 0: continue
            # dependent: z = s1 x + s2 y
            for s1 in (1, -1):
                for s2 in (1, -1):
                    if (L[z] == s1 * L[x] + s2 * L[y]).all() or (L[z] == -(s1 * L[x] + s2 * L[y])).all():
                        A2.append((1 << x) | (1 << y) | (1 << z))
A2 = sorted(set(A2))
print('A2 planes', len(A2), flush=True)
ALPHA = {}
def alpha(P):
    r = ALPHA.get(P)
    if r is None:
        tri = [T for T in A2 if T & ~P == 0]
        if not tri: r = 0
        else:
            M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in tri]
            for u in bits(P):
                lst = [x[i] for i, T in enumerate(tri) if T >> u & 1]
                if len(lst) > 1: M.Add(sum(lst) <= 1)
            M.Maximize(sum(x)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 20; sv.Solve(M)
            r = int(sv.BestObjectiveBound() + 1e-6)
        ALPHA[P] = r
    return r
VAL = {}
def val(N):
    r = VAL.get(N)
    if r is None:
        cov_ = 0
        for C in cells:
            if C & ~N == 0: cov_ |= C
        a = pc(cov_); P = pm(N); b = pc(P)
        best = 0
        if 2 * b > 0 and a > 0:
            al = alpha(P)
            for k in range(1, 4 * b + 2):
                best = max(best, min(a, 2 * k) * min(b, 2 * k + min(k, al)) / k)
        r = (best, a, b); VAL[N] = r
    return r
out = {}; t0 = time.time()
for ci, C in enumerate(cells):
    N0 = pm(pm(C)); bestv = val(N0)[0]; arg = N0
    stack = [N0]; seen = {N0}
    while stack:
        N = stack.pop()
        v, a, b = val(N)
        if 2 * b <= bestv: continue
        if v > bestv: bestv, arg = v, N
        P = pm(N)
        for D in cells:
            if D & ~N == 0: continue
            P2 = P
            for s in bits(D): P2 &= HYP[s]
            if 2 * pc(P2) <= bestv: continue
            N2 = pm(P2)
            if N2 not in seen: seen.add(N2); stack.append(N2)
    out[ci] = (bestv, val(arg)[1], val(arg)[2], alpha(pm(arg)))
    if ci % 32 == 0: print(ci, 'best %.2f' % bestv, 'a,b,alpha', out[ci][1:], 'elapsed %.0fs' % (time.time() - t0), flush=True)
vals = [v[0] for v in out.values()]
X = 2 * sum(vals); req = sum(pc(HYP[t]) for t in range(V)) - 2 * V
print('refined per-cell values:', sorted(collections.Counter(round(v, 1) for v in vals).items()))
print('X = %.0f, required %d, deficit %.0f -> extra registers >= %d (each <= 40) -> one-level R >= %d'
      % (X, req, req - X, max(0, -(-(req - X) // 40)), 2 * len(cells) - V + max(0, -(-(req - X) // 40))))
json.dump(out, open('lreach3_%s.json' % os.path.basename(sys.argv[1]).split('.')[0], 'w'))
