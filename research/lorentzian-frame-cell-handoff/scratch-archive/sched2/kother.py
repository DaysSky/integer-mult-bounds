"""Best conceivable layouts under the touch-time bounds for K = 3, 5 (pre <= 2,4,..; post <= 2,4,..; middle fills the
rest), priced with whole hosting + banks; compare with B_K."""
import sys, itertools
sys.path.insert(0, '../k3')
import k3slots as KS
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
def pr(K, sl):
    s = 2 * K + 1
    c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, [7 * g for g in sl])
    return float((c / KS.ref - 1) * 100) if c else -999
for K in (3, 4, 5):
    s = 2 * K + 1; tot = (K - 1) * s
    bk = [g // 7 for g in P.idle_slots(K, 7)]
    print('K', K, 'B_K', sorted(bk, reverse=True), '%+.3f%%' % pr(K, bk))
    pre = list(range(2, 2 * K - 1, 2)); post = list(pre)
    mid = tot - sum(pre) - sum(post)
    for nm in range(1, K):
        # split mid into nm parts as unequally as possible
        parts = [mid - (nm - 1)] + [1] * (nm - 1)
        sl = pre + post + parts
        print('   middle in %d stretch(es):' % nm, sorted(sl, reverse=True), 'stretches', len(sl), '%+.3f%%' % pr(K, sl))
