"""Break-even R for I_{11,1}/I_{13,1} shape models with bank overflow allowed (the old 'hosting wall' is soft)."""
import sys
sys.path.insert(0, '.')
import bankprice as B
from mpmath import mp
def split(t, k):
    b, r = divmod(t, k); return [b + 1] * r + [b] * (k - r)
def shape(h, v, cst, ks, kt, groups):
    a = h - 1; loc = {}
    def add(r, z):
        if z: loc[r] = loc.get(r, 0) + z
    for p in split(a, ks): add(p, v)
    for p in split(a, kt): add(p, v)
    widths = []
    for cnt, e, k in groups:
        for p in split(h - e, k): add(p, cnt)
        widths += [h - e] * cnt
    q, r = divmod(cst, a); add(a, q); add(r, 1 if r else 0)
    return loc, widths
def be(h, v, cst, ks, kt, kh, e, floor0=0):
    lo, hi = 0, 20 * v
    def ok(R):
        g = [(min(R, floor0), 0, kh), (max(0, R - floor0), e, kh)]
        loc, w = shape(h, v, cst, ks, kt, g)
        c, d = B.price(loc, v, h, w)
        return c is not None and c >= B.P111
    if not ok(0): return None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ok(mid): lo = mid
        else: hi = mid
    return lo
if __name__ == "__main__":
  for name, h, v, cst, fl in (('I11', 11, 220, 110, 426), ('I13', 13, 364, 156, 706)):
     for ks, kt, kh in ((3, 2, 3), (5, 2, 5), (4, 3, 4)):
         r0 = be(h, v, cst, ks, kt, kh, 0)
         r1 = be(h, v, cst, ks, kt, kh, 1, fl)
         print(name, 'stops s/t/h %d/%d/%d' % (ks, kt, kh), 'break-even R all frame-0:', r0, '(%.2fv)' % (r0 / v), '| floor frame-0 + rest entrance 1:', r1, '(%.2fv)' % (r1 / v) if r1 else '', flush=True)
