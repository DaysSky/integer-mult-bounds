"""Frame-cell CAPACITY model (E8, depth 2): cells -> nodes -> section slots, with EXACT GF(2) contents spanned by
cell streams.  Sections = perps of the cells (frame top, 2 users each), cells = the same cells (env DESIGN).
Cell C={lo,hi}: 2 + e_C registers; streams to nodes Y ⊇ C (Y = Q-perp ∩ Q'-perp for sections Q,Q', or Y = C
itself = direct), contents sum/lo/hi, <= 1 + e_C sum streams.  Node Y: inputs = streams into Y + e_Y empties; each
section slot fed by Y uses one register (#slots fed <= #inputs); a slot's content = any XOR of Y's inputs (per cell:
a vector in the span of that cell's streams into Y).  RELAXATION: node outputs need not be independent; deeper
nesting is NOT modelled (restriction).  Users: delivered rows independent, <= 1 in-chain section per target (any
combination), plus one nested node read inside it and one in-chain cell read.  Minimise N = 360 + sum e."""
import sys, itertools, os, json
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); KX = int(sys.argv[2]); sym = int(sys.argv[3]) if len(sys.argv) > 3 else 1
Qp = {Q: perpmask(Q) for Q in planes}
cells = planes
cells_in = lambda X: [C for C in cells if C & ~X == 0]
def g_(o):
    k, v = o
    return (k, perm[v]) if k == 'L' else ((k, act(v)) if k in ('S', 'C', 'Y') else o)
def canon(tup):
    if not sym: return tup
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g_(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel(); V_ = {}
def var(tup, ub=None):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return V_[c]
# nodes
nodes = set()
for Q in planes:
    for Q2 in planes:
        if Q2 != Q:
            Y = Qp[Q] & Qp[Q2]
            if cells_in(Y): nodes.add(Y)
nodes |= set(cells)
nodes = sorted(nodes)
nodes_of_cell = {C: [Y for Y in nodes if C & ~Y == 0] for C in cells}
print('nodes', len(nodes), 'avg nodes per cell', sum(len(v) for v in nodes_of_cell.values()) / len(cells), flush=True)
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
def span_ok(C, Y, zl, zh, extra_true=None):
    """constrain (zl,zh) in span of C's stream contents into Y (or anything if extra_true)."""
    a = {k: st(C, Y, k) for k in ('sum', 'lo', 'hi')}
    b11 = M.NewBoolVar(''); M.AddBoolAnd([zl, zh]).OnlyEnforceIf(b11); M.AddBoolOr([zl.Not(), zh.Not(), b11])
    b10 = M.NewBoolVar(''); M.AddBoolAnd([zl, zh.Not()]).OnlyEnforceIf(b10); M.AddBoolOr([zl.Not(), zh, b10])
    b01 = M.NewBoolVar(''); M.AddBoolAnd([zl.Not(), zh]).OnlyEnforceIf(b01); M.AddBoolOr([zl, zh.Not(), b01])
    plh = M.NewBoolVar(''); M.AddBoolAnd([a['lo'], a['hi']]).OnlyEnforceIf(plh)
    psh = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['hi']]).OnlyEnforceIf(psh)
    psl = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['lo']]).OnlyEnforceIf(psl)
    ex = [extra_true] if extra_true is not None else []
    M.AddBoolOr([b11.Not(), a['sum'], plh] + ex)
    M.AddBoolOr([b10.Not(), a['lo'], psh] + ex)
    M.AddBoolOr([b01.Not(), a['hi'], psl] + ex)
