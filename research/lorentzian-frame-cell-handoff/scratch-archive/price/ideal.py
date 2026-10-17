"""Exact upper bound on the nine-stage (and other K) bit price of ANY word of a unit with given (v, h, cst, R) in the
hub template: every register climbs in one move (sources 1 -> h, targets 0 -> h-1, helpers 0 -> h), copies at their
COPY ranks.  Bigger children are cheaper per unit mass, so this profile maximises c for fixed R."""
import sys
from mpmath import mp
from pricer import price
mp.dps = 30
P111 = mp.mpf('0.001733052823330162099157')
def ideal_local(v, h, R, copies):
    loc = {}
    def add(r, k):
        if r > 0 and k: loc[r] = loc.get(r, 0) + k
    add(h - 1, v)          # sources 1 -> h
    add(h - 1, v)          # targets 0 -> h-1
    add(h, R)              # helpers 0 -> h
    for r in copies: add(r, 1)
    return loc
units = {
    'E8 P111 (v111 h8, 9 totals rank 7)': (111, 8, [7] * 9),
    'I11,1 (v220 h11, 11 totals rank 10)': (220, 11, [10] * 11),
    'I13,1 (v364 h13, 13 totals rank 12)': (364, 13, [12] * 13),
}
for name, (v, h, cp) in units.items():
    print('==', name)
    for K in (3, 4, 5, 6):
        row = []
        for rho in (0, 1, 2, 2.5, 3, 3.5, 3.95, 4):
            R = int(round(rho * v))
            c, prof, d = price(ideal_local(v, h, R, cp), v, h, R, K=K)
            row.append('%.2f:%s' % (rho, mp.nstr(c, 6) if c is not None else d.get('error')))
        print('  K=%d (stages %d):' % (K, 2 * K + 1), ' '.join(row), flush=True)
    # break-even R vs P111 at K=4 (exact bisection over integer R)
    lo, hi = 0, 4 * v
    c0, _, _ = price(ideal_local(v, h, 0, cp), v, h, 0)
    if c0 is None or c0 < P111:
        print('  ideal c at R=0 below P111: no R works'); continue
    while hi - lo > 1:
        mid = (lo + hi) // 2
        c, _, _ = price(ideal_local(v, h, mid, cp), v, h, mid)
        if c is not None and c >= P111: lo = mid
        else: hi = mid
    print('  K=4: ideal profile beats P111 iff R <= %d (%.3f helpers/port)' % (lo, lo / v), flush=True)
