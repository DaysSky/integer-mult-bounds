"""Relaxed rank-8 frame-section top design (Z11-symmetric CP-SAT).  Each target t chooses 4 rank-3 frames F through t
(its sections, x[t,F]) whose perps cover R(t), and one of them in-chain (c[t,F]); the in-chain section needs a co-user
b in F (b != t) that uses F as a DELIVERED section (x[b,F] and not c[b,F]).  Frames need not be used by all their
lines.  Variables live on Z11 orbit-representative targets.  Objective: maximise covered pairs (all = feasible).
usage: lr8design2.py timelimit [min perp size] -> lr8design2.json {target: {'secs': [hex], 'in': hex}}"""
import sys, json, itertools, collections, time
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); MINP = int(sys.argv[2]) if len(sys.argv) > 2 else 0; t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
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
frames_of = {}
for r in reps:
    fs = set()
    for a, b in itertools.combinations([x for x in range(V) if x != r], 2):
        m = (1 << r) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if pc(pm(F)) >= MINP: fs.add(F)
    frames_of[r] = sorted(fs)
log('frames per rep', [len(frames_of[r]) for r in reps])
M = cp_model.CpModel()
X = {}; C = {}
def canon(t, F):
    o, k = orb[t]; return (reps[o], rotm(F, -k % n))
def xv(t, F):
    key = canon(t, F)
    if key not in X: X[key] = M.NewBoolVar('')
    return X[key]
def cv(t, F):
    key = canon(t, F)
    if key not in C: C[key] = M.NewBoolVar('')
    return C[key]
cov = []
for r in reps:
    fs = frames_of[r]
    M.Add(sum(xv(r, F) for F in fs) == 4)
    M.AddExactlyOne([cv(r, F) for F in fs])
    for F in fs: M.AddImplication(cv(r, F), xv(r, F))
    P = {F: pm(F) for F in fs}
    for u in bits(HYP[r]):
        z = M.NewBoolVar(''); M.AddBoolOr([xv(r, F) for F in fs if P[F] >> u & 1]).OnlyEnforceIf(z); cov.append(z)
    # in-chain co-user condition
    for F in fs:
        co = []
        for b in bits(F):
            if b == r: continue
            d = M.NewBoolVar('')
            M.AddBoolAnd([xv(b, F), cv(b, F).Not()]).OnlyEnforceIf(d)
            co.append(d)
        M.AddBoolOr(co).OnlyEnforceIf(cv(r, F))
log('vars x', len(X), 'c', len(C), 'coverage', len(cov))
M.Maximize(sum(cov))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = int(__import__("os").environ.get("NW", "3"))
st = sv.Solve(M)
log('status', sv.StatusName(st), 'covered', int(sv.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'of', len(cov), 'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    out = {}
    for r in reps:
        out[r] = {'secs': [hex(F) for F in frames_of[r] if sv.Value(xv(r, F))], 'in': [hex(F) for F in frames_of[r] if sv.Value(cv(r, F))][0]}
    json.dump(out, open('lr8design2.json', 'w'))
