import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/sched')
from genprice import price
import mpmath as mp
ref = mp.mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def parts(n, k, mx):
    if k == 0:
        if n == 0: yield ()
        return
    for x in range(min(n - (k - 1), mx), 0, -1):
        for rest in parts(n - x, k - 1, x): yield (x,) + rest
rows = []
for pt in parts(27, 9, 7):
    sl = [7 * g for g in pt]
    c, d = price(tuned, 111, 8, 439, 9, 4, sl)
    rows.append((float((c / ref - 1) * 100) if c else -999, sl))
rows.sort(reverse=True)
for r in rows[:15]: print('%+.3f%%' % r[0], r[1])
print('B_K', [r for r in rows if sorted(r[1]) == sorted([42, 14, 7, 28, 28, 7, 14, 42, 7])])
