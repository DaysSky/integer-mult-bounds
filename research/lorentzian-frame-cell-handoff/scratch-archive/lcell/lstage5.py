"""Lorentzian section-level content test for a frame-cell source system (json line -> cover), Z11-canonical:
sections = perps of the system's cells (users = endpoints whose cover holds the other), slots per section <= users + KX,
arrival support = union of cells inside a nondegenerate node Q-perp ∩ Q'-perp, or one cell inside Q-perp (cell-routed,
maximal supports: RELAXATION), contents any subset of the support; delivered users' rows independent, in-chain user
any combination, <= 1 in-chain section per target plus one nested read (a cell or node inside it).
Minimise total used arrivals (each slot orbit = 11 registers).  usage: lstage5.py SYS KX tl"""
import sys, os, json, itertools, collections
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
SYS, KX, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
cov = {int(k): v for k, v in json.load(open(SYS)).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
users_of = {C: [x for x in bits(C) if any(cov[x] >> y & 1 for y in bits(C) if y != x)] for C in cells}
Qp = {C: perp(C) for C in cells}
def cellcov(X):
    m = 0
    for C in cells:
        if C & ~X == 0: m |= C
    return m
def canon(tup):
    best = None
    for p in PERMS:
        c = tuple((k, p[v]) if k == 'L' else ((k, act(v, p)) if k == 'S' else (k, v)) for k, v in tup)
        if best is None or c < best: best = c
    return best
M = cp_model.CpModel(); VV = {}
def var(tup):
    c = canon(tup)
    if c not in VV: VV[c] = M.NewBoolVar('')
    return VV[c]
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
ND = {}
def nd(m):
    if m not in ND: ND[m] = nondeg_span(m)
    return ND[m]
reps_S = []; seen = set()
for Q in cells:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); reps_S.append(Q)
used = []
node_sup = {}
for Q in reps_S:
    sup = set()
    for Q2 in cells:
        if Q2 == Q: continue
        X = Qp[Q] & Qp[Q2]
        if X and nd(X):
            s_ = cellcov(X)
            if s_: sup.add(s_)
    for C in cells:
        if C & ~Qp[Q] == 0: sup.add(C)
    sup = sorted(sup); node_sup[Q] = sup
    us = users_of[Q]; n = len(us); nsl = n + KX
    for j in range(nsl):
        u_ = M.NewBoolVar(''); used.append(u_)
        chs = [M.NewBoolVar('') for _ in sup]; M.AddExactlyOne(chs)
        for s in bits(Qp[Q]):
            M.AddImplication(abit(Q, j, s), u_)
            M.AddBoolOr([abit(Q, j, s).Not()] + [c for c, S_ in zip(chs, sup) if S_ >> s & 1])
        for t in us: M.AddImplication(lam(t, Q, j), u_)
    allowed = []
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
    M.AddAllowedAssignments([lam(t, Q, j) for t in us for j in range(nsl)] + [zin(t, Q) for t in us], allowed)
nsl_of = {Q: len(users_of[Q]) + KX for Q in cells}
treps = sorted(set(min(p[t] for p in PERMS) for t in range(V)))
for t in treps:
    mine = [Q for Q in cells if t in users_of[Q]]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    opts = []
    for Qs in mine:
        Xs = set(C for C in cells if C & ~Qp[Qs] == 0)
        for Q2 in cells:
            if Q2 != Qs:
                X = Qp[Qs] & Qp[Q2]
                if X and nd(X):
                    s_ = cellcov(X)
                    if s_: Xs.add(s_)
        for X in Xs:
            b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); opts.append((b, X))
    M.Add(sum(b for b, X in opts) <= 1)
    inch = {}
    for s in bits(HYP[t]):
        bb = M.NewBoolVar(''); inch[s] = bb
        M.AddBoolOr([bb.Not()] + [b for b, X in opts if X >> s & 1])
    for s in bits(HYP[t]):
        terms = []
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(nsl_of[Q]):
                x = M.NewBoolVar(''); a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        terms.append(inch[s])
        M.AddBoolXOr(terms)
M.Minimize(sum(used))
print('built; vars', len(VV), 'section reps', len(reps_S), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); ok = r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
print(SYS, 'KX', KX, 'status', sol.StatusName(r), 'used slot orbits', sol.ObjectiveValue() if ok else None, 'bound', sol.BestObjectiveBound(),
      '(x11 registers) => arrivals', 11 * sol.ObjectiveValue() if ok else None, flush=True)
