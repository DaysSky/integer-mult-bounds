"""Parts layer for a rank-8 frame-section design (Z11-symmetric CP-SAT).
Input: used frames (lr8design_K.json; Z11-invariant family, every line in exactly K frames).
Per target t: one in-chain section F (c[t,F]); parts p[t,F,u] (u in F-perp) with sum_F p[t,F,u] == 1 for every u in R(t)
(union partition); for every section F and every in-chain user a of F: p[a,F,.] = XOR_b lam[a,F,b] p[b,F,.] over the
delivered users b of F (span condition, linearised); delivered users' parts pairwise distinct (necessary for
independence); every section has >= 1 delivered user.  Z11: variables for orbit-representative targets only.
usage: lr8parts.py design.json timelimit -> lr8parts_sol.json"""
import sys, json, collections, time
from lgeo import *
from ortools.sat.python import cp_model
TL = float(sys.argv[2]); t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)
used = [int(h, 16) for h in json.load(open(sys.argv[1]))]
rot = [img_line(s, [(i + 1) % n for i in range(n)]) for s in range(V)]
def rotk(x, k):
    for _ in range(k % n): x = rot[x]
    return x
def rotm(m, k):
    r = 0
    for s in bits(m): r |= 1 << rotk(s, k)
    return r
orb = {}; reps = []
for s in range(V):
    if s in orb: continue
    reps.append(s); x = s
    for k in range(n): orb[x] = (len(reps) - 1, k); x = rot[x]
secs = {t: [F for F in used if F >> t & 1] for t in range(V)}
M = cp_model.CpModel()
# variables for rep targets; images by rotation map (t,F,u) -> (rot^k t, rot^k F, rot^k u)
P = {}; C = {}
def canon(t, F, u=None):
    o, k = orb[t]; r = reps[o]
    return (r, rotm(F, -k % n), None if u is None else rotk(u, -k % n))
def pvar(t, F, u):
    key = canon(t, F, u)
    if key not in P: P[key] = M.NewBoolVar('')
    return P[key]
def cvar(t, F):
    key = canon(t, F)
    if key not in C: C[key] = M.NewBoolVar('')
    return C[key]
for r in reps:
    M.AddExactlyOne([cvar(r, F) for F in secs[r]])
    for u in bits(HYP[r]):
        lits = [pvar(r, F, u) for F in secs[r] if pm(F) >> u & 1]
        M.Add(sum(lits) == 1)
log('targets done; part vars', len(P))
# sections: one per orbit of frames
seen = set(); nsec = 0; nprod = 0
for F in used:
    key = min(rotm(F, k) for k in range(n))
    if key in seen: continue
    seen.add(key); nsec += 1
    us = bits(F); FP = bits(pm(F))
    deliv = {a: cvar(a, F).Not() for a in us}
    M.AddBoolOr([deliv[a] for a in us])                      # >= 1 delivered user
    for a in us:
        # if a in-chain: p[a] = XOR_b lam_b p[b] over delivered b
        lam = {b: M.NewBoolVar('') for b in us if b != a}
        for b in lam: M.AddImplication(lam[b], deliv[b])    # only delivered users in the combination
        for u in FP:
            terms = []
            for b in lam:
                pr = M.NewBoolVar(''); nprod += 1
                M.AddMultiplicationEquality(pr, [lam[b], pvar(b, F, u)])
                terms.append(pr)
            # parity: p[a,u] + sum terms == 0 mod 2, enforced only if a in-chain
            par = M.NewIntVar(0, len(terms) + 1, '')
            q = M.NewIntVar(0, (len(terms) + 1) // 2 + 1, '')
            M.Add(par == pvar(a, F, u) + sum(terms))
            M.Add(par == 2 * q).OnlyEnforceIf(cvar(a, F))
    # delivered parts pairwise distinct
    for a, b in [(a, b) for i, a in enumerate(us) for b in us[i + 1:]]:
        dif = []
        for u in FP:
            d = M.NewBoolVar(''); M.Add(pvar(a, F, u) != pvar(b, F, u)).OnlyEnforceIf(d); dif.append(d)
        both = M.NewBoolVar(''); M.AddBoolAnd([deliv[a], deliv[b]]).OnlyEnforceIf(both)
        M.AddBoolOr([deliv[a].Not(), deliv[b].Not()] + [both]).OnlyEnforceIf(both.Not()) if False else None
        M.AddBoolOr(dif + [deliv[a].Not(), deliv[b].Not()])
log('sections', nsec, 'product vars', nprod)
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = TL; sv.parameters.num_workers = 3
st = sv.Solve(M)
log('status', sv.StatusName(st))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    json.dump({'c': {'%d,%s' % (k[0], hex(k[1])): sv.Value(v) for k, v in C.items()},
               'p': {'%d,%s,%d' % (k[0], hex(k[1]), k[2]): sv.Value(v) for k, v in P.items()}}, open('lr8parts_sol.json', 'w'))
