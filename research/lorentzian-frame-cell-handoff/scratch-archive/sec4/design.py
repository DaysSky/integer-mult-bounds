"""Z15-invariant 4-plane design for E8: each line in exactly one orthogonal-pair plane and three A2 planes of the
family; for every line t, its 4 sections (plane-perps) cover R(t) with all private sets proper (non-spanning).
CP-SAT over plane orbits.  Saves the family."""
import sys, json, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
V = e8.V; GI = e8.GI
pc = lambda m: bin(m).count('1')
perm = json.load(open('coxeter.json'))['perm']
def act(mask, k=1):
    out = mask
    for _ in range(k):
        m = 0
        for s in e8.bits(out): m |= 1 << perm[s]
        out = m
    return out
# planes
pairs = set(); a2 = set()
for a in range(V):
    for b in range(a + 1, V):
        if GI[a, b] == 0: pairs.add((1 << a) | (1 << b))
        else:
            F, d = e8.closure((1 << a) | (1 << b)); a2.add(F)
def orbits(S):
    S = set(S); out = []
    while S:
        x = S.pop(); orb = [x]; y = act(x)
        while y != x: orb.append(y); S.discard(y); y = act(y)
        out.append(orb)
    return out
po = orbits(pairs); ao = orbits(a2)
print('pair orbits', len(po), collections.Counter(len(o) for o in po), ' A2 orbits', len(ao), collections.Counter(len(o) for o in ao), flush=True)
# line orbit representatives
seen = set(); reps = []
for s in range(V):
    if s in seen: continue
    reps.append(s); x = s
    while x not in seen: seen.add(x); x = perm[x]
print('line orbit reps', reps)
# for each rep t: planes through t in each orbit
def perpmask(F):
    m = (1 << V) - 1
    for s in e8.bits(F): m &= e8.HYP[s]
    return m
R = {t: e8.HYP[t] for t in reps}
M = cp_model.CpModel()
xp = [M.NewBoolVar('p%d' % i) for i in range(len(po))]
xa = [M.NewBoolVar('a%d' % i) for i in range(len(ao))]
through = {}
for t in reps:
    lp = [(i, F) for i, o in enumerate(po) for F in o if F >> t & 1]
    la = [(i, F) for i, o in enumerate(ao) for F in o if F >> t & 1]
    through[t] = (lp, la)
    M.Add(sum(xp[i] for i, F in lp) == 1)     # each orbit contains each line at most... count with multiplicity
    M.Add(sum(xa[i] for i, F in la) == 3)
# cover validity: for each rep t, for each candidate 4-tuple (1 pair plane + 3 A2 planes through t) that is NOT an
# all-proper cover, forbid choosing all four orbits together.  Enumerate valid covers instead: require that the chosen
# planes through t form a valid cover -> add constraint via allowed combinations.
valid_tuples = {}
for t in reps:
    lp, la = through[t]
    secp = {F: perpmask(F) & R[t] for _, F in lp}
    seca = {F: perpmask(F) & R[t] for _, F in la}
    good = []
    for (ip, Fp) in lp:
        for trip in itertools.combinations(la, 3):
            Fs = [Fp] + [F for _, F in trip]
            secs = [secp[Fp]] + [seca[F] for F in Fs[1:]]
            u = 0
            for s_ in secs: u |= s_
            if u != R[t]: continue
            ok = True
            for k in range(4):
                oth = 0
                for j in range(4):
                    if j != k: oth |= secs[j]
                P = secs[k] & ~oth
                if not P or e8.dim(P) == e8.dim(secs[k]): ok = False; break
            if ok: good.append((ip, tuple(sorted(i for i, _ in trip))))
    valid_tuples[t] = set(good)
    print('rep', t, 'valid (pair-orbit, A2-orbit triple) combos:', len(valid_tuples[t]), flush=True)
for t in reps:
    lp, la = through[t]
    # selector: exactly one valid combo chosen, consistent with x vars
    sel = {c: M.NewBoolVar('') for c in valid_tuples[t]}
    M.AddExactlyOne(sel.values())
    for (ip, tri), b in sel.items():
        M.AddImplication(b, xp[ip])
        for i in tri: M.AddImplication(b, xa[i])
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
r = s.Solve(M)
print('status', s.StatusName(r))
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    fam = [F for i, o in enumerate(po) if s.Value(xp[i]) for F in o] + [F for i, o in enumerate(ao) if s.Value(xa[i]) for F in o]
    cnt = collections.Counter(x for F in fam for x in e8.bits(F))
    print('planes', len(fam), 'line multiplicities', collections.Counter(cnt.values()))
    json.dump({'planes': [hex(F) for F in fam]}, open('design.json', 'w'))
