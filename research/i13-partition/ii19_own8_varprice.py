"""THE WORD4 VARIANT PRICE-TEST: the [253]x2 removal (the hist-shape hist[6]-6/hist[8]+6!!)"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')

def price_damped(local, v, h, R, K=4, T=32, w=None, max_iter=200):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L; W_ = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, None, dict(error='hosting wall')
    q = mpf('0.0017'); q2 = None; conv = False
    for it in range(max_iter):
        rem = host_greedy(slots, nres, w, q, m)
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        q2 = root(prof, m, W_)
        if q2 is None: return None, prof, dict(error='no root')
        if abs(q2 - q) < mpf(10) ** -25: conv = True; break
        q = (q + q2) / 2
    return q2, prof, dict(converged=conv, iters=it + 1)

V, H, R = 121, 9, 472
h4 = {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2}      # the word4 TRUE hist
hv = dict(h4); hv[6] -= 1; hv[8] += 6; del hv[6]                  # the [253]x2 removed
for nm, hst in [('the word4 (the built!!)', h4), ('the variant (the 253s removed!!)', hv)]:
    c, prof, d = price_damped(hst, V, H, R)
    print('%-34s: c = %.9f (%+.2f%% vs frontier) [%s]' % (
        nm, float(c), float((c / FRONTIER - 1) * 100), d))
