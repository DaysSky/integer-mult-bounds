"""EXHAUSTIVE: is R(t) covered by 4 rank-7 sets M_i = Q_i-perp (Q_i a rank-4 closed set through t)?
Any such cover refines a 4-cover by rank-8 sets F_i-perp (F_i a rank-3 frame through t inside Q_i), with
M_i = perp(F_i) & HYP[x_i] for a line x_i outside F_i.  Uses the exhaustive rank-8 4-covers (lr8allcovers_<kind>.pkl,
all covers containing each Stab(t)-orbit representative frame; every cover contains some representative's image,
so checking these covers up to Stab(t) is exhaustive).  usage: lr7refine.py P|T"""
import sys, pickle, itertools, collections, time
from lgeo import *
kind = sys.argv[1]; D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
t0 = time.time(); checked = 0; found = []
for F1, covs in D['covers'].items():
    for c in covs:
        checked += 1
        P = [pm(F) & R for F in c]
        opts = []
        for i in range(4):
            ex = P[i] & ~(P[(i + 1) % 4] | P[(i + 2) % 4] | P[(i + 3) % 4])
            cands = set()
            for x in range(V):
                if c[i] >> x & 1: continue
                if ex & ~HYP[x]: continue          # exclusive lines must stay
                cands.add(P[i] & HYP[x])
            cands = sorted(cands, key=pc, reverse=True); maxi = []
            for m in cands:
                if not any(m & ~q == 0 for q in maxi): maxi.append(m)
            opts.append(maxi)
        if any(not o for o in opts): continue
        for combo in itertools.product(*opts):
            if combo[0] | combo[1] | combo[2] | combo[3] == R:
                found.append(c); break
print(kind, 'rank-8 covers checked', checked, '| refinable to rank-7 4-covers:', len(found), '| %.0fs' % (time.time() - t0))
