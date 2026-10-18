"""THE NATIVE-BUILD PAYOFF-MAP: the 121-model (CST 73!!) at the R-grid 240-472 —
the crossing-R + the native-assembly's target-band!!"""
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
    if nres > cap: return None, None, dict(error='hosting wall (cap %d < %d!!)' % (cap, nres))
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

def hist_D_121(R, CST, rho=9):
    V, H = 121, 9
    climb = H * R + 2 * V * (H - 1)
    hist = {1: int(round(0.262 * climb)), 2: int(round(0.571 * climb / 2.0)),
            4: int(round(0.048 * climb / 4.0)), 5: int(round(0.119 * climb / 5.0)),
            max(1, H - 1): rho}
    mass = sum(k * z for k, z in hist.items())
    dd = (H * R + CST + 2 * V * (H - 1)) - mass
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

print('THE NATIVE-PAYOFF-MAP (the 121-model, the CST 73, the D-hist!!):')
print('  (the word4 TRUE at R=472: -23.42% | the transplant-floor 451: -22.78% (the model!!))')
for R in (240, 260, 280, 300, 320, 340, 360, 380, 400, 420):
    h = hist_D_121(R, 73)
    c, prof, d = price_damped(h, 121, 9, R)
    if c is None:
        print('  R=%d: NO PRICE (%s)' % (R, d))
    else:
        print('  R=%d: c = %.9f (%+.2f%% vs frontier) [mass %d]' % (
            R, float(c), float((c / FRONTIER - 1) * 100), sum(k * z for k, z in h.items())))
