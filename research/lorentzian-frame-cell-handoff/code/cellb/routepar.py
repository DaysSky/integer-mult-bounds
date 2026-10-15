"""ROUTE-LEVEL relaxation, UNRESTRICTED top (a target may receive any register whose node lies in t-perp), for any
3-branch frame-cell source system: cell C = {s,a} has 2 + j_C registers; streams go to nodes N = closure(C + x)
(nondegenerate), at most 1 + j_C carry s+a, at most 2 + j_C in total.  x_u reaches t iff a stream of a cell of u
containing u has N ⊂ t-perp, or t reads that cell in-chain (<= 1 rank-2 read per target).  Minimise sum j_C
(exact lower bound on extra cell registers for this class: R >= 2v + sum j_C).  Symmetry-canonical.
usage: routefree.py SYSTEM(e8|lor) GRAPH(json or 'r420') tl"""
import sys, os, json, collections
from ortools.sat.python import cp_model
SYSTEM, GRAPH, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
if SYSTEM == 'e8':
    sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
    import e8
    V = e8.V; HYP = e8.HYP; bits = e8.bits
    perm = json.load(open('../sec4/coxeter.json'))['perm']
    P = [list(range(V))]; q = perm
    while q != list(range(V)): P.append(q); q = [perm[i] for i in q]
    PERMS = P
    clos = lambda m: e8.closure(m)[0]; nondeg = lambda m: True
    if GRAPH == 'r420': cells = [int(h, 16) for h in json.load(open('../sec4/r420cells.json'))['planes']]
    else:
        adj = json.load(open(GRAPH)); cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in adj[a]))
else:
    sys.path.insert(0, '../lcell'); os.environ.setdefault('GRP', '55')
    from lbase import V, HYP, bits, PERMS, nondeg_span, closure as clos
    nondeg = nondeg_span
    if os.environ.get('NOSYM') == '1': PERMS = [list(range(V))]
    Fa = {int(k): v for k, v in json.load(open(GRAPH)).items()}
    cells = sorted(set((1 << a) | (1 << b) for a in range(V) for b in bits(Fa[a]) if b != a))
def actp(m, p):
    r = 0
    for s in bits(m): r |= 1 << p[s]
    return r
_CANON = {}
def canon_tup(tup):
    if tup in _CANON: return _CANON[tup]
    _CANON[tup] = _canon_tup(tup); return _CANON[tup]
def _canon_tup(tup):
    best = None
    for p in PERMS:
        c = tuple((k, p[v]) if k == 'L' else ((k, actp(v, p)) if k in ('C', 'N') else (k, v)) for k, v in tup)
        if best is None or c < best: best = c
    return best
cellset = set(cells); assert all(actp(C, p) in cellset for C in cells for p in PERMS)
cells_of = {s: [C for C in cells if C >> s & 1] for s in range(V)}
CL = {}
def closure(m):
    if m not in CL: CL[m] = clos(m)
    return CL[m]
nodes_of = {}
for C in cells:
    ns = set()
    for x in range(V):
        if C >> x & 1: continue
        N = closure(C | (1 << x))
        if nondeg(N) or os.environ.get('ALLNODES') == '1': ns.add(N)
    nodes_of[C] = sorted(ns)
M = cp_model.CpModel(); VV = {}
def var(tup, ub=None):
    c = canon_tup(tup)
    if c not in VV: VV[c] = M.NewBoolVar('') if ub is None else M.NewIntVar(0, ub, '')
    return VV[c]
st = lambda C, N, k: var((('C', C), ('N', N), ('k', k)))
jC = lambda C: var((('C', C), ('j', 0)), 3)
seen = set(); reps = []
for C in cells:
    c = canon_tup((('C', C),))
    if c in seen: continue
    seen.add(c); reps.append(C)
    ns = nodes_of[C]
    M.Add(sum(st(C, N, 'sum') for N in ns) <= 1 + jC(C))
    M.Add(sum(st(C, N, k) for N in ns for k in ('sum', 'lo', 'hi')) <= 2 + jC(C))
