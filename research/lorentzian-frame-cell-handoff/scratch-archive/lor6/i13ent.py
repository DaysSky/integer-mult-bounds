"""Break-even R for I_{n,1}-type units with entrance-ranked helpers (generic h, v, cst).  Sources ks, targets kt stops;
C frame-0 helpers (kc stops) + H entrance-ranked (rank e, kh stops).  Best-fit mixed hosting, exact root."""
import sys, bisect
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
K, T = 4, 32; L = 2*K + 1
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def price(h, v, cst, C, kc, eC, H, e, kh, ks=2, kt=3):
    a = h - 1; m = 1 + L*a; W = 2*K*v*T
    loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in split(h - 1, ks): add(p, v)
    for p in split(h - 1, kt): add(p, v)
    for p in split(h - eC, kc): add(p, C)
    for p in split(h - e, kh): add(p, H)
    q, r = divmod(cst, h - 1); add(h - 1, q); add(r, 1 if r else 0)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2*v))
    res = sorted([h - eC]*(C*L) + [h - e]*(H*L), reverse=True)
    for w in res:
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
def be(h, v, cst, kc, eC):
    lo, hi = 0, 8000
    def ok(R):
        c = price(h, v, cst, R, kc, eC, 0, 0, 1); return c is not None and c >= P111
    if not ok(1): return 0
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
if __name__ == "__main__":
  pass
systems = [] if __name__ != "__main__" else [('I11', 11, 220, 110), ('I12', 12, 286, 143), ('I13', 13, 364, 156), ('I15', 15, 560, 210)]
for name, h, v, cst in systems:
    row = []
    for eC in (0, 1, 2, 3):
        for kc in (4, 5):
            row.append('e%d/k%d:%d' % (eC, kc, be(h, v, cst, kc, eC)))
    print('%s (v=%d, x=%.3f): break-even R  %s  | 3.5v=%d' % (name, v, cst / v, ' '.join(row), int(3.5 * v)), flush=True)
