"""I11 analogue of the E8 exact-hosting search: each line picks one 4-cover (from r8covers.pkl); the exact hosting
layer (multiply-covered lines assigned once per target; in-chain part identical to a delivered co-user's part on the
same rank-8 section) is solved by CP-SAT; annealing over cover choices maximises #hosted.
usage: lr8host_sa.py seed minutes -> lr8hostsel_<seed>.json"""
import sys, json, pickle, random, time, math
from lgeo import *
from ortools.sat.python import cp_model
seed = int(sys.argv[1]); MIN = float(sys.argv[2]); random.seed(seed)
cov = pickle.load(open('r8covers.pkl', 'rb'))
PM = {}
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
def solve(sel, TL=5.0):
    secs = {t: list(cov[t][sel[t]]) for t in range(V)}
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
    M.Maximize(sum(hosted))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 1
    st = sv.Solve(M)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return -1, [0] * V
    return int(sv.ObjectiveValue()), [sv.Value(x) for x in hosted]
# co-usage objective first: start from random covers, quick greedy to increase shared frames
sel = [random.randrange(len(cov[t])) for t in range(V)]
cur, h = solve(sel); best = cur; bests = list(sel); t0 = time.time(); it = 0
print('init exact hosted', cur, flush=True)
while time.time() - t0 < MIN * 60:
    it += 1
    un = [t for t in range(V) if not h[t]]
    t = random.choice(un) if un and random.random() < 0.8 else random.randrange(V)
    if random.random() < 0.5:
        F = random.choice(cov[t][sel[t]]); t = random.choice(bits(F))
    old = sel[t]; sel[t] = random.randrange(len(cov[t]))
    val, h2 = solve(sel)
    T = 1.0 * (0.05 / 1.0) ** ((time.time() - t0) / (MIN * 60))
    if val >= cur or random.random() < math.exp((val - cur) / T):
        cur, h = val, h2
        if cur > best:
            best = cur; bests = list(sel); print('[%4.0fs] it %d exact hosted %d' % (time.time() - t0, it, best), flush=True)
            json.dump(bests, open('lr8hostsel_%d.json' % seed, 'w'))
    else: sel[t] = old
print('best exact hosted', best, 'iterations', it, flush=True)
