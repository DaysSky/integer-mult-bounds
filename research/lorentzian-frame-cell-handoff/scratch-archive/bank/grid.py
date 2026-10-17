import sys; sys.path.insert(0, '.')
from bebank import shape
import bankprice as B
from mpmath import mp
for R in (900, 1000, 1100, 1300, 1600, 2000, 3656):
    row = []
    for ks, kt, kh in ((3, 2, 3), (4, 3, 4), (5, 3, 5)):
        loc, w = shape(11, 220, 110, ks, kt, [(R, 0, kh)]); c0, _ = B.price(loc, 220, 11, w)
        loc, w = shape(11, 220, 110, ks, kt, [(min(R, 430), 0, kh), (max(0, R - 430), 1, kh)]); c1, _ = B.price(loc, 220, 11, w)
        row.append('%d/%d/%d: %+.1f%% | %+.1f%%' % (ks, kt, kh, float(c0 / B.P111 - 1) * 100, float(c1 / B.P111 - 1) * 100))
    print('R', R, ' ; '.join(row), flush=True)
