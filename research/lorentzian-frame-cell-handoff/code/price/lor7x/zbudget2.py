import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
from i13ent import price, P111
for name, h, v, cst in (('I10', 10, 165, 99), ('I11', 11, 220, 110), ('I12', 12, 286, 143), ('I13', 13, 364, 156), ('E8', 8, 120, 72), ('h9-120', 9, 120, 72), ('h9-111', 9, 111, 72)):
    out = []
    for ks, kt, kc, kh in ((3, 2, 3, 3), (3, 3, 3, 3), (4, 3, 4, 4), (5, 2, 5, 4)):
        lo, hi = -1, 12000
        def ok(H):
            c = price(h, v, cst, 2*v, kc, 0, H, 1, kh, ks, kt); return c is not None and c >= P111
        if not ok(0): out.append('ks%d kt%d kc%d kh%d: none' % (ks, kt, kc, kh)); continue
        while hi - lo > 1:
            mid = (lo + hi)//2
            if ok(mid): lo = mid
            else: hi = mid
        out.append('ks%d kt%d kc%d kh%d: H<=%d (%.2fv)' % (ks, kt, kc, kh, lo, lo/v))
    print(name, ' | '.join(out), flush=True)
