"""Mixed-width whole-residual hosting: n7 helpers of width 7 (entrance rank 1), the rest width 8.  Per replica, L
residuals per helper.  Exact small DP over fillings per slot type (counts of 7s and 8s per slot), minimising the
paid remainder cost f(r) = r((m/r)^q - 1) at the fixed point q (same root as code/price/pricer.py)."""
import sys, itertools
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf
def host(slots, n7, n8, q, m):
    # greedy by marginal saving over 'fill patterns' per slot: enumerate patterns (a7, a8) with 7a7 + 8a8 <= c
    f = lambda r: 0 if r == 0 else r * ((mpf(m) / r) ** q - 1)
    pats = {}
    for c in slots:
        pats[c] = sorted([(a7, a8) for a7 in range(c // 7 + 1) for a8 in range((c - 7 * a7) // 8 + 1)],
                         key=lambda p: f(c - 7 * p[0] - 8 * p[1]))
    # LP-ish greedy: assign best patterns to slots while residuals remain; simple heuristic: prefer patterns with
    # largest saving per residual used, respecting counts
    remaining = {7: n7, 8: n8}; rem = {}
    slotlist = []
    for c, n in slots.items(): slotlist += [c] * n
    # sort slots by capacity descending; fill each with the best feasible pattern given remaining counts
    for c in sorted(slotlist, reverse=True):
        best = None
        for a7, a8 in pats[c]:
            if a7 <= remaining[7] and a8 <= remaining[8]:
                sav = f(c) - f(c - 7 * a7 - 8 * a8)
                key = (sav / max(1, a7 + a8)) if (a7 + a8) else 0
                if best is None or sav > best[0]: best = (sav, a7, a8)
        _, a7, a8 = best
        remaining[7] -= a7; remaining[8] -= a8
        r = c - 7 * a7 - 8 * a8
        if r: rem[r] = rem.get(r, 0) + 1
    if remaining[7] or remaining[8]: return None, remaining
    return rem, None
def price(local, v, h, R, n7, K=4, T=32):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a
    slots = {}
    for c in P.idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    W = 2 * K * v * T; q = mpf('0.0017')
    for _ in range(40):
        rem, left = host(slots, n7 * L, (R - n7) * L, q, m)
        if rem is None: return None, left
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = P.root(prof, m, W)
        if abs(q2 - q) < mpf(10) ** -25: break
        q = q2
    return q2, rem
if __name__ == '__main__':
    import mpmath as mp
    ref = mp.mpf('0.001733427039589844')
    tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
    for n7 in (0, 50, 100, 200, 300, 439):
        loc = dict(tuned); loc[1] -= n7        # each width-7 helper loses its 0 -> line rank-1 block
        c, rem = price(loc, 111, 8, 439, n7)
        print('helpers with entrance rank 1: %3d ->' % n7, (mp.nstr(c, 10) + '  %+.2f%%' % float((c / ref - 1) * 100)) if c else rem)
