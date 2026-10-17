from mix import price, E1, mp
def maxH(h, v, cstp, src, tgt, fixed, gp, ge=1, hi_mult=20):
    def ok(H):
        c = price(h, v, cstp, src, tgt, fixed + [(H, ge, gp)])
        return c is not None and c >= E1
    if not ok(0): return None
    lo, hi = 0, hi_mult*v
    while hi - lo > 1:
        mid = (lo+hi)//2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
import sys
sysname = sys.argv[1]
if sysname == 'I11':
    h, v, cstp = 11, 220, [10]*11
    srcs = ([1,9], [1,2,7], [1,1,2,6], [1,2,3,4])
    tgts = ([1,9], [1,2,7], [1,3,6], [1,2,3,4])
    brs = ([1,10], [1,1,9], [1,1,2,7], [1,1,2,3,4])
    gps = ([10], [2,8], [3,7], [2,3,5], [2,2,2,4])
else:
    h, v, cstp = 8, 120, [8]*9
    srcs = ([1,6], [1,2,4], [1,1,2,3], [1,2,2,1,1])
    tgts = ([1,6], [1,2,4], [1,3,3], [2,5])
    brs = ([1,7], [1,1,6], [1,1,2,4], [1,1,2,2,1,1])
    gps = ([7], [2,5], [3,4], [2,2,3], [2,2,2,1])
for src in srcs:
    for tgt in tgts:
        for br in brs:
            row = []
            for gp in gps:
                H = maxH(h, v, cstp, src, tgt, [(2*v, 0, br)], gp)
                row.append('%s:%s' % ('-'.join(map(str, gp)), '%.2f' % (H/v) if H is not None else 'X'))
            print('src', '-'.join(map(str,src)), 'tgt', '-'.join(map(str,tgt)), 'br(2v)', '-'.join(map(str,br)), '| H/v:', ' '.join(row), flush=True)
