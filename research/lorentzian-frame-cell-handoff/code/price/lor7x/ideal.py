"""Ideal-word upper bound: every register one stop, helpers entrance rank e (width h-e), cst copies.  Exact pricer."""
import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
P = mp.mpf('0.001733427039589844')
def ideal(h, v, cst, R, e=0, ks=1, kt=1, kh=1):
    a = h - 1; loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    def split(tot, k):
        b, r = divmod(tot, k); return [b + 1]*r + [b]*(k - r)
    for p in split(a, ks): add(p, v)
    for p in split(a, kt): add(p, v)
    for p in split(h - e, kh): add(p, R)
    q, r = divmod(cst, a); add(a, q); add(r, 1 if r else 0)
    c, prof, d = price(loc, v, h, R, w=h - e)
    return c
for name, h, v, cst in (('E8', 8, 120, 72), ('P111', 8, 111, 72), ('I10', 10, 165, 90), ('I11', 11, 220, 110), ('I13', 13, 364, 156)):
    for e in (0, 1):
        best = None
        for R in (0, int(0.5*v), v, 2*v, 3*v, 4*v, 5*v):
            c = ideal(h, v, cst, R, e)
            if c is not None and (best is None or c > best[0]): best = (c, R)
        print(name, 'e=%d' % e, 'best ideal c', mp.nstr(best[0], 8) if best else None, 'R', best[1] if best else None, 'vs P111 %+.1f%%' % (float(best[0]/P - 1)*100) if best else '', flush=True)
