"""H55-invariant 4-plane design for I_{11,1}: each line in exactly 4 planes (orthogonal pairs or A2-type rank-2 flats);
for each line t the 4 sections R(t) ∩ Q-perp cover R(t) with nonempty private sets; cross-orthogonality: every
(t, s in R(t)) has chosen P ∋ s, Q ∋ t with P ⊂ Q-perp.  Private-set properness (non-spanning) is checked after solving
and enforced by no-good cuts (lazy loop).  Writes ldesign.json."""
import json, time
from lcommon import *
from ortools.sat.python import cp_model
import sys as _s
FULLM = int(_s.argv[1]) if len(_s.argv) > 1 else 0
MIN3 = int(_s.argv[2]) if len(_s.argv) > 2 else 2
pairs, a2 = planes_all()
allp = pairs + a2
orb = {}; orbs = []
for F in allp:
    if F in orb: continue
    o = orbit_mask(F); k = len(orbs); orbs.append(o)
    for H in o: orb[H] = k
print('plane orbits', len(orbs), flush=True)
through = collections.defaultdict(list)
for F in allp:
    for s in bits(F): through[s].append(F)
QP = {}
def qp(F):
    if F not in QP: QP[F] = perpmask(F)
    return QP[F]
cuts = []
xo_pairs = set()
def build():
    M = cp_model.CpModel()
    x = [M.NewBoolVar('') for _ in orbs]
    for t in line_reps:
        thr = through[t]
        M.Add(sum(x[orb[F]] for F in thr) == 4)
        M.Add(sum(x[orb[F]] for F in thr if pc(F) == 3) >= MIN3)
        R = HYP[t]
        sec = {F: qp(F) & R for F in thr}
        for s in bits(R):
            M.AddBoolOr([x[orb[F]] for F in thr if sec[F] >> s & 1])
        if not FULLM: continue
        # nonempty private set: if F chosen, some line of sec(F) is covered by no other chosen plane through t
        for F in thr:
            wit = []
            for s in bits(sec[F]):
                oth = [x[orb[H]] for H in thr if H != F and sec[H] >> s & 1 and orb[H] != orb[F]]
                w = M.NewBoolVar('')
                for o in oth: M.AddImplication(w, o.Not())
                wit.append(w)
            M.AddBoolOr(wit + [x[orb[F]].Not()])
        # cross-orthogonality
        pq = {}
        for s in bits(R):
            terms = []
            for Q in thr:
                Qp = qp(Q)
                if not (Qp >> s & 1): continue
                for P in through[s]:
                    if P & ~Qp: continue
                    key = (orb[P], orb[Q])
                    if key not in pq:
                        b = M.NewBoolVar(''); M.AddImplication(b, x[key[0]]); M.AddImplication(b, x[key[1]]); pq[key] = b
                    terms.append(pq[key])
            M.AddBoolOr(terms)
    pqv = {}
    for (t, s) in xo_pairs:
        thr = through[t]; terms = []
        for Q in thr:
            Qp = qp(Q)
            if not (Qp >> s & 1): continue
            for P in through[s]:
                if P & ~Qp: continue
                key = (orb[P], orb[Q])
                if key not in pqv:
                    b = M.NewBoolVar(''); M.AddImplication(b, x[key[0]]); M.AddImplication(b, x[key[1]]); pqv[key] = b
                terms.append(pqv[key])
        M.AddBoolOr(terms)
    for cut in cuts: M.AddBoolOr([x[k].Not() for k in cut])
    return M, x
for it in range(200):
    M, x = build()
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 3000; sol.parameters.num_workers = 4
    t0 = time.time(); r = sol.Solve(M)
    print('iter', it, 'status', sol.StatusName(r), 'time %.0f' % (time.time() - t0), flush=True)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): break
    chosen = [k for k in range(len(orbs)) if sol.Value(x[k])]
    fam = [F for k in chosen for F in orbs[k]]
    famset = set(fam)
    bad = []
    for t in range(V):
        mine = [F for F in through[t] if F in famset]
        assert len(mine) == 4
        R = HYP[t]; secs = [qp(F) & R for F in mine]
        for i in range(4):
            oth = 0
            for j in range(4):
                if j != i: oth |= secs[j]
            Pm = secs[i] & ~oth
            if not Pm or g.dim(Pm) == g.dim(secs[i]):
                bad.append(sorted(set(orb[F] for F in mine))); break
    xo_bad = 0
    for t in line_reps:
        mine = [F for F in through[t] if F in famset]
        for s in bits(HYP[t]):
            if not any(qp(Q) >> s & 1 and any(P in famset and P & ~qp(Q) == 0 for P in through[s]) for Q in mine):
                xo_bad += 1
    print('  planes', len(fam), 'types', collections.Counter(pc(F) for F in fam), 'lines with improper covers', len(bad), 'rep (t,s) failing cross-orth', xo_bad, flush=True)
    # private-line screen (raw mode): each section's users' private union covered by <= |Q| supports
    import itertools as _it
    Qp_ = {Q: qp(Q) for Q in fam}
    thr_f = collections.defaultdict(list)
    for F in fam:
        for s in bits(F): thr_f[s].append(F)
    scr_bad = 0; seenQ = set()
    for Q in fam:
        cQ = orb[Q]
        if cQ in seenQ: continue
        seenQ.add(cQ)
        need = 0
        for t in bits(Q):
            oth = 0
            for F in thr_f[t]:
                if F != Q: oth |= Qp_[F] & HYP[t]
            need |= (Qp_[Q] & HYP[t]) & ~oth
        sup = set()
        for Q2 in fam:
            if Q2 != Q:
                s_ = Qp_[Q] & Qp_[Q2] & need
                if s_: sup.add(s_)
        maxi = [s for s in sup if not any(s != o and s & ~o == 0 for o in sup)]
        ok = False
        for combo in _it.combinations(maxi, pc(Q)):
            u = 0
            for s in combo: u |= s
            if u == need: ok = True; break
        if not ok:
            scr_bad += 1
            cut = sorted(set(orb[F] for t in bits(Q) for F in thr_f[t]))
            if cut not in cuts: cuts.append(cut)
    print('  sections failing private-line screen (orbits):', scr_bad, flush=True)
    if not bad and not scr_bad:
        json.dump({'planes': [hex(F) for F in fam]}, open('ldesign_R3.json', 'w')); print('DESIGN FOUND (proper + private screen, raw mode, >= MIN3 three-line planes)'); break
    for b in bad:
        if b not in cuts: cuts.append(b)
