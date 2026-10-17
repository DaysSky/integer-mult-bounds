"""I_{11,1} section-level content model (port of sec4/stageS*.py) for a design in ldesign.json.
Each section Q (design plane) gets |Q| arrivals; arrival (Q,j) is supported in ONE candidate support:
  raw mode (cg=0): lines of X = Q-perp ∩ Q'-perp for a design section Q' != Q (maximal multi-section nodes), or a cell
  P ⊂ Q-perp, or a single line;
  cell mode (cg=1): union of design cells inside such an X (content routed through cells), or a cell.
Deliveries c_t(Q) = sum_j lam[t,Q,j] a[Q,j], lam invertible.  Optional in-chain read per target (ic=1): any vector
supported on (cells inside) Q'-perp ∩ t-perp for a design section Q'.  Target equations: sum = R(t).
Symmetry: H55-canonical variables (sym=1) or none (sym=0)."""
import sys, json, itertools
from lcommon import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); cg = int(sys.argv[2]); ic = int(sys.argv[3]); sym = int(sys.argv[4]); EMPT = int(sys.argv[5]) if len(sys.argv) > 5 else 0; DES = sys.argv[6] if len(sys.argv) > 6 else 'ldesign.json'; IC2 = int(sys.argv[7]) if len(sys.argv) > 7 else 0; NOIND = int(sys.argv[8]) if len(sys.argv) > 8 else 0
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
Qp = {Q: perpmask(Q) for Q in planes}
cells_in = lambda X: [P for P in planes if P & ~X == 0]
def cellcov(X):
    m = 0
    for P in cells_in(X): m |= P
    return m
def canon(tup):
    if not sym: return tup
    best = None
    for p in PERMS:
        img = tuple((k, p[v]) if k == 'L' else ((k, act(v, p)) if k in ('S',) else (k, v)) for k, v in tup)
        if best is None or img < best: best = img
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
        if not X: continue
        s_ = cellcov(X) if cg else X
        if s_: sup.add(s_)
    for P in cells_in(Qp[Q]): sup.add(P)
    if not cg:
        for s in bits(Qp[Q]): sup.add(1 << s)
    sup = sorted(sup)
    for j in range(pc(Q)):
        chs = [M.NewBoolVar('') for _ in sup]; M.AddExactlyOne(chs)
        for s in bits(Qp[Q]):
            M.AddBoolOr([abit(Q, j, s).Not()] + [c for c, S_ in zip(chs, sup) if S_ >> s & 1])
        if not EMPT: M.AddBoolOr([abit(Q, j, s) for s in bits(Qp[Q])])
    users = bits(Q); n = len(users); allowed = []
    for combo in itertools.product(range(0, 2 ** n), repeat=n):
        for zs in (itertools.product((0, 1), repeat=n) if IC2 else [(0,) * n]):
            b = []; ok = True
            for v, z in zip(combo, zs):
                if z: continue
                for x in b:
                    if v ^ x < v: v ^= x
                if not v: ok = False; break
                b.append(v); b.sort(reverse=True)
            if ok: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)] + (list(zs) if IC2 else []))
    M.AddAllowedAssignments([lam(t, Q, j) for t in users for j in range(n)] + ([zin(t, Q) for t in users] if IC2 else []), allowed)
TG = line_reps if sym else list(range(V))
for t in TG:
    mine = [Q for Q in planes if Q >> t & 1]
    if IC2: M.Add(sum(zin(t, Q) for Q in mine) <= (4 if NOIND else 1))
    inch = None
    if ic:
        Fs = set()
        for Q2 in planes:
            X = Qp[Q2] & HYP[t]
            s_ = cellcov(X) if cg else X
            if s_: Fs.add(s_)
        Fs = sorted(Fs); chs = [M.NewBoolVar('') for _ in Fs]; M.AddExactlyOne(chs)
        inch = {}
        for s in bits(HYP[t]):
            b = M.NewBoolVar(''); inch[s] = b
            M.AddBoolOr([b.Not()] + [c for c, F in zip(chs, Fs) if F >> s & 1])
    for s in bits(HYP[t]):
        terms = []
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(pc(Q)):
                x = M.NewBoolVar(''); a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        if inch: terms.append(inch[s])
        M.AddBoolXOr(terms)
print('vars', len(V_), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); print(DES, 'cg', cg, 'ic', ic, 'sym', sym, 'empties', EMPT, 'inchain-dep', IC2, 'status', sol.StatusName(r), flush=True)
