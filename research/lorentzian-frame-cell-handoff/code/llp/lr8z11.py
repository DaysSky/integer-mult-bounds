"""Z11-equivariant EXACT parts/hosting/leftover layer for rank-8 frame-section tops, plus annealing over cover choices.
Design: each Z11 orbit representative r picks a 4-cover of R(r) (r8covers.pkl index); line rot^k(r) uses the rotated
cover AND the rotated assignment (equivariant).  Exact layer (CP-SAT, solved to optimality when possible):
  - every multiply-covered line u of R(r) is assigned to exactly one frame of the cover (part of r on that frame);
  - one in-chain frame per target; target hosted iff some co-user b of its in-chain frame F delivers F (F not b's
    in-chain frame) with an IDENTICAL part on F-perp;
  - leftover: a used frame whose ONLY delivered user has a part spanning the rank-8 node (rank(ex) = 8, or an
    assigned line outside span(ex) when rank(ex) = 7 (exact); rank(ex) <= 6: outside-span assignment counted
    spanning, conservative).
Cost = #unhosted targets + #leftovers = 11 * (orbit counts); R ~ 440 + cost.
usage: lr8z11.py init.json|random seed minutes  -> lr8z11_<seed>.json {rep: cover index}"""
import sys, json, pickle, random, time, math, collections
from lgeo import *
from ortools.sat.python import cp_model
t0 = time.time()
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
NR = len(reps)
cov = pickle.load(open('r8covers.pkl', 'rb'))
PM = {}
def pmc(F):
    if F not in PM: PM[F] = pm(F)
    return PM[F]
EXC = {}
def excl(ri, c):
    key = (ri, c)
    if key not in EXC:
        r = reps[ri]; R = HYP[r]; P = [pmc(F) & R for F in cov[r][c]]; out = []
        for i in range(4):
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4]); rx = rank(ex) if ex else 0
            outside = [u for u in bits(P[i] & ~ex) if rx < 8 and rank(ex | (1 << u)) > rx]
            out.append((P[i], ex, rx, outside))
        EXC[key] = out
    return EXC[key]
def solve(sel, TL=10.0, workers=1, want=False):
    M = cp_model.CpModel(); A = {}
    secs = [list(cov[reps[ri]][sel[ri]]) for ri in range(NR)]
    info = [excl(ri, sel[ri]) for ri in range(NR)]
    for ri in range(NR):
        r = reps[ri]
        for u in bits(HYP[r]):
            cs = [i for i in range(4) if info[ri][i][0] >> u & 1]
            if len(cs) == 1: A[(ri, cs[0], u)] = True
            else:
                ls = [M.NewBoolVar('') for _ in cs]; M.AddExactlyOne(ls)
                for i, l in zip(cs, ls): A[(ri, i, u)] = l
    def Av(b, j, u):   # assignment of line u to frame j by line b (equivariant)
        o, k = orb[b]; return A.get((o, j, rotp[-k % n][u]), False)
    SPN = {}
    for ri in range(NR):
        for i in range(4):
            P, ex, rx, outside = info[ri][i]
            if rx >= 8: SPN[(ri, i)] = True; continue
            outs = [A[(ri, i, u)] for u in outside if (ri, i, u) in A and A[(ri, i, u)] is not True]
            if any(A.get((ri, i, u)) is True for u in outside): SPN[(ri, i)] = True; continue
            if not outs: SPN[(ri, i)] = False; continue
            s = M.NewBoolVar('')
            for a in outs: M.AddImplication(a, s)
            SPN[(ri, i)] = s
    cin = {}
    for ri in range(NR):
        ls = [M.NewBoolVar('') for _ in range(4)]; M.AddExactlyOne(ls)
        for i in range(4): cin[(ri, i)] = ls[i]
    def secidx(b, F):
        o, k = orb[b]; Fr = rotm(F, -k)
        return (o, secs[o].index(Fr)) if Fr in secs[o] else None
    hosted = []
    for ri in range(NR):
        r = reps[ri]; opts = []
        for i, F in enumerate(secs[ri]):
            P = pmc(F)
            for b in bits(F):
                if b == r: continue
                sj = secidx(b, F)
                if sj is None: continue
                o, j = sj
                h = M.NewBoolVar(''); M.AddImplication(h, cin[(ri, i)]); M.AddImplication(h, cin[(o, j)].Not())
                bad = False; eqs = []
                for u in bits(P):
                    a = A.get((ri, i, u), False); c = Av(b, j, u)
                    if a is True and c is True: continue
                    if a is False and c is False: continue
                    if (a is True and c is False) or (a is False and c is True): bad = True; break
                    eqs.append((a, c))
                if bad: M.Add(h == 0); continue
                for a, c in eqs:
                    if a is True: M.AddImplication(h, c)
                    elif a is False: M.AddImplication(h, c.Not())
                    elif c is True: M.AddImplication(h, a)
                    elif c is False: M.AddImplication(h, a.Not())
                    else: M.Add(a == c).OnlyEnforceIf(h)
                opts.append(h)
        hv = M.NewBoolVar(''); hosted.append(hv)
        if opts: M.AddBoolOr(opts + [hv.Not()])
        else: M.Add(hv == 0)
    # leftovers per frame orbit
    seen = set(); singles = []
    for ri in range(NR):
        for F in secs[ri]:
            key = min(rotm(F, k) for k in range(n))
            if key in seen: continue
            seen.add(key)
            us = [(b, secidx(b, F)) for b in bits(F)]; us = [(b, sj) for b, sj in us if sj is not None]
            for b, (o, j) in us:
                sp = SPN[(o, j)]
                if sp is False: continue
                others = [cin[sj2].Not() for b2, sj2 in us if b2 != b]
                s = M.NewBoolVar(''); singles.append(s)
                M.Add(s + sum(others) >= (1 if sp is True else sp) - cin[(o, j)])
    M.Minimize(NR - sum(hosted) + sum(singles))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = workers
    st = sv.Solve(M)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 10 ** 6, None
    val = int(round(sv.ObjectiveValue()))
    det = None
    if want:
        det = {'status': sv.StatusName(st), 'bound': sv.BestObjectiveBound(),
               'hosted': [sv.Value(h) for h in hosted], 'L': sum(sv.Value(s) for s in singles),
               'cin': [[sv.Value(cin[(ri, i)]) for i in range(4)] for ri in range(NR)],
               'assign': {'%d,%d,%d' % k: (1 if v is True else sv.Value(v)) for k, v in A.items() if v is not False}}
    return val, det
