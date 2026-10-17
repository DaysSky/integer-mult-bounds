"""Depth-2 capacity model for the 4-plane design at R = 360 (480 registers, 4 per line), Z15-canonical.
Registers: line -> [cell] -> [node] -> section slot.  Each section Q has |Q| arrival slots; slot (Q,j) is fed by ONE
source: a raw line s in Q-perp, a design cell P inside Q-perp, or a multi-section node X inside Q-perp.
Node X: inputs = raw line registers raw(s,X) + cell registers cellin(P,X); #inputs = #arrival slots it feeds (n_X).
Cell P: inputs = line registers inP(s,P) (s in P); #outputs (to nodes and slots) = #inputs.
Line s: raw(s,*) + inP(s,*) + raw slots = 4.
Arrival content a[Q,j] is supported on lines available at its source: raw line {s}; cell P -> lines that entered P;
node X -> raw lines into X and entered lines of cells into X.  (RELAXATION: exact span/basis conditions at nodes and cells
are dropped; nested nodes and in-chain reads other than the optional B' block total are not modeled.)
Deliveries c_t(Q) = sum_j lam[t,Q,j] a[Q,j], lam invertible; sum_{Q∋t} c_t(Q) = R(t) (minus B' if excl)."""
import sys, pickle, itertools
from common import *
from ortools.sat.python import cp_model
tl = float(sys.argv[1]); excl = int(sys.argv[2])
D4 = load_d4()
full = [W for W in D4 if len([P for P in planes if P & ~W == 0]) == 12 and len([Q for Q in planes if Q & ~perpmask(W) == 0]) == 12]
blk = {s: k for k, W in enumerate(full) for s in e8.bits(W)}
comp = {k: full.index(perpmask(W)) for k, W in enumerate(full)}
flats = pickle.load(open('flats.pkl', 'rb'))
nodes = [F for F, r, c, s in flats if len(s) >= 2]
Qperp = {Q: perpmask(Q) for Q in planes}
def g(o):
    k, v = o
    if k in ('L', 'R'): return (k, perm[v])
    if k in ('S', 'C', 'X'): return (k, act(v))
    return o
def rot(tup, k):
    for _ in range(k): tup = tuple(g(o) for o in tup)
    return tup
def canon(tup):
    best = tup; cur = tup
    for _ in range(14):
        cur = tuple(g(o) for o in cur)
        if cur < best: best = cur
    return best
M = cp_model.CpModel()
V_ = {}
def var(tup):
    c = canon(tup)
    if c not in V_: V_[c] = M.NewBoolVar('')
    return V_[c]
srep = []; seen = set()
for Q in planes:
    c = canon((('S', Q),))
    if c not in seen: seen.add(c); srep.append(Q)
def cands(Q):
    Qp = Qperp[Q]
    return [('R', s) for s in e8.bits(Qp)] + [('C', P) for P in planes if P & ~Qp == 0] + [('X', G) for G in nodes if G & ~Qp == 0]
def ch(Q, j, src): return var((('S', Q), ('j', j), src))
def abit(Q, j, s): return var((('S', Q), ('j', j), ('L', s)))
def lam(t, Q, j): return var((('L', t), ('S', Q), ('j', j)))
def zin(t, Q): return var((('L', t), ('S', Q), ('z', 0)))
def raw(s, X): return var((('L', s), ('X', X), ('raw', 0)))
def cellin(P, X): return var((('C', P), ('X', X), ('in', 0)))
def inP(s, P): return var((('L', s), ('C', P), ('inP', 0)))
# feeding counts: for an object (node X / cell P / raw line s), number of slots it feeds = sum over all slots (Q', j)
# of ch(Q', j, obj); by symmetry ch(rot^k Q, j, obj) = ch(Q, j, rot^-k obj).
feeds = collections.defaultdict(list)
for Q in srep:
    orbitQ = []
    cur = Q
    for k in range(15):
        orbitQ.append((k, cur)); cur = act(cur)
        if cur == Q: break
    cl = cands(Q)
    for j in range(pc(Q)):
        chs = [ch(Q, j, c) for c in cl]
        M.AddExactlyOne(chs)
        for c in cl:
            # this slot (Q,j) choosing c corresponds, under rotation by k, to slot (rot^k Q, j) choosing rot^k c
            for k, Qk in orbitQ:
                ck = rot((c,), k)[0]
                feeds[canon((ck,))].append((ck, ch(Q, j, c)))
