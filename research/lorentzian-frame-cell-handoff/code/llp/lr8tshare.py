"""Sharing-maximising Z11 cover design.  T reps: covers (exhaustive lists) whose 4 nodes all have >= MINT usable T
users (lr8usable census); P reps: covers whose nodes all have >= MINP usable P users.  CP-SAT picks one cover per rep
minimising the number of used node orbits (no part model).  Saves a pool file with exactly the chosen covers (one
per line, r8covers format) for the exact layer (lr8z11.py index 0).  usage: lr8tshare.py MINT MINP NMAX timelimit"""
import sys, pickle, itertools, random, collections, time, json, os
from lgeo import *
from ortools.sat.python import cp_model
MINT, MINP, NMAX, TL = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); random.seed(5)
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
def inv(p):
    q = [0] * n
    for i, x in enumerate(p): q[x] = i
    return q
tabs = {}; full = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    fr = set()
    for a, b in itertools.combinations([x for x in range(V) if x != t], 2):
        m = (1 << t) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        fr.add(pp(m))
    canon_of = {F: canon((1 << t, F)) for F in fr}
    tabs[kind] = {canon_of[F1][0]: len(c) for F1, c in D['covers'].items()}
    for F in fr: tabs[kind].setdefault(canon_of[F][0], 0)
    full[kind] = (t, D, fr, canon_of)
usable = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    for F1 in D['covers']:
        usable[canon_of[F1][0]] = (sum(1 for b in bits(F1) if KIND[b] == 'P' and tabs['P'][canon((1 << b, F1))[0]] > 0),
                                   sum(1 for b in bits(F1) if KIND[b] == 'T' and tabs['T'][canon((1 << b, F1))[0]] > 0))
pools = {}
for kind in ('P', 'T'):
    t, D, fr, canon_of = full[kind]
    rep_of = {canon_of[F1][0]: F1 for F1 in D['covers']}
    allc = set()
    for F in fr:
        cf, pF = canon_of[F]; F1 = rep_of.get(cf)
        if F1 is None: continue
        p1 = canon_of[F1][1]; ipF = inv(pF); g = [ipF[p1[x]] for x in range(n)]
        for c in D['covers'][F1]: allc.add(tuple(sorted(act(X, g) for X in c)))
    idx = 1 if kind == 'T' else 0; thr = MINT if kind == 'T' else MINP
    good = [c for c in allc if all(usable.get(canon_of[F][0], (0, 0))[idx] >= thr for F in c)]
    log(kind, 'covers', len(allc), 'eligible', len(good))
    pools[kind] = (t, good)
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
covs = {}
for r in reps:
    t, good = pools[KIND[r]]
    src = list(SUPP[t]); dst = list(SUPP[r])
    rest_s = [x for x in range(n) if x not in src]; rest_d = [x for x in range(n) if x not in dst]
    perm = [None] * n
    for a, b in zip(src + rest_s, dst + rest_d): perm[a] = b
    smp = random.sample(good, min(NMAX, len(good)))
    covs[r] = [tuple(sorted(act(X, perm) for X in c)) for c in smp]
def fkey(F): return min(rotm(F, k) for k in range(n))
M = cp_model.CpModel(); USED = {}; YS = {}
for r in reps:
    ys = [M.NewBoolVar('') for _ in covs[r]]; M.AddExactlyOne(ys); YS[r] = ys
    for y, c in zip(ys, covs[r]):
        for F in c:
            k = fkey(F)
            if k not in USED: USED[k] = M.NewBoolVar('')
            M.AddImplication(y, USED[k])
M.Minimize(sum(USED.values()))
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        log('used node orbits %d (x11 = %d nodes)  bound %.1f' % (self.ObjectiveValue(), 11 * self.ObjectiveValue(), self.BestObjectiveBound()))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 4
st = sv.Solve(M, CB()); log('status', sv.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    chosen = {r: [c for c, y in zip(covs[r], YS[r]) if sv.Value(y)][0] for r in reps}
    allc = {t: [tuple(sorted(rotm(F, orb[t][1]) for F in chosen[reps[orb[t][0]]]))] for t in range(V)}
    out = os.environ.get('OUT', 'r8tshare.pkl'); pickle.dump(allc, open(out, 'wb'))
    json.dump({str(r): 0 for r in reps}, open(out.replace('.pkl', '_sel.json'), 'w'))
    users = collections.Counter(F for t in range(V) for F in allc[t][0])
    log('saved', out, '| nodes', len(users), '| users per node', sorted(collections.Counter(users.values()).items()))
