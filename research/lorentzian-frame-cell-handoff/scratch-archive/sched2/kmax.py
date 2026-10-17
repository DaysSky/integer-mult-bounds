"""Upper bound on any schedule's price for each K under the touch-time theorem: pre <= (2,4,..,2K-2), post <= same,
the rest of the idle in ONE middle stretch (the most favourable case), plus every pre/post at its max.  Also the
alternative of shortening pre/post.  Whole hosting + banks."""
import sys
sys.path.insert(0, '../k3')
import k3slots as KS
def pr(K, sl):
    s = 2 * K + 1
    c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, [7 * g for g in sl])
    return float((c / KS.ref - 1) * 100) if c else -999
for K in (2, 3, 4, 5, 6, 7, 8):
    s = 2 * K + 1; tot = (K - 1) * s
    pre = list(range(2, 2 * K - 1, 2)); mid = tot - 2 * sum(pre)
    sl = pre + pre + [mid]
    print('K', K, 'stages', s, 'best conceivable', sorted(sl, reverse=True), '%+.3f%%' % pr(K, sl))