tseen = set(); treps = []
for t in range(V):
    c = canon_tup((('L', t),))
    if c in tseen: continue
    tseen.add(c); treps.append(t)
PAR = int(os.environ.get('PAR', '1')); XB = int(os.environ.get('XB', '0')); TOP = os.environ.get('TOP', 'free')
def _perp(m):
    r = (1 << V) - 1
    for x in bits(m): r &= HYP[x]
    return r
if SYSTEM == 'e8' and GRAPH == 'r420':
    _nb = {t: [y for C in cells if C >> t & 1 for y in bits(C) if y != t] for t in range(V)}
elif SYSTEM == 'e8':
    _nb = {t: adj[t] for t in range(V)}
else:
    _nb = {t: list(bits(Fa[t])) for t in range(V)}
OWN = {t: [_perp((1 << t) | (1 << f)) for f in _nb[t]] for t in range(V)}
TOPFR = {}
if TOP == 'choose':
    import pickle as _pk
    if SYSTEM == 'e8': _frs = _pk.load(open('d4frames.pkl', 'rb'))
    else:
        from lbase import goodframes as _gf
        _frs = _gf()
    for t in range(V):
        TOPFR[t] = [(F, [_perp((1 << t) | (1 << f)) for f in bits(F) if f != t]) for F in _frs if F >> t & 1]
PLANES_T = {}
MAXSEC = int(os.environ.get('MAXSEC', '4'))
if TOP == 'sec4':
    for t in range(V):
        ps = set()
        for x in range(V):
            if x != t:
                Q = closure((1 << t) | (1 << x))
                if nondeg(Q): ps.add(Q)
        PLANES_T[t] = sorted((Q, _perp(Q)) for Q in ps)
_ytf = {}
_use = {}
def inside_t(t, N):
    if TOP == 'frame': return bool(any(N & ~S == 0 for S in OWN[t]))
    if TOP == 'sec4':
        key = (t, N)
        if key not in _use:
            lits = [var((('L', t), ('N', Q), ('sec', 0))) for Q, P in PLANES_T[t] if N & ~P == 0]
            if not lits: _use[key] = False
            else:
                y = M.NewBoolVar(''); M.AddBoolOr([y.Not()] + lits); _use[key] = y
        return _use[key]
    if TOP == 'choose':
        key = (t, N)
        if key not in _use:
            lits = [var((('L', t), ('N', F), ('top', 0))) for F, secs in TOPFR[t] if any(N & ~S2 == 0 for S2 in secs)]
            if not lits: _use[key] = False
            else:
                y = M.NewBoolVar(''); M.AddBoolOr([y.Not()] + lits); _use[key] = y
        return _use[key]
    return bool(N & ~HYP[t] == 0)
xb_planes = {}
if XB:
    for u in range(V):
        ps = set()
        for x in range(V):
            if x != u:
                Q = closure((1 << u) | (1 << x))
                if nondeg(Q): ps.add(Q)
        xb_planes[u] = sorted(ps)
