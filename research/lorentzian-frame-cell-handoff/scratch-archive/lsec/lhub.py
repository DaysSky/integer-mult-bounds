"""I_{11,1} hub model (capacity-EXACT for raw-input hubs), H55-canonical, for a design (sections = design planes).
Hubs: apex flats D(S,p) = {P(ij), T(ijp) : i,j in S}, |S| in HS, nondegenerate, lying in >= 1 section perp.
An active hub X takes all |X| of its lines as raw input registers (span = F2^X exactly) and emits <= |X| arrivals,
each any vector on X's lines, to sections Q with X ⊂ Q-perp; surplus inputs die (waste counted).
Section slots (|Q| per section): source = active hub ⊂ Q-perp, raw line in Q-perp (1 register), empty fresh helper
(1 register), or absent (no register; delivered users may not use it).  Delivered users' lam rows independent; at most
one in-chain section per target (any combination) + optional in-chain read at an ACTIVE hub nested in that section
(any vector on the hub's lines).  Targets: sum = R(t).  Objective: total registers N = sum active |X| + raw + empty.
R = N - v (+ 11 decoder totals not counted)."""
import sys, json, itertools
from lcommon import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); DES = sys.argv[2]; HS = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [3, 4, 5]
NCAP = int(sys.argv[4]) if len(sys.argv) > 4 else 0
planes = [int(h, 16) for h in json.load(open(DES))['planes']]
Qp = {Q: perpmask(Q) for Q in planes}
def Dflat(S, p):
    m = 0
    for i, j in itertools.combinations(sorted(S), 2):
        m |= 1 << g.P(i, j); m |= 1 << g.T(i, j, p)
    return m
hubs = set()
for p in range(11):
    others = [i for i in range(11) if i != p]
    for k in HS:
        for S in itertools.combinations(others, k):
            X = Dflat(S, p)
            if any(X & ~Qp[Q] == 0 for Q in planes) and nondeg_span(X): hubs.add(X)
hubs = sorted(hubs)
print('hubs', len(hubs), collections.Counter(pc(X) for X in hubs), flush=True)
def gimg(o, p):
    k, v = o
    if k == 'L': return (k, p[v])
    if k in ('S', 'X'): return (k, act(v, p))
    return o
def canon(tup): return min(tuple(gimg(o, p) for o in tup) for p in PERMS)
M = cp_model.CpModel(); V_ = {}
def var(tup):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('')
    return V_[c]
act_h = lambda X: var((('X', X), ('act', 0)))
ch = lambda Q, j, src: var((('S', Q), ('j', j), src))
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
reps_S = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); reps_S.append(Q)
hubs_in = {Q: [X for X in hubs if X & ~Qp[Q] == 0] for Q in planes}
feeds = collections.defaultdict(list)
cost_terms = []
for Q in reps_S:
    cl = [('N', 0), ('F', 0)] + [('R', s) for s in bits(Qp[Q])] + [('X', X) for X in hubs_in[Q]]
    for j in range(pc(Q)):
        M.AddExactlyOne([ch(Q, j, c) for c in cl])
        for c in cl:
            if c[0] == 'X': M.AddImplication(ch(Q, j, c), act_h(c[1]))
            seenk = set()
            for p in PERMS:
                key = (act(Q, p), j)
                if key in seenk: continue
                seenk.add(key)
                feeds[gimg(c, p)].append(ch(Q, j, c))
        for s in bits(Qp[Q]):
            a = abit(Q, j, s)
            for c in cl:
                k, v = c
                if k in ('N', 'F'): M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                elif k == 'R':
                    if v != s: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                else:
                    if not (v >> s & 1): M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
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
# hub capacity (orbit reps) and register cost
done = set(); hub_cost = []
for X in hubs:
    c = canon((('X', X),))
    if c in done: continue
    done.add(c)
    outs = feeds.get(('X', X), [])
    M.Add(sum(outs) <= pc(X) * act_h(X))
    orbsz = len(set(act(X, p) for p in PERMS))
    hub_cost.append(orbsz * pc(X) * act_h(X))
raw_cost = []
for s in line_reps:
    orbsz = len(set(p[s] for p in PERMS))
    # each raw slot fed by line s is one register; feeds lists all slot images, so count all
    raw_cost += feeds.get(('R', s), []) and [sum(feeds.get(('R', s), [])) * 0] or []
raw_all = []
for s in range(V): raw_all += feeds.get(('R', s), [])
fresh = feeds.get(('F', 0), [])
print('model: hubs reps', len(done), flush=True)
# targets
for t in line_reps:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    opts = []
    for Qs in mine:
        for X in hubs_in[Qs]:
            if X & ~HYP[t]: continue
            b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); M.AddImplication(b, act_h(X)); opts.append((b, X))
    M.Add(sum(b for b, X in opts) <= 1)
    for s in bits(HYP[t]):
        terms = []
        rb = M.NewBoolVar('')
        M.AddBoolOr([rb.Not()] + [b for b, X in opts if X >> s & 1])
        terms.append(rb)
        for Q in mine:
            if not (Qp[Q] >> s & 1): continue
            for j in range(pc(Q)):
                x = M.NewBoolVar(''); a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        M.AddBoolXOr(terms)
N = sum(hub_cost) + sum(raw_all) + sum(fresh)
if NCAP: M.Add(N <= NCAP)
M.Minimize(N)
print('built; vars', len(V_), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    Nv = sol.ObjectiveValue()
    print('registers N =', Nv, ' R = N - v =', Nv - V, ' (+11 totals); break-even R <= ~739;  proven N >=', sol.BestObjectiveBound(), flush=True)
    print('active hub orbits:', sum(1 for X in hubs if sol.Value(act_h(X))), flush=True)
