"""Exact hosting layer for an I11 rank-8 frame-section top (design from lr8design2.json, Z11 images).  Every line u of
R(t) is assigned to exactly one of t's 4 sections containing it; t's in-chain section F must have a host b in F
(b uses F as a DELIVERED section) with IDENTICAL parts on F-perp.  Maximise #hosted targets (CP-SAT, no symmetry).
Also reports how many delivered parts span their section (closure = F-perp; single-delivered-user sections with a
spanning part need an assembly leftover).  usage: lr8host.py design.json timelimit"""
import sys, json, collections
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
secs = {}; inF = {}
for t in range(V):
    o, k = orb[t]; d = D[reps[o]]
    secs[t] = [rotm(int(h, 16), k) for h in d['secs']]; inF[t] = rotm(int(d['in'], 16), k)
M = cp_model.CpModel(); A = {}
for t in range(V):
    R = HYP[t]; P = [pm(F) for F in secs[t]]
    for u in bits(R):
        cs = [i for i in range(4) if P[i] >> u & 1]
        assert cs, ('uncovered', t, u)
        if len(cs) == 1: A[(t, cs[0], u)] = True
        else:
            ls = [M.NewBoolVar('') for _ in cs]; M.AddExactlyOne(ls)
            for i, l in zip(cs, ls): A[(t, i, u)] = l
cin = {}
for t in range(V):
    ls = [M.NewBoolVar('') for _ in secs[t]]; M.AddExactlyOne(ls)
    for F, l in zip(secs[t], ls): cin[(t, F)] = l
hosted = []
for t in range(V):
    opts = []
    for i, F in enumerate(secs[t]):
        P = pm(F)
        for b in bits(F):
            if b == t or F not in secs[b]: continue
            j = secs[b].index(F); h = M.NewBoolVar(''); opts.append(h)
            M.AddImplication(h, cin[(t, F)]); M.AddImplication(h, cin[(b, F)].Not())
            bad = False
            for u in bits(P):
                a = A.get((t, i, u), False); c = A.get((b, j, u), False)
                if a is True and c is True: continue
                if (a is True and c is False) or (a is False and c is True): bad = True; break
                if a is False and c is False: continue
                if a is True: M.AddImplication(h, c)
                elif a is False: M.AddImplication(h, c.Not())
                elif c is True: M.AddImplication(h, a)
                elif c is False: M.AddImplication(h, a.Not())
                else: M.Add(a == c).OnlyEnforceIf(h)
            if bad: M.Add(h == 0)
    hv = M.NewBoolVar(''); hosted.append(hv)
    if opts: M.AddBoolOr(opts + [hv.Not()])
    else: M.Add(hv == 0)
M.Maximize(sum(hosted))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M)
print('status', sv.StatusName(st), 'hosted', int(sv.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'of', V, 'bound', sv.BestObjectiveBound(), flush=True)
