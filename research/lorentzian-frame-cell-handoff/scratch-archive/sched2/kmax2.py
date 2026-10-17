"""Rigorous-in-model upper bound per K: any schedule has K-1 pre-stretches (sorted lengths <= 2,4,..,2K-2; each >= 1),
K-1 post-stretches (same), and >= 1 further stretch carrying the rest.  More stretches only lower hosting, and
splitting the rest into more parts makes the multiset less unequal; so the max over (pre, post, one rest stretch)
bounds every layout.  Price with whole hosting + banks."""
import sys, itertools
sys.path.insert(0, '../k3')
import k3slots as KS
def pr(K, sl):
    s = 2 * K + 1
    c, over = KS.price_slots(KS.tuned, 111, 8, 439, s, K, [7 * g for g in sl])
    return float((c / KS.ref - 1) * 100) if c else -999
def vecs(K):
    bounds = list(range(2, 2 * K - 1, 2))
    def rec(i, lo):
        if i == len(bounds): yield (); return
        for x in range(lo, bounds[i] + 1):
            for rest in rec(i + 1, x): yield (x,) + rest
    return list(rec(0, 1))
for K in (3, 5, 6, 7):
    s = 2 * K + 1; tot = (K - 1) * s
    V = vecs(K); best = None; cache = {}
    for a in V:
        for b in V:
            if b < a: continue
            rest = tot - sum(a) - sum(b)
            if rest < 1: continue
            sl = tuple(sorted(a + b + (rest,), reverse=True))
            if sl in cache: continue
            cache[sl] = pr(K, list(sl))
            if best is None or cache[sl] > best[0]: best = (cache[sl], sl)
    print('K', K, 'upper bound %+.3f%%' % best[0], best[1], 'checked', len(cache), flush=True)
