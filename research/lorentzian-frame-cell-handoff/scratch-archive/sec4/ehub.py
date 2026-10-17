"""E8 hub model (capacity-EXACT for raw-input hubs), Z15-canonical, for a 4-plane design (env DESIGN).
Hubs: flats from flats.pkl (rank 3..5, >= 1 design cell and >= 1 section) + block D4s.  Active hub X: all |X| lines as
raw input registers, emits <= |X| arrivals (any vector on X's lines) to sections Q with X ⊂ Q-perp.  Slots: hub / raw
line / empty / absent.  Delivered users' rows independent; <= 1 in-chain section per target + optional nested in-chain
read at an active hub inside it.  Objective: N = sum active |X| + raw + empty;  R = N - 120 (+9 totals)."""
import sys, json, itertools, pickle
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); MAXR = int(sys.argv[2]) if len(sys.argv) > 2 else 5
Qp = {Q: perpmask(Q) for Q in planes}
flats = pickle.load(open('flats.pkl', 'rb'))
hubs = set(F for F, r, c, s in flats if r <= MAXR)
D4 = load_d4()
for W in D4:
    if any(W & ~Qp[Q] == 0 for Q in planes): hubs.add(W)
hubs = sorted(hubs)
print('hubs', len(hubs), collections.Counter(pc(X) for X in hubs).most_common(8), flush=True)
def g_(o):
    k, v = o
    if k == 'L': return (k, perm[v])
    if k in ('S', 'X'): return (k, act(v))
    return o
def rot(o, k):
    for _ in range(k): o = g_(o)
    return o
def canon(tup):
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
for Q in reps_S:
    cl = [('N', 0), ('F', 0)] + [('R', s) for s in e8.bits(Qp[Q])] + [('X', X) for X in hubs_in[Q]]
    orbitQ = []; cur = Q
    for k in range(15):
        orbitQ.append(k); cur = act(cur)
        if cur == Q: break
    for j in range(pc(Q)):
        M.AddExactlyOne([ch(Q, j, c) for c in cl])
        for c in cl:
            if c[0] == 'X': M.AddImplication(ch(Q, j, c), act_h(c[1]))
            for k in orbitQ: feeds[rot(c, k)].append(ch(Q, j, c))
        for s in e8.bits(Qp[Q]):
            a = abit(Q, j, s)
            for c in cl:
                k_, v = c
                if k_ in ('N', 'F'): M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                elif k_ == 'R':
                    if v != s: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                else:
                    if not (v >> s & 1): M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
    users = e8.bits(Q); n = len(users); allowed = []
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
done = set(); hub_cost = []
for X in hubs:
    c = canon((('X', X),))
    if c in done: continue
    done.add(c)
    outs = feeds.get(('X', X), [])
    M.Add(sum(outs) <= pc(X) * act_h(X))
    orbsz = len(orbit(X))
    hub_cost.append(orbsz * pc(X) * act_h(X))
raw_all = []
for s in range(V): raw_all += feeds.get(('R', s), [])
fresh = feeds.get(('F', 0), [])
print('hub reps', len(done), flush=True)
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    opts = []
    for Qs in mine:
        for X in hubs_in[Qs]:
            if X & ~e8.HYP[t]: continue
            b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); M.AddImplication(b, act_h(X)); opts.append((b, X))
    M.Add(sum(b for b, X in opts) <= 1)
    for s in e8.bits(e8.HYP[t]):
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
M.Minimize(N)
print('built; vars', len(V_), flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M); print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    Nv = sol.ObjectiveValue()
    print('registers N =', Nv, ' R = N - 120 =', Nv - 120, ' (+9 totals; R420 = 420, wall 480 at v=120)  proven N >=', sol.BestObjectiveBound(), flush=True)
