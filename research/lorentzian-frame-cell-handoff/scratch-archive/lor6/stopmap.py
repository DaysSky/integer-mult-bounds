"""Exact break-even R for I_{11,1} (v 220, h 11, cst 110) as a function of stop counts (even splits).
sources climb 1->11 in ks steps, targets 0->10 in kt steps, helpers 0->11 in kh steps; 11 copies rank 10."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
v, h, cst = 220, 11, 110
def split(total, k):
    b, r = divmod(total, k); return [b + 1]*r + [b]*(k - r)
def hist(R, ks, kt, kh):
    H = {}
    def add(r, z):
        if z: H[r] = H.get(r, 0) + z
    for p in split(10, ks): add(p, v)
    for p in split(10, kt): add(p, v)
    for p in split(11, kh): add(p, R)
    add(10, 11)
    assert sum(r*z for r, z in H.items()) == h*R + cst + 2*v*(h-1)
    return H
def be(ks, kt, kh):
    def ok(R):
        c, _, _ = pricer.price(hist(R, ks, kt, kh), v, h, R)
        return c is not None and c >= P111
    if not ok(300): return '<300'
    lo, hi = 300, 881
    if ok(880): return '>=880 (wall)'
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
print('ks kt kh -> break-even R')
for ks in (1, 2, 3):
    for kt in (2, 3, 4):
        print(ks, kt, [be(ks, kt, kh) for kh in (2, 3, 4, 5, 6)], flush=True)