xbv = lambda u, Q: var((('L', u), ('N', Q), ('xb', 0)))
for t in treps:
    if TOP == 'choose':
        M.AddExactlyOne([var((('L', t), ('N', F), ('top', 0))) for F, secs in TOPFR[t]])
    if TOP == 'sec4':
        M.Add(sum(var((('L', t), ('N', Q), ('sec', 0))) for Q, P in PLANES_T[t]) <= MAXSEC)
    cr = {}
    for C in cells:
        u_ = inside_t(t, C)
        if u_ is False: continue
        cr[C] = M.NewBoolVar('')
        if u_ is not True: M.AddImplication(cr[C], u_)
    M.Add(sum(cr.values()) <= 1)
    if not PAR:
        for u in bits(HYP[t]):
            opts = []
            for C in cells_of[u]:
                if C in cr: opts.append(cr[C])
                lo = min(bits(C))
                for N in nodes_of[C]:
                    u_ = inside_t(t, N)
                    if u_ is False: continue
                    for lit in (st(C, N, 'sum'), st(C, N, 'lo' if u == lo else 'hi')):
                        if u_ is True: opts.append(lit)
                        else:
                            z_ = M.NewBoolVar(''); M.AddImplication(z_, lit); M.AddImplication(z_, u_); opts.append(z_)
            if XB: opts += [xbv(u, Q) for Q in xb_planes[u] if Q & ~HYP[t] == 0]
            M.AddBoolOr(opts)
        continue
    # PARITY relaxation: t picks from each cell C ⊂ t-perp a vector z_C in span(contents of C's streams with node in
    # t-perp) (full span if t reads C); sum over cells must equal R(t) on every line.
    z = {}
    for C in cr:
        lo, hi = sorted(bits(C))
        av = {k: M.NewBoolVar('') for k in ('sum', 'lo', 'hi')}
        for k in av:
            lits = []
            for N in nodes_of[C]:
                u_ = inside_t(t, N)
                if u_ is False: continue
                if u_ is True: lits.append(st(C, N, k))
                else:
                    z_ = M.NewBoolVar(''); M.AddImplication(z_, st(C, N, k)); M.AddImplication(z_, u_); lits.append(z_)
            M.AddBoolOr([av[k].Not()] + lits) if lits else M.Add(av[k] == 0)
        zl, zh = M.NewBoolVar(''), M.NewBoolVar('')
        rd = cr[C]
        # (zl,zh)=(1,1) needs sum in span: av_sum or (av_lo and av_hi) or read
        b11 = M.NewBoolVar(''); M.AddBoolAnd([zl, zh]).OnlyEnforceIf(b11); M.AddBoolOr([zl.Not(), zh.Not(), b11])
        b10 = M.NewBoolVar(''); M.AddBoolAnd([zl, zh.Not()]).OnlyEnforceIf(b10); M.AddBoolOr([zl.Not(), zh, b10])
        b01 = M.NewBoolVar(''); M.AddBoolAnd([zl.Not(), zh]).OnlyEnforceIf(b01); M.AddBoolOr([zl, zh.Not(), b01])
        p_lh = M.NewBoolVar(''); M.AddBoolAnd([av['lo'], av['hi']]).OnlyEnforceIf(p_lh)
        p_sh = M.NewBoolVar(''); M.AddBoolAnd([av['sum'], av['hi']]).OnlyEnforceIf(p_sh)
        p_sl = M.NewBoolVar(''); M.AddBoolAnd([av['sum'], av['lo']]).OnlyEnforceIf(p_sl)
        M.AddBoolOr([b11.Not(), av['sum'], p_lh, rd])
        M.AddBoolOr([b10.Not(), av['lo'], p_sh, rd])
        M.AddBoolOr([b01.Not(), av['hi'], p_sl, rd])
        z[C] = (lo, zl, hi, zh)
    for u in bits(HYP[t]):
        terms = []
        for C, (lo, zl, hi, zh) in z.items():
            if C >> u & 1: terms.append(zl if u == lo else zh)
        if XB:
            xs = [xbv(u, Q) for Q in xb_planes[u] if Q & ~HYP[t] == 0]
            if xs:
                w = M.NewBoolVar('')                       # t takes x_u from one available extra branch of u
                M.AddBoolOr([w.Not()] + xs); terms.append(w)
        M.AddBoolXOr(terms)
def orb(C): return len(set(actp(C, p) for p in PERMS))
def orbx(c):
    u = c[0][1]; Q = c[1][1]
    return len(set((p[u], actp(Q, p)) for p in PERMS))
J = sum(orb(C) * jC(C) for C in reps)
if XB:
    xb_reps = [c for c in VV if any(o[0] == 'xb' for o in c)]
    J = J + sum(orbx(c) * VV[c] for c in xb_reps)
M.Minimize(J)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 2
r = sol.Solve(M)
print(SYSTEM, GRAPH, 'TOP', TOP, 'PAR', PAR, 'cells', len(cells), 'reps', len(reps), 'status', sol.StatusName(r), 'min sum j_C',
      sol.ObjectiveValue() if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None, 'bound', sol.BestObjectiveBound(), flush=True)
