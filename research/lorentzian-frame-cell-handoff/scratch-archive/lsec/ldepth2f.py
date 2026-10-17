"""I_{11,1} depth-2 min-register model for a design (port of sec4/depth2s.py), H55-canonical.
Registers: line -> [cell] -> [node] -> section slot.  Nodes = flats Q1-perp ∩ Q2-perp (∩ Q3-perp) of design sections that
are fed by >= 2 sections... (candidate shared nodes).  Slot sources: absent (no register; delivered users may not use it),
fresh empty helper, raw line, design cell inside Q-perp, node inside Q-perp.  Node: #inputs (raw lines + cells inside)
>= #slots fed; cell: #lines entering >= #outputs; line register count free (>= 1).  Content supports as in depth2s.
Deliveries: lam rows of delivered users independent; each target reads at most one section in-chain (any combination).
Objective: total registers N = sum_lines regs + fresh.  RELAXATION of exact node spans (supports only)."""
import sys, json, itertools
from lcommon import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); DES = sys.argv[2]; TRIPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 1; INX = int(sys.argv[4]) if len(sys.argv) > 4 else 1; ND = int(sys.argv[5]) if len(sys.argv) > 5 else 1; NCAP = int(sys.argv[6]) if len(sys.argv) > 6 else 959
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
Qp = {Q: perpmask(Q) for Q in planes}
nodes = set()
for i, Q1 in enumerate(planes):
    for Q2 in planes[i + 1:]:
        X = Qp[Q1] & Qp[Q2]
        if X and pc(X) >= 2 and (not ND or nondeg_span(Q1 | Q2)): nodes.add(X)
if TRIPLES:
    base = list(nodes)
    for X in base:
        for Q3 in planes:
            Y = X & Qp[Q3]
            if Y and Y != X and pc(Y) >= 2: nodes.add(Y)
nodes = sorted(nodes)
secs_of = {X: [Q for Q in planes if X & ~Qp[Q] == 0] for X in nodes}
nodes = [X for X in nodes if len(secs_of[X]) >= 2]
print('candidate nodes', len(nodes), flush=True)
def gimg(o, p):
    k, v = o
    if k in ('L', 'R'): return (k, p[v])
    if k in ('S', 'C', 'X'): return (k, act(v, p))
    return o
def canon(tup): return min(tuple(gimg(o, p) for o in tup) for p in PERMS)
M = cp_model.CpModel(); V_ = {}
def var(tup):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('')
    return V_[c]
reps_S = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); reps_S.append(Q)
cells_in = {X: [P for P in planes if P & ~X == 0] for X in nodes}
def cands(Q):
    q = Qp[Q]
    return [('N', 0), ('F', 0)] + [('R', s) for s in bits(q)] + [('C', P) for P in planes if P & ~q == 0] + [('X', X) for X in nodes if X & ~q == 0]
ch = lambda Q, j, src: var((('S', Q), ('j', j), src))
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
raw = lambda s, X: var((('L', s), ('X', X), ('raw', 0)))
cellin = lambda P, X: var((('C', P), ('X', X), ('in', 0)))
inP = lambda s, P: var((('L', s), ('C', P), ('inP', 0)))
feeds = collections.defaultdict(list)
for Q in reps_S:
    cl = cands(Q)
    orbQ = []
    for p in PERMS:
        orbQ.append(p)
    for j in range(pc(Q)):
        M.AddExactlyOne([ch(Q, j, c) for c in cl])
        for c in cl:
            for p in PERMS:
                ck = gimg(c, p)
                feeds[ck].append((p, Q, j, c))
def slots_fed(obj):
    out = []; seenv = set()
    for (p, Q, j, c) in feeds.get(obj, []):
        key = (act(Q, p), j)
        if key in seenv: continue
        seenv.add(key); out.append(ch(Q, j, c))
    return out
done = set()
for X in nodes:
    c = canon((('X', X),))
    if c in done: continue
    done.add(c)
    M.Add(sum([raw(s, X) for s in bits(X)] + [cellin(P, X) for P in cells_in[X]]) >= sum(slots_fed(('X', X))))