# objects' counts (orbit reps only)
def slots_fed(obj): return [v for (ck, v) in feeds.get(canon((obj,)), []) if ck == obj]
done = set()
nodes_used_reps = []
for G in nodes:
    c = canon((('X', G),))
    if c in done: continue
    done.add(c)
    ins = [raw(s, G) for s in e8.bits(G)] + [cellin(P, G) for P in planes if P & ~G == 0]
    M.Add(sum(ins) == sum(slots_fed(('X', G))))
print('node reps', len(done), flush=True)
done = set()
for P in planes:
    c = canon((('C', P),))
    if c in done: continue
    done.add(c)
    outs = [cellin(P, G) for G in nodes if P & ~G == 0] + slots_fed(('C', P))
    M.Add(sum(inP(s, P) for s in e8.bits(P)) == sum(outs))
done = set()
for s in range(V):
    c = canon((('L', s),))
    if c in done: continue
    done.add(c)
    M.Add(sum(raw(s, G) for G in nodes if G >> s & 1) + sum(inP(s, P) for P in planes if P >> s & 1)
          + sum(slots_fed(('R', s))) == 4)
print('counts built', flush=True)
# availability and arrival supports
avail = {}
def av(X, s):
    key = canon((('X', X), ('L', s), ('av', 0)))
    if key not in avail:
        b = M.NewBoolVar(''); avail[key] = b
        terms = [raw(s, X)]
        for P in planes:
            if P >> s & 1 and P & ~X == 0:
                y = M.NewBoolVar(''); M.AddImplication(y, cellin(P, X)); M.AddImplication(y, inP(s, P)); terms.append(y)
        M.AddBoolOr(terms + [b.Not()])
    return avail[key]
for Q in srep:
    Qp = Qperp[Q]; cl = cands(Q)
    for j in range(pc(Q)):
        for s in e8.bits(Qp):
            a = abit(Q, j, s)
            for c in cl:
                k, v = c
                if k == 'R':
                    if v != s: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                elif k == 'C':
                    if v >> s & 1: M.AddBoolOr([ch(Q, j, c).Not(), a.Not(), inP(s, v)])
                    else: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
                else:
                    if v >> s & 1: M.AddBoolOr([ch(Q, j, c).Not(), a.Not(), av(v, s)])
                    else: M.AddBoolOr([ch(Q, j, c).Not(), a.Not()])
        M.AddBoolOr([abit(Q, j, s) for s in e8.bits(Qp)])
    users = e8.bits(Q); n = len(users)
    allowed = []
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
print('supports built; vars', len(V_), 'avail', len(avail), flush=True)
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    M.Add(sum(zin(t, Q) for Q in mine) <= 1)
    for s in e8.bits(e8.HYP[t]):
        want = 0 if (excl and blk[s] == comp[blk[t]]) else 1
        terms = []
        for Q in mine:
            if not (Qperp[Q] >> s & 1): continue
            for j in range(pc(Q)):
                x = M.NewBoolVar('')
                a, l = abit(Q, j, s), lam(t, Q, j)
                M.AddBoolAnd([a, l]).OnlyEnforceIf(x); M.AddBoolOr([a.Not(), l.Not()]).OnlyEnforceIf(x.Not())
                terms.append(x)
        M.AddBoolXOr(terms if want else terms + [M.NewConstant(1)])
print('model built', flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = tl; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r), flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    out = {str(k): int(sol.Value(v)) for k, v in V_.items() if sol.Value(v)}
    json.dump(out, open('depth2_ex%d.json' % excl, 'w'))
