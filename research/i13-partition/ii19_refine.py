"""II19 c-refinement sweep: full shape grid at the projection scenarios.
Levers: (1) free in-chain corrections (Sigma c_t drops 361), (2) shape optimization at the
ACTUAL R (not the budget ceiling), (3) cst variants (E8-grade 72 through estimate 90).
price(h, v, cst_pieces, src, tgt, helpers): src/tgt piece lists sum h-1; helpers
(count, e, pieces) with sum(pieces) = h - e.  R = 2v + H."""
import sys, itertools
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
h, v = 10, 361

SRCS = [[1, 8], [2, 7], [3, 6], [4, 5], [1, 1, 7], [9]]
MIDS = [[9], [1, 8], [4, 5], [3, 6], [2, 3, 4]]
CSTS = ([7] * 10, [8] * 10, [9] * 10)

scen = [
    ('probe c_t 10.3, dead 300', 3720, 300),
    ('free corrections (361 off), dead 300', 3359, 300),
    ('free corrections, dead 150', 3359, 150),
    ('c_t 8.5 + free corr, dead 300', 2700, 300),
]
for label, sct, dead in scen:
    R = sct - v + dead
    H = R - 3 * v
    if H < 0:
        print('%s: R=%d below 2v, skip' % (label, R)); continue
    bbest = None
    for cst in CSTS:
        for src in SRCS:
            for tgt in SRCS:
                for mid in MIDS:
                    c = price(h, v, cst, src, tgt, [(2 * v, 0, [1, 9]), (H, 1, mid)])
                    if c and (bbest is None or c > bbest[0]):
                        bbest = (c, cst[0], src, tgt, mid)
    if bbest:
        c, cstv, src, tgt, mid = bbest
        print('%s: R=%d (H=%d) BEST c=%s (%+.2f%% vs frontier) @ cst %d src %s tgt %s mid %s' %
              (label, R, H, mp.nstr(c, 8), float(c / NEWF - 1) * 100, cstv, src, tgt, mid))