"""All span-closed line sets of rank 1..K inside a given line set U (I11), by closure growth with dedupe; and exact
rank-k cover numbers kappa_k(X) (CP-SAT set cover by maximal rank-k closed sets).  Library + CLI:
usage: lclosed.py SETNAME K   (SETNAME: L7 = L({4..10}), node:<frame hex>)"""
import sys, itertools, collections
import numpy as np
from lgeo import *
from ortools.sat.python import cp_model
LA = np.array(g.LA, dtype=float)
def closure_vec(Ubits, S):
    B = LA[bits(S)]
    q, r = np.linalg.qr(B.T)
    keep = np.abs(np.diag(r)) > 1e-9
    Q = q[:, keep]
    X = LA[Ubits]
    res = X - (X @ Q) @ Q.T
    inside = np.linalg.norm(res, axis=1) < 1e-7
    m = 0
    for idx, ok in zip(Ubits, inside):
        if ok: m |= 1 << idx
    return m, int(keep.sum())
def closed_sets(U, K):
    Ub = bits(U); levels = {1: set()}
    for x in Ub:
        c, _ = closure_vec(Ub, 1 << x); levels[1].add(c)
    for k in range(2, K + 1):
        nxt = set()
        for S in levels[k - 1]:
            for x in Ub:
                if S >> x & 1: continue
                c, r = closure_vec(Ub, S | (1 << x))
                if r == k: nxt.add(c)
        levels[k] = nxt
    return levels
def kappa(X, sets, tl=60):
    inter = set(S & X for S in sets if S & X)
    keys = sorted(inter, key=pc, reverse=True); maxi = []
    for I in keys:
        if not any(I & ~J == 0 for J in maxi): maxi.append(I)
    M = cp_model.CpModel(); xs = [M.NewBoolVar('') for _ in maxi]
    for u in bits(X): M.AddBoolOr([xs[i] for i, I in enumerate(maxi) if I >> u & 1])
    M.Minimize(sum(xs)); sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 4
    st = sv.Solve(M); return int(sv.ObjectiveValue()), int(round(sv.BestObjectiveBound())), sv.StatusName(st)
if __name__ == '__main__':
    name, K = sys.argv[1], int(sys.argv[2])
    if name == 'L7':
        S7 = set(range(4, 11)); U = 0
        for s in range(V):
            if set(SUPP[s]) <= S7: U |= 1 << s
    else:
        U = pm(int(name.split(':')[1], 16))
    print('U lines', pc(U), 'rank', rank(U), flush=True)
    lv = closed_sets(U, K)
    for k in sorted(lv): print('rank', k, 'closed sets', len(lv[k]), 'max lines', max(pc(S) for S in lv[k]), flush=True)
    for k in range(3, K + 1): print('kappa_%d(U) =' % k, kappa(U, lv[k]), flush=True)
