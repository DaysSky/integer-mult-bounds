"""Per-cell one-level value restricted to node RANK m (exhaustive over flats N = pp(cells) containing the cell with
dim(N) == m, A2-packing reach limit as in lreach3).  Output per m: list of per-cell best values.
usage: lreach4.py SYSTEM.json"""
import sys, os, json, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ['GRP'] = '11'
from lbase import V, bits, HYP, g as geo
from lw import dim
from ortools.sat.python import cp_model
pc = lambda m: bin(m).count('1')
G = geo.G; L = geo.L
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
A2 = set()
for x in range(V):
    for y in range(x + 1, V):
        if G[x, y] == 0: continue
        for z in range(y + 1, V):
            if G[x, z] == 0 or G[y, z] == 0: continue
            for s1 in (1, -1):
                for s2 in (1, -1):
                    if (L[z] == s1 * L[x] + s2 * L[y]).all() or (L[z] == -(s1 * L[x] + s2 * L[y])).all():
                        A2.add((1 << x) | (1 << y) | (1 << z))
A2 = sorted(A2)
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
        c = 0
        for C in cells:
            if C & ~N == 0: c |= C
        a = pc(c); P = pm(N); b = pc(P); best = 0
        if a and b:
            al = alpha(P)
            for k in range(1, 4 * b + 2): best = max(best, min(a, 2 * k) * min(b, 2 * k + min(k, al)) / k)
        r = (best, dim(N)); VAL[N] = r
    return r
out = collections.defaultdict(list)
t0 = time.time()
for ci, C in enumerate(cells):
    N0 = pm(pm(C)); best = collections.defaultdict(float)
    stack = [N0]; seen = {N0}
    while stack:
        N = stack.pop(); v, m = val(N)
        if v > best[m]: best[m] = v
        P = pm(N)
        dN = dim(N)
        if dN >= 8: continue                       # middle nodes have rank <= 8 (rank 9 = sections)
        cap = min([best[mm] for mm in range(dN + 1, 9)] + [10 ** 9])
        if 2 * pc(P) <= cap: continue
        for D in cells:
            if D & ~N == 0: continue
            P2 = P
            for s in bits(D): P2 &= HYP[s]
            if 2 * pc(P2) <= cap: continue
            N2 = pm(P2)
            if dim(N2) > 8: continue
            if N2 not in seen: seen.add(N2); stack.append(N2)
    for m in range(2, 10): out[m].append(best[m])
    if ci % 48 == 0: print(ci, dict((m, round(best[m], 1)) for m in sorted(best)), '%.0fs' % (time.time() - t0), flush=True)
json.dump({m: v for m, v in out.items()}, open('lreach4_%s.json' % os.path.basename(sys.argv[1]).split('.')[0], 'w'))
for m in sorted(out): print('rank', m, 'sum over cells x2 =', round(2 * sum(out[m])), 'max', max(out[m]))
