"""IDENTICAL-PARTS design test (Z11-symmetric CP-SAT).  Every used node F carries ONE part W_F (subset of F-perp), taken
by all its users; each line t uses 4 nodes (one of its candidate covers) and R(t) must be the DISJOINT union of the
W_F of its nodes.  Hosting is then automatic (in-chain part = a delivered part) and the node needs only
#rank-5 pieces(W_F) registers.  Pool: per Z11 rep the NPOOL covers of smallest total perp overlap (full exhaustive
lists).  Objective: feasibility first; reports the solution and per-node piece counts are checked afterwards.
usage: lr8identical.py NPOOL timelimit"""
import sys, pickle, itertools, collections, time, json, os
from lgeo import *
from ortools.sat.python import cp_model
NPOOL = int(sys.argv[1]); TL = float(sys.argv[2]); t0 = time.time()
PARITY = int(os.environ.get('PARITY', '0'))   # 1: each line of R(t) in an ODD number of its nodes' parts (F2 sum)
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
rotp = [list(range(V))]
for k in range(1, n): rotp.append([rot[x] for x in rotp[-1]])
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotp[k % n][s]
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
pool = {}
POOLF = os.environ.get('POOL')
for kind in (() if POOLF else ('P', 'T')):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {F: canon((1 << t, F)) for F in fr}
    rep_of = {canon_of[F1][0]: F1 for F1 in D['covers']}
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]; F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]; ipF = inv(pF); g = [ipF[p1[x]] for x in range(n)]
        for c in D['covers'][F1]: allc.add(tuple(sorted(act(X, g) for X in c)))
    allc = sorted(allc, key=lambda c: (sum(pc(pm(F) & R) for F in c), c))
    pool[kind] = (t, allc)
    log(kind, 'covers', len(allc))
covs = {}
import random; random.seed(3)
if POOLF:
    _pl = pickle.load(open(POOLF, 'rb'))
    for r in reps: covs[r] = _pl[r][:NPOOL]
for r in ([] if POOLF else reps):
    t, allc = pool[KIND[r]]
    src = list(SUPP[t]); dst = list(SUPP[r])
    rest_s = [x for x in range(n) if x not in src]; rest_d = [x for x in range(n) if x not in dst]
    perm = [None] * n
    for a, b in zip(src + rest_s, dst + rest_d): perm[a] = b
    # smallest-overlap covers plus a random sample of the rest
    chosen = allc[:NPOOL // 2] + random.sample(allc[NPOOL // 2:], NPOOL - NPOOL // 2)
    covs[r] = [tuple(sorted(act(X, perm) for X in c)) for c in chosen]
def fkey(F):
    """canonical Z11 representative of frame F and the rotation k with F = rotm(Fc, k)"""
    best = None
    for k in range(n):
        Fc = rotm(F, -k)
        if best is None or Fc < best[0]: best = (Fc, k)
    return best
M = cp_model.CpModel()
W = {}; YS = {}; USED = {}
def wvar(F, u):
    Fc, k = fkey(F); uc = rotp[-k % n][u]
    key = (Fc, uc)
    if key not in W: W[key] = M.NewBoolVar('')
    return W[key]
for ri, r in enumerate(reps):
    ys = [M.NewBoolVar('') for _ in covs[r]]; M.AddExactlyOne(ys); YS[r] = ys
    xs = collections.defaultdict(list)
    for y, c in zip(ys, covs[r]):
        for F in c: xs[F].append(y)
    X = {}
    for F, yl in xs.items():
        x = M.NewBoolVar(''); M.Add(x == sum(yl)); X[F] = x
    PM = {F: pm(F) for F in X}
    for u in bits(HYP[r]):
        zs = []
        for F, x in X.items():
            if not PM[F] >> u & 1: continue
            w = wvar(F, u); z = M.NewBoolVar('')
            M.AddBoolAnd([x, w]).OnlyEnforceIf(z); M.AddBoolOr([x.Not(), w.Not(), z])
            zs.append(z)
        if PARITY:
            kk = M.NewIntVar(0, len(zs) // 2, ''); M.Add(sum(zs) == 2 * kk + 1)
        else:
            M.AddExactlyOne(zs)
    # a used node's part must be non-empty for this user (else it is not a 4-cover use)
    for F, x in X.items():
        M.AddBoolOr([wvar(F, u) for u in bits(PM[F])]).OnlyEnforceIf(x)
        Fc, k = fkey(F)
        if Fc not in USED: USED[Fc] = M.NewBoolVar('')
        M.AddImplication(x, USED[Fc])
log('model: w vars', len(W))
if os.environ.get('SHARE', '1') == '1': M.Minimize(sum(USED.values()))
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        log('used node orbits %d (x11 = %d nodes for 880 uses)  bound %.1f' % (self.ObjectiveValue(), 11 * self.ObjectiveValue(), self.BestObjectiveBound()))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = int(os.environ.get('NW', '4'))
st = sv.Solve(M, CB())
log('status', sv.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = {'covers': {}, 'W': {}}
    for r in reps:
        c = [cv for cv, y in zip(covs[r], YS[r]) if sv.Value(y)][0]
        sol['covers'][str(r)] = [hex(F) for F in c]
    for (Fc, uc), w in W.items():
        if sv.Value(w): sol['W'][hex(Fc)] = hex(int(sol['W'].get(hex(Fc), '0x0'), 16) | (1 << uc))
    json.dump(sol, open(os.environ.get('OUT', 'lr8identical_sol.json'), 'w'))
    log('saved')
