import sys
from fractions import Fraction as Fr
from math import comb
sys.argv = ['x', '/home/user/integer-mult-bounds']
sys.path.insert(0, '../lor2/hub')
import est_model as E
CAL = {m: E.calibration('bit', m) for m in ('abs', 'rel')}
def val(h, x, rho, m):
    b = E.estimate('bit', h, Fr(x).limit_denominator(2000), Fr(rho).limit_denominator(1000), m)
    return b[1] * CAL[m] if b else 0
REF = {m: val(8, Fr(63, 111), Fr(439, 111), m) for m in ('abs', 'rel')}
def xstar(h, rho, m):
    lo, hi = 0.0, 1.2
    if val(h, lo, rho, m) < REF[m]: return None
    for _ in range(30):
        mid = (lo + hi) / 2
        if val(h, mid, rho, m) >= REF[m]: lo = mid
        else: hi = mid
    return lo
rho = 1.93 + 1.58
for h in range(9, 23):
    ceil = comb(h + 1, 3) + (h - 1 if h < 10 else 0 if h == 10 else 1)
    xi = 6 / (h + 1) if h % 2 else None      # I_{h,1}, odd h: c = h totals at rank h-1
    row = []
    for m in ('abs', 'rel'):
        xs = xstar(h, rho, m)
        need = h * (h - 1) / xs if xs else float('inf')
        row.append('%s x*=%.3f need v>=%.0f' % (m, xs if xs else -1, need))
    print('h=%2d ceiling %5d | %s | I_{h,1} x=%s' % (h, ceil, ' | '.join(row), '%.3f' % xi if xi else '-'), flush=True)
