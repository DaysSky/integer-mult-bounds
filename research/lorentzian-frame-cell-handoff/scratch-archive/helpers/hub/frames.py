"""E8 skeleton features transferred to I_{n,1}: good 4-frames, F2 parity, partitions, cell-perp sizes.
A 4-frame is a set of 4 pairwise orthogonal lines.  It is GOOD when for every member t and every line s orthogonal to t
(s not in the frame) the number of other members orthogonal to s is odd (E8: the half-sum of a 4-frame is a lattice
vector, so the count is 1 or 3).  Then the three cells {t, e} of t cover t-perp, and over F2 the three cell-perp sums
count every non-frame reader of t an odd number of times (the inclusion-exclusion is free; only the 3 frame lines
are counted twice and need the single 'd-line' reads of #493/#543).
Checks: number of 4-frames, number of good 4-frames, orbit types, and whether the lines can be partitioned into good
4-frames (CP-SAT exact cover).  Usage: python frames.py n   (n = 8 is the E8 control)"""
import sys, itertools
from collections import Counter
import numpy as np
from ortools.sat.python import cp_model
sys.dont_write_bytecode = True
import units as U


def setup(n):
    if n == 8:
        L = U.roots_E8(); G = U.gram_doubled(L); LN = [tuple(r) for r in L]
    else:
        L, G, lab = U.lorentz_family(n)
        LN = list(itertools.combinations(range(n), 3)) + list(itertools.combinations(range(n), 2))
    return L, G, LN


def frames4(G):
    v = len(G)
    O = [set(np.nonzero(G[i] == 0)[0]) - {i} for i in range(v)]
    out = []
    for a in range(v):
        for b in O[a]:
            if b <= a: continue
            for c in O[a] & O[b]:
                if c <= b: continue
                for d in O[a] & O[b] & O[c]:
                    if d <= c: continue
                    out.append((a, b, c, d))
    return out, O


def good(F, O):
    for t in F:
        others = [e for e in F if e != t]
        for s in O[t]:
            if s in F: continue
            if sum(1 for e in others if s in O[e]) % 2 == 0:
                return False
    return True


if __name__ == '__main__':
    n = int(sys.argv[1])
    L, G, LN = setup(n)
    v = len(G)
    Fs, O = frames4(G)
    gd = [F for F in Fs if good(F, O)]
    typ = Counter(tuple(sorted(len(LN[t]) if n != 8 else 0 for t in F)) for F in gd)
    print('n=%d v=%d 4-frames=%d good=%d types(line sizes)=%s' % (n, v, len(Fs), len(gd), dict(typ)), flush=True)
    if n != 8:
        for ty in typ:
            ex = next(F for F in gd if tuple(sorted(len(LN[t]) for t in F)) == ty)
            print('  example', [LN[t] for t in ex])
    # cell-perp sizes
    if gd:
        F = gd[0]; t, e = F[0], F[1]
        print('cell-perp {t,e} contains %d lines; t-perp %d' % (len(O[t] & O[e]), len(O[t])))
    if n != 8:
        npairs = sum(1 for t in range(v) if len(LN[t]) == 2)
        ppf = sorted(set(sum(1 for t in F if len(LN[t]) == 2) for F in gd))
        print('pairs per good frame: %s; pairs in total: %d' % (ppf, npairs))
        if all(c % 2 == 0 for c in ppf) and npairs % 2 == 1:
            print('NO partition into good 4-frames: every good frame holds an even number of pairs, %d is odd' % npairs)
            sys.exit(0)
    if v % 4 == 0 and gd:
        m = cp_model.CpModel()
        x = [m.NewBoolVar('f%d' % i) for i in range(len(gd))]
        inc = [[] for _ in range(v)]
        for i, F in enumerate(gd):
            for t in F: inc[t].append(x[i])
        for t in range(v):
            m.AddExactlyOne(inc[t])
        so = cp_model.CpSolver(); so.parameters.max_time_in_seconds = 600; so.parameters.num_workers = 4
        st = so.Solve(m)
        print('partition into good 4-frames:', so.StatusName(st))
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            P = [gd[i] for i in range(len(gd)) if so.Value(x[i])]
            assert sorted(t for F in P for t in F) == list(range(v)) and all(good(F, O) for F in P)
            print('  verified partition of %d lines into %d good 4-frames; frame types %s' % (
                v, len(P), dict(Counter(tuple(sorted(len(LN[t]) if n != 8 else 0 for t in F)) for F in P))))
