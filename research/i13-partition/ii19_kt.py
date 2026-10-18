"""THE K/T SENSITIVITY SCAN (the SS1867 audit's item #11: the pricer's K=4/T=32 — THE E8-CALIBRATED
PIPELINE CONSTANTS — NEVER RE-EXAMINED for the Lorentzian!!).

THE AUDIT's QUESTION (SS1868!!): the pricer's K=4/T=32 were calibrated at the E8 words (the
R420/R434/P111: the exact matches!) — the Lorentzian systems' words: the SAME K/T?! — the scan:
the K x T grid at the 121-line's window (the best Lorentzian window: the m=73, the v/m=1.66!!)
+ the R420's control!!

THE QUESTIONS:
(1) THE K/T's EFFECT on the 121-line's prices (the K 2-6 x the T 16/32/64!)
(2) THE R420's CONTROL at the variants (the published c at the K=4/T=32: the anchor!)
(3) THE VERDICT: does any K/T configuration price the 121-line above the frontier?!
"""
import sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price as pprice

t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

FRONTIER = 0.001744386
V121, H121 = 121, 9
climb_st = 2 * V121 * (H121 - 1)
DFRAC = {1: 0.258, 2: 0.563, 4: 0.047, 5: 0.117, 8: 0.014}

def d_hist(climb, rank=9, dec_r=9):
    hist = {}
    used = 0
    for d in (1, 2, 4):
        z = int(round(DFRAC[d] * climb / d))
        hist[d] = hist.get(d, 0) + z
        used += d * z
    rem = climb - used
    hist[5] = hist.get(5, 0) + rem // 5
    if rem % 5:
        hist[1] = hist.get(1, 0) + rem % 5
    hist[dec_r] = hist.get(dec_r, 0) + rank
    return hist

log('THE R420 CONTROL at the K/T variants:')
for K in (2, 3, 4, 5, 6):
    for T in (16, 32, 64):
        try:
            res = pprice({1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}, 120, 8, 420, K=K, T=T)
            c = res[0] if isinstance(res, tuple) else res
            if c is None or c <= 0:
                print('    K %d T %2d | NO ROOT' % (K, T))
            else:
                print('    K %d T %2d | c %.9f | vs the published 0.001653827: %+.2f%%'
                      % (K, T, c, (c - 0.001653827) / 0.001653827 * 100))
        except Exception as e:
            print('    K %d T %2d | EXCEPTION %s' % (K, T, e))

log('THE 121-LINE (the D-hist + the dr=9 decoder) at the K/T grid:')
for R in (380, 420, 440):
    climb = climb_st + R * H121
    for K in (2, 3, 4, 5, 6):
        for T in (16, 32, 64):
            try:
                res = pprice(d_hist(climb), V121, H121, R, K=K, T=T)
                c = res[0] if isinstance(res, tuple) else res
                if c is None or c <= 0:
                    print('    R %d K %d T %2d | NO ROOT' % (R, K, T))
                else:
                    print('    R %d K %d T %2d | c %.9f | %+.2f%%'
                          % (R, K, T, c, (c - FRONTIER) / FRONTIER * 100))
            except Exception as e:
                print('    R %d K %d T %2d | EXCEPTION %s' % (R, K, T, e))
log('DONE')
