"""THE II19 BREAKTHROUGH STEP 2 — THE ln-MASS MAP: THE (R, SHAPE)-GRID (ii19_own2.py).

THE MASTER LAW (THE OWN1's DISCOVERY, VERIFIED ON THE WORD3/R420/P111!!!):
    c = deficit / ln-mass,   deficit = 256v - 288*CST (the h/R-INVARIANT!!!),
    ln-mass = sum(z * r * ln(m/r)) over the global profile (local*288 + rem*32).
THE 121-LINE: deficit = 30,976 - 23,904 = 7,072 (CST=83!!) | the frontier (0.001744386)
needs ln-mass <= 7,072/0.001744 = 4.056M.

THE LEVERS (THE ln-mass's!!): (1) THE R down (the local-mass ~ 9R: the ln ~ proportional!!);
(2) THE HIGH-RANK SHAPES (the wln: the ln(73/1) = 4.29 vs the ln(73/6) = 2.50!!!);
(3) THE CST down (the deficit's +288 per CST-unit!!!).

THE MAP: the wln-grid {2.4, 2.6, 2.8, 3.0, 3.3, 3.56 (the word3's!!)} x the R-grid
{121, 126, 131, 135, 140, 150, 158, 160, 175, 200, 230, 300, 339, 420, 463!!}
-> THE c(R, wln)-TABLE -> THE BREAKTHROUGH ZONE (c >= 0.001744!!!!!)!!!

THE SHAPES' REALIZABILITY (THE honest anchor!!): the pieces' chains [0, 4, the read-dims, 9]
(the SS1695's: the wln ~ the 3.2-3.5!!) vs THE HIGH-START PIECES ([0, 6, 8, 9]-style: the
wln ~ 2.6-2.8!!) — THE MAP's READ: WHICH (R, wln) DOES THE OWN-STRUCTURE NEED?!
"""
import sys, time
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

sys.path.insert(0, 'research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp, mpf
mp.dps = 40
P111 = mp.mpf('0.001733052823330162099157')
FRONTIER = mp.mpf('0.001744386')
V, H, CST = 121, 9, 83

def hist_for_wln(mass, wln_target):
    """a mass-exact hist with the given wln = sum(z*r*ln(73/r))/mass: the 2-rank mix {hi, lo}!!"""
    m = 1 + 9 * (H - 1)
    import math
    # the 2-rank mixes: {hi, lo}: the wln = (hi_n*hi*ln(m/hi) + lo_n*lo*ln(m/lo))/mass!!
    # the honest realization: the (hi, lo) pairs sweeping the wln!!
    pairs = [(8, 3), (8, 2), (8, 1), (7, 3), (7, 2), (6, 3), (6, 2), (6, 1), (5, 2), (5, 1), (4, 2), (4, 1), (9, 4), (9, 2)]
    best = None
    for hi, lo in pairs:
        lhi = math.log(m / hi) if hi < m else 0
        llo = math.log(m / lo) if lo < m else 0
        # the mass split: x*hi + (1-x)*... — the mass-exact: n_hi*hi + n_lo*lo = mass: the wln =
        # (n_hi*hi*lhi + n_lo*lo*llo)/mass: the continuous sweep: n_lo/n_hi = ...
        # the corner-sweep: the pure-hi (wln = lhi) .. the pure-lo (wln = llo)!!
        for frac in [i / 40 for i in range(41)]:
            m_hi = mass * frac
            m_lo = mass - m_hi
            n_hi = m_hi / hi
            n_lo = m_lo / lo
            w = (n_hi * hi * lhi + n_lo * lo * llo) / mass
            if best is None or abs(w - wln_target) < abs(best[0] - wln_target):
                best = (w, hi, lo, n_hi, n_lo)
    (w, hi, lo, n_hi, n_lo) = best
    out = {hi: round(n_hi), lo: round(n_lo)}
    d = mass - sum(k * z for k, z in out.items())
    while d:
        if d > 0:
            out[1] = out.get(1, 0) + 1
            d -= 1
        else:
            k = max(out)
            if out.get(k, 0) > 0:
                out[k] -= 1
                d += k
            else:
                out[1] = out.get(1, 0) + 1
                d -= 1
    return {k: z for k, z in out.items() if z}

log('THE MAP: the (R, wln)-grid -> the c(R, wln)!!! (the frontier 0.001744386!!)')
log('    the deficit = 256*%d - 288*%d = %d (the h/R-invariant!!!)' % (V, CST, 256 * V - 288 * CST))
hdr = '    R     mass  ' + ''.join('   wln=%.2f        ' % w for w in [2.4, 2.6, 2.8, 3.0, 3.3, 3.56])
log(hdr)
for R in [121, 126, 131, 135, 140, 150, 158, 160, 175, 200, 230, 300, 339, 420, 463]:
    mass = 9 * R + CST + 2 * V * (H - 1)
    row = '    %d  %d  ' % (R, mass)
    for w in [2.4, 2.6, 2.8, 3.0, 3.3, 3.56]:
        h = hist_for_wln(mass, w)
        assert sum(k * z for k, z in h.items()) == mass
        c, prof, d = price(h, V, H, R)
        if c is None:
            row += '  %-15s' % ('NONE(%s)' % d.get('error'))
        else:
            mark = '*' if c >= FRONTIER else ' '
            row += '  %s%-14s' % (mark, mp.nstr(c, 9))
    log(row)
log('    * = ABOVE THE FRONTIER (0.001744386)!!!')
log('DONE — THE BREAKTHROUGH ZONE MAP!!')