if __name__ == '__main__':
    init, seed, MIN = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); random.seed(seed)
    if init == 'random': sel = [random.randrange(len(cov[r])) for r in reps]
    else:
        d = json.load(open(init)); sel = [d[str(r)][0] if isinstance(d[str(r)], list) else d[str(r)] for r in reps]
    cur, det = solve(sel, TL=60, workers=2, want=True)
    log('init cost (orbits) %d -> U+L = %d  status %s bound %.1f hosted reps %d L orbits %d' % (cur, 11 * cur, det['status'], det['bound'], sum(det['hosted']), det['L']))
    best = cur; bests = list(sel); it = 0
    json.dump({str(r): bests[ri] for ri, r in enumerate(reps)}, open('lr8z11_%d.json' % seed, 'w'))
    withF = [collections.defaultdict(list) for _ in range(NR)]
    for ri, r in enumerate(reps):
        for ci, c in enumerate(cov[r]):
            for F in c: withF[ri][F].append(ci)
    while time.time() - t0 < MIN * 60:
        it += 1
        ri = random.randrange(NR); r = reps[ri]
        if random.random() < 0.6:
            # co-user adoption: pick a frame of a random neighbour's cover through r, adopt a cover containing it
            F = random.choice(cov[r][sel[ri]]); bs = [b for b in bits(F) if b != r]
            b = random.choice(bs); o, k = orb[b]; Fr = rotm(F, -k)
            if withF[o].get(Fr): ri, newc = o, random.choice(withF[o][Fr])
            else: newc = random.randrange(len(cov[r]))
        else: newc = random.randrange(len(cov[reps[ri]]))
        old = sel[ri]; sel[ri] = newc
        val, _ = solve(sel, TL=5.0)
        T = 1.0 * (0.05) ** ((time.time() - t0) / (MIN * 60))
        if val <= cur or random.random() < math.exp((cur - val) / T):
            cur = val
            if cur < best:
                best = cur; bests = list(sel)
                log('it %d cost (orbits) %d -> U+L = %d' % (it, best, 11 * best))
                json.dump({str(r): bests[ri2] for ri2, r in enumerate(reps)}, open('lr8z11_%d.json' % seed, 'w'))
        else: sel[ri] = old
    val, det = solve(bests, TL=120, workers=2, want=True)
    log('final best cost (orbits) %d -> U+L = %d status %s bound %.1f; hosted reps %d, L orbits %d; iterations %d' % (val, 11 * val, det['status'], det['bound'], sum(det['hosted']), det['L'], it))
    json.dump({'sel': {str(r): bests[ri] for ri, r in enumerate(reps)}, 'det': det}, open('lr8z11_%d_det.json' % seed, 'w'))
