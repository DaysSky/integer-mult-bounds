"""I11 shape scan with the exact 6g-7c conventions (grid2.py I11 block, verbatim).
mix.price interface; max group helpers H on top of 2v branches; c >= the NEW frontier."""
import sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
h, v, cstp = 11, 220, [10] * 11
log('I11 scan vs NEW frontier', mp.nstr(NEWF, 8))

def maxH(src, tgt, br, gp, ge=1, hi_mult=20):
    def ok(H):
        c = price(h, v, cstp, list(src), list(tgt), [(2 * v, 0, br), (H, ge, gp)])
        return c is not None and c >= NEWF
    if not ok(0): return None
    lo, hi = 0, hi_mult * v
    if not ok(hi): return None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo

srcs = ([1, 9], [1, 2, 7], [1, 1, 2, 6], [1, 2, 3, 4])
tgts = ([1, 9], [1, 2, 7], [1, 3, 6], [1, 2, 3, 4])
brs = ([1, 10], [1, 1, 9], [1, 1, 2, 7], [1, 1, 2, 3, 4])
gps = ([10], [2, 8], [3, 7], [2, 3, 5], [2, 2, 2, 4], [1, 4, 5], [1, 1, 3, 5], [2, 4, 4], [1, 3, 6], [3, 3, 4])
results = []
for src in srcs:
    for tgt in tgts:
        for br in brs:
            for gp in gps:
                H = maxH(src, tgt, br, gp)
                if H is not None:
                    results.append((H, src, tgt, br, gp))
results.sort(key=lambda x: -x[0])
log('viable shapes: %d' % len(results))
log('top 15 shape-optimal budgets (max group helpers H on top of 2v branches, at NEW frontier):')
for H, src, tgt, br, gp in results[:15]:
    log('  H = %d (%.2fv)  total R = %d (%.2fv): src %s tgt %s br %s gp %s' %
        (H, H / v, H + 3 * v, (H + 3 * v) / v, src, tgt, br, gp))
if results:
    log('SHAPE-OPTIMAL I11 budget: total R = %d (%.2fv)  [3-section needs 4.2-4.8v; 6g-7c tables said 3.8-4.1v vs E1]' %
        (results[0][0] + 3 * v, (results[0][0] + 3 * v) / v))