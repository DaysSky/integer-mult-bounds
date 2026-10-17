import i13ent as Q
def be(h, v, cst, frac, e, kc=5, kh=2):
    def ok(R):
        H = int(frac * R); C = R - H
        c = Q.price(h, v, cst, C, kc, 0, H, e, kh); return c is not None and c >= Q.P111
    lo, hi = 0, 12000
    if not ok(1): return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
for nm, h, v in (('I11', 11, 220), ('I13', 13, 364)):
    for cst in ((110, 100, 90, 80, 66) if h == 11 else (156, 140, 120, 100)):
        r0 = be(h, v, cst, 0, 0); r1 = be(h, v, cst, 0.25, 4)
        print('%s cst %d: break-even f0 %.2fv, f0.25e4 %.2fv' % (nm, cst, r0 / v, r1 / v), flush=True)
