import i13ent as Q
def be(h, v, cst, f, e, kh, kc=5):
    def ok(R):
        H = int(f * R); C = R - H
        c = Q.price(h, v, cst, C, kc, 0, H, e, kh); return c is not None and c >= Q.P111
    lo, hi = 0, 40000
    if not ok(1): return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
for nm, h, v, cst in (('I11', 11, 220, 110), ('I13', 13, 364, 156)):
    for e in (4, 8, h - 3, h - 2, h - 1):
        row = []
        for f in (0.5, 0.75, 0.9):
            r = be(h, v, cst, f, e, 1); row.append('f%.2f:%d(%.1fv)' % (f, r, r / v))
        print('%s hubs e=%d kh=1: %s' % (nm, e, '  '.join(row)), flush=True)
