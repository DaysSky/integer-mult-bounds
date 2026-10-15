"""Exact hosting + single-section cost of a Z11 pool design (from lr8poolmip.json): expands rep choices by Z11 to all
220 lines, then solves the exact parts layer (lr8host_sa2 model: multiply-covered lines assigned once per target; a
hosted in-chain part is IDENTICAL to a delivered co-user part on the same section) with CP-SAT, objective
max hosted - singles.  Reports U, L and R ~ 440 + U + L.  usage: lr8exact.py design.json timelimit"""
import sys, json, pickle, collections, time
from lgeo import *
from ortools.sat.python import cp_model
des = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}; TL = float(sys.argv[2])
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
cov = pickle.load(open('r8covers.pkl', 'rb'))
sel = [des[reps[orb[t][0]]][0] for t in range(V)]
secs = {t: list(cov[t][sel[t]]) for t in range(V)}
PM = {}
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
for t in range(V):
    U = 0
    for F in secs[t]: U |= pmc(F)
    assert U & HYP[t] == HYP[t], 'not a cover'
M = cp_model.CpModel(); A = {}
for t in range(V):
    P = [pmc(F) for F in secs[t]]
    for u in bits(HYP[t]):
        cs = [i for i in range(4) if P[i] >> u & 1]
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
        P = pmc(F)
        for b in bits(F):
            if b == t or F not in secs[b]: continue
            j = secs[b].index(F); h = M.NewBoolVar(''); opts.append(h)
            M.AddImplication(h, cin[(t, F)]); M.AddImplication(h, cin[(b, F)].Not())
            for u in bits(P):
                a = A.get((t, i, u), False); c = A.get((b, j, u), False)
                if a is True and c is True: continue
                if a is False and c is False: continue
                if (a is True and c is False) or (a is False and c is True): M.Add(h == 0); break
                if a is True: M.AddImplication(h, c)
                elif a is False: M.AddImplication(h, c.Not())
                elif c is True: M.AddImplication(h, a)
                elif c is False: M.AddImplication(h, a.Not())
                else: M.Add(a == c).OnlyEnforceIf(h)
    hv = M.NewBoolVar(''); hosted.append(hv)
    if opts: M.AddBoolOr(opts + [hv.Not()])
    else: M.Add(hv == 0)
users = collections.defaultdict(list)
for t in range(V):
    for F in secs[t]: users[F].append(t)
singles = []
for F, us in users.items():
    dl = [cin[(t, F)].Not() for t in us]
    one = M.NewBoolVar('')
    M.Add(sum(dl) <= 1).OnlyEnforceIf(one); M.Add(sum(dl) >= 2).OnlyEnforceIf(one.Not())
    singles.append(one)
# hint: the relaxed in-chain choice
for t in range(V):
    o, k = orb[t]; F0 = int(des[reps[o]][1], 16)
    Fk = 0
    for s in bits(F0):
        x = s
        for _ in range(k): x = rot[x]
        Fk |= 1 << x
    for F in secs[t]: M.AddHint(cin[(t, F)], 1 if F == Fk else 0)
M.Maximize(sum(hosted) - sum(singles))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
st = sv.Solve(M)
print('status', sv.StatusName(st), 'sections', len(users))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    H = sum(sv.Value(h) for h in hosted); L = sum(sv.Value(s) for s in singles)
    print('exact hosted %d  U %d  single-delivered L %d  -> U+L %d  R ~ %d  (bound on hosted-singles %.1f)' % (H, V - H, L, V - H + L, 440 + V - H + L, sv.BestObjectiveBound()))
