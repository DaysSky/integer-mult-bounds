import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
from i13ent import price, P111
from mpmath import mp
for name, h, v, cst in (('I11', 11, 220, 110), ('I13', 13, 364, 156), ('E8', 8, 120, 72)):
    for ks, kt, kc in ((3, 3, 4), (5, 2, 5)):
        # all helpers frame-0
        def be(eC, k, e=None, C=0):
            lo, hi = -1, 12000
            def ok(H):
                if e is None: c = price(h, v, cst, H, k, eC, 0, 1, 1, ks, kt)
                else: c = price(h, v, cst, C, kc, 0, H, e, k, ks, kt)
                return c is not None and c >= P111
            if not ok(0): return None
            while hi - lo > 1:
                mid = (lo + hi)//2
                if ok(mid): lo = mid
                else: hi = mid
            return lo
        f0 = be(0, kc); e1 = be(1, kc); e2 = be(2, kc)
        mixed = be(None, kc, e=1, C=2*v)
        print('%s ks=%d kt=%d k=%d: all frame-0 R<=%s (%.2fv) | all entrance-1 R<=%s (%.2fv) | all e2 %s (%.2fv) | 2v frame-0 + e1 group helpers H<=%s (R=%s, %.2fv)' % (
            name, ks, kt, kc, f0, f0/v, e1, e1/v, e2, e2/v, mixed, (2*v + mixed) if mixed is not None else None, ((2*v + mixed)/v) if mixed is not None else 0), flush=True)
