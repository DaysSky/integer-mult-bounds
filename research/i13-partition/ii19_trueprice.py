"""II19 TRUE-HISTOGRAM exact pricer — fires when ii19_design.pkl lands.
Computes the final c from the design's real ledger (Sigma c_t, distinct flats, content):
- correction accounting both ways (counted, and free in-chain per the R434 mechanism)
- dead bands: content//17 (E8 compression), content//8 (2x-worse pessimism), 600 (flat)
- full shape grid (src/tgt/middle piece shapes) x cst variants (72/80/90)
Reports the best c per band vs the frontier 0.0017444."""
import sys, pickle
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
E1 = mpf = mp.mpf('0.001734473240795253742474')
h, v = 10, 361

d = pickle.load(open('ii19_design.pkl', 'rb'))
design, use_count, ct_total = d['design'], d['use_count'], d['ct_total']
content = sum(bin(fm).count('1') for fm in use_count)
corr = sum(1 for (w1, w2, lv) in design.values() if lv > 0)
print('LEDGER: sum c_t %d, corrections %d, distinct flats %d, content %d' %
      (ct_total, corr, len(use_count), content))

SRCS = [[1, 8], [2, 7], [3, 6], [4, 5], [1, 1, 7], [9]]
MIDS = [[9], [1, 8], [4, 5], [3, 6], [2, 3, 4]]
CSTS = ([7] * 10, [8] * 10, [9] * 10)

for label, sct in [('corrections counted', ct_total), ('corrections free (in-chain)', ct_total - corr)]:
    R_id = sct - v
    for dlabel, dead in [('mids=content/17 (E8)', content // 17),
                         ('mids=content/8 (pessimistic)', content // 8),
                         ('mids=600 (flat)', 600)]:
        R = R_id + dead
        H = R - 3 * v
        if H < 0:
            print('%s / %s: R=%d below 2v skip' % (label, dlabel, R)); continue
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
            print('%s / %s: R=%d (%.1fv) BEST c=%s (%+.2f%% vs frontier, %+.2f%% vs E1) @ cst %d src %s tgt %s mid %s' %
                  (label, dlabel, R, R / v, mp.nstr(c, 8), float(c / NEWF - 1) * 100,
                   float(c / mp.mpf('0.001734473240795253742474') - 1) * 100, cstv, src, tgt, mid))