"""Rank-8 frame-section top design (Z11-symmetric CP-SAT).  Choose a family of rank-3 closed frames F (closure of 3
independent lines, nondegenerate) such that (a) every line lies in exactly K used frames (its sections F-perp, users =
lines of F), (b) every orthogonal pair (t,u) has a used frame F containing t with u _|_ F (u in the section).
Frames are taken up to Z11 rotation (variables = frame orbits).  Objective: maximise covered pairs (feasibility if all).
usage: lr8design.py K timelimit [minlines] -> lr8design_K.json (list of used frames as hex masks)"""
import sys, json, itertools, collections, time
import numpy as np
from lgeo import *
from ortools.sat.python import cp_model
K = int(sys.argv[1]); TL = float(sys.argv[2]); MINL = int(sys.argv[3]) if len(sys.argv) > 3 else 3
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
def rotm(m):
    r = 0
    for s in bits(m): r |= 1 << rot[s]
    return r
# line orbit reps
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
# enumerate rank-3 closed frames through each rep line (all frames meet some rep's orbit; collect orbit reps of frames)
frames = {}
for r in reps:
    others = [x for x in range(V) if x != r]
    for a, b in itertools.combinations(others, 2):
        m = (1 << r) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)
        if pc(F) < MINL: continue
        # canonical orbit rep under Z11: min over rotations
        c = F; x = F
        for _ in range(n - 1):
            x = rotm(x); c = min(c, x)
        frames[c] = True
fr = sorted(frames)
log('frame orbits', len(fr), 'size hist', collections.Counter(pc(F) for F in fr))
# images of each frame orbit
img = []
for F in fr:
    L = [F]; x = F
    for _ in range(n - 1):
        x = rotm(x); L.append(x)
    img.append(L)
M = cp_model.CpModel()
y = [M.NewBoolVar('') for _ in fr]
# degree: for each rep line r, number of used frame images containing r == K
deg = collections.defaultdict(list)
for i, L in enumerate(img):
    for F in set(L):
        for r in reps:
            if F >> r & 1: deg[r].append(y[i])
for r in reps: M.Add(sum(deg[r]) == K)
# coverage for rep targets r and u in R(r)
cov = []
FP = {}
for i, L in enumerate(img):
    for F in set(L): FP[F] = (i, pm(F))
by_t = collections.defaultdict(list)
for F, (i, P_) in FP.items():
    for r in reps:
        if F >> r & 1: by_t[r].append((i, P_))
for r in reps:
    for u in bits(HYP[r]):
        lits = list({y[i] for i, P_ in by_t[r] if P_ >> u & 1})
        z = M.NewBoolVar(''); M.AddBoolOr(lits).OnlyEnforceIf(z); cov.append(z)
log('model: vars', len(y), 'coverage literals', len(cov))
M.Maximize(sum(cov))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 3
st = sv.Solve(M)
log('status', sv.StatusName(st), 'covered rep pairs', int(sv.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'of', len(cov), 'bound', sv.BestObjectiveBound())
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    used = [F for i, L in enumerate(img) if sv.Value(y[i]) for F in sorted(set(L))]
    json.dump([hex(F) for F in used], open('lr8design_%d.json' % K, 'w'))
    log('used frames', len(used), 'types', collections.Counter(pc(F) for F in used))
