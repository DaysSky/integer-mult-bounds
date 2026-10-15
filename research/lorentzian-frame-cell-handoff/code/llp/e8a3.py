"""E8 A3-parity architecture on R420's D4 partition (sec4/r420cells.json).
Source side: every line s takes 2 triangle cells (A2 planes inside its D4 block) + 1 pair cell (orthogonal pair inside its
block) forming the planes through s of an A3 (so the transposed parity identity holds: sum of the three branch
sections = R(s) + opp(s)).  Chosen triangles are used by all 3 lines, chosen pairs by both (symmetric cells).
Top: every target t uses an A3 containing t (any A3 of E8 if TOPANY=1, else its source A3); sections = perps of the two
triangles through t and of {t, opp(t)}.  Objective: unroutable (section, line) incidences (line with no source cell
inside the section), then number of distinct sections.  usage: e8a3.py timelimit [TOPANY]"""
import sys, os, json, itertools, collections, time
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); TOPANY = int(sys.argv[2]) if len(sys.argv) > 2 else 0
V = e8.V; G = e8.GI; HYP = e8.HYP; bits = e8.bits
pc = lambda m: bin(m).count('1')
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
# frames: connected components of the cell graph; blocks: closure of a frame
adj = collections.defaultdict(set)
for C in cells:
    a, b = bits(C); adj[a].add(b); adj[b].add(a)
frames = set()
for s in range(V): frames.add(frozenset({s} | adj[s]))
frames = [sorted(f) for f in frames]
assert len(frames) == 30 and all(len(f) == 4 for f in frames)
blocks = sorted(set(e8.closure(sum(1 << x for x in f))[0] for f in frames))
assert len(blocks) == 10 and all(pc(B) == 12 for B in blocks)
blk = {s: i for i, B in enumerate(blocks) for s in bits(B)}
# A2 planes (triangles) of E8
A2 = set()
for a in range(V):
    for b in e8.NEIGH[a]:
        if b < a: continue
        F, r = e8.closure((1 << a) | (1 << b))
        if pc(F) == 3: A2.add(F)
A2 = sorted(A2)
tri_of = collections.defaultdict(list)
for T in A2:
    for s in bits(T): tri_of[s].append(T)
# A3s: 6-line closures of two triangles sharing one line with an orthogonal opposite
A3 = set()
for t in range(V):
    for T1, T2 in itertools.combinations(tri_of[t], 2):
        if pc(T1 & T2) != 1: continue
        F, r = e8.closure(T1 | T2)
        if r == 3 and pc(F) == 6: A3.add(F)
A3 = sorted(A3)
log('A2', len(A2), 'A3', len(A3))
def planes_through(X, t):
    tris = [T for T in tri_of[t] if T & ~X == 0]
    opp = [e for e in bits(X) if e != t and not any(T >> e & 1 for T in tris)]
    assert len(tris) == 2 and len(opp) == 1, (len(tris), opp)
    return tris[0], tris[1], (1 << t) | (1 << opp[0])
inblock = [X for X in A3 if len(set(blk[s] for s in bits(X))) == 1]
log('A3 inside blocks', len(inblock))
M = cp_model.CpModel()
# source: per line choose an in-block A3 -> its planes through s are s's cells
src = {s: [(X, planes_through(X, s)) for X in inblock if X >> s & 1] for s in range(V)}
xs = {s: [M.NewBoolVar('') for _ in src[s]] for s in range(V)}
for s in range(V): M.AddExactlyOne(xs[s])
tri_cells = sorted(set(T for s in range(V) for X, (T1, T2, P) in src[s] for T in (T1, T2)))
pair_cells = sorted(set(P for s in range(V) for X, (T1, T2, P) in src[s]))
ct = {T: M.NewBoolVar('') for T in tri_cells}; cp_ = {P: M.NewBoolVar('') for P in pair_cells}
for s in range(V):
    for k, (X, (T1, T2, P)) in enumerate(src[s]):
        M.AddImplication(xs[s][k], ct[T1]); M.AddImplication(xs[s][k], ct[T2]); M.AddImplication(xs[s][k], cp_[P])
    # exactly 2 chosen triangles through s, exactly 1 chosen pair through s (symmetric cells)
    M.Add(sum(ct[T] for T in tri_cells if T >> s & 1) == 2)
    M.Add(sum(cp_[P] for P in pair_cells if P >> s & 1) == 1)
# top: per target choose an A3 (source A3 if not TOPANY)
if TOPANY:
    tops = {t: [(X, planes_through(X, t)) for X in A3 if X >> t & 1] for t in range(V)}
    xt = {t: [M.NewBoolVar('') for _ in tops[t]] for t in range(V)}
    for t in range(V): M.AddExactlyOne(xt[t])
else:
    tops = src; xt = xs
# section usage and routability: section S = pm(plane); line u in S routable iff some chosen source cell of u inside S
secs = sorted(set(p for t in range(V) for X, pl in tops[t] for p in pl))
use = {p: M.NewBoolVar('') for p in secs}
for t in range(V):
    for k, (X, pl) in enumerate(tops[t]):
        for p in pl: M.AddImplication(xt[t][k], use[p])
allcells = {**{T: ct[T] for T in tri_cells}, **{P: cp_[P] for P in pair_cells}}
cells_of = collections.defaultdict(list)
for Cm in allcells:
    for s in bits(Cm): cells_of[s].append(Cm)
unr = []
for p in secs:
    S = pm(p)
    for u in bits(S):
        inside = [allcells[Cm] for Cm in cells_of[u] if Cm & ~S == 0]
        z = M.NewBoolVar('')
        M.AddBoolOr(inside + [use[p].Not(), z])      # z = 1 if section used and u unroutable
        unr.append(z)
M.Minimize(100 * sum(unr) + sum(use.values()))
log('model: tri cells', len(tri_cells), 'pair cells', len(pair_cells), 'sections', len(secs), 'unr vars', len(unr))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M)
log('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    nu = sum(sv.Value(z) for z in unr); ns = sum(sv.Value(v) for v in use.values())
    log('unroutable incidences', nu, 'sections used', ns)
    sol = dict(src={s: hex(src[s][k][0]) for s in range(V) for k in range(len(src[s])) if sv.Value(xs[s][k])},
               top={t: hex(tops[t][k][0]) for t in range(V) for k in range(len(tops[t])) if sv.Value(xt[t][k])},
               tri=[hex(T) for T in tri_cells if sv.Value(ct[T])], pair=[hex(P) for P in pair_cells if sv.Value(cp_[P])])
    json.dump(sol, open('e8a3_sol_%d.json' % TOPANY, 'w'))
