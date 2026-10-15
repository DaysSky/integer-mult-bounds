"""A2-parity top design.  For every target t: all triples of plane sections through t whose section totals XOR to
1_{R(t)} + one line d (defect 1), plus the frame triples (defect 3: good-frame mates) as fallback.  CP-SAT: choose one
triple per target minimising the number of distinct sections used (each used section must be assembled once), with
optional symmetry (cyclic group on points).
usage: ltopA2.py n(9|11) timelimit [allow_frames(0|1)] [sym(0|1)]   -> topA2_n.json"""
import sys, os, itertools, collections, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lword'))
from geom import Geom
import numpy as np
from ortools.sat.python import cp_model
n = int(sys.argv[1]); TL = float(sys.argv[2]); FR = int(sys.argv[3]) if len(sys.argv) > 3 else 1
SYM = int(sys.argv[4]) if len(sys.argv) > 4 else 1
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
w = np.array([1] * n + [3])
NULLW = (n - 9 == 0)
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    if G[a][b] != 0:
        for sg in (1, -1):
            v = g.L[a] - sg * g.L[b]
            for k in (range(-3, 4) if NULLW else (0,)):
                c = VEC.get(tuple(int(x) for x in (v + k * w)))
                if c is not None and c not in (a, b): m |= 1 << c
    return m
def img_line(s, perm):
    return g.idx[(g.kind[s], tuple(sorted(perm[i] for i in g.supp[s])))]
def act(m, perm):
    r = 0
    for s in bits(m): r |= 1 << img_line(s, perm)
    return r
def triples_of(t):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    S = [pm(p) for p in pl]
    out = []
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        D = S[i] ^ S[j] ^ S[k] ^ R
        d = pc(D)
        if d == 1 or (FR and d == 3 and all(G[x][y] == 0 for x, y in itertools.combinations(bits(D) + [t], 2))):
            out.append((pl[i], pl[j], pl[k], D))
    return out
# representatives: one line per S_n orbit (P and T)
reps = {}
for t in range(V):
    if g.kind[t] not in reps: reps[g.kind[t]] = t
TR = {}
for kd, t in reps.items():
    TR[t] = triples_of(t); log('rep', kd, t, 'triples', len(TR[t]), collections.Counter(pc(x[3]) for x in TR[t]))
allT = {}
for t in range(V):
    r = reps[g.kind[t]]
    # permutation of points mapping supp(r) -> supp(t)
    a = list(g.supp[r]); b = list(g.supp[t])
    rest_a = [i for i in range(n) if i not in a]; rest_b = [i for i in range(n) if i not in b]
    perm = [0] * n
    for x, y in zip(a + rest_a, b + rest_b): perm[x] = y
    assert img_line(r, perm) == t
    allT[t] = [(act(p1, perm), act(p2, perm), act(p3, perm), act(D, perm)) for p1, p2, p3, D in TR[r]]
secs = {}
for t in range(V):
    for tr in allT[t]:
        for p in tr[:3]:
            if p not in secs: secs[p] = len(secs)
log('candidate sections', len(secs))
M = cp_model.CpModel()
X = {}
for t in range(V):
    X[t] = [M.NewBoolVar('') for _ in allT[t]]
    M.AddExactlyOne(X[t])
use = [M.NewBoolVar('') for _ in secs]
users = collections.defaultdict(list)
for t in range(V):
    for k, tr in enumerate(allT[t]):
        for p in tr[:3]:
            M.AddImplication(X[t][k], use[secs[p]])
if SYM:
    # cyclic symmetry on points (Z_n): x -> x+1
    perm = [(i + 1) % n for i in range(n)]
    for t in range(V):
        t2 = img_line(t, perm)
        idx2 = {tr: k for k, tr in enumerate(allT[t2])}
        for k, tr in enumerate(allT[t]):
            im = (act(tr[0], perm), act(tr[1], perm), act(tr[2], perm), act(tr[3], perm))
            # triple order may differ: match as a set
            key = None
            for perm3 in itertools.permutations(im[:3]):
                if perm3 + (im[3],) in idx2: key = idx2[perm3 + (im[3],)]; break
            assert key is not None
            M.Add(X[t][k] == X[t2][key])
M.Minimize(sum(use))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
log('status', sv.StatusName(st), 'sections', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    choice = {}
    for t in range(V):
        for k, tr in enumerate(allT[t]):
            if sv.Value(X[t][k]): choice[t] = tr
    cnt = collections.Counter()
    for t, tr in choice.items():
        for p in tr[:3]: cnt[p] += 1
    typ = collections.Counter((pc(p), cnt[p]) for p in cnt)
    log('sections used', len(cnt), 'by (plane lines, users):', sorted(typ.items()),
        'defect sizes', collections.Counter(pc(tr[3]) for tr in choice.values()))
    json.dump({str(t): [hex(x) for x in tr] for t, tr in choice.items()}, open('topA2_%d.json' % n, 'w'))
