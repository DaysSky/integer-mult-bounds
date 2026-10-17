# Break-even helper density rho* (helpers per line) vs P111 in the #620 helper model (est_model, abs/rel), grid (h, x).
import sys
from fractions import Fraction as Fr
sys.argv = ['x', '/home/user/integer-mult-bounds']
sys.path.insert(0, '../lor2/hub')
import est_model as E
CAL = {m: E.calibration('bit', m) for m in ('abs', 'rel')}
def val(h, x, rho, m):
    b = E.estimate('bit', h, Fr(x).limit_denominator(2000), Fr(rho).limit_denominator(1000), m)
    return b[1] * CAL[m] if b else 0
REF = {m: val(8, Fr(63, 111), Fr(439, 111), m) for m in ('abs', 'rel')}
def tie(h, x, m):
    lo, hi = 0.0, 12.0
    if val(h, x, lo, m) < REF[m]: return None
    for _ in range(28):
        mid = (lo + hi) / 2
        if val(h, x, mid, m) >= REF[m]: lo = mid
        else: hi = mid
    return lo
xs = (0.4, 0.5, 0.6, 0.65, 0.7, 0.75, 0.8)
print('rows h, cols x =', xs, ' entries rho* abs/rel ("-" = cannot tie even with 0 helpers)')
for h in (3, 4, 5, 6, 7, 8, 9, 10, 12):
    cells = []
    for x in xs:
        a, r = tie(h, x, 'abs'), tie(h, x, 'rel')
        cells.append('%s/%s' % ('%.2f' % a if a is not None else '-', '%.2f' % r if r is not None else '-'))
    print('h=%2d ' % h + '  '.join('%11s' % c for c in cells), flush=True)
