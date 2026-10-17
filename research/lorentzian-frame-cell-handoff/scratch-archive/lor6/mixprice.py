"""Price an I_{11,1} hub-native profile: classes (count, entrance e, stops k); sources ks, targets kt."""
import sys, bisect
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
P111 = mp.mpf('0.001733427039589844'); K, T = 4, 32; L = 2*K + 1
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def price(h, v, cst, classes, ks=2, kt=4):
    a = h - 1; m = 1 + L*a; W = 2*K*v*T; loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in split(h - 1, ks): add(p, v)
    for p in split(h - 1, kt): add(p, v)
    widths = []
    for n, e, k in classes:
        for p in split(h - e, k): add(p, n)
        widths += [h - e] * (n * L)
    q, r = divmod(cst, h - 1); add(h - 1, q); add(r, 1 if r else 0)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    for w in sorted(widths, reverse=True):
        i = bisect.bisect_left(free, w)
        if i == len(free): return None
        c = free.pop(i)
        if c > w: bisect.insort(free, c - w)
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r_, z in loc.items(): prof[r_] = prof.get(r_, 0) + z*T*L
    for r_, z in rem.items(): prof[r_] = prof.get(r_, 0) + z*T
    return root(prof, m, W)
h, v, cst = 11, 220, 110
scen = {
 'A: 300 carriers(0,8) + 440 xfer(e2,3) + 330 xfer(e7,3) + 495 D8hub(e8,2) + 220 top(e10,1)':
   [(300, 0, 8), (440, 2, 3), (330, 7, 3), (495, 8, 2), (220, 10, 1)],
 'B: A + 1000 assembly hubs(e7,2)': [(300, 0, 8), (440, 2, 3), (330, 7, 3), (495, 8, 2), (220, 10, 1), (1000, 7, 2)],
 'C: A + 1000 assembly hubs(e5,3)': [(300, 0, 8), (440, 2, 3), (330, 7, 3), (495, 8, 2), (220, 10, 1), (1000, 5, 3)],
 'D: 200 carriers + 440 xfer(e3,3) + 330 xfer(e7,2) + 495(e8,1) + 220(e10,1) + 600(e7,2)':
   [(200, 0, 8), (440, 3, 3), (330, 7, 2), (495, 8, 1), (220, 10, 1), (600, 7, 2)],
}
for kt in (4, 8):
    for nm, cl in scen.items():
        c = price(h, v, cst, cl, ks=2, kt=kt)
        R = sum(n for n, e, k in cl)
        print('kt=%d %s  R=%d: %s' % (kt, nm, R, ('%+.2f%%' % float((c / P111 - 1) * 100)) if c else 'wall'), flush=True)
