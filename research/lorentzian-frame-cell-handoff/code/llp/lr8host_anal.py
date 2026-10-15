"""I11 analogue of the E8 exact-hosting search: each line picks one 4-cover (from r8covers.pkl); the exact hosting
layer (multiply-covered lines assigned once per target; in-chain part identical to a delivered co-user's part on the
same rank-8 section) is solved by CP-SAT; annealing over cover choices maximises #hosted.
usage: lr8host_sa.py seed minutes -> lr8hostsel_<seed>.json"""
import sys, json, pickle, random, time, math
from lgeo import *
from ortools.sat.python import cp_model
SEL = sys.argv[1]
cov = pickle.load(open('r8covers.pkl', 'rb'))
PM = {}
import collections
withF = {t: collections.defaultdict(list) for t in range(V)}
for t in range(V):
    for ci, c in enumerate(cov[t]):
        for F in c: withF[t][F].append(ci)
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
def solve(sel, TL=5.0):
    secs = {t: list(cov[t][sel[t]]) for t in range(V)}
    M = cp_model.CpModel(); A = {}; global HREL; HREL = {}
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
                j = secs[b].index(F); h = M.NewBoolVar(''); opts.append(h); HREL[(t, b, F)] = h
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
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 2
    st = sv.Solve(M)
    rel = [(t, b, F) for (t, b, F), hv in HREL.items() if sv.Value(hv)]
    global PARTS, CIN
    PARTS = {}; CIN = {}
    for t in range(V):
        for i, F in enumerate(secs[t]):
            m = 0
            for u in bits(pmc(F)):
                a = A.get((t, i, u), False)
                if a is True or (a is not False and sv.Value(a)): m |= 1 << u
            PARTS[(t, F)] = m
            CIN[(t, F)] = sv.Value(cin[(t, F)])
    return int(sv.ObjectiveValue()), [sv.Value(x) for x in hosted], rel, sv.StatusName(st)

sel = json.load(open(SEL))
val, h, rel, st = solve(sel, TL=60)
import collections
hosts = collections.Counter(b for t, b, F in rel)
riders = set(t for t, b, F in rel)
print('status', st, 'hosted', val, 'relations', len(rel))
print('riders per host:', sorted(collections.Counter(hosts.values()).items()))
print('hosts that are themselves hosted:', sum(1 for b in hosts if b in riders))
print('host orthogonal to rider:', sum(1 for t, b, F in rel if G[t][b] == 0), 'non-orthogonal:', sum(1 for t, b, F in rel if G[t][b] != 0))
print('section sizes (users) of hosting frames:', sorted(collections.Counter(pc(F) for t, b, F in rel).items()))

# leftovers: per section frame, delivered users (CIN == 0); single delivered user with spanning part -> +1;
# dependent delivered parts -> flag; in-chain users not hosted -> need own arrivals
secusers = collections.defaultdict(list)
for (t, F), c in CIN.items(): secusers[F].append((t, c))
def gf2_rank(vs):
    rows = list(vs); r = 0
    for bit in range(V):
        piv = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r
L = dep = nsec = 0; spancount = 0
for F, us in secusers.items():
    deliv = [PARTS[(t, F)] for t, c in us if c == 0 and PARTS[(t, F)]]
    nsec += 1
    if gf2_rank(deliv) < len(deliv): dep += 1
    if len(deliv) == 1:
        if rank(pp(deliv[0])) >= rank(F ^ F) + 8 or rank(pp(deliv[0])) == 8: L += 1
    spancount += sum(1 for d in deliv if rank(pp(d)) == 8)
print('sections', nsec, '| single-delivered spanning leftovers L =', L, '| sections with dependent delivered parts', dep, '| delivered parts spanning rank 8:', spancount)
