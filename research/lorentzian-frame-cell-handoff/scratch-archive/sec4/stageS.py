"""Stage S' (relaxation of the content problem, upstream dropped).  Each section Q gets |Q| arrival vectors a[Q,j] in
F2^(lines of Q-perp); each arrival is supported inside ONE flat chosen from: lines, design cells inside Q-perp, or
multi-section nodes (flats of rank 3..5 in the perp of >= 2 design sections) inside Q-perp.  Deliveries
c_t(Q) = sum_j lam[t,Q,j] a[Q,j] with the |Q| x |Q| matrix lam invertible.  Target equations: sum_{Q∋t} c_t(Q) = R(t)
(argv excl=1: minus the complement block, which t reads in-chain as one block total at frame B').  Z15-canonical."""
import sys, pickle, itertools
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); excl = int(sys.argv[2]); cellgen = int(sys.argv[3]) if len(sys.argv) > 3 else 0; inchain = int(sys.argv[4]) if len(sys.argv) > 4 else 0
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
flats = pickle.load(open('flats.pkl', 'rb'))
nodes = [F for F, r, c, s in flats if len(s) >= 2]
Qperp = {Q: perpmask(Q) for Q in planes}
def g(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else (k, act(v)) if k in ('S', 'F') else o
def canon(tup):
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel()
V_ = {}
def var(tup):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('')
    return V_[c]
def abit(Q, j, s): return var((('S', Q), ('j', j), ('L', s)))
def lam(t, Q, j): return var((('L', t), ('S', Q), ('j', j)))
def ch(Q, j, F): return var((('S', Q), ('j', j), ('F', F)))
srep = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); srep.append(Q)
cand_count = []
for Q in srep:
    Qp = Qperp[Q]
    if cellgen:
        cands = []
        for F in [P for P in planes if P & ~Qp == 0] + [G for G in nodes if G & ~Qp == 0]:
            cov = 0
            for P in planes:
                if P & ~F == 0: cov |= P
            if cov: cands.append(cov)      # support = union of design cells inside the node
        cands = sorted(set(cands))
    else:
        cands = [1 << s for s in e8.bits(Qp)] + [P for P in planes if P & ~Qp == 0] + [G for G in nodes if G & ~Qp == 0]
    cand_count.append(len(cands))
    for j in range(pc(Q)):
        chs = [ch(Q, j, F) for F in cands]
        M.AddExactlyOne(chs)
        for s in e8.bits(Qp):
            M.AddBoolOr([abit(Q, j, s).Not()] + [ch(Q, j, F) for F in cands if F >> s & 1])
        M.AddBoolOr([abit(Q, j, s) for s in e8.bits(Qp)])   # nonzero arrival
    # lam invertible
    users = e8.bits(Q); n = len(users)
    allowed = []
    for combo in itertools.product(range(1, 2 ** n), repeat=n):
        b = []
        for v in combo:
            for x in b:
                if v ^ x < v: v ^= x
            if v: b.append(v); b.sort(reverse=True)
        if len(b) == n: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)])
    M.AddAllowedAssignments([lam(t, Q, j) for t in users for j in range(n)], allowed)
print('candidate supports per section rep', cand_count, flush=True)
inch = {}
if inchain:
    for t in reps:
        mine = [Q for Q in planes if Q >> t & 1]
        Fs = set()
        for Q in mine:
            Qp = Qperp[Q]
            for F in [P for P in planes if P & ~Qp == 0] + [G for G in nodes if G & ~Qp == 0]:
                if excl and not ((full[comp[blk[t]]] & ~F == 0) or (F & ~full[comp[blk[t]]] == 0)): continue
                cov = 0
                for P in planes:
                    if P & ~F == 0: cov |= P
                if cov: Fs.add(cov)
        Fs = sorted(Fs)
        chs = [M.NewBoolVar('') for F in Fs]; M.AddExactlyOne(chs)
        rb = {s: M.NewBoolVar('') for s in e8.bits(e8.HYP[t])}
        for s, b in rb.items(): M.AddBoolOr([b.Not()] + [c for c, F in zip(chs, Fs) if F >> s & 1])
        inch[t] = rb
        print('target', t, 'in-chain candidate supports', len(Fs), flush=True)
nprod = 0
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    for s in e8.bits(e8.HYP[t]):
        want = 0 if (excl and blk[s] == comp[blk[t]]) else 1
        terms = []
        for Q in mine:
            if not (Qperp[Q] >> s & 1): continue
            for j in range(pc(Q)):
                x = M.NewBoolVar(''); nprod += 1
                a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        if inchain: terms.append(inch[t][s])
        if want: M.AddBoolXOr(terms)
        else: M.AddBoolXOr(terms + [M.NewConstant(1)])
print('vars', len(V_), 'products', nprod, flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    res = {}
    for Q in srep:
        Qp = Qperp[Q]
        for j in range(pc(Q)):
            a = sum(1 << s for s in e8.bits(Qp) if sol.Value(abit(Q, j, s)))
            res['%x/%d' % (Q, j)] = hex(a)
    json.dump(res, open('stageS_ex%d_cg%d_ic%d.json' % (excl, cellgen, inchain), 'w'))
    print('arrival sizes', collections.Counter(pc(int(v, 16)) for v in res.values()))
