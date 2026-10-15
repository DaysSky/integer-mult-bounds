"""Source-side analogue (transpose) of the rank-8 class with R420-style cells: 660 registers = 3 per cell, so every
line u lies in exactly 2 cells {u,f1}, {u,f2} (f_i orthogonal to u).  The 4 registers carrying x_u at the cell level
(x_u and x_u+x_f from each cell) first stop at rank-3 frames containing their cell, and (reach lemma, no target
reads at rank <= 2) their perps must cover R(u): a 4-cover of R(u) by rank-8 node perps that splits into two pairs,
pair i through a common line f_i orthogonal to u.  Exhaustive census over the representative covers (every cover is
an image of one).  usage: lsrccell.py"""
import pickle, itertools, collections
from lgeo import *
for kind in ('P', 'T'):
    D = pickle.load(open('lr8allcovers_%s.pkl' % kind, 'rb')); t = D['t']; R = HYP[t]
    tot = 0; good = 0; ex = None
    for F1, covs in D['covers'].items():
        for c in covs:
            tot += 1
            ok = False
            for pairing in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
                fs = []
                for i, j in pairing:
                    common = c[i] & c[j] & R & ~(1 << t)     # lines f orthogonal to t in both frames
                    if not common: break
                    fs.append(common)
                else:
                    # the two partners must be distinct lines
                    if any(a != b for a in bits(fs[0]) for b in bits(fs[1])): ok = True; break
            if ok:
                good += 1
                if ex is None: ex = c
    print(kind, 'representative covers', tot, '| splittable into two cell pairs:', good)
