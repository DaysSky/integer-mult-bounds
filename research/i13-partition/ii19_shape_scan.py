"""II19 shape-budget scan: max R with kappa >= the new frontier (grid2-style, mix.price).
h=10, v=361, cst estimated [9]*10 (decoder design unknown -- FLAGGED as estimate).
If the budget is ~9-11v, weight-5/6 covers (c_t=6-7 -> R=1,800-2,200+dead) could fit."""
import sys, time
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/s7')
from mix import price
import mpmath as mp
t0 = time.time()
def log(*a): print('[%5.0fs]' % (time.time() - t0), *a, flush=True)

NEWF = mp.mpf(1744385950814795279853) / mp.mpf(10)**24
h, v, cstp = 10, 361, [9] * 10   # cst ESTIMATE: decoder for II19 never designed (flagged)
log('II19 shape-budget scan vs NEW frontier', mp.nstr(NEWF, 8), 'cst = 90 (ESTIMATED)')

def maxH(src, tgt, br, gp, ge=1, hi_mult=12):
    def ok(H):
        c = price(h, v, cstp, list(src), list(tgt), [(2 * v, 0, br), (H, ge, gp)])
        return c is not None and c >= NEWF
    if not ok(0): return None
    lo, hi = 0, hi_mult * v
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo

# piece conventions for h=10: src/tgt sum to 9 (h-1), br sums to 10, gp sums to 9 (h-ge)
srcs = ([1, 8], [1, 2, 6], [1, 1, 2, 5], [1, 2, 3, 3])
tgts = ([1, 8], [1, 2, 6], [1, 3, 5], [1, 2, 2, 4])
brs = ([1, 9], [1, 1, 8], [1, 1, 2, 6], [1, 1, 2, 3, 3])
gps = ([9], [2, 7], [3, 6], [2, 3, 4], [1, 3, 5], [2, 2, 5], [1, 2, 6], [4, 5])
results = []
for src in srcs:
    for tgt in tgts:
        for br in brs:
            for gp in gps:
                H = maxH(src, tgt, br, gp)
                if H is not None:
                    results.append((H, src, tgt, br, gp))
results.sort(key=lambda x: -x[0])
log('viable: %d' % len(results))
for H, src, tgt, br, gp in results[:12]:
    log('  H = %d (%.2fv) total R = %d (%.2fv): src %s tgt %s br %s gp %s' %
        (H, H / v, H + 3 * v, (H + 3 * v) / v, src, tgt, br, gp))
if results:
    log('II19 SHAPE BUDGET (cst 90 ESTIMATED): total R = %d (%.2fv)  [weight-5/6 covers need R = 1,800-2,200 + dead = 5.0-6.1v + dead]' %
        (results[0][0] + 3 * v, (results[0][0] + 3 * v) / v))