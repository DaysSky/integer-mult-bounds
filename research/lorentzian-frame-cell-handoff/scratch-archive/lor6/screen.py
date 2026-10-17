# For each window h: the decoder cost per line x* at which a word with floor 1.93 v plus a middle of
# M v (M = 1.58: R420-quality; M = 2.05: P111-quality) ties P111 in the #620 helper model, and the line count v
# a unit needs to reach x* with c totals at rank h-1 (c = h: I_{n,1}-type; c = h+1: E8-type).  Compared with the
# best known Lorentzian systems.  MODEL (est_model, abs/rel piece scaling), not a bound.
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
def xstar(h, rho, m):
    lo, hi = 0.0, 1.2           # val decreases in x
    if val(h, lo, rho, m) < REF[m]: return None
    for _ in range(30):
        mid = (lo + hi) / 2
        if val(h, mid, rho, m) >= REF[m]: lo = mid
        else: hi = mid
    return lo
known = {8: (120, 'E8'), 9: (None, 'LP <= 136'), 10: (176, '165 I10 / 176 abstract'), 11: (231, '220 I11 / 231 abstract'),
         12: (299, '298 lattice'), 13: (364, 'I13'), 14: (455, 'I14'), 15: (560, 'I15'), 16: (680, 'I16')}
for M in (1.58, 2.05):
    rho = 1.93 + M
    print('middle %.2f v (rho = %.2f):' % (M, rho))
    for h in range(8, 17):
        row = []
        for m in ('abs', 'rel'):
            xs = xstar(h, rho, m)
            if xs is None: row.append('%s: x*<0' % m); continue
            vh, vh1 = h * (h - 1) / xs if xs > 0 else float('inf'), (h + 1) * (h - 1) / xs if xs > 0 else float('inf')
            row.append('%s: x*=%.3f v>=%.0f (c=h) %.0f (c=h+1)' % (m, xs, vh, vh1))
        print('  h=%2d | %s | known %s' % (h, ' | '.join(row), known[h][0] or '-'), known[h][1], flush=True)
