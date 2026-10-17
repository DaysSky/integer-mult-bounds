"""Lorentzian frame-cell CAPACITY model (depth 2), analogue of sec4/fcap.py, for a source system json (line -> cover).
Cells = {a,b} for b in cover(a).  Sections: for each line t, the perps of its own cells (frame top); a section
{a,b}-perp has users = those of a,b whose cover contains the other.  Nodes = nondegenerate Q-perp ∩ Q'-perp holding
>= 1 cell, plus the cells themselves (direct).  Cell C: 2 + e_C registers (+1 forced if C is a defect: the partner's
content needs an extra branch, counted in N), <= 1 + e_C sum streams.  Node Y: #slots fed <= #streams in + e_Y.
Slot content per cell = vector in span(C's streams into the source node).  Users: delivered rows independent, <= 1
in-chain section, one nested node read inside it, one cell read.  Z11-canonical.  Minimise N = 660 + defects + sum e.
usage: lfcap.py SYSJSON KX tl"""
import sys, os, json, itertools, collections
os.environ['GRP'] = '11'
from lbase import *
from ortools.sat.python import cp_model
SYS, KX, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
cov = {int(k): v for k, v in json.load(open(SYS)).items()}
cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(cov[a])))
defect = {C: not all(cov[x] >> y & 1 for x in bits(C) for y in bits(C) if x != y) for C in cells}
users_of = {C: [x for x in bits(C) if any(cov[x] >> y & 1 for y in bits(C) if y != x)] for C in cells}
Qp = {C: perp(C) for C in cells}
cells_in = lambda X: [C for C in cells if C & ~X == 0]
nodes = set(cells)
for i, Q in enumerate(cells):
    for Q2 in cells[i + 1:]:
        Y = closure(Qp[Q] & Qp[Q2]) if False else (Qp[Q] & Qp[Q2])
        if Y and cells_in(Y) and nondeg_span(Y): nodes.add(Y)
nodes = sorted(nodes)
print('cells', len(cells), 'defects', sum(defect.values()), 'nodes', len(nodes), flush=True)
def canon(tup):
    best = None
    for p in PERMS:
        c = tuple((k, p[v]) if k == 'L' else ((k, act(v, p)) if k in ('S', 'C', 'Y') else (k, v)) for k, v in tup)
        if best is None or c < best: best = c
    return best
