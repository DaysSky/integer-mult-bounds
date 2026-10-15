"""A3 subsystems (6 lines, 4 A2 triangles, 3 orthogonal opposite pairs) and A3 partitions (exact covers) via CP-SAT.
Also verifies that each A3 gives every line t a defect-1 parity triple (two triangles through t + cell {t, opp(t)},
defect = opp(t)).   usage: la3.py n(9|11) timelimit [sym(0|1)]  -> a3part_n.json"""
import sys, os, itertools, collections, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
from ortools.sat.python import cp_model
n = int(sys.argv[1]); TL = float(sys.argv[2]); SYM = int(sys.argv[3]) if len(sys.argv) > 3 else 0
t0_ = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0_), *a, flush=True)
g = Geom(n); V = g.V; G = g.G; HYP = g.HYP; bits = g.bits
pc = lambda m: bin(m).count('1')
FULL = (1 << V) - 1
def pm(m):
    r = FULL
    for s in bits(m): r &= HYP[s]
    return r
VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
w = np.array([1] * n + [3]); NULLW = (n == 9)
def third(a, b):
    """lines c with c = +-a +- b (A2 completion), modulo w for E8"""
    out = set()
    if G[a][b] == 0: return out
    for sg in (1, -1):
        v = g.L[a] - sg * g.L[b]
        for k in (range(-3, 4) if NULLW else (0,)):
            c = VEC.get(tuple(int(x) for x in (v + k * w)))
            if c is not None and c not in (a, b): out.add(c)
    return out
A2 = set()
for a in range(V):
    for b in range(a + 1, V):
        for c in third(a, b): A2.add(frozenset((a, b, c)))
A2 = [tuple(sorted(x)) for x in A2]
log('A2 planes', len(A2))
tri_of = collections.defaultdict(list)
for T in A2:
    for x in T: tri_of[x].append(T)
# A3: two A2s sharing exactly one line t: {t,a,b}, {t,c,d}; the other two triangles {a,?,?}... check K4 structure
A3 = set()
for t in range(V):
    for T1, T2 in itertools.combinations(tri_of[t], 2):
        s = set(T1) | set(T2)
        if len(s) != 5: continue
        a, b = [x for x in T1 if x != t]; c, d = [x for x in T2 if x != t]
        # need opposite e with {a,c,e} or {a,d,e} triangle etc.
        for (p, q), (r, s2) in (((a, c), (b, d)), ((a, d), (b, c))):
            for e in third(p, q) & third(r, s2):
                six = frozenset((t, a, b, c, d, e))
                if len(six) != 6: continue
                tris = [T for T in A2 if set(T) <= six]
                if len(tris) == 4 and G[t][e] == 0:
                    A3.add(six)
A3 = [tuple(sorted(x)) for x in A3]
log('A3 subsystems', len(A3), 'per line', collections.Counter(sum(1 for X in A3 if s in X) for s in range(V)))
# verify parity triple property on a sample
def check(X):
    six = set(X); tris = [T for T in A2 if set(T) <= six]
    for t in X:
        two = [T for T in tris if t in T]; opp = [e for e in X if e != t and all(e not in T for T in two)]
        assert len(two) == 2 and len(opp) == 1
        e = opp[0]
        S1 = pm(sum(1 << x for x in two[0])); S2 = pm(sum(1 << x for x in two[1])); S3 = pm((1 << t) | (1 << e))
        D = S1 ^ S2 ^ S3 ^ HYP[t]
        if D != (1 << e): return False
    return True
bad = sum(1 for X in A3[:200] if not check(X))
log('parity check on first 200 A3s: failures', bad)
M = cp_model.CpModel()
x = [M.NewBoolVar('') for _ in A3]
by = collections.defaultdict(list)
for i, X in enumerate(A3):
    for s in X: by[s].append(x[i])
for s in range(V): M.Add(sum(by[s]) <= 1)
if SYM:
    perm = [(i + 1) % n for i in range(n)]
    def img(s): return g.idx[(g.kind[s], tuple(sorted(perm[i] for i in g.supp[s])))]
    idx = {X: i for i, X in enumerate(A3)}
    for i, X in enumerate(A3): M.Add(x[i] == x[idx[tuple(sorted(img(s) for s in X))]])
M.Maximize(sum(x))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
k = int(sv.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
log('status', sv.StatusName(st), 'max disjoint A3s', k, 'bound', sv.BestObjectiveBound(), 'lines covered', None if k is None else 6 * k, 'of', V)
if k:
    sol = [A3[i] for i in range(len(A3)) if sv.Value(x[i])]
    json.dump(sol, open('a3part_%d.json' % n, 'w'))
