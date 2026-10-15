"""Stage 2 (exact): E8 parts layer for fixed cover choices.  Multiply-covered lines of each target are assigned to
exactly one of its covering sets; each target picks an in-chain A3 X of its cover and a host b in X (b's cover
contains X, b delivered on X) with IDENTICAL parts on X-perp.  CP-SAT feasibility; also maximises #hosted targets.
usage: e8parts.py covsel.json timelimit -> e8parts_sol.json"""
import sys, json, pickle, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V; HYP = e8.HYP; bits = e8.bits
def pm(m):
    r = e8.FULL
    for s in bits(m): r &= HYP[s]
    return r
cov = pickle.load(open('covers.pkl', 'rb'))['covers']
def solve(sel, TL=3.0, ret=False):
    C = {t: cov[t][sel[t]] for t in range(V)}
    M = cp_model.CpModel()
    inpart = {}            # (t, setindex, u) -> literal or True
    setsof = {}
    for t in range(V):
        Xs, Z = C[t]; R = HYP[t] & ~(1 << t)
        sets = [pm(Y) & R for Y in Xs] + [pm(Z) & R]; setsof[t] = sets
        for u in bits(R):
            cs = [i for i in range(4) if sets[i] >> u & 1]
            if len(cs) == 1: inpart[(t, cs[0], u)] = True
            else:
                lits = [M.NewBoolVar('') for _ in cs]; M.AddExactlyOne(lits)
                for i, l in zip(cs, lits): inpart[(t, i, u)] = l
    def lit(t, i, u):
        v = inpart.get((t, i, u), False)
        return v
    cin = {}; hosted = []
    for t in range(V):
        Xs, Z = C[t]
        cs = [M.NewBoolVar('') for _ in Xs]; M.AddExactlyOne(cs)
        for i, X in enumerate(Xs): cin[(t, X)] = cs[i]
    for t in range(V):
        Xs, Z = C[t]
        hv = M.NewBoolVar(''); hosted.append(hv)
        opts = []
        for i, X in enumerate(Xs):
            P = pm(X)
            for b in bits(X):
                if b == t or X not in C[b][0]: continue
                j = list(C[b][0]).index(X)
                h = M.NewBoolVar(''); opts.append(h)
                M.AddImplication(h, cin[(t, X)])
                M.AddImplication(h, cin[(b, X)].Not())
                for u in bits(P):
                    a, bb = lit(t, i, u), lit(b, j, u)
                    if a is True and bb is True: continue
                    if a is False and bb is False: continue
                    if a is True and bb is False or a is False and bb is True: M.AddBoolOr([h.Not()]); break
                    if a is True: M.AddImplication(h, bb)
                    elif a is False: M.AddImplication(h, bb.Not())
                    elif bb is True: M.AddImplication(h, a)
                    elif bb is False: M.AddImplication(h, a.Not())
                    else: M.Add(a == bb).OnlyEnforceIf(h)
        M.AddBoolOr(opts + [hv.Not()]) if opts else M.Add(hv == 0)
    M.Maximize(sum(hosted))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 1
    st = sv.Solve(M)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return -1, None
    h = [sv.Value(x) for x in hosted]
    return sum(h), h
if __name__ == '__main__':
    import random, time, math
    seed = int(sys.argv[2]); MIN = float(sys.argv[3]); random.seed(seed)
    sel = json.load(open(sys.argv[1]))
    cur, h = solve(sel); best = cur; bests = list(sel); t0 = time.time(); it = 0
    print('init exact hosted', cur, flush=True)
    while time.time() - t0 < MIN * 60:
        it += 1
        un = [t for t in range(V) if not h[t]]
        t = random.choice(un) if un and random.random() < 0.8 else random.randrange(V)
        if random.random() < 0.5:
            Xs = cov[t][sel[t]][0]; t = random.choice([b for X in Xs for b in bits(X)])
        old = sel[t]; sel[t] = random.randrange(len(cov[t]))
        val, h2 = solve(sel)
        T = 1.0 * (0.05 / 1.0) ** ((time.time() - t0) / (MIN * 60))
        if val >= cur or random.random() < math.exp((val - cur) / T):
            cur, h = val, h2
            if cur > best:
                best = cur; bests = list(sel); print('[%4.0fs] it %d exact hosted %d' % (time.time() - t0, it, best), flush=True)
                json.dump(bests, open('e8covsel_exact_%d.json' % seed, 'w'))
        else: sel[t] = old
    print('best exact hosted', best, 'iterations', it, flush=True)
