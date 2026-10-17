"""Rigorous upper bound per K, with the stretch cap from the interval lemma (any stretch has <= 2K-2 stages: a
non-initial stretch of g stages leaves d >= 1 so g <= 2(K-1); an initial one is a pre-stretch, <= 2K-2 by the
touch-time theorem).  Middle idle is merged into as few parts as the cap allows (merging never lowers the price).
Hosting relaxed upward (every slot fully hosted), exact deficit, pressure form."""
import sys
sys.argv = sys.argv[:1] + sys.argv[1:]
exec(open('kbound.py').read().split('def vecs(K):')[0])
def vecs(K):
    bounds = list(range(2, 2 * K - 1, 2))
    def rec(i, lo):
        if i == len(bounds): yield (); return
        for x in range(lo, bounds[i] + 1):
            for rest in rec(i + 1, x): yield (x,) + rest
    return list(rec(0, 1))
for K in [int(x) for x in sys.argv[1:]]:
    s = 2 * K + 1; tot = (K - 1) * s; cap = 2 * K - 2
    V = vecs(K); best = None; seen = set()
    for a in V:
        for b in V:
            if b < a: continue
            rest = tot - sum(a) - sum(b)
            if rest < 1: continue
            mid = [cap] * (rest // cap) + ([rest % cap] if rest % cap else [])
            sl = tuple(sorted(a + b + tuple(mid), reverse=True))
            if sl in seen: continue
            seen.add(sl)
            q = ub(K, sl)
            if best is None or q > best[0]: best = (q, sl)
    print('K', K, 'rigorous capped bound %+.3f%%' % float((best[0] / ref - 1) * 100), best[1], 'multisets', len(seen), flush=True)