print('node reps', len(done), flush=True)
done = set()
for P in planes:
    c = canon((('C', P),))
    if c in done: continue
    done.add(c)
    outs = [cellin(P, X) for X in nodes if P & ~X == 0] + slots_fed(('C', P))
    M.Add(sum(inP(s, P) for s in bits(P)) >= sum(outs))
linecount = []; done = set()
for s in range(V):
    c = canon((('L', s),))
    if c in done: continue
    done.add(c)
    nl = M.NewIntVar(1, 60, ''); linecount.append((nl, len(set(p[s] for p in PERMS))))
    M.Add(sum(raw(s, X) for X in nodes if X >> s & 1) + sum(inP(s, P) for P in planes if P >> s & 1) + sum(slots_fed(('R', s))) <= nl)
print('counts built', flush=True)
avail = {}
def av(X, s):
    key = canon((('X', X), ('L', s), ('av', 0)))
    if key not in avail:
        b = M.NewBoolVar(''); avail[key] = b
        terms = [raw(s, X)]
        for P in cells_in[X]:
            if P >> s & 1:
                y = M.NewBoolVar(''); M.AddImplication(y, cellin(P, X)); M.AddImplication(y, inP(s, P)); terms.append(y)
        M.AddBoolOr(terms + [b.Not()])
    return avail[key]
for Q in reps_S:
    q = Qp[Q]; cl = cands(Q)
    for j in range(pc(Q)):
        for s in bits(q):
            a = abit(Q, j, s)
            for c in cl:
                k, v = c
                if k in ('N', 'F'): M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                elif k == 'R':
                    if v != s: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                elif k == 'C':
                    M.AddBoolOr([ch(Q, j, c).Not(), a.Not()] + ([inP(s, v)] if v >> s & 1 else []))
                else:
                    M.AddBoolOr([ch(Q, j, c).Not(), a.Not()] + ([av(v, s)] if v >> s & 1 else []))
    users = bits(Q); n = len(users); allowed = []
    for combo in itertools.product(range(0, 2 ** n), repeat=n):
        for zs in itertools.product((0, 1), repeat=n):
            b = []; ok = True
            for v, z in zip(combo, zs):
                if z: continue
                for x in b:
                    if v ^ x < v: v ^= x
                if not v: ok = False; break
                b.append(v); b.sort(reverse=True)
            if ok: allowed.append([((combo[i] >> j) & 1) for i in range(n) for j in range(n)] + list(zs))
    M.AddAllowedAssignments([lam(t, Q, j) for t in users for j in range(n)] + [zin(t, Q) for t in users], allowed)
    for j in range(n):
        for t in users: M.AddBoolOr([ch(Q, j, ('N', 0)).Not(), zin(t, Q), lam(t, Q, j).Not()])
print('supports built; vars', len(V_), flush=True)
for t in line_reps:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    opts = []
    if INX:
        for Qs in mine:
            for X in nodes:
                if X & ~Qp[Qs] == 0:
                    b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); opts.append((b, X))
        M.Add(sum(b for b, X in opts) <= 1)
    for s in bits(HYP[t]):
        terms = []
        if INX:
            rb = M.NewBoolVar('')
            for b, X in opts:
                if X >> s & 1: M.AddBoolOr([b.Not(), rb.Not(), av(X, s)])
                else: M.AddBoolOr([b.Not(), rb.Not()])
            M.AddBoolOr([rb.Not()] + [b for b, X in opts if X >> s & 1])
            terms.append(rb)
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(pc(Q)):
                x = M.NewBoolVar(''); a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        M.AddBoolXOr(terms)
fresh = slots_fed(('F', 0))
M.Add(sum(n * o for n, o in linecount) + sum(fresh) <= NCAP)
print('model built', flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    N = sum(sol.Value(n) * o for n, o in linecount) + sum(sol.Value(x) for x in fresh)
    print('registers N =', N, ' R = N - v =', N - V, ' (zero-waste in-chain ideal N = 3v = 660, R = 440; break-even R ~ 682-743)',
          flush=True)
