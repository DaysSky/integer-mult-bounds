"""THE WORD4's TOOL-LEVEL LEVERS: the exact-DP hosting + the K=5 (at the TRUE hist!!)."""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, host_greedy, host, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')
P111 = mpf('0.001733052823330162099157')

def price_damped(local, v, h, R, K=4, T=32, w=None, use_dp=False, max_iter=200):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L; W_ = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, None, dict(error='hosting wall')
    q = mpf('0.0017'); q2 = None; conv = False
    for it in range(max_iter):
        rem = host(slots, nres, w, q, m) if use_dp else host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W_)
        if q2 is None: return None, prof, dict(error='no root')
        if abs(q2 - q) < mpf(10) ** -25: conv = True; break
        q = (q + q2) / 2
    return q2, prof, dict(converged=conv, iters=it + 1)

V, H, R = 121, 9, 472
h4 = {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2}
print('THE WORD4 (the TRUE hist %s):' % dict(sorted(h4.items())))
for tag, kw in [('the greedy K=4 (the built word!!)', {}),
                ('the EXACT-DP K=4 (the host-lever!!)', dict(use_dp=True)),
                ('the greedy K=5 (the SS1879!!)', dict(K=5)),
                ('the EXACT-DP K=5', dict(K=5, use_dp=True))]:
    c, prof, d = price_damped(h4, V, H, R, **kw)
    if c is None:
        print('  %-38s: NO PRICE (%s)' % (tag, d))
    else:
        print('  %-38s: c = %.9f (%+.2f%% vs frontier / %+.2f%% vs P111) [%s]' % (
            tag, float(c), float((c / FRONTIER - 1) * 100), float((c / P111 - 1) * 100), d))
