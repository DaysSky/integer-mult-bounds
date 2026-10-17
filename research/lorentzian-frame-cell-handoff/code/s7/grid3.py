from mix import price, E1, mp
def maxH(h, v, cstp, src, tgt, fixed, gp, ge=1):
    def ok(H):
        c = price(h, v, cstp, src, tgt, fixed + [(H, ge, gp)]); return c is not None and c >= E1
    if not ok(0): return None
    lo, hi = 0, 20*v
    while hi - lo > 1:
        mid = (lo+hi)//2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
h, v = 11, 220
for cstp, nf0, srcp, lab in (([11]*11, 2*v, [10], 'src->FULL feeds totals, 2v group-entry copies, cst121'),
                            ([10]*11, 2*v, [1,9], 'idealised: rank-10 totals free, 2v copies, cst110'),
                            ([11]*11, 2*v, [1,9], 'cst121 totals free (optimistic), 2v copies')):
    print(lab)
    for brp in ([1,1,9], [1,1,2,7], [1,1,3,6], [1,1,2,3,4]):
        for tgt in ([1,9], [1,2,7], [1,3,6]):
            row = []
            for gp in ([10], [2,8], [3,7], [2,3,5], [2,2,6], [1,2,7]):
                H = maxH(h, v, cstp, srcp, tgt, [(nf0, 0, brp)], gp)
                row.append('%s:%s' % ('-'.join(map(str,gp)), '%.2f' % (H/v) if H is not None else 'X'))
            print('  copies', '-'.join(map(str,brp)), 'tgt', '-'.join(map(str,tgt)), '| H/v', ' '.join(row), flush=True)
