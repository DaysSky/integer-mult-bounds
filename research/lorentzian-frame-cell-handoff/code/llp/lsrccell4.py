"""Weakest source-side condition for R = 440 with orthogonal-pair cells: each of the 4 carrier registers of x_u
first stops at a frame containing its cell {u,f} (f orthogonal to u), so every frame of u's 4-cover must contain a
line orthogonal to u; the register budget (880 carrier slots from 660 registers) forces 220 SUM registers whose hub
lies in the covers of both lines of its cell, i.e. on average 2 of u's 4 frames are shared with cell partners.
Census over representative covers: (a) every frame contains a line orthogonal to u; (b) histogram of the number of
frames F of the cover containing a line f orthogonal to u such that F is ALSO in some 4-cover of R(f) (shareable).
usage: lsrccell4.py"""
import pickle, collections
from lgeo import *
tabs = {}
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']
    tabs[kind] = {canon((1 << t, F1))[0]: len(c) for F1, c in D['covers'].items()}
def usable(b, F):
    return tabs[KIND[b]].get(canon((1 << b, F))[0], 0) > 0
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    tot = 0; alla = 0; sh = collections.Counter(); memo = {}
    for F1, covs in D['covers'].items():
        for c in covs:
            tot += 1
            partners = [F & R & ~(1 << t) for F in c]
            if all(partners): alla += 1
            k = 0
            for F, pt in zip(c, partners):
                if F not in memo: memo[F] = any(usable(f, F) for f in bits(pt))
                if memo[F]: k += 1
            sh[k] += 1
    print(kind, 'covers', tot, '| (a) all 4 frames contain a partner orthogonal to u:', alla,
          '| (b) #frames shareable with a partner (hist):', sorted(sh.items()), flush=True)
