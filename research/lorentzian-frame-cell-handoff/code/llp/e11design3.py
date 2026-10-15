"""Z11-quotient consistent self-dual design for I_{11,1} WITH routability (generalises e11design2.py).
Each line picks a defect-1 triple (A3 triple or TT* triple) of planes through it = its top AND its source cells.
Consistency: a used plane is used by all its lines.  Routability: for every used section S = pm(plane) and every
line u in S some used plane (cell) through u lies inside S; violations z are penalised (weight W).
Variables live on Z11 orbits (20 line orbits, 1800 plane orbits), so the model is 11x smaller than e11a3.py.
Objective: sum of option costs (shareability model, as e11design2) * 100 + W * unroutable orbit-incidences.
usage: e11design3.py timelimit [W] [hint.json]   -> e11design3_sol.json ({line: [plane hex x3]})"""
import sys, json, itertools, collections, time
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 300
HINT = sys.argv[3] if len(sys.argv) > 3 else None
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
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
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    for c in third(a, b): m |= 1 << c
    return m
RATIO = {(3, 85, 29): 0.78, (2, 70, 14): 21.5, (3, 85, 43): 0.54, (2, 56, 14): 6.8, (3, 71, 29): 0.78,
         (3, 85, 38): 0.54, (3, 71, 24): 1.17, (2, 66, 19): 4.25, (2, 70, 28): 0.78, (2, 66, 29): 1.86,
         (2, 61, 24): 0.75, (2, 66, 30): 0.44, (3, 71, 34): 0.78, (2, 56, 19): 4.25}
def cost(P, S, E):
    r = RATIO.get((pc(P), pc(S), pc(E)), 0.6)
    u = pc(P)
    return (2.0 / min(1.0, r)) / u + (u - 1) / u
# Z11 rotation on lines
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
def rotm(m, k=1):
    for _ in range(k % n):
        r = 0
        for s in bits(m): r |= 1 << rot[s]
        m = r
    return m
# line orbits
lorb = {}; reps = []
for s in range(V):
    if s in lorb: continue
    o = len(reps); reps.append(s); x = s
    for k in range(n):
        lorb[x] = (o, k); x = rot[x]          # rot^k(rep) = x  -> x maps to rep by rot^(-k)
assert len(reps) == 20 and len(lorb) == V
# all planes and plane orbits
planes = sorted(set(plane_of(a, b) for a in range(V) for b in range(a + 1, V) if G[a][b] == 0 or plane_of(a, b)))
porb = {}; prep = []
for p in planes:
    if p in porb: continue
    o = len(prep); prep.append(p); x = p
    for k in range(n):
        porb[x] = o; x = rotm(x)
log('planes', len(planes), 'plane orbits', len(prep))
planes_through = collections.defaultdict(list)
for p in planes:
    for s in bits(p): planes_through[s].append(p)
# options for rep lines: all defect-1 triples
def triples(t):
    R = HYP[t]
    pl = sorted(set(planes_through[t]))
    Sm = [pm(p) for p in pl]; out = []
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        if pc(Sm[i] ^ Sm[j] ^ Sm[k] ^ R) == 1: out.append((pl[i], pl[j], pl[k]))
    return out
opts = []
for r in reps:
    TR = triples(r); lst = []
    for pl in TR:
        S = {p: pm(p) for p in pl}; c = 0.0
        for p in pl:
            o2 = [q for q in pl if q != p]
            c += cost(p, S[p], S[p] & ~S[o2[0]] & ~S[o2[1]])
        lst.append((pl, c))
    opts.append(lst)
log('options per rep line', [len(x) for x in opts])
M = cp_model.CpModel()
x = [[M.NewBoolVar('') for _ in opts[o]] for o in range(20)]
for o in range(20): M.AddExactlyOne(x[o])
# use(p, s): rotate (p, s) so that s becomes its rep
by_rep_plane = [collections.defaultdict(list) for _ in range(20)]
for o in range(20):
    for k, (pl, c) in enumerate(opts[o]):
        for p in pl: by_rep_plane[o][p].append(x[o][k])
def use_expr(p, s):
    o, k = lorb[s]
    p2 = rotm(p, -k % n)
    assert p2 >> reps[o] & 1
    return by_rep_plane[o].get(p2, [])
U = {}
for po, P in enumerate(prep):
    lits = [use_expr(P, s) for s in bits(P)]
    if any(not l for l in lits):
        # some line of P never uses P -> P unused by consistency
        for l in lits:
            for v_ in l: M.Add(v_ == 0)
        continue
    u = M.NewBoolVar(''); U[po] = u
    for l in lits: M.Add(sum(l) == u)
log('usable plane orbits', len(U))
# routability on orbit reps of sections
unr = []
for po, u in U.items():
    S = pm(prep[po])
    for w in bits(S):
        cand = sorted(set(porb[c] for c in planes_through[w] if c & ~S == 0 and porb[c] in U))
        z = M.NewBoolVar('')
        M.AddBoolOr([U[c] for c in cand] + [u.Not(), z]); unr.append(z)
log('unroutable vars', len(unr))
M.Minimize(sum(int(round(100 * c)) * x[o][k] for o in range(20) for k, (pl, c) in enumerate(opts[o])) + W * sum(unr))
if HINT:
    hs = {int(k): tuple(int(h, 16) for h in v) for k, v in json.load(open(HINT)).items()}
    for o in range(20):
        want = tuple(sorted(hs[reps[o]]))
        for k, (pl, c) in enumerate(opts[o]): M.AddHint(x[o][k], int(tuple(sorted(pl)) == want))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
log('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    nu = sum(sv.Value(z) for z in unr)
    tot = 11 * sum(c for o in range(20) for k, (pl, c) in enumerate(opts[o]) if sv.Value(x[o][k]))
    log('unroutable orbit incidences', nu, '(x11 =', 11 * nu, ') estimated registers', round(tot, 1), '-> R ~', round(tot - 220, 1))
    sol = {}
    for s in range(V):
        o, k = lorb[s]
        kk = next(j for j in range(len(opts[o])) if sv.Value(x[o][j]))
        sol[s] = [hex(rotm(p, k)) for p in opts[o][kk][0]]
    json.dump(sol, open('e11design3_sol.json', 'w'))
