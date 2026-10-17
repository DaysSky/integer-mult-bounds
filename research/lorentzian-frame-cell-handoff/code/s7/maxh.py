from mix import price, E1
def maxH(h, v, cstp, src, tgt, fixed, gp, ge=1, hi=20):
    def ok(H):
        c = price(h, v, cstp, src, tgt, fixed + [(H, ge, gp)]); return c is not None and c >= E1
    if not ok(0): return None
    lo, up = 0, hi * v
    while up - lo > 1:
        mid = (lo + up) // 2
        if ok(mid): lo = mid
        else: up = mid
    return lo
