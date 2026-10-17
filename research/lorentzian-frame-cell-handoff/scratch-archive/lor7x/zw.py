"""Price of a zero-waste mover skeleton: v sources (ks pieces), 2v frame-0 relays (kc pieces), targets (kt), plus
scratch hubs at high entrance (in-chain lever): S9 at rank-9 sections (width h-9) and S6 at rank-e hubs.
Exact nine-stage pricer with best-fit mixed-width hosting (generalises lor6/i13ent.price to two hub classes)."""
import sys, bisect
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
K, T = 4, 32; L = 2 * K + 1
def split(total, k):
    b, r = divmod(total, k); return [b + 1] * r + [b] * (k - r)
def price(h, v, cst, groups, ks, kt):
    """groups: list of (count, entrance e, pieces k)"""
    a = h - 1; m = 1 + L * a; W = 2 * K * v * T; loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in split(a, ks): add(p, v)
    for p in split(a, kt): add(p, v)
    res = []
    for cnt, e, k in groups:
        for p in split(h - e, k): add(p, cnt)
        res += [h - e] * (cnt * L)
    q, r = divmod(cst, a); add(a, q); add(r, 1 if r else 0)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2 * v))
    for w in sorted(res, reverse=True):
        i = bisect.bisect_left(free, w)
        if i == len(free): return None
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r_, z in loc.items(): prof[r_] = prof.get(r_, 0) + z * T * L
    for r_, z in rem.items(): prof[r_] = prof.get(r_, 0) + z * T
    return root(prof, m, W)
f = lambda x: '%+.2f%%' % (float(x / P111 - 1) * 100) if x is not None else 'wall'
if __name__ == '__main__':
    for v, cst in ((216, 110), (220, 110)):
        for kc, ks, kt in ((6, 5, 3), (5, 4, 3), (6, 5, 2)):
            for S9, S6 in ((0, 0), (324, 0), (324, 216), (324, 432), (648, 432)):
                c = price(11, v, cst, [(2 * v, 0, kc), (S9, 9, 1), (S6, 6, 1)], ks, kt)
                print('v=%d cst=%d kc=%d ks=%d kt=%d relays=%d scratch9=%d scratch6=%d: %s' % (v, cst, kc, ks, kt, 2 * v, S9, S6, f(c)))
