import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-integer-mult-bounds/be920f64-2d39-5bb5-8de0-871e6c23a743/scratchpad/lor6')
from i13ent import price, P111
from mpmath import mp
# minimum v at window h for an R = rho*v word with all helpers at entrance e (k stops), sources ks, targets kt, cst = h*(h-1) or given
for h, cst in ((9, 72), (9, 64), (9, 56), (10, 90), (10, 81)):
    for rho in (3.0, 3.5, 4.0):
        for e, k in ((0, 4), (1, 4), (1, 3)):
            for ks, kt in ((5, 2), (3, 3)):
                vmin = None
                for v in range(60, 260):
                    c = price(h, v, cst, int(rho*v), k, e, 0, 1, 1, ks, kt)
                    if c is not None and c >= P111: vmin = v; break
                print('h=%d cst=%d rho=%.1f e=%d k=%d ks=%d kt=%d: v_min=%s' % (h, cst, rho, e, k, ks, kt, vmin), flush=True)
