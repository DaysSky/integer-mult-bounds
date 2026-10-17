"""Consistent self-dual A3 design for I_{11,1} (no routability terms in the model; evaluated afterwards).
Each line s picks an A3 X containing s (its top = planes of X through s; its source cells = the same planes).
Consistency: a triangle used by one of its lines is used by all three; a pair used by one is used by the other
(no defects).  Z11 symmetry.  Objective: minimise the estimated register cost
   sum over lines s of sum over its 3 planes P of cost(sig(s, X, P))
with cost per (user, section) = kappa_eff/u + (u-1)/u from the measured shareability table (lkex2), keyed by the
section's exclusive-part signature for that user.   usage: e11design4.py timelimit MODEL(A|B) SYM(0|1) -> e11design4_<MODEL><SYM>.json
(e11design2 generalised: MODEL A = kappa 2 for every section (per user (u+1)/u), B = measured shareability; SYM 0 = no symmetry)"""
import sys, json, itertools, collections, time, pickle
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[1]); MODEL = sys.argv[2]; SYM = int(sys.argv[3]); TYPES = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else None
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

VEC = {}
for s in range(V):
    VEC[tuple(int(x) for x in g.L[s])] = s; VEC[tuple(-int(x) for x in g.L[s])] = s
def third(a, b):
    out = []
    if G[a][b] == 0: return out
    for sg in (1, -1):
        c = VEC.get(tuple(int(x) for x in (g.L[a] - sg * g.L[b])))
        if c is not None and c not in (a, b): out.append(c)
    return out
def planes_through(X, t):
    tris = set()
    for a in bits(X):
        if a == t: continue
        for c in third(t, a):
            if X >> c & 1: tris.add((1 << t) | (1 << a) | (1 << c))
    tris = sorted(tris)
    opp = [e for e in bits(X) if e != t and not any(T >> e & 1 for T in tris)]
    return tris[0], tris[1], (1 << t) | (1 << opp[0])
# shareability ratio table from lkex2 (best 2-cover min sinks/need) keyed by (plane size, |S|, |E|)
RATIO = {(3, 85, 29): 0.78, (2, 70, 14): 21.5, (3, 85, 43): 0.54, (2, 56, 14): 6.8, (3, 71, 29): 0.78,
         (3, 85, 38): 0.54, (3, 71, 24): 1.17, (2, 66, 19): 4.25, (2, 70, 28): 0.78, (2, 66, 29): 1.86,
         (2, 61, 24): 0.75, (2, 66, 30): 0.44, (3, 71, 34): 0.78, (2, 56, 19): 4.25}
def cost(P, S, E):
    if MODEL == 'A': return (pc(P) + 1) / pc(P)
    r = RATIO[(pc(P), pc(S), pc(E))]
    u = pc(P)
    return (2.0 / min(1.0, r)) / u + (u - 1) / u
def plane_of(a, b):
    m = (1 << a) | (1 << b)
    for c in third(a, b): m |= 1 << c
    return m
def triples(t):
    R = HYP[t]
    pl = sorted(set(plane_of(t, e) for e in range(V) if e != t))
    Sm = [pm(p) for p in pl]; out = []
    for i, j, k in itertools.combinations(range(len(pl)), 3):
        D = Sm[i] ^ Sm[j] ^ Sm[k] ^ R
        if pc(D) == 1: out.append((pl[i], pl[j], pl[k]))
    return out
REPT = {}
for t in range(V):
    if KIND[t] not in REPT: REPT[KIND[t]] = (t, triples(t))
opts = {s: [] for s in range(V)}
for s in range(V):
    r, TR = REPT[KIND[s]]
    a_ = list(SUPP[r]); b_ = list(SUPP[s]); perm_ = [0] * n
    for x, y in zip(a_ + [i for i in range(n) if i not in a_], b_ + [i for i in range(n) if i not in b_]): perm_[x] = y
    for tr in TR:
        pl = tuple(act(p, perm_) for p in tr)
        S = {p: pm(p) for p in pl}
        c = 0.0
        for p in pl:
            others = [q for q in pl if q != p]
            E = S[p] & ~S[others[0]] & ~S[others[1]]
            c += cost(p, S[p], E)
        key = sum(1 << 0 for _ in ()) or tuple(sorted(pl))
        opts[s].append((tuple(sorted(pl)), pl, c))
def ptype(p):
    L = bits(p); ks = ''.join(sorted(KIND[x] for x in L))
    if len(L) == 3: return ks
    a_, b_ = L
    if ks == 'PT':
        P_ = a_ if KIND[a_] == 'P' else b_; T_ = b_ if P_ == a_ else a_
        return 'PTi' if set(SUPP[P_]) <= set(SUPP[T_]) else 'PTd'
    if ks == 'TT': return 'TT' if G[a_][b_] == 0 else 'TTs'
    return ks
if TYPES:
    for s_ in range(V):
        opts[s_] = [o for o in opts[s_] if '+'.join(sorted(ptype(p) for p in o[1])) in TYPES]
log('options per line', collections.Counter(len(v) for v in opts.values()))
M = cp_model.CpModel()
xs = {s: [M.NewBoolVar('') for _ in opts[s]] for s in range(V)}
for s in range(V): M.AddExactlyOne(xs[s])
use = collections.defaultdict(list)      # (plane, line) -> literals
for s in range(V):
    for k, (X, pl, c) in enumerate(opts[s]):
        for p in pl: use[(p, s)].append(xs[s][k])
planes = sorted(set(p for (p, s) in use))
for p in planes:
    lines = bits(p)
    sums = [sum(use[(p, s)]) if use[(p, s)] else 0 for s in lines]
    for a, b in zip(sums, sums[1:]): M.Add(a == b)          # all lines of the plane use it, or none
perm = [(i + 1) % n for i in range(n)]
idx = {(s, X): k for s in range(V) for k, (X, pl, c) in enumerate(opts[s])}
def actkey(X, perm): return tuple(sorted(act(p, perm) for p in X))
for s in (range(V) if SYM else []):
    s2 = img_line(s, perm)
    for k, (X, pl, c) in enumerate(opts[s]): M.Add(xs[s][k] == xs[s2][idx[(s2, actkey(X, perm))]])
M.Minimize(sum(int(round(100 * c)) * xs[s][k] for s in range(V) for k, (X, pl, c) in enumerate(opts[s])))
log('model built')
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 3; sv.parameters.log_search_progress = True; sv.parameters.log_to_stdout = True
st = sv.Solve(M)
log('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() / 100 if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
    'bound', sv.BestObjectiveBound() / 100)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = {s: [hex(p) for p in opts[s][k][1]] for s in range(V) for k in range(len(opts[s])) if sv.Value(xs[s][k])}
    json.dump(sol, open('e11design4_%s%d%s.json' % (MODEL, SYM, '_typed' if TYPES else ''), 'w'))
    tot = sum(opts[s][k][2] for s in range(V) for k in range(len(opts[s])) if sv.Value(xs[s][k]))
    log('estimated registers', round(tot, 1), '-> R ~', round(tot - 220, 1))
