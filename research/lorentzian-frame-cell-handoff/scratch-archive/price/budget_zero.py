# Where does the I11 stop budget hit zero, and what R is compatible with minimal per-register split costs?
import sys; sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import budget as B
from mpmath import mpf
def bud(R):
    try: return -B.F_parts({10: 220 + 220 + 11, 11: R}, R) / B.unit
    except AttributeError: return mpf(-1)   # beyond the hosting wall
lo, hi = 880, 7900
while hi - lo > 1:
    mid = (lo + hi) // 2
    if bud(mid) > 0: lo = mid
    else: hi = mid
print('budget zero at R ~', lo, '(all single jumps)')
for per_helper, per_tgt in ((B.D(1, 10), B.D(1, 9)), (B.D(2, 9), B.D(1, 9)), (2 * B.D(1, 10), B.D(1, 9))):
    R = 426
    while bud(R) > per_helper * R + per_tgt * 220: R += 2
    print('min split per helper %.4f per target %.4f -> break-even R <= %d' % (per_helper, per_tgt, R))
