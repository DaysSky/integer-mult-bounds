"""Register-slot matching for a rank-8 frame-section top: every line u has 3 branch registers, one per cell of an
exact union cover of R(u) (covers3.pkl: pair cells {u,f}); every delivered slot (target b, section frame F) takes
exactly one register whose cell lies in F-perp (cell _|_ every line of F); zero waste = perfect assignment.
CP-SAT chooses each line's cover and the assignment.  usage: lr8slots.py design.json timelimit
design.json: {target: {'secs': [frame hex x4], 'in': frame hex}} (lr8design2.json format; non-rep targets by Z11)"""
import sys, json, pickle, collections
from lgeo import *
from ortools.sat.python import cp_model
D = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}; TL = float(sys.argv[2])
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
def rotk(x, k):
    for _ in range(k % n): x = rot[x]
    return x
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotk(s, k)
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
slots = []
for b in range(V):
    o, k = orb[b]; r = reps[o]
    d = D[r]; Fin = rotm(int(d['in'], 16), k)
    for h in d['secs']:
        F = rotm(int(h, 16), k)
        if F != Fin: slots.append((b, F))
print('delivered slots', len(slots))
cov = pickle.load(open('covers3.pkl', 'rb'))
M = cp_model.CpModel()
ych = {u: [M.NewBoolVar('') for _ in cov[u]] for u in range(V)}
for u in range(V): M.AddExactlyOne(ych[u])
cellopt = collections.defaultdict(list)      # (u, f) -> cover literals using cell {u,f}
for u in range(V):
    for i, (ms, gd) in enumerate(cov[u]):
        for f in ms: cellopt[(u, f)].append(ych[u][i])
asg = collections.defaultdict(list); per_cell = collections.defaultdict(list)
for j, (b, F) in enumerate(slots):
    P = pm(F); lits = []
    for (u, f), ls in cellopt.items():
        if P >> u & 1 and P >> f & 1:
            z = M.NewBoolVar(''); lits.append(z); per_cell[(u, f)].append(z)
    M.AddExactlyOne(lits) if lits else M.AddBoolOr([])
for (u, f), zs in per_cell.items():
    used = M.NewBoolVar(''); M.AddBoolOr(cellopt[(u, f)]).OnlyEnforceIf(used); M.AddBoolAnd([l.Not() for l in cellopt[(u, f)]]).OnlyEnforceIf(used.Not())
    M.Add(sum(zs) == used)                    # each used cell register serves exactly one slot
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M)
print('status', sv.StatusName(st))
