"""Z11-symmetric CP-SAT over the cover pool (r8covers.pkl), SPANNING-AWARE: each orbit representative r picks one
4-cover and one in-chain frame; minimise  #unhosted rep orbits + #frame orbits whose ONLY delivered user has an
exclusive part of rank 8 (the part then spans the rank-8 section: assembly leftover)  (x11 = U + L_span).
Optimistic about rank-7 exclusive parts (assumes multiply-covered lines can be kept inside their span; lr8exact2 checks).
Relaxation of lr8host_sa2 (no exact part-identity for hosting); a lower cost here is necessary, not sufficient.
usage: lr8poolmip2.py timelimit -> lr8poolmip2.json {rep: [cover index, in-chain frame hex]}"""
import sys, json, pickle, collections, time, os
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
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
cov = pickle.load(open(__import__('os').environ.get('POOL', 'r8covers.pkl'), 'rb'))
FORCED = {}
for ri, r in enumerate(reps):
    R = HYP[r]
    for ci, c in enumerate(cov[r]):
        P = [pm(F) & R for F in c]
        for i, F in enumerate(c):
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
            if ex and rank(ex) == 8: FORCED[(ri, ci, F)] = 1
log('forced rank-8 exclusive parts', len(FORCED))
M = cp_model.CpModel()
Y = {}; FSP = {}; X = {}; CIN = {}; D = {}
for ri, r in enumerate(reps):
    ys = [M.NewBoolVar('') for _ in cov[r]]; M.AddExactlyOne(ys); Y[ri] = ys
    byF = collections.defaultdict(list); byFs = collections.defaultdict(list)
    for ci, (c, y) in enumerate(zip(cov[r], ys)):
        for F in c:
            byF[F].append(y)
            if (ri, ci, F) in FORCED: byFs[F].append(y)
    cins = []
    for F, yl in byF.items():
        x = M.NewBoolVar(''); M.Add(x == sum(yl)); X[(ri, F)] = x
        ci = M.NewBoolVar(''); M.AddImplication(ci, x); CIN[(ri, F)] = ci; cins.append(ci)
        d = M.NewBoolVar(''); M.Add(d == x - ci); D[(ri, F)] = d
        fs = M.NewBoolVar(''); M.Add(fs == sum(byFs[F])); FSP[(ri, F)] = fs
    M.AddExactlyOne(cins)
log('reps', len(reps), 'x vars', len(X))
def dvar(b, F):
    o, k = orb[b]; return D.get((o, rotm(F, -k)))
def fvar(b, F):
    o, k = orb[b]; return FSP.get((o, rotm(F, -k)))
# frame orbits: canonical key
seen = set(); singles = []; nfo = 0
hosted = []
for ri, r in enumerate(reps):
    hs = []
    for (rj, F), ci in CIN.items():
        if rj != ri: continue
        co = [dvar(b, F) for b in bits(F) if b != r]; co = [v for v in co if v is not None]
        if not co: continue
        h = M.NewBoolVar(''); M.AddImplication(h, ci); M.Add(sum(co) >= 1).OnlyEnforceIf(h); hs.append(h)
    hv = M.NewBoolVar(''); hosted.append(hv)
    if hs: M.Add(sum(hs) >= 1).OnlyEnforceIf(hv)
    else: M.Add(hv == 0)
for (ri, F) in list(D.keys()):
    key = min(rotm(F, k) for k in range(n))
    if key in seen: continue
    seen.add(key); nfo += 1
    bl = [b for b in bits(F) if dvar(b, F) is not None]
    ds = [dvar(b, F) for b in bl]; fsl = [fvar(b, F) for b in bl]
    s = M.NewBoolVar(''); singles.append(s)
    for j, dj in enumerate(ds):
        M.Add(s >= dj + fsl[j] - 1 - sum(ds[:j] + ds[j + 1:]))
log('frame orbits', nfo)
M.Minimize(len(reps) - sum(hosted) + sum(singles))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = int(os.environ.get('NW', '4'))
sv.parameters.log_search_progress = False
class CB(cp_model.CpSolverSolutionCallback):
    def on_solution_callback(self):
        log('solution cost (orbits) %d -> U+L_span = %d  bound %.1f' % (self.ObjectiveValue(), 11 * self.ObjectiveValue(), self.BestObjectiveBound()))
        out = {}
        for ri, r in enumerate(reps):
            c = [i for i, y in enumerate(Y[ri]) if self.Value(y)][0]
            F = [F for (rj, F), ci in CIN.items() if rj == ri and self.Value(ci)][0]
            out[r] = [c, hex(F)]
        json.dump(out, open('lr8poolmip2.json', 'w'))
st = sv.Solve(M, CB())
log('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    out = {}
    for ri, r in enumerate(reps):
        c = [i for i, y in enumerate(Y[ri]) if sv.Value(y)][0]
        F = [F for (rj, F), ci in CIN.items() if rj == ri and sv.Value(ci)][0]
        out[r] = [c, hex(F)]
    json.dump(out, open('lr8poolmip2.json', 'w'))
    log('hosted reps', sum(sv.Value(h) for h in hosted), 'single frame orbits', sum(sv.Value(s) for s in singles))
