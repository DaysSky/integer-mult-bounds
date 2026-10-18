"""The CEILING measurement: kappa(H) curves for I11 (and I13) out to the hosting wall.
If max kappa over H < frontier for every shape, the system is closed BY ARITHMETIC (no
architecture at any R can win).  If a curve crosses the frontier, the crossing R is the
shape budget any architecture must fit.  mix.price, grid2-verbatim conventions."""
import sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
def curve(h, v, cstp, src, tgt, br, gp, ge, tag, wall_v):
    """kappa(H) for H in steps to the wall; report max and frontier crossings."""
    best_c, best_H = None, -1
    Hs = list(range(0, wall_v * v + 1, max(1, v // 2)))
    cross = None
    for H in Hs:
        c = price(h, v, cstp, list(src), list(tgt), [(2 * v, 0, br), (H, ge, gp)])
        if c is None:
            break
        if best_c is None or c > best_c:
            best_c, best_H = c, H
        if cross is None and c >= NEWF:
            cross = H
    log('%s: max kappa = %s at H = %d (%.2fv, R = %.2fv)%s' %
        (tag, mp.nstr(best_c, 8) if best_c else 'None', best_H, best_H / v if best_H >= 0 else 0,
         (best_H + 3 * v) / v if best_H >= 0 else 0,
         '  *** CROSSES FRONTIER at H = %d (%.2fv) ***' % (cross, cross / v) if cross is not None else '  (below frontier everywhere)'))
    return best_c, cross

# I11: best grid2 shapes (from the recorded 6g-7c tables), cstp = [10]*11, wall ~36v
h, v, cstp = 11, 220, [10] * 11
log('--- I11 curves (wall ~36v, scan to 34v) ---')
for src, tgt, br, gp in (
    ([1, 9], [1, 9], [1, 10], [10]),
    ([1, 2, 7], [1, 2, 7], [1, 1, 9], [2, 8]),
    ([1, 1, 2, 6], [1, 3, 6], [1, 1, 2, 7], [3, 7]),
    ([1, 2, 3, 4], [1, 2, 3, 4], [1, 1, 2, 3, 4], [2, 3, 5]),
    ([1, 9], [1, 2, 7], [1, 1, 9], [2, 2, 2, 4]),
    ([1, 2, 7], [1, 9], [1, 10], [3, 7]),
):
    curve(h, v, cstp, src, tgt, br, gp, 1, 'I11 src%s tgt%s br%s gp%s' % (src, tgt, br, gp), 34)

# I13: i13exit conventions, cstp = [12]*13, wall: hosting wall for v=364...
h, v, cstp = 13, 364, [12] * 13
log('--- I13 curves (scan to 12v) ---')
for src, tgt, br, gp in (
    ([12], [11, 1], [1, 1, 2, 3, 6], [3, 4, 6]),
    ([12], [11, 1], [1, 1, 2, 3, 6], [1, 2, 3, 6]),
    ([12], [11, 1], [2, 2, 3, 4, 2], [2, 4, 5]),
    ([12], [11, 1], [1, 1, 2, 3, 6], [1, 3, 4, 5]),
):
    curve(h, v, cstp, src, tgt, br, gp, 1, 'I13 src%s tgt%s gp%s' % (src, tgt, gp), 12)
log('frontier', mp.nstr(NEWF, 8))