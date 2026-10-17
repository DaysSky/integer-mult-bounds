import i13ent as Q
systems = [('E8', 8, 120, 72), ('I10', 10, 165, 99), ('I11', 11, 220, 110), ('I12', 12, 286, 143), ('I13', 13, 364, 156), ('I16', 16, 680, 240)]
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
print('break-even R / v  (frame-0 helpers kc=5; hub fraction f at entrance e with kh=2)')
for nm, h, v, cst in systems:
    row = []
    for frac, e in ((0, 0), (0.25, 2), (0.25, 4), (0.5, 2), (0.5, 4)):
        r = be(h, v, cst, frac, e); row.append('f%.2f e%d: %d (%.2fv)' % (frac, e, r, r / v))
    print(nm, ' | '.join(row), flush=True)
