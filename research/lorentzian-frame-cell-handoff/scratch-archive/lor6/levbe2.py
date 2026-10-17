import i13ent as Q
systems = [('E8', 8, 120, 72), ('E8-111', 8, 111, 63), ('h9 v120', 9, 120, 72), ('h9 v127', 9, 127, 72), ('h9 v128', 9, 128, 72),
           ('h10 v165', 10, 165, 99), ('h10 v165 c90', 10, 165, 90)]
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
for nm, h, v, cst in systems:
    row = []
    for frac, e in ((0, 0), (0.25, 4), (0.5, 4)):
        r = be(h, v, cst, frac, e); row.append('f%.2f e%d: %d (%.2fv)' % (frac, e, r, r / v))
    print(nm, ' | '.join(row), flush=True)
