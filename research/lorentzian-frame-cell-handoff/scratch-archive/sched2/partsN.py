import sys
sys.path.insert(0, '../k3')
import k3slots as KS
def parts(n, k, mx):
    if k == 0:
        if n == 0: yield ()
        return
    for x in range(min(n - (k - 1), mx), 0, -1):
        for rest in parts(n - x, k - 1, x): yield (x,) + rest
for N in (9, 10, 11):
    rows = []
    for pt in parts(27, N, 7):
        sl = [7 * g for g in pt]
        c, over = KS.price_slots(KS.tuned, 111, 8, 439, 9, 4, sl)
        rows.append((float((c / KS.ref - 1) * 100) if c else -999, sl, over))
    rows.sort(reverse=True)
    print('stretches', N, 'best:', ['%+.3f%% %s banked %d' % r for r in rows[:3]])
