import i13ent as Q
def ok(h, v, cst, rho, f, e=4):
    R = int(rho * v); H = int(f * R); C = R - H
    c = Q.price(h, v, cst, C, 5, 0, H, e, 2); return c is not None and c >= Q.P111
for cst in (56, 63, 72):
    for rho in (3.0, 3.5, 4.0):
        row = []
        for f in (0, 0.25, 0.5, 0.75):
            lo, hi = 20, 400
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if ok(8, mid, cst, rho, f): hi = mid
                else: lo = mid
            row.append('f%.2f:%d' % (f, hi))
        print('h=8 cst %d R=%.1fv  v needed  %s' % (cst, rho, '  '.join(row)), flush=True)
