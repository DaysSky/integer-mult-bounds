"""THE HIST-SHAPE LEVER SCAN: at the FIXED (v=121, h=9, R=472, CST=73, mass=6257!!) —
which climb-distribution {n_k} MAXIMIZES c?!  (the TRUE word4 vs the D-model vs the
extremes!!) -> THE FRAME-RESTRUCTURING LEVER'S MAGNITUDE!!"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')
V, H, R = 121, 9, 472
MASS = 6257

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

def show(nm, hist):
    mass = sum(k * z for k, z in hist.items())
    assert mass == MASS, '%s: the mass %d != %d!!' % (nm, mass, MASS)
    c, prof, d = price_damped(hist, V, H, R)
    if c is None:
        print('  %-34s: NO PRICE (%s) | %s' % (nm, d, dict(sorted(hist.items()))))
    else:
        print('  %-34s: c = %.9f (%+.2f%%) [%s] | %s' % (
            nm, float(c), float((c / FRONTIER - 1) * 100), d.get('converged'), dict(sorted(hist.items()))))

print('THE HIST-SHAPE SCAN (the FIXED mass %d!!):' % MASS)
show('THE WORD4 TRUE (the built!!)', {1: 1100, 2: 1710, 3: 331, 4: 144, 6: 1, 8: 18, 9: 2})
# the extremes:
show('ALL-1s (the finest chains!!)', {1: MASS})
show('ALL-2s', {2: MASS // 2, 1: MASS % 2})
show('ALL-3s', {3: MASS // 3, 1: MASS % 3})
show('ALL-5s', {5: MASS // 5, 1: MASS % 5})
show('ALL-8s (the ret-frame shape!!)', {8: MASS // 8, 1: MASS % 8})
show('ALL-9s (the direct climbs!!)', {9: MASS // 9, 1: MASS % 9})
# the interpolations: the TRUE with the mid-k -> 1s:
h2 = {1: 1100 + 3 * 331, 2: 1710, 4: 144, 6: 1, 8: 18, 9: 2}
show('the TRUE-3s->1s', h2)
h3 = {1: 1100 + 3 * 331 + 4 * 144, 2: 1710 + 2 * 144, 6: 1, 8: 18, 9: 2}
show('the TRUE-3/4s->1/2s', h3)
h4 = {1: 1100 + 331 * 3 + 144 * 4 + 1710, 6: 1, 8: 18, 9: 2}
show('the TRUE-all->1s (the 2s too!!)', h4)
h5 = {1: 1100, 2: 1710 + 3 * 331 // 3, 4: 144, 6: 1, 8: 18, 9: 2}
show('the TRUE-3s->2s', {1: 1100, 2: 1710 + (3 * 331) // 2, 3: (3 * 331) % 2, 4: 144, 6: 1, 8: 18, 9: 2})
# the TRUE with the low-k -> HIGH-k (the reverse direction!!):
h6 = {1: 1100 - 500, 2: 1710, 3: 331, 4: 144, 6: 1, 7: 0, 8: 18 + (500 * 1) // 8, 9: 2 + (500 * 1) % 8}
show('the TRUE-1s->8s (the coarse!!)', {k: z for k, z in h6.items() if z})
