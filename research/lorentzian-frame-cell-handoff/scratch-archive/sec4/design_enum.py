"""Z15-invariant self-dual 4-plane design for E8 with CROSS-ORTHOGONALITY: each line in exactly one orthogonal-pair
plane and three A2 planes; every line's 4 sections are an all-proper cover of R(t); and for every orthogonal (t, s)
there are planes P ∋ s, Q ∋ t of the family with P ⊥ Q and a D4 W with P ⊂ W ⊂ Q-perp."""
import sys, json, itertools, collections
sys.path.insert(0, '/home/user/integer-mult-bounds/research/e8-bit-carrier-skeleton/code/skeleton')
import e8
from ortools.sat.python import cp_model
from common import act, perpmask, load_d4, reps, pc
V = e8.V; GI = e8.GI
pairs = set(); a2 = set()
for a in range(V):
    for b in range(a + 1, V):
        if GI[a, b] == 0: pairs.add((1 << a) | (1 << b))
        else: a2.add(e8.closure((1 << a) | (1 << b))[0])
def orbits(S):
    S = set(S); out = []
    while S:
        x = S.pop(); orb = [x]; y = act(x)
        while y != x: orb.append(y); S.discard(y); y = act(y)
        out.append(orb)
    return out
po = orbits(pairs); ao = orbits(a2)
allorbs = [('p', o) for o in po] + [('a', o) for o in ao]
porb = {}
for k, (typ, o) in enumerate(allorbs):
    for F in o: porb[F] = k
D4 = load_d4()
d4_by_line = collections.defaultdict(list)
for W in D4:
    for s in e8.bits(W): d4_by_line[s].append(W)
M = cp_model.CpModel()
through = collections.defaultdict(list)
for F in list(pairs) + list(a2):
    for q in e8.bits(F): through[q].append(F)
QP = {F: perpmask(F) for F in list(pairs) + list(a2)}
witness = {}
x = [M.NewBoolVar('') for _ in allorbs]
R = {t: e8.HYP[t] for t in reps}
for t in reps:
    lp = [k for k, (typ, o) in enumerate(allorbs) if typ == 'p' for F in o if F >> t & 1]
    la = [k for k, (typ, o) in enumerate(allorbs) if typ == 'a' for F in o if F >> t & 1]
    M.Add(sum(x[k] for k in lp) == 1); M.Add(sum(x[k] for k in la) == 3)
    # valid covers
    thr_p = [F for F in pairs if F >> t & 1]; thr_a = [F for F in a2 if F >> t & 1]
    sec = {F: perpmask(F) & R[t] for F in thr_p + thr_a}
    good = []
    for Fp in thr_p:
        for tri in itertools.combinations(thr_a, 3):
            Fs = (Fp,) + tri; secs = [sec[F] for F in Fs]
            u = secs[0] | secs[1] | secs[2] | secs[3]
            if u != R[t]: continue
            ok = True
            for k in range(4):
                oth = 0
                for j in range(4):
                    if j != k: oth |= secs[j]
                P = secs[k] & ~oth
                if not P or e8.dim(P) == e8.dim(secs[k]): ok = False; break
            if ok: good.append(Fs)
    sel = []
    for Fs in good:
        b = M.NewBoolVar(''); sel.append(b)
        for F in Fs: M.AddImplication(b, x[porb[F]])
    M.AddBoolOr(sel)
    print('rep', t, 'valid covers', len(good), flush=True)
    # cross-orthogonality with D4 witness
    thr_all = thr_p + thr_a
    pq = {}
    for s in e8.bits(R[t]):
        terms = []
        for Q in thr_all:
            Qp = QP[Q]
            if not (Qp >> s & 1): continue
            for P in through[s]:
                if P & ~Qp: continue
                key = (P, Q)
                if key not in witness:
                    witness[key] = True   # general middle: only P ⊂ Q-perp required
                if not witness[key]: continue
                if key not in pq:
                    b = M.NewBoolVar(''); M.AddImplication(b, x[porb[P]]); M.AddImplication(b, x[porb[Q]]); pq[key] = b
                terms.append(pq[key])
        M.AddBoolOr(terms)
print('model built', flush=True)
import sys as _s
NMAX = int(_s.argv[1]) if len(_s.argv) > 1 else 20
for it in range(NMAX):
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 1800; sol.parameters.num_workers = 4
    r = sol.Solve(M)
    print('design', it, 'status', sol.StatusName(r), flush=True)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
    ch = [k for k in range(len(allorbs)) if sol.Value(x[k])]
    fam = [F for k in ch for F in allorbs[k][1]]
    json.dump({'planes': [hex(F) for F in fam]}, open('designs/design_%d.json' % it, 'w'))
    print('  orbits', ch, 'types', collections.Counter(pc(F) for F in fam), flush=True)
    M.AddBoolOr([x[k].Not() for k in ch])
