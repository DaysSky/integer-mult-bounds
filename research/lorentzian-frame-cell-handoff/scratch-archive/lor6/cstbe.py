import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
import mixcore as M
from mpmath import mp
def local(C, kc, H, e, kh, ks, kt, cst_units):
    Hs = {}
    def add(r, z):
        if z: Hs[r] = Hs.get(r, 0) + z
    for p in M.split(10, ks): add(p, M.v)
    for p in M.split(10, kt): add(p, M.v)
    for p in M.split(11, kc): add(p, C)
    for p in M.split(11 - e, kh): add(p, H)
    # copies: cst_units of rank-10 copies approximated as (cst_units // 10) copies of rank 10 + remainder
    q, r = divmod(cst_units, 10); add(10, q); add(r, 1 if r else 0)
    return Hs
for cst in (110, 121, 132, 143, 165):
    row = []
    for C, kc in ((440, 4), (440, 5)):
        for e in (6, 8):
            def ok(H):
                c = M.price_mixed(local(C, kc, H, e, 1, 3, 2, cst), [(11, C), (11 - e, H)])
                return c is not None and c >= M.P111
            if not ok(0): row.append('C%d/k%d e%d: fail' % (C, kc, e)); continue
            lo, hi = 0, 5000
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if ok(mid): lo = mid
                else: hi = mid
            row.append('k%d e%d: H<=%d' % (kc, e, lo))
    print('cst %d (x=%.3f):' % (cst, cst / 220), ' | '.join(row), flush=True)
