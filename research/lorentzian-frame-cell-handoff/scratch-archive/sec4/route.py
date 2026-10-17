"""Stage 0: Z15-invariant routing cells -> D4 quads -> sections for the 4-plane design, with coverage: every (t, s),
s in R(t), has a path s in P -> W -> Q containing t.  Each cell P sends |P| registers to distinct quads containing P;
each section Q receives |Q| registers from distinct quads inside Q-perp; every used quad has in = out."""
import sys, collections, json
from common import *
from ortools.sat.python import cp_model
D4 = load_d4()
d4idx = {W: i for i, W in enumerate(D4)}
plidx = {P: i for i, P in enumerate(planes)}
# orbits of D4 and planes
def orbits_of(objs, idx):
    seen = set(); orbs = []
    for x in objs:
        if x in seen: continue
        o = orbit(x); orbs.append(o); seen.update(o)
    return orbs
d4orbs = orbits_of(D4, d4idx); plorbs = orbits_of(planes, plidx)
d4orb = {W: k for k, o in enumerate(d4orbs) for W in o}
plorb = {P: k for k, o in enumerate(plorbs) for P in o}
print('D4 orbits', len(d4orbs), ' plane orbits', len(plorbs), flush=True)
inner = {W: [P for P in planes if P & ~W == 0] for W in D4}
Wperp = {W: perpmask(W) for W in D4}
outer = {W: [Q for Q in planes if Q & ~Wperp[W] == 0] for W in D4}
useful = [W for W in D4 if inner[W] and outer[W]]
print('D4s with both inner cells and outer sections:', len(useful), flush=True)
M = cp_model.CpModel()
# orbit-level edge variables: y[(P_orbit_rep, W)] for P in a plane-orbit representative... use full objects but tie by orbit
yv = {}; zv = {}
def ykey(P, W):
    # canonical: rotate so that P is its orbit representative
    o = plorbs[plorb[P]]; k = o.index(P)
    Wc = W
    for _ in range((15 - k) % len(o) if len(o) == 15 else 0): pass
    return None
# simpler: create variables for every (P, W) and add equality constraints along the orbit
for W in useful:
    for P in inner[W]: yv[(P, W)] = M.NewBoolVar('')
    for Q in outer[W]: zv[(W, Q)] = M.NewBoolVar('')
for (P, W), v in list(yv.items()):
    M.Add(v == yv[(act(P), act(W))])
for (W, Q), v in list(zv.items()):
    M.Add(v == zv[(act(W), act(Q))])
for P in planes:
    M.Add(sum(v for (P2, W), v in yv.items() if P2 == P) == pc(P))
for Q in planes:
    M.Add(sum(v for (W, Q2), v in zv.items() if Q2 == Q) == pc(Q))
for W in useful:
    M.Add(sum(yv[(P, W)] for P in inner[W]) == sum(zv[(W, Q)] for Q in outer[W]))
# coverage for representative targets
for t in reps:
    mine = [Q for Q in planes if Q >> t & 1]
    R = e8.HYP[t]
    for s in e8.bits(R):
        terms = []
        for Q in mine:
            for W in useful:
                if (W, Q) not in zv or not (W >> s & 1): continue
                for P in inner[W]:
                    if P >> s & 1:
                        a = M.NewBoolVar(''); M.AddBoolAnd([yv[(P, W)], zv[(W, Q)]]).OnlyEnforceIf(a)
                        M.AddImplication(a, yv[(P, W)]); M.AddImplication(a, zv[(W, Q)])
                        terms.append(a)
        if not terms: print('uncoverable', t, s); sys.exit(1)
        M.AddBoolOr(terms)
print('model built', flush=True)
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 1200; sol.parameters.num_workers = 4
r = sol.Solve(M)
print('status', sol.StatusName(r))
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    Y = [(hex(P), hex(W)) for (P, W), v in yv.items() if sol.Value(v)]
    Z = [(hex(W), hex(Q)) for (W, Q), v in zv.items() if sol.Value(v)]
    used = set(W for _, W in Y)
    print('registers', len(Y), len(Z), 'quads used', len(used), 'n_W', collections.Counter(collections.Counter(W for _, W in Y).values()))
    json.dump({'Y': Y, 'Z': Z}, open('routing.json', 'w'))
