"""Exact CP-SAT: does I_{11,1} admit a good-frame source system (every line picks one good 4-frame; cells = all arcs
a->b, b in F(a)) that is FULLY ROUTABLE for the own-frame top (R420's property: for every system cell C and every line
u in perp(C), some system cell D containing u lies inside perp(C))?  Optional symmetry (GRP=11: Z11-invariant
systems, GRP=1: none).  Objective: minimise defects (arcs a->b with a not in F(b)); SOFT=1 minimises unroutable pairs
instead of requiring zero.  usage: fru0.py timelimit [workers]"""
import sys, os, json, collections, itertools, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lcell'))
os.environ.setdefault('GRP', '11')
from lbase import V, bits, HYP, goodframes, PERMS, act
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 4
SOFT = os.environ.get('SOFT') == '1'
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
FR = goodframes()
frames_of = collections.defaultdict(list)
for F in FR:
    for s in bits(F): frames_of[s].append(F)
perm_list = [list(range(V))] if os.environ.get('NOSYM') == '1' else PERMS
def img_line(s, p): return p[s]
# orbit representatives of lines
def canon_line(s): return min(p[s] for p in perm_list)
# frame variables only for representative lines; others by symmetry: x[a,F] == x[p(a), p(F)]
M = cp_model.CpModel()
X = {}
rep_of = {}; perm_to = {}
for s in range(V):
    best = None
    for p in perm_list:
        if best is None or p[s] < best[0]: best = (p[s], p)
    r, p = best; rep_of[s] = r; perm_to[s] = p     # p maps s -> r
inv = {}
def invperm(p):
    q = [0] * V
    for i, j in enumerate(p): q[j] = i
    return q
reps = sorted(set(rep_of.values()))
for r in reps:
    for F in frames_of[r]: X[(r, F)] = M.NewBoolVar('')
    M.AddExactlyOne([X[(r, F)] for F in frames_of[r]])
def xv(a, F):
    """literal 'line a uses frame F'"""
    p = perm_to[a]; r = rep_of[a]
    return X[(r, act(F, p))]
# arc variables arc[a,b] = OR_{F containing a,b} x[a,F] (exactly-one -> sum)
ARC = {}
def arc(a, b):
    key = (a, b)
    if key not in ARC:
        p = perm_to[a]; r = rep_of[a]; b2 = p[b]
        k2 = (r, b2)
        if k2 not in ARC:
            v = M.NewBoolVar('')
            fs = [X[(r, F)] for F in frames_of[r] if F >> b2 & 1]
            if fs: M.Add(sum(fs) == v)
            else: M.Add(v == 0)
            ARC[k2] = v
        ARC[key] = ARC[k2]
    return ARC[key]
orth = [set(bits(HYP[t])) for t in range(V)]
# potential cells = orthogonal pairs lying in a common good frame
pot = set()
for F in FR:
    for a, b in itertools.combinations(bits(F), 2): pot.add((1 << a) | (1 << b))
log('potential cells', len(pot))
# cell-active literal
CA = {}
def cell_active(C):
    if C not in CA:
        a, b = bits(C); v = M.NewBoolVar('')
        M.AddBoolOr([arc(a, b), arc(b, a)]).OnlyEnforceIf(v)
        M.AddImplication(arc(a, b), v); M.AddImplication(arc(b, a), v)
        CA[C] = v
    return CA[C]
pot_of = collections.defaultdict(list)
for C in pot:
    for s in bits(C): pot_of[s].append(C)
# routability: only cell-orbit representatives needed (constraints are symmetric)
def canon_cell(C):
    return min(act(C, p) for p in perm_list)
cell_reps = sorted(set(canon_cell(C) for C in pot))
log('cell orbit reps', len(cell_reps))
unr = []
if os.environ.get('NOROUTE') == '1': cell_reps = []
for C in cell_reps:
    S = HYP[bits(C)[0]] & HYP[bits(C)[1]]
    ca = cell_active(C)
    for u in bits(S):
        Ds = [D for D in pot_of[u] if D & ~S == 0]
        lits = [cell_active(D) for D in Ds]
        if SOFT:
            z = M.NewBoolVar('')       # z = unroutable pair
            M.AddBoolOr(lits + [ca.Not(), z])
            unr.append(z)
        else:
            M.AddBoolOr(lits + [ca.Not()])
log('constraints built; arcs', len(ARC), 'cells', len(CA))
defects = []
for r in reps:
    for b in range(V):
        if b == r: continue
        d = M.NewBoolVar('')
        M.AddBoolOr([arc(r, b).Not(), arc(b, r), d])     # d >= arc(r,b) and not arc(b,r)
        defects.append(d)
if SOFT: M.Minimize(sum(unr) * 1000 + sum(defects))
else: M.Minimize(sum(defects))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = W
sv.parameters.log_search_progress = False
st = sv.Solve(M)
log('status', sv.StatusName(st), 'objective', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sysF = {}
    for a in range(V):
        for F in frames_of[a]:
            if sv.Value(xv(a, F)): sysF[a] = F
    json.dump({str(k): v for k, v in sysF.items()}, open('fru0_sol_%s%s.json' % ('nosym' if os.environ.get('NOSYM') == '1' else os.environ['GRP'], '_noroute' if os.environ.get('NOROUTE') == '1' else ''), 'w'))
    if SOFT: log('unroutable pairs (per orbit rep cell) =', sum(sv.Value(z) for z in unr))
