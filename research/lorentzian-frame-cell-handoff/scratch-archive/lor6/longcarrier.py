"""Regime 'long-chain carriers + near-top hubs' for I_{11,1}: C frame-0 carriers with kc stops (one hub injection per
stop), H hubs entering at rank e with kh stops, targets kt stops (one hub read level per stop), sources ks = 2.
Report max H that still beats P111-tuned for each (C, kc, kt, e)."""
import i13ent as Q
h, v, cst = 11, 220, 110
def maxH(C, kc, kt, e, kh=1):
    def ok(H):
        c = Q.price(h, v, cst, C, kc, 0, H, e, kh, ks=2, kt=kt); return c is not None and c >= Q.P111
    if not ok(0): return -1
    lo, hi = 0, 20000
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
for kt in (3, 6, 10):
    for kc in (5, 8, 11):
        row = []
        for C in (300, 500, 700, 900):
            H = maxH(C, kc, kt, 10)
            row.append('C%d:H<=%d (inj~%d)' % (C, H, (C + v) * kc) if H >= 0 else 'C%d: loses' % C)
        print('kt=%d kc=%d e=10: %s' % (kt, kc, '  '.join(row)), flush=True)
