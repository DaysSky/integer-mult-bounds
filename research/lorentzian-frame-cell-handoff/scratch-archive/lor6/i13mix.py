import i13ent as Q
from mpmath import mp
h, v, cst = 13, 364, 156
print('I13 mixed: C frame-0 carriers (kc stops), H hubs at entrance e (kh stops); vs P111-tuned')
for C, kc in ((706, 3), (706, 4), (800, 4)):
    for e, kh in ((0, 2), (5, 1), (6, 1), (8, 1), (6, 2), (8, 2)):
        def ok(H):
            c = Q.price(h, v, cst, C, kc, 0, H, e, kh); return c is not None and c >= Q.P111
        if not ok(0): print(' C=%d kc=%d: C alone loses' % (C, kc)); break
        lo, hi = 0, 6000
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ok(mid): lo = mid
            else: hi = mid
        c568 = Q.price(h, v, cst, C, kc, 0, 568, e, kh)
        print(' C=%d kc=%d, hubs e=%d kh=%d: H <= %d ; at H=568: %s' % (C, kc, e, kh, lo,
              ('%+.2f%%' % float((c568 / Q.P111 - 1) * 100)) if c568 else 'wall'), flush=True)
