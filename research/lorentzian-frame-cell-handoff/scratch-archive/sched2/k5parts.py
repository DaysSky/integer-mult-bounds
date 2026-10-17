import sys
sys.path.insert(0, '../k3')
import k3slots as KS
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
def parts(n, k, mx):
    if k == 0:
        if n == 0: yield ()
        return
    for x in range(min(n - (k - 1), mx), 0, -1):
        for rest in parts(n - x, k - 1, x): yield (x,) + rest
K = 5; s = 11
b5 = P.idle_slots(5, 7)
c, o = KS.price_slots(KS.tuned, 111, 8, 439, s, K, b5)
print('B_5 split', sorted(b5, reverse=True), '%+.3f%%' % float((c / KS.ref - 1) * 100))
for N in (12, 13):
    rows = []
    for pt in parts(44, N, 9):
        sl = [7 * g for g in pt]
        c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, sl)
        rows.append((float((c / KS.ref - 1) * 100) if c else -999, sl, over))
    rows.sort(reverse=True)
    print('K=5 stretches', N, 'best:', ['%+.3f%% %s banked %d' % r for r in rows[:3]])