# section slots
reps_S = []; seenS = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seenS: seenS.add(c); reps_S.append(Q)
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
src = lambda Q, j, Y: var((('S', Q), ('j', j), ('Y', Y), ('src', 0)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
def orbQ(m):
    if not sym: return 1
    o = {m}; y = act(m)
    while y != m: o.add(y); y = act(y)
    return len(o)
feeds = {}   # canonical node -> list of slot-source literals (orbit-expanded)
for Q in reps_S:
    nsl = 2 + KX
    Ys = [Y for Y in nodes if Y & ~Qp[Q] == 0]
    for j in range(nsl):
        lits = [src(Q, j, Y) for Y in Ys]
        M.Add(sum(lits) <= 1)
        for Y in Ys:
            # orbit expansion of feeds: map (Q,Y) pairs under Z15
            YY = Y
            for _ in range(orbQ(Q)):
                feeds.setdefault(YY, []).append(src(Q, j, Y))
                YY = act(YY)
        # content: per cell inside Q-perp, (zl,zh) chosen; must be in span of the source node's streams
        for C in cells_in(Qp[Q]):
            lo, hi = sorted(e8.bits(C))
            zl, zh = M.NewBoolVar(''), M.NewBoolVar('')
            for Y in Ys:
                if C & ~Y: 
                    M.AddBoolOr([src(Q, j, Y).Not(), zl.Not()]); M.AddBoolOr([src(Q, j, Y).Not(), zh.Not()])
                    continue
                # if src = Y then (zl,zh) in span(C->Y)
                s_ = src(Q, j, Y)
                a = {k: st(C, Y, k) for k in ('sum', 'lo', 'hi')}
                plh = M.NewBoolVar(''); M.AddBoolAnd([a['lo'], a['hi']]).OnlyEnforceIf(plh)
                psh = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['hi']]).OnlyEnforceIf(psh)
                psl = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['lo']]).OnlyEnforceIf(psl)
                M.AddBoolOr([s_.Not(), zl.Not(), zh.Not(), a['sum'], plh])
                M.AddBoolOr([s_.Not(), zl.Not(), zh, a['lo'], psh])
                M.AddBoolOr([s_.Not(), zl, zh.Not(), a['hi'], psl])
            # slot content bits: abit(Q,j,u) = XOR over cells of u inside Q-perp of their z for u
            feeds.setdefault(('z', Q, j), []).append((C, lo, zl, hi, zh))
    for j in range(nsl):
        terms = {}
        for (C, lo, zl, hi, zh) in feeds[('z', Q, j)]:
            terms.setdefault(lo, []).append(zl); terms.setdefault(hi, []).append(zh)
        for s in e8.bits(Qp[Q]):
            ts = terms.get(s, [])
            M.AddBoolXOr(ts + [abit(Q, j, s).Not()]) if ts else M.Add(abit(Q, j, s) == 0)
        if j >= 2:
            u_ = M.NewBoolVar(''); M.Add(sum(src(Q, j, Y) for Y in Ys) == u_)
    users = e8.bits(Q); n = len(users); allowed = []
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
# node capacity (per canonical node rep)
yreps = []; seenY = set()
for Y in nodes:
    c = canon((('Y', Y),))
    if c in seenY: continue
    seenY.add(c); yreps.append(Y)
    ins = [st(C, Y, k) for C in cells_in(Y) for k in ('sum', 'lo', 'hi')]
    M.Add(sum(feeds.get(Y, [])) <= sum(ins) + eY(Y))
# targets
TG = reps if sym else list(range(V))
for t in TG:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    # nested node read inside the in-chain section + one cell read
    nr = {}
    for Qs in mine:
        for Y in nodes:
            if Y & ~Qp[Qs] == 0 and len(cells_in(Y)) >= 1:
                b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); nr[(Qs, Y)] = b
    M.Add(sum(nr.values()) <= 1)
    crd = {C: M.NewBoolVar('') for C in cells if C & ~e8.HYP[t] == 0}
    M.Add(sum(crd.values()) <= 1)
    zt = {}
    for C in cells:
        if C & ~e8.HYP[t]: continue
        lo, hi = sorted(e8.bits(C))
        zl, zh = M.NewBoolVar(''), M.NewBoolVar('')
        # from node read: (zl,zh) in span(C->Y) of the read node Y, or anything if cell read of C
        ok_lits = []
        for (Qs, Y), b in nr.items():
            if C & ~Y: continue
            a = {k: st(C, Y, k) for k in ('sum', 'lo', 'hi')}
            plh = M.NewBoolVar(''); M.AddBoolAnd([a['lo'], a['hi']]).OnlyEnforceIf(plh)
            psh = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['hi']]).OnlyEnforceIf(psh)
            psl = M.NewBoolVar(''); M.AddBoolAnd([a['sum'], a['lo']]).OnlyEnforceIf(psl)
            M.AddBoolOr([b.Not(), zl.Not(), zh.Not(), a['sum'], plh, crd[C]])
            M.AddBoolOr([b.Not(), zl.Not(), zh, a['lo'], psh, crd[C]])
            M.AddBoolOr([b.Not(), zl, zh.Not(), a['hi'], psl, crd[C]])
            ok_lits.append(b)
        M.AddBoolOr([zl.Not()] + ok_lits + [crd[C]]); M.AddBoolOr([zh.Not()] + ok_lits + [crd[C]])
        zt[C] = (lo, zl, hi, zh)
    for s in e8.bits(e8.HYP[t]):
        terms = []
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(2 + KX):
                x = M.NewBoolVar(''); a_, l_ = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a_, l_]).OnlyEnforceIf(x); M.AddBoolOr([a_.Not(), l_.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        for C, (lo, zl, hi, zh) in zt.items():
            if lo == s: terms.append(zl)
            elif hi == s: terms.append(zh)
        M.AddBoolXOr(terms)
def orb(m):
    if not sym: return 1
    o = {m}; y = act(m)
    while y != m: o.add(y); y = act(y)
    return len(o)
E = sum(orb(C) * eC(C) for C in creps) + sum(orb(Y) * eY(Y) for Y in yreps)
M.Minimize(E)
print('built; vars', len(V_), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
ok = r in (cp_model.OPTIMAL, cp_model.FEASIBLE)
print(os.environ.get('DESIGN'), 'KX', KX, 'status', sol.StatusName(r), 'extra registers', sol.ObjectiveValue() if ok else None,
      'bound', sol.BestObjectiveBound(), ' => N =', 360 + sol.ObjectiveValue() if ok else None, 'R =', 240 + sol.ObjectiveValue() if ok else None, flush=True)
