"""Break-even helper budgets for hypothetical E8 words (v = 111, cst 63, P111 data runs) whose helpers all have the
same run pattern; hosting whole + banks beyond the wall."""
import sys, math
sys.path.insert(0, '../k3')
import k3slots as KS
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
ref = KS.ref
data = {1: 317 + 10, 2: 209 + 92, 3: 10, 4: 3, 5: 92, 6: 10, 7: 9 + 9}   # x + y runs + 9 copies of rank 7
def price_R(pattern, R):
    loc = dict(data)
    for r in pattern: loc[r] = loc.get(r, 0) + R
    c, over = KS.price_slots(loc, 111, 8, R, 9, 4, P.idle_slots(4, 7))
    return float((c / ref - 1) * 100) if c else -999
pats = [(8,), (1, 7), (2, 6), (3, 5), (4, 4), (1, 1, 6), (1, 2, 5), (2, 2, 4), (1, 3, 4), (2, 3, 3), (1, 1, 1, 5), (1, 1, 2, 4), (1, 2, 2, 3),
        (2, 2, 2, 2), (1, 1, 1, 1, 4), (1, 1, 2, 2, 2), (1, 1, 1, 2, 3), (1, 1, 1, 1, 2, 2), (1, 1, 1, 1, 1, 1, 2), (1,) * 8]
print('control: P111-tuned helper histogram at R=439 ->', end=' ')
loc = dict(data); 
for r, z in {1: 996, 2: 1041, 3: 69, 4: 41, 5: 10, 6: 1, 7: 1}.items(): loc[r] = loc.get(r, 0) + z
c, o = KS.price_slots(loc, 111, 8, 439, 9, 4, P.idle_slots(4, 7)); print('%+.3f%%' % float((c / ref - 1) * 100))
for pt in pats:
    lo, hi = 100, 3000
    if price_R(pt, lo) < 0: print(pt, 'loses even at R=100'); continue
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if price_R(pt, mid) >= 0: lo = mid
        else: hi = mid
    print('pattern', pt, 'runs', len(pt), 'break-even R =', lo)
