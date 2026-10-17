from exitmix import price, E1
from mix import pct
h, v = 13, 364
cst = [12]*13
def maxR(src, tgt, coll_frac, coll_exit, collp, deadp, lo=0, hi=8*364):
    """collectors = coll_frac*R (consumed at tops), the rest dead; returns max R with c >= E1"""
    def ok(R):
        nc = int(coll_frac * R); nd = R - nc
        if coll_exit: hs = [(nc, 0, 12, collp[:-1])] if sum(collp[:-1]) == 12 else None
        else: hs = [(nc, 0, 13, collp)]
        hs = hs + [(nd, 0, 13, deadp)]
        c = price(h, v, cst, [(v, src)], [(v, tgt)], hs)
        return c is not None and c >= E1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
for collp in ([11, 1, 1], [10, 1, 1, 1], [2, 9, 1, 1], [4, 7, 1, 1]):
    for deadp in ([11, 2], [10, 3], [8, 5], [2, 9, 2]):
        r0 = maxR([12], [11, 1], 0.5, False, collp, deadp); r1 = maxR([12], [11, 1], 0.5, True, collp, deadp)
        print('coll', collp, 'dead', deadp, 'maxR no-exit %.2fv  exit %.2fv' % (r0 / v, r1 / v), flush=True)
