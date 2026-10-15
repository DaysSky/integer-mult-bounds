"""Reach check for cell-free sources: can R(u) be covered by the perps of k rank-3 frames F containing u?
(Each of u's 3 branch registers carries x_u alone at <u>; their first frames F_i have reach lines(F_i-perp).)
Exact minimum k by CP-SAT set cover over all distinct rank-3 frames F = closure(u, a, b) (nondegenerate).
Also: covers by k frames where additionally each F is spanned by u and a pair that is a plane section partner
structure is NOT required.  usage: lr3cover.py"""
import itertools, collections
from lgeo import *
from ortools.sat.python import cp_model
for kind in ('P', 'T'):
    u = next(s for s in range(V) if KIND[s] == kind)
    R = HYP[u]
    perps = {}
    others = [x for x in range(V) if x != u]
    for a, b in itertools.combinations(others, 2):
        m = (1 << u) | (1 << a) | (1 << b)
        if rank(m) != 3: continue
        F = pp(m)                         # closure (lines in the span)
        if F in perps: continue
        P_ = pm(F) & R
        perps[F] = P_
    sets = sorted(set(perps.values()), key=pc, reverse=True)
    # remove dominated
    maxi = []
    for s_ in sets:
        if not any(s_ & ~t == 0 for t in maxi): maxi.append(s_)
    for slack in (0, 1):
        M = cp_model.CpModel(); x = [M.NewBoolVar('') for _ in maxi]
        miss = {w: M.NewBoolVar('') for w in bits(R)}
        for w in bits(R): M.AddBoolOr([x[i] for i, s_ in enumerate(maxi) if s_ >> w & 1] + [miss[w]])
        M.Add(sum(miss.values()) <= slack)
        M.Add(sum(x) <= 3)
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = 600; sv.parameters.num_workers = 3
        st = sv.Solve(M)
        print(kind, '|R(u)|', pc(R), 'maximal perp sets', len(maxi), '| cover by <= 3 frames with <= %d uncovered:' % slack, sv.StatusName(st), flush=True)
