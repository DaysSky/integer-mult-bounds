"""Aggregated counting LP (model A: kappa = 2 arrivals per section + 1 per extra delivered user) with the IN-CHAIN
option for T lines: h-type tops (PT-disj, TT*, TT*) whose defect d (a P line) lies in both TT* sections can read one
TT* section in-chain (0 -> <d> -> S -> t-perp).  An in-chain TT* section read in-chain by BOTH its users with the same
need costs 2 arrivals (no differentiator); a delivered section costs kappa + q - 1.  Optimistic for the in-chain
option (same need assumed).  Section types: PPP, PP, PTT, PTd, PTi, TT, TTs (delivered), TTsI (in-chain by both)."""
from scipy.optimize import linprog
import numpy as np
names = ['a', 'b', 'c', 'k', 'd', 'e1', 'e2', 'f', 'g', 'hI']
uses = {'a': {'PP': 1, 'PPP': 2}, 'b': {'PPP': 1, 'PTd': 1, 'PTT': 1}, 'c': {'PP': 1, 'PTT': 2}, 'k': {'PPP': 1, 'PTi': 1, 'PTT': 1},
        'd': {'PTd': 1, 'PTT': 2}, 'e1': {'PTi': 1, 'PTT': 2}, 'e2': {'TT': 1, 'PTT': 2}, 'f': {'PTT': 1, 'TTs': 1, 'TT': 1},
        'g': {'PTd': 1, 'TTs': 2}, 'hI': {'PTd': 1, 'TTs': 1, 'TTsI': 1}}
isP = {x: x in 'abck' for x in names}
Pl = {'PPP': 3, 'PP': 2, 'PTT': 1, 'PTd': 1, 'PTi': 1, 'TT': 0, 'TTs': 0, 'TTsI': 0}
Tl = {'PPP': 0, 'PP': 0, 'PTT': 2, 'PTd': 1, 'PTi': 1, 'TT': 2, 'TTs': 2, 'TTsI': 2}
# registers per section (all its lines users): delivered = 2 + u - 1; in-chain-by-both = 2
secreg = {'PPP': 4, 'PP': 3, 'PTT': 4, 'PTd': 3, 'PTi': 3, 'TT': 3, 'TTs': 3, 'TTsI': 2}
types = list(Pl)
for cons in (False, True):
    nv = len(names) + len(types)
    c = np.zeros(nv)
    for j, t in enumerate(types): c[len(names) + j] = secreg[t]
    Aeq = [np.r_[[1.0 if isP[x] else 0 for x in names], np.zeros(len(types))], np.r_[[0 if isP[x] else 1.0 for x in names], np.zeros(len(types))]]
    beq = [55, 165]; Aub = []; bub = []
    for j, t in enumerate(types):
        for side, cnt in (('P', Pl[t]), ('T', Tl[t])):
            row = np.zeros(nv)
            for x in names:
                if (side == 'P') == isP[x]: row[names.index(x)] = uses[x].get(t, 0)
            if cnt == 0:
                if row.any(): Aeq.append(row); beq.append(0)
                continue
            row[len(names) + j] = -cnt
            # sections must be fully used by users of each kind (consistent) or at least cover the uses (relaxed)
            if cons or t == 'TTsI': Aeq.append(row); beq.append(0)
            else: Aub.append(row); bub.append(0)
    r = linprog(c, A_ub=np.array(Aub) if Aub else None, b_ub=np.array(bub) if Aub else None, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method='highs')
    x = dict(zip(names + ['N_' + t for t in types], np.round(r.x, 2)))
    print('consistent=%-5s registers %.2f -> R >= %.2f' % (cons, r.fun, r.fun - 220), {k: v for k, v in x.items() if v > 1e-6})
