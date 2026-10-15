"""I_{11,1} A3-parity architecture search (generalises e8a3.py; no block structure).
Each line s picks an A3 X containing s; its source cells are the planes of X through s (2 triangles + the pair
{s, opp_X(s)}).  Cells must be symmetric: a chosen triangle is used by all 3 of its lines, a chosen pair by both
(SOFT: a violation = defect, penalised).  Self-dual top: target t uses its own A3's planes (sections = their perps).
Objective: W_U * unroutable (section, line) incidences + W_D * defects + #sections.
Optional Z11 symmetry.  usage: e11a3.py timelimit [sym] [W_U] [W_D]"""
import sys, os, json, itertools, collections, time, pickle
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); SYM = int(sys.argv[2]) if len(sys.argv) > 2 else 1
WU = int(sys.argv[3]) if len(sys.argv) > 3 else 100; WD = int(sys.argv[4]) if len(sys.argv) > 4 else 100
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
d = pickle.load(open('a3compat_11.pkl', 'rb')); A3 = [sum(1 << s for s in X) for X in d['A3']]
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
    xs = bits(X)
    tris = []
    for a, b in itertools.combinations([x for x in xs if x != t], 2):
        for c in third(a, b):
            pass
    tris = set()
    for a in xs:
        if a == t: continue
        for c in third(t, a):
            if X >> c & 1: tris.add((1 << t) | (1 << a) | (1 << c))
    tris = sorted(tris)
    opp = [e for e in xs if e != t and not any(T >> e & 1 for T in tris)]
    assert len(tris) == 2 and len(opp) == 1, (len(tris), opp)
    return tris[0], tris[1], (1 << t) | (1 << opp[0])
opts = {s: [] for s in range(V)}
for X in A3:
    for s in bits(X): opts[s].append((X, planes_through(X, s)))
log('A3 options per line', collections.Counter(len(v) for v in opts.values()))
M = cp_model.CpModel()
xs = {s: [M.NewBoolVar('') for _ in opts[s]] for s in range(V)}
for s in range(V): M.AddExactlyOne(xs[s])
cellset = sorted(set(p for s in range(V) for X, pl in opts[s] for p in pl))
use_by = collections.defaultdict(list)          # (cell, line) -> literals of line choosing an A3 with that cell
for s in range(V):
    for k, (X, pl) in enumerate(opts[s]):
        for p in pl: use_by[(p, s)].append(xs[s][k])
cv = {}
for p in cellset:
    # cell active iff some line uses it; defect for each line of p not using it while active
    lits = [l for s in bits(p) for l in use_by[(p, s)]]
    a = M.NewBoolVar(''); cv[p] = a
    for l in lits: M.AddImplication(l, a)
    M.AddBoolOr(lits + [a.Not()])
defects = []
for p in cellset:
    for s in bits(p):
        u = M.NewBoolVar('')            # line s in active cell p does not use p  -> defect
        M.AddBoolOr(use_by[(p, s)] + [cv[p].Not(), u])
        defects.append(u)
# each line uses exactly 3 cells by construction; sections = active cells (self-dual top)
cells_of = collections.defaultdict(list)
for p in cellset:
    for s in bits(p): cells_of[s].append(p)
unr = []
for p in cellset:
    S = pm(p)
    for u in bits(S):
        inside = [cv[c] for c in cells_of[u] if c & ~S == 0]
        z = M.NewBoolVar('')
        M.AddBoolOr(inside + [cv[p].Not(), z]); unr.append(z)
if SYM:
    perm = [(i + 1) % n for i in range(n)]
    idx = {(s, X): k for s in range(V) for k, (X, pl) in enumerate(opts[s])}
    for s in range(V):
        s2 = img_line(s, perm)
        for k, (X, pl) in enumerate(opts[s]):
            M.Add(xs[s][k] == xs[s2][idx[(s2, act(X, perm))]])
M.Minimize(WU * sum(unr) + WD * sum(defects) + sum(cv.values()))
log('model: cells', len(cellset), 'unr vars', len(unr), 'defect vars', len(defects))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
log('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    nu = sum(sv.Value(z) for z in unr); nd = sum(sv.Value(z) for z in defects); ns = sum(sv.Value(v) for v in cv.values())
    log('unroutable', nu, 'defects', nd, 'sections (active cells)', ns,
        'by size', collections.Counter(pc(p) for p in cellset if sv.Value(cv[p])))
    sol = {s: hex(opts[s][k][0]) for s in range(V) for k in range(len(opts[s])) if sv.Value(xs[s][k])}
    json.dump(sol, open('e11a3_sol_%d.json' % SYM, 'w'))
