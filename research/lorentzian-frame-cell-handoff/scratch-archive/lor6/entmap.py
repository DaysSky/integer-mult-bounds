"""Break-even R for I_{11,1} when every helper enters at rank e (E1 double-read mechanism) and climbs e -> 11 in kh
steps; sources ks steps, targets kt steps; 11 copies of rank 10.  Residual width w = 11 - e (uniform)."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
v, h, cst = 220, 11, 110
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def hist(R, ks, kt, kh, e):
    H = {}
    def add(r, z):
        if z: H[r] = H.get(r, 0) + z
    for p in split(10, ks): add(p, v)
    for p in split(10, kt): add(p, v)
    for p in split(11 - e, kh): add(p, R)
    add(10, 11)
    return H
def be(ks, kt, kh, e):
    def ok(R):
        c, _, d = pricer.price(hist(R, ks, kt, kh, e), v, h, R, w=11 - e)
        return c is not None and c >= P111
    lo, hi = 300, 3000
    if not ok(lo): return '<300'
    # find upper failing point (hosting wall grows with smaller w)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
print('targets kt=3, sources ks=2; rows: entrance rank e; cols: helper stops after entrance kh=1..4')
for e in (0, 3, 5, 7, 8, 9):
    print('e=%d' % e, [be(2, 3, kh, e) if kh <= 11 - e else '-' for kh in (1, 2, 3, 4)], flush=True)
