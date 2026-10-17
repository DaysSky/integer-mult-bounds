"""I_{11,1} 3-level middle (support-level relaxation, exact register counts), H55-canonical.
lines -> hubs (apex D(S,p), |S| in HS; active hub = all |X| lines as raw inputs, emits <= |X| registers) -> mid nodes
(Y = Q-perp ∩ Q'-perp, nondegenerate, containing >= 1 hub, feeding >= 2 sections; inputs = hub registers sent to Y,
outputs <= inputs) -> section slots (source: mid node, hub directly, raw line, empty, absent).
Supports: hub output any vector on hub lines; mid output supported on lines of hubs feeding it (av); in-chain read at an
active hub or a fed mid node nested in the in-chain section.  N = sum active |X| + raw + empty."""
import sys, json, itertools, os
FREEMID = os.environ.get('FREEMID') == '1'
from lcommon import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); DES = sys.argv[2]; HS = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [3, 4]
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
            if nondeg_span(X): hubs.add(X)
hubs = sorted(hubs)
mids = set()
for i, Q1 in enumerate(planes):
    for Q2 in planes[i + 1:]:
        Y = Qp[Q1] & Qp[Q2]
        if Y and nondeg_span(Q1 | Q2) and (FREEMID or any(X & ~Y == 0 for X in hubs)): mids.add(Y)
mids = sorted(mids)
secs_of = {Y: [Q for Q in planes if Y & ~Qp[Q] == 0] for Y in mids}
mids = [Y for Y in mids if len(secs_of[Y]) >= 2]
hubs_in_mid = {Y: [X for X in hubs if X & ~Y == 0] for Y in mids}
hubs = sorted(set(X for Y in mids for X in hubs_in_mid[Y]) | set(X for X in hubs if any(X & ~Qp[Q] == 0 for Q in planes)))
print('hubs', len(hubs), 'mids', len(mids), flush=True)
def gimg(o, p):
    k, v = o
    if k == 'L': return (k, p[v])
    if k in ('S', 'X', 'Y'): return (k, act(v, p))
    return o
def canon(tup): return min(tuple(gimg(o, p) for o in tup) for p in PERMS)
M = cp_model.CpModel(); V_ = {}
def var(tup, integer=False):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewIntVar(0, 20, '') if integer else M.NewBoolVar('')
    return V_[c]
act_h = lambda X: var((('X', X), ('act', 0)))
hy = lambda X, Y: var((('X', X), ('Y', Y), ('hy', 0)), True)       # registers hub X -> mid Y
hyu = lambda X, Y: var((('X', X), ('Y', Y), ('hyu', 0)))
ch = lambda Q, j, src: var((('S', Q), ('j', j), src))
abit = lambda Q, j, s: var((('S', Q), ('j', j), ('L', s)))
lam = lambda t, Q, j: var((('L', t), ('S', Q), ('j', j)))
zin = lambda t, Q: var((('L', t), ('S', Q), ('z', 0)))
reps_S = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); reps_S.append(Q)
mids_in = {Q: [Y for Y in mids if Y & ~Qp[Q] == 0] for Q in planes}
hubs_inQ = {Q: [X for X in hubs if X & ~Qp[Q] == 0] for Q in planes}
feeds = collections.defaultdict(list)
for Q in reps_S:
    cl = [('N', 0), ('F', 0)] + [('R', s) for s in bits(Qp[Q])] + [('X', X) for X in hubs_inQ[Q]] + [('Y', Y) for Y in mids_in[Q]]
    for j in range(pc(Q)):
        M.AddExactlyOne([ch(Q, j, c) for c in cl])
        for c in cl:
            if c[0] == 'X': M.AddImplication(ch(Q, j, c), act_h(c[1]))
            seenk = set()
            for p in PERMS:
                key = (act(Q, p), j)
                if key in seenk: continue
                seenk.add(key); feeds[gimg(c, p)].append(ch(Q, j, c))
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
# availability at mid nodes
avm = {}
def av_mid(Y, s):
    key = canon((('Y', Y), ('L', s), ('av', 0)))
    if key not in avm:
        b = M.NewBoolVar(''); avm[key] = b
        if not FREEMID: M.AddBoolOr([b.Not()] + [hyu(X, Y) for X in hubs_in_mid[Y] if X >> s & 1])
    return avm[key]
for Q in reps_S:
    for j in range(pc(Q)):
        for s in bits(Qp[Q]):
            a = abit(Q, j, s)
            M.AddBoolOr([a.Not(), ch(Q, j, ('R', s))] + [ch(Q, j, ('X', X)) for X in hubs_inQ[Q] if X >> s & 1] +
                        [ch(Q, j, ('Y', Y)) for Y in mids_in[Q] if Y >> s & 1])
            for Y in mids_in[Q]:
                if Y >> s & 1: M.AddBoolOr([ch(Q, j, ('Y', Y)).Not(), a.Not(), av_mid(Y, s)])
                else: M.AddBoolOr([ch(Q, j, ('Y', Y)).Not(), a.Not()])
# a=1 needs a source containing s (raw s, a hub or a mid containing s); a mid source additionally needs av_mid(Y,s)
print('supports built', flush=True)
# capacities (orbit reps)
done = set(); hub_cost = []
for X in hubs:
    c = canon((('X', X),))
    if c in done: continue
    done.add(c)
    tomid = [hy(X, Y) for Y in mids if X in hubs_in_mid[Y]]
    for Y in mids:
        if X in hubs_in_mid[Y]:
            M.Add(hy(X, Y) >= 1).OnlyEnforceIf(hyu(X, Y)); M.Add(hy(X, Y) == 0).OnlyEnforceIf(hyu(X, Y).Not())
            M.AddImplication(hyu(X, Y), act_h(X))
    direct = feeds.get(('X', X), [])
    M.Add(sum(tomid) + sum(direct) <= pc(X) * act_h(X))
    hub_cost.append(len(set(act(X, p) for p in PERMS)) * pc(X) * act_h(X))
done = set()
for Y in mids:
    c = canon((('Y', Y),))
    if c in done: continue
    done.add(c)
    ins = [hy(X, Y) for X in hubs_in_mid[Y]]
    if not FREEMID: M.Add(sum(feeds.get(('Y', Y), [])) <= sum(ins))
raw_all = []
for s in range(V): raw_all += feeds.get(('R', s), [])
fresh = feeds.get(('F', 0), [])
for t in line_reps:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    opts = []
    for Qs in mine:
        for X in hubs_inQ[Qs]:
            if X & ~HYP[t]: continue
            b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); M.AddImplication(b, act_h(X)); opts.append((b, X, None))
        for Y in mids_in[Qs]:
            if Y & ~HYP[t]: continue
            b = M.NewBoolVar(''); M.AddImplication(b, zin(t, Qs)); opts.append((b, Y, 'mid'))
    M.Add(sum(o[0] for o in opts) <= 1)
    for s in bits(HYP[t]):
        terms = []
        rb = M.NewBoolVar('')
        lits = []
        for b, Xm, kind in opts:
            if not (Xm >> s & 1): continue
            if kind == 'mid':
                y = M.NewBoolVar(''); M.AddImplication(y, b); M.AddImplication(y, av_mid(Xm, s)); lits.append(y)
            else: lits.append(b)
        M.AddBoolOr([rb.Not()] + lits)
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
    print('registers N =', Nv, ' R =', Nv - V, '(+11 totals); break-even (2 levels) R <= ~655;  proven N >=', sol.BestObjectiveBound(), flush=True)
