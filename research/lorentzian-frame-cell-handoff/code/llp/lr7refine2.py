"""EXHAUSTIVE (extension of lr7refine.py): is R(t) covered by 4 rank-<=7 SPAN-closed line sets M_i, each inside a
rank-8 node F_i-perp (F_i a rank-3 frame through t)?  (M_i any hyperplane line set of span(F_i-perp), not only perps.)
Any such cover gives a rank-8 4-cover (F_1..F_4) with exclusive part ex_i inside M_i; enumerate, for every exhaustive
rank-8 4-cover up to Stab(t) (lr8allcovers_<kind>.pkl), all maximal hyperplane line sets of P_i = perp(F_i) & R(t)
containing ex_i (span closures grown from ex_i one line at a time until rank 7), and test all 4-tuples.
usage: lr7refine2.py P|T"""
import sys, pickle, itertools, time
import numpy as np
from lgeo import *
kind = sys.argv[1]; D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
LA = np.array(g.LA, dtype=float)
def closure_in(S, Pm):
    """lines of Pm in span(S) (exact rational rank via integer matrices through lgeo.rank)"""
    r = rank(S); out = S
    for v in bits(Pm & ~S):
        if rank(S | (1 << v)) == r: out |= 1 << v
    return out, r
memo = {}
def hyper(ex, Pm):
    key = (ex, Pm)
    if key in memo: return memo[key]
    c0, r0 = closure_in(ex, Pm)
    if r0 >= 8: memo[key] = []; return []
    level = {c0}; r = r0
    while r < 7:
        nxt = set()
        for S in level:
            for u in bits(Pm & ~S):
                c, _ = closure_in(S | (1 << u), Pm); nxt.add(c)
        level = nxt; r += 1
    res = sorted(level, key=pc, reverse=True); maxi = []
    for m in res:
        if not any(m & ~q == 0 for q in maxi): maxi.append(m)
    memo[key] = maxi; return maxi
t0 = time.time(); checked = 0; found = []
for F1, covs in D['covers'].items():
    for c in covs:
        checked += 1
        P = [pm(F) & R for F in c]
        opts = []
        for i in range(4):
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
            opts.append(hyper(ex, P[i]))
        if any(not o for o in opts): continue
        for combo in itertools.product(*opts):
            if combo[0] | combo[1] | combo[2] | combo[3] == R:
                found.append((c, combo)); break
        if checked % 500 == 0: print(checked, len(found), round(time.time() - t0), flush=True)
print(kind, 'rank-8 covers checked', checked, '| refinable to 4 hyperplane line sets:', len(found), '| %.0fs' % (time.time() - t0))
if found: pickle.dump(found, open('lr7refine2_%s.pkl' % kind, 'wb'))
