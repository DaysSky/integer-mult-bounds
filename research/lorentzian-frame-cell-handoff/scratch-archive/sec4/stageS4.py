"""E8 section-level content test for any design (env DESIGN), maximal candidate supports (relaxation):
cg=1: arrival support = design cells inside Q-perp ∩ Q'-perp (Q' another design section) or one design cell in Q-perp;
cg=0: lines of Q-perp ∩ Q'-perp, a cell, or a single line.  lam invertible; target equations sum = R(t)
(excl=1: minus the complement-free... general: no block assumption; in-chain read optional ic=1 with support
(cells inside) Q'-perp ∩ t-perp).  Z15-canonical (sym=1) or none."""
import sys, itertools
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); cg = int(sys.argv[2]); ic = int(sys.argv[3]); sym = int(sys.argv[4]); EMPT = int(sys.argv[5]) if len(sys.argv) > 5 else 0; IC2 = int(sys.argv[6]) if len(sys.argv) > 6 else 0; KX = int(sys.argv[7]) if len(sys.argv) > 7 else 0
extra_used = []
Qp = {Q: perpmask(Q) for Q in planes}
def cellcov(X):
    m = 0
    for P in planes:
        if P & ~X == 0: m |= P
    return m
def g_(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else ((k, act(v)) if k == 'S' else o)
def canon(tup):
    if not sym: return tup
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g_(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel(); V_ = {}
def var(tup):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('')
    return V_[c]
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
reps_S = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); reps_S.append(Q)
for Q in reps_S:
    sup = set()
    for Q2 in planes:
        if Q2 == Q: continue
        X = Qp[Q] & Qp[Q2]
        s_ = cellcov(X) if cg else X
        if s_: sup.add(s_)
    for P in planes:
        if P & ~Qp[Q] == 0: sup.add(P)
    if not cg:
        for s in e8.bits(Qp[Q]): sup.add(1 << s)
    sup = sorted(sup)
    nsl = pc(Q) + KX
    for j in range(nsl):
        if j >= pc(Q):
            u_ = M.NewBoolVar(''); extra_used.append(u_)
            for s in e8.bits(Qp[Q]): M.AddImplication(abit(Q, j, s), u_)
            for t in e8.bits(Q): M.AddImplication(lam(t, Q, j), u_)
        chs = [M.NewBoolVar('') for _ in sup]; M.AddExactlyOne(chs)
        for s in e8.bits(Qp[Q]):
            M.AddBoolOr([abit(Q, j, s).Not()] + [c for c, S_ in zip(chs, sup) if S_ >> s & 1])
        if not EMPT: M.AddBoolOr([abit(Q, j, s) for s in e8.bits(Qp[Q])])
    users = e8.bits(Q); n = len(users); allowed = []
    if not IC2:
        for combo in itertools.product(range(1, 2 ** n), repeat=n):
            b = []
            for v in combo:
                for x in b:
                    if v ^ x < v: v ^= x
                if v: b.append(v); b.sort(reverse=True)
            if len(b) == n: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)])
        M.AddAllowedAssignments([lam(t, Q, j) for t in users for j in range(n)], allowed)
    else:
        # in-chain users (z=1) read any combination; rows of delivered users (z=0) must be independent
        for combo in itertools.product(range(0, 2 ** nsl), repeat=n):
            for zs in itertools.product((0, 1), repeat=n):
                b = []; ok = True
                for v, z in zip(combo, zs):
                    if z: continue
                    for x in b:
                        if v ^ x < v: v ^= x
                    if not v: ok = False; break
                    b.append(v); b.sort(reverse=True)
                if ok: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(nsl)] + list(zs))
        M.AddAllowedAssignments([lam(t, Q, j) for t in users for j in range(nsl)] + [zin(t, Q) for t in users], allowed)
TG = reps if sym else list(range(V))
for t in TG:
    mine = [Q for Q in planes if Q >> t & 1]
    if IC2: M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    inch = None
    if ic == 2:
        # NESTED in-chain node: X = a design cell or Q*-perp ∩ Q'-perp inside the in-chain section Q* (zin(t,Q*)=1)
        opts = []
        for Qs in mine:
            Xs = set()
            for P in planes:
                if P & ~Qp[Qs] == 0: Xs.add(P)
            for Q2 in planes:
                if Q2 != Qs:
                    X = Qp[Qs] & Qp[Q2]
                    s_ = cellcov(X) if cg else X
                    if s_: Xs.add(s_)
            for X in Xs:
                b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); opts.append((b, X))
        M.Add(sum(b for b, X in opts) <= 1)
        inch = {}
        for s in e8.bits(e8.HYP[t]):
            bb = M.NewBoolVar(''); inch[s] = bb
            M.AddBoolOr([bb.Not()] + [b for b, X in opts if X >> s & 1])
    elif ic:
        Fs = set()
        for Q2 in planes:
            X = Qp[Q2] & e8.HYP[t]
            s_ = cellcov(X) if cg else X
            if s_: Fs.add(s_)
        Fs = sorted(Fs); chs = [M.NewBoolVar('') for _ in Fs]; M.AddExactlyOne(chs); inch = {}
        for s in e8.bits(e8.HYP[t]):
            b = M.NewBoolVar(''); inch[s] = b
            M.AddBoolOr([b.Not()] + [c for c, F in zip(chs, Fs) if F >> s & 1])
    for s in e8.bits(e8.HYP[t]):
        terms = []
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(pc(Q) + KX):
                x = M.NewBoolVar(''); a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        if inch: terms.append(inch[s])
        M.AddBoolXOr(terms)
if extra_used: M.Minimize(sum(extra_used))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
if extra_used and r in (cp_model.OPTIMAL, cp_model.FEASIBLE): print('extra-slot orbits used', int(sol.ObjectiveValue()), 'proven min >=', sol.BestObjectiveBound(), '(each orbit = 15 registers)', flush=True); print(os.environ.get('DESIGN', 'design.json'), 'cg', cg, 'ic', ic, 'sym', sym, 'empties', EMPT, 'inchain-dependent', IC2, 'KX', KX, 'status', sol.StatusName(r), flush=True)