M = cp_model.CpModel(); VV = {}
def var(tup, ub=None):
    c = canon(tup)
    if c not in VV: VV[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return VV[c]
def orb(m): return len(set(act(m, p) for p in PERMS))
nodes_of_cell = {C: [Y for Y in nodes if C & ~Y == 0] for C in cells}
st = lambda C, Y, k: var((('C', C), ('Y', Y), ('k', k)))
eC = lambda C: var((('C', C), ('e', 0)), 2)
eY = lambda Y: var((('Y', Y), ('e', 0)), 4)
creps = []; seen = set()
for C in cells:
    c = canon((('C', C),))
    if c in seen: continue
    seen.add(c); creps.append(C)
    M.Add(sum(st(C, Y, k) for Y in nodes_of_cell[C] for k in ('sum', 'lo', 'hi')) <= 2 + eC(C))
    M.Add(sum(st(C, Y, 'sum') for Y in nodes_of_cell[C]) <= 1 + eC(C))
def span_clauses(guard, C, Y, zl, zh, extra=()):
    a = {k: st(C, Y, k) for k in ('sum', 'lo', 'hi')}
    plh = M.NewBoolVar(''); M.AddBoolAnd([a['lo'], a['hi']]).OnlyEnforceIf(plh)
    psh = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['hi']]).OnlyEnforceIf(psh)
    psl = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['lo']]).OnlyEnforceIf(psl)
    M.AddBoolOr([guard.Not(), zl.Not(), zh.Not(), a['sum'], plh] + list(extra))
    M.AddBoolOr([guard.Not(), zl.Not(), zh, a['lo'], psh] + list(extra))
    M.AddBoolOr([guard.Not(), zl, zh.Not(), a['hi'], psl] + list(extra))
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
src = lambda Q, j, Y: var((('S', Q), ('j', j), ('Y', Y), ('src', 0)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
feeds = collections.defaultdict(list)
sreps = []; seenS = set()
for Q in cells:
    c = canon((('S', Q),))
    if c not in seenS: seenS.add(c); sreps.append(Q)
nsl = 2 + KX
for Q in sreps:
    Ys = [Y for Y in nodes if Y & ~Qp[Q] == 0]
    for j in range(nsl):
        M.Add(sum(src(Q, j, Y) for Y in Ys) <= 1)
        for Y in Ys:
            seenimg = set()
            for p in PERMS:
                key = (act(Q, p), act(Y, p))
                if key in seenimg: continue
                seenimg.add(key); feeds[act(Y, p)].append(src(Q, j, Y))
        terms = collections.defaultdict(list)
        for C in cells_in(Qp[Q]):
            lo, hi = sorted(bits(C))
            zl, zh = M.NewBoolVar(''), M.NewBoolVar('')
            for Y in Ys:
                if C & ~Y:
                    M.AddBoolOr([src(Q, j, Y).Not(), zl.Not()]); M.AddBoolOr([src(Q, j, Y).Not(), zh.Not()])
                else: span_clauses(src(Q, j, Y), C, Y, zl, zh)
            terms[lo].append(zl); terms[hi].append(zh)
        for s in bits(Qp[Q]):
            ts = terms.get(s, [])
            if ts: M.AddBoolXOr(ts + [abit(Q, j, s).Not()])
            else: M.Add(abit(Q, j, s) == 0)
    users = users_of[Q]; n = len(users); allowed = []
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
    for j in range(nsl):
        used = M.NewBoolVar(''); M.Add(sum(src(Q, j, Y) for Y in Ys) == used)
        for t in users: M.AddImplication(lam(t, Q, j), used)
yreps = []; seenY = set()
for Y in nodes:
    c = canon((('Y', Y),))
    if c in seenY: continue
    seenY.add(c); yreps.append(Y)
    M.Add(sum(feeds.get(Y, [])) <= sum(st(C, Y, k) for C in cells_in(Y) for k in ('sum', 'lo', 'hi')) + eY(Y))
treps = sorted(set(min(p[t] for p in PERMS) for t in range(V)))
for t in treps:
    mine = [Q for Q in cells if t in users_of[Q]]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    nr = {}
    for Qs in mine:
        for Y in nodes:
            if Y & ~Qp[Qs] == 0:
                b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); nr[(Qs, Y)] = b
    M.Add(sum(nr.values()) <= 1)
    crd = {C: M.NewBoolVar('') for C in cells if C & ~HYP[t] == 0}
    M.Add(sum(crd.values()) <= 1)
    zt = {}
    for C in crd:
        lo, hi = sorted(bits(C)); zl, zh = M.NewBoolVar(''), M.NewBoolVar(''); okl = []
        for (Qs, Y), b in nr.items():
            if C & ~Y: continue
            span_clauses(b, C, Y, zl, zh, extra=[crd[C]]); okl.append(b)
        M.AddBoolOr([zl.Not()] + okl + [crd[C]]); M.AddBoolOr([zh.Not()] + okl + [crd[C]])
        zt[C] = (lo, zl, hi, zh)
    for s in bits(HYP[t]):
        terms = []
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(nsl):
                x = M.NewBoolVar(''); a_, l_ = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a_, l_]).OnlyEnforceIf(x); M.AddBoolOr([a_.Not(), l_.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        for C, (lo, zl, hi, zh) in zt.items():
            if lo == s: terms.append(zl)
            elif hi == s: terms.append(zh)
        M.AddBoolXOr(terms)
E = sum(orb(C) * eC(C) for C in creps) + sum(orb(Y) * eY(Y) for Y in yreps)
M.Minimize(E)
print('built; vars', len(VV), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); ok = r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
nd = sum(defect.values())
print(SYS, 'KX', KX, 'status', sol.StatusName(r), 'extra', sol.ObjectiveValue() if ok else None, 'bound', sol.BestObjectiveBound(),
      '=> N =', 660 + nd + sol.ObjectiveValue() if ok else None, 'R =', 440 + nd + sol.ObjectiveValue() if ok else None, flush=True)
