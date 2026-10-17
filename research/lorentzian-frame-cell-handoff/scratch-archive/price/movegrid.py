"""Exact (R, moves) landscape for E8 vs P111-tuned (0.001733427...): every register's climb split in k near-equal moves
(sources 7, targets 7, helpers 8), totals [7]*9 (v=111) or [8]*9 (v=120).  Prints break-even R per k."""
from mpmath import mp
from pricer import price
from scen import local, split
P = mp.mpf('0.001733427039589844234749')
def loc2(v, h, R, copies, ks, kt, kh):
    loc = {}
    for c, n, k in ((h - 1, v, ks), (h - 1, v, kt), (h, R, kh)):
        for p in split(c, k): loc[p] = loc.get(p, 0) + n
    for r in copies: loc[r] = loc.get(r, 0) + 1
    return loc
for v, cp in ((111, [7] * 9), (120, [8] * 9)):
    for ks, kt, kh in ((1, 1, 2), (2, 1, 2), (2, 2, 2), (2, 2, 3), (3, 2, 3), (3, 3, 3), (3, 2, 4), (4, 2, 4), (4, 4, 4), (4, 2, 5), (5, 5, 5)):
        lo, hi = 0, 4 * v
        f = lambda R: price(loc2(v, 8, R, cp, ks, kt, kh), v, 8, R)[0]
        if f(hi) is not None and f(hi) >= P:
            print('v=%d moves (src %d, tgt %d, helper %d): beats P111t even at R=%d (c=%s)' % (v, ks, kt, kh, hi, mp.nstr(f(hi), 7)), flush=True); continue
        if f(0) is None or f(0) < P:
            print('v=%d moves (src %d, tgt %d, helper %d): below P111t even at R=0' % (v, ks, kt, kh), flush=True); continue
        while hi - lo > 1:
            mid = (lo + hi) // 2
            c = f(mid)
            if c is not None and c >= P: lo = mid
            else: hi = mid
        print('v=%d moves (src %d, tgt %d, helper %d): beats P111t iff R <= %d  (%.2f/port); c(R=360)=%s c(R=420)=%s' %
              (v, ks, kt, kh, lo, lo / v, mp.nstr(f(360), 7), mp.nstr(f(420), 7)), flush=True)
