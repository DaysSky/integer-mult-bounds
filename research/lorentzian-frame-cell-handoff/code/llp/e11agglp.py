"""Aggregated (plane-type counting) LP lower bounds for defect-1-triple designs of I_{11,1}.
Option classes (exhaustive, from e11design2 option enumeration; plane types exact):
  P: a (PP, PPP, PPP)  b (PPP, PT-disj, PTT)  c (PP, PTT, PTT)  k (PPP, PT-inc, PTT)
  T: d (PT-disj, PTT, PTT)  e1 (PT-inc, PTT, PTT)  e2 (TT, PTT, PTT)  f (PTT, TT*, TT)  g, h (PT-disj, TT*, TT*)
Plane-type users: PPP 3P, PP 2P, PTT 1P+2T, PT-disj 1P+1T, PT-inc 1P+1T, TT 2T, TT* 2T.
Sections of type tau: N_tau >= (uses of tau by P)/(#P lines in tau) and >= (uses by T)/(#T lines in tau);
consistent designs: equality for both.  Registers = sum over sections (kappa + users - 1) = 660 + sum (kappa_tau - 1) N_tau
(model A: kappa = 2 everywhere; model B: kappa_eff = 2/min(1, ratio) per (type, signature) -- lower-bounded by the
min over the signatures that type takes).  Model B's per-option costs (e11design2) are also evaluated directly for
consistent designs (each user pays kappa_eff/u + (u-1)/u)."""
from scipy.optimize import linprog
import numpy as np
names = ['a', 'b', 'c', 'k', 'd', 'e1', 'e2', 'f', 'g', 'h']
uses = {  # per option: counts of plane types used
 'a': {'PP': 1, 'PPP': 2}, 'b': {'PPP': 1, 'PTd': 1, 'PTT': 1}, 'c': {'PP': 1, 'PTT': 2}, 'k': {'PPP': 1, 'PTi': 1, 'PTT': 1},
 'd': {'PTd': 1, 'PTT': 2}, 'e1': {'PTi': 1, 'PTT': 2}, 'e2': {'TT': 1, 'PTT': 2}, 'f': {'PTT': 1, 'TTs': 1, 'TT': 1},
 'g': {'PTd': 1, 'TTs': 2}, 'h': {'PTd': 1, 'TTs': 2}}
isP = {x: x in 'abck' for x in names}
Plines = {'PPP': 3, 'PP': 2, 'PTT': 1, 'PTd': 1, 'PTi': 1, 'TT': 0, 'TTs': 0}
Tlines = {'PPP': 0, 'PP': 0, 'PTT': 2, 'PTd': 1, 'PTi': 1, 'TT': 2, 'TTs': 2}
types = list(Plines)
optcost = {'a': 4.54, 'b': 4.73, 'c': 4.82, 'k': 4.92, 'd': 4.17, 'e1': 4.54, 'e2': 4.54, 'f': 4.85, 'g': 5.17, 'h': 6.44}
# kappa_eff minima per type (model B) from the lkex2 table over the signatures each type takes in these options
kB = {'PPP': 2 / 0.78, 'PP': 2.0, 'PTT': 2.0, 'PTd': 2.0, 'PTi': 2.0, 'TT': 2.0, 'TTs': 2 / 0.75}
def solve(kappa, consistent):
    nv = len(names) + len(types)          # option counts + section counts N_tau
    c = np.zeros(nv)
    for j, t in enumerate(types): c[len(names) + j] = kappa[t] - 1
    Aeq, beq, Aub, bub = [], [], [], []
    row = np.zeros(nv); row[[names.index(x) for x in names if isP[x]]] = 1; Aeq.append(row); beq.append(55)
    row = np.zeros(nv); row[[names.index(x) for x in names if not isP[x]]] = 1; Aeq.append(row); beq.append(165)
    for j, t in enumerate(types):
        for side, cnt in (('P', Plines[t]), ('T', Tlines[t])):
            row = np.zeros(nv)
            for x in names:
                if (side == 'P') == isP[x]: row[names.index(x)] = uses[x].get(t, 0)
            if cnt == 0:
                if consistent or True: Aeq.append(row); beq.append(0) if row.any() else None
                if not row.any(): Aeq.pop()
                continue
            row[len(names) + j] = -cnt          # uses - cnt * N_tau (<= 0; == 0 if consistent)
            (Aeq if consistent else Aub).append(row); (beq if consistent else bub).append(0)
    res = linprog(c, A_ub=np.array(Aub) if Aub else None, b_ub=np.array(bub) if bub else None,
                  A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method='highs')
    return res
for mname, kappa in (('A (kappa=2)', {t: 2.0 for t in types}), ('B (kappa_eff min per type)', kB)):
    for cons in (False, True):
        r = solve(kappa, cons)
        x = dict(zip(names + ['N_' + t for t in types], np.round(r.x, 2)))
        print('%-28s consistent=%-5s registers %.2f -> R >= %.2f' % (mname, cons, 660 + r.fun, 660 + r.fun - 220),
              {k: v for k, v in x.items() if v > 1e-6})
# per-option cost model (e11design2) for consistent designs
nv = len(names); c = np.array([optcost[x] for x in names])
Aeq = [[1 if isP[x] else 0 for x in names], [0 if isP[x] else 1 for x in names]]; beq = [55, 165]
for t in types:
    if Plines[t] and Tlines[t]:
        Aeq.append([uses[x].get(t, 0) / (Plines[t] if isP[x] else -Tlines[t]) for x in names]); beq.append(0)
r = linprog(c, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method='highs')
print('per-option cost model, consistent: registers %.2f -> R >= %.2f' % (r.fun, r.fun - 220), dict(zip(names, np.round(r.x, 2))))
