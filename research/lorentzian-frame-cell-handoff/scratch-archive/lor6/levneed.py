import i13ent as Q
# v needed at R = rho*v for given h (cst = h(h-1)), lever fraction f at e=4 (hubs 2 stops), frame-0 helpers 5 stops
def ok(h, v, rho, f, e=4):
    R = int(rho * v); H = int(f * R); C = R - H
    c = Q.price(h, v, h * (h - 1), C, 5, 0, H, e, 2); return c is not None and c >= Q.P111
for rho in (3.5, 4.0):
    for h in (8, 9, 10, 11, 13):
        row = []
        for f in (0, 0.1, 0.25, 0.5):
            lo, hi = 20, 3000
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if ok(h, mid, rho, f): hi = mid
                else: lo = mid
            row.append('f%.2f: %d' % (f, hi))
        print('R=%.1fv h=%d  v needed  %s' % (rho, h, '  '.join(row)), flush=True)
