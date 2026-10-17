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
    lo, hi = 0.0, 8.0
    if val(h, x, lo, m) < REF[m]: return None
    for _ in range(30):
        mid = (lo + hi) / 2
        if val(h, x, mid, m) >= REF[m]: lo = mid
        else: hi = mid
    return lo
for x in (0.45, 0.5, 0.55, 0.6, 0.65, 0.7):
    print('h=11 x=%.2f tie rho abs %s rel %s' % (x, *['%.2f' % tie(11, x, m) if tie(11, x, m) is not None else '-' for m in ('abs', 'rel')]), flush=True)
