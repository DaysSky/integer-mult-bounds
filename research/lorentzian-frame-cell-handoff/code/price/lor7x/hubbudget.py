import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
from i13ent import price, P111
from mpmath import mp
h, v, cst = 11, 220, 110
for C, kc in ((440, 4), (440, 6), (330, 4), (550, 4)):
    for ks, kt in ((3, 3), (5, 4)):
        row = []
        for e, kh in ((2, 2), (5, 1), (5, 2), (8, 1), (9, 1)):
            lo, hi = -1, 6000
            def ok(H):
                c = price(h, v, cst, C, kc, 0, H, e, kh, ks, kt); return c is not None and c >= P111
            if not ok(0): row.append('e%d/k%d:none' % (e, kh)); continue
            while hi - lo > 1:
                mid = (lo + hi)//2
                if ok(mid): lo = mid
                else: hi = mid
            row.append('e%d/k%d:%d' % (e, kh, lo))
        c0 = price(h, v, cst, C, kc, 0, 0, 1, 1, ks, kt)
        print('C=%d kc=%d ks=%d kt=%d  c(H=0)=%s  maxH: %s' % (C, kc, ks, kt, mp.nstr(c0, 6), ' '.join(row)), flush=True)
