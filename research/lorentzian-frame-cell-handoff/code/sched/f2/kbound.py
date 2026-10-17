"""Rigorous upper bound on the price of ANY schedule with K pairs (2K + 1 locals; P111-tuned local word):
 (a) touch-time theorem: K-1 pre-stretches with sorted lengths <= (2, 4, .., 2K-2), K-1 post-stretches likewise, each
     >= 1 stage; the remaining idle units sit in middle stretches;
 (b) combining two stretches never lowers the price (more hosting by floor superadditivity; one remainder child of
     the summed rank is cheaper than two since f is concave with f(0) = 0), so all middle parts may be merged;
 (c) hosting is relaxed upward: every slot hosts floor(c/8) residuals (even beyond the R*s that exist) and bank
     overflow is free (no pad, W not enlarged... banks add W which only helps; we add it).
Enumerate every (pre, post) pair and take the max."""
import sys, math
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
T, v, R = 32, 111, 439
def ub(K, stretches):
    """pressure form with the exact deficit D = T(2Kv - s cst): sum_children z r((m/r)^q - 1) = D"""
    s = 2 * K + 1; m = 1 + 7 * s
    D = T * (2 * K * v - s * 63)
    prof = {r: z * T * s for r, z in tuned.items()}
    for g in stretches:
        c = 7 * g; rem = c - 8 * (c // 8)
        if rem: prof[rem] = prof.get(rem, 0) + 2 * v * T
    def F(q): return sum(mpf(z) * r * ((mpf(m) / r) ** q - 1) for r, z in prof.items()) - D
    lo, hi = mpf(0), mpf('0.05')
    for _ in range(120):
        mid = (lo + hi) / 2
        if F(mid) > 0: hi = mid
        else: lo = mid
    return lo
def vecs(K):
    bounds = list(range(2, 2 * K - 1, 2))
    def rec(i, lo):
        if i == len(bounds): yield (); return
        for x in range(lo, bounds[i] + 1):
            for rest in rec(i + 1, x): yield (x,) + rest
    return list(rec(0, 1))
for K in [int(x) for x in sys.argv[1:]]:
    s = 2 * K + 1; tot = (K - 1) * s
    V = vecs(K); best = None; seen = set()
    for a in V:
        for b in V:
            if b < a: continue
            rest = tot - sum(a) - sum(b)
            if rest < 1: continue
            sl = tuple(sorted(a + b + (rest,), reverse=True))
            if sl in seen: continue
            seen.add(sl)
            q = ub(K, sl)
            if q is not None and (best is None or q > best[0]): best = (q, sl)
    print('K', K, 'rigorous upper bound %+.3f%%' % float((best[0] / ref - 1) * 100), best[1], 'multisets', len(seen), flush=True)
