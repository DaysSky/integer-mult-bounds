"""Exact prices of stated fragmentation scenarios: every register's climb split into k near-equal moves."""
import sys
from mpmath import mp
from pricer import price
P111 = mp.mpf('0.001733052823330162099157')
def split(c, k):
    k = min(k, c); q, r = divmod(c, k)
    return [q + 1] * r + [q] * (k - r)
def local(v, h, R, copies, k):
    loc = {}
    for c, n in ((h - 1, v), (h - 1, v), (h, R)):
        for p in split(c, k): loc[p] = loc.get(p, 0) + n
    for r in copies: loc[r] = loc.get(r, 0) + 1
    return loc
if __name__ == '__main__':
    # control: E8 with k moves -> compare with the real P111 price
    for k in (3, 4, 5):
        c, _, _ = price(local(111, 8, 439, [7] * 9, k), 111, 8, 439)
        print('E8 P111 scenario k=%d: c = %s (real word %s)' % (k, mp.nstr(c, 8), mp.nstr(P111, 8)))
    for name, v, h, cp in (('I11,1', 220, 11, [10] * 11), ('I13,1', 364, 13, [12] * 13)):
        for k in (3, 4, 5, 6):
            lo, hi = 0, 4 * v
            if price(local(v, h, 0, cp, k), v, h, 0)[0] < P111:
                print(name, 'k=%d: below P111 even at R=0' % k); continue
            while hi - lo > 1:
                mid = (lo + hi) // 2
                c = price(local(v, h, mid, cp, k), v, h, mid)[0]
                if c is not None and c >= P111: lo = mid
                else: hi = mid
            c = price(local(v, h, lo, cp, k), v, h, lo)[0]
            print('%s k=%d moves/register: beats P111 iff R <= %d (%.3f helpers/port; c at that R = %s)' % (name, k, lo, lo / v, mp.nstr(c, 8)), flush=True)
