"""THE P111's NATIVE-MAP (ii19_p111map.py) — the OTHER frontier-class system!!
The P111: v=111, h=8, the CST-floor 63 (9 rets x dim-7!!), the deficit 10,272 (BIGGER than
the 121's 9,952!!!!) — the published R=439: -0.65%.  THE QUESTION: the crossing-R!!
"""
import sys
sys.path.insert(0, '/Users/dayssky/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, host_greedy, root
from mpmath import mp, mpf
mp.dps = 40
FRONTIER = mpf('0.001744386')
P111 = mpf('0.001733052823330162099157')

def price_damped(local, v, h, R, K=4, T=32, w=None, max_iter=200):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h if w is None else w
    slots = {}
    for c in idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L; W_ = 2 * K * v * T
    cap = sum(n * (c // w) for c, n in slots.items())
    if nres > cap: return None, None, dict(error='hosting wall (cap %d)' % cap)
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

def hist_D(v, h, R, CST, rho):
    climb = h * R + 2 * v * (h - 1)
    hist = {1: int(round(0.262 * climb)), 2: int(round(0.571 * climb / 2.0)),
            4: int(round(0.048 * climb / 4.0)), 5: int(round(0.119 * climb / 5.0)),
            max(1, h - 1): rho}
    mass = sum(k * z for k, z in hist.items())
    dd = (h * R + CST + 2 * v * (h - 1)) - mass
    guard = 0
    while dd != 0 and guard < 100000:
        guard += 1
        if dd > 0:
            hist[1] = hist.get(1, 0) + 1; dd -= 1
        else:
            k = max(z for z in hist if hist[z] > 0)
            hist[k] -= 1; dd += k
            if hist[k] == 0: del hist[k]
    return {k: int(z) for k, z in hist.items() if z}

V, H, CST, RHO = 111, 8, 63, 9
print('THE P111-MAP (the deficit 256*111 - 288*63 = %d!!):' % (256 * 111 - 288 * CST))
print('  (the published: R=439, the hist {1:1321, 2:1342, 3:80, 4:47, 5:102, 6:10, 7:18}: c = -0.65%)')
for R in (300, 330, 360, 390, 410, 420, 430, 439):
    h = hist_D(V, H, R, CST, RHO)
    c, prof, d = price_damped(h, V, H, R)
    if c is None:
        print('  R=%d: NO PRICE (%s)' % (R, d))
    else:
        print('  R=%d: c = %.9f (%+.2f%% vs frontier) [mass %d]' % (
            R, float(c), float((c / FRONTIER - 1) * 100), sum(k * z for k, z in h.items())))
# THE TRUE-HIST CONTROL (the published P111 hist!!):
h111 = {1: 1321, 2: 1342, 3: 80, 4: 47, 5: 102, 6: 10, 7: 18}
c, prof, d = price_damped(h111, V, H, 439)
print('  THE TRUE-HIST control: c = %s (%+.2f%%) [%s]' % (
    mp.nstr(c, 12), float((c / P111 - 1) * 100), d))
# THE P111 TRUE-HIST at the LOWER Rs (the native-shape bonus!!):
for R in (400, 420, 430):
    hh = dict(h111)
    # the mass fix: the climb-shrink: the R-part h*R shrinks -> the 1s absorb!!
    dd = H * (439 - R)
    hh[1] = hh[1] - dd
    c, prof, d = price_damped(hh, V, H, R)
    if c is None:
        print('  R=%d (the true-shape): NO PRICE (%s)' % (R, d))
    else:
        print('  R=%d (the true-shape): c = %.9f (%+.2f%% vs frontier) [%s]' % (
            R, float(c), float((c / FRONTIER - 1) * 100), d))
