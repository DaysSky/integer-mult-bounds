"""Fewer stages with unhosted helper residuals on bank streams (exact width-m tiling; a bank stream adds m to m*W and
its residual coordinates are executed by the local helper climbs already in the local profile)."""
import sys, math
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf, mp
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def price_bank(local, v, h, R, K, nh=None, T=32):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a; w = h
    slots = {}
    for c in P.idle_slots(K, a): slots[c] = slots.get(c, 0) + 2 * v
    nres = R * L
    cap = sum(n * (c // w) for c, n in slots.items())
    nh = min(nres, cap) if nh is None else nh
    over = nres - nh
    nb = math.ceil(over * w / m); pad = nb * m - over * w      # bank streams per replica and padding
    W = 2 * K * v * T + nb * T
    q = mpf('0.0017')
    for _ in range(60):
        rem = P.host_greedy(slots, nh, w, q, m) if nh else {c: n for c, n in slots.items()}
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * L
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        if pad: prof[pad] = prof.get(pad, 0) + T
        q2 = P.root(prof, m, W, env=False)
        if q2 is None: return None, over, cap
        if abs(q2 - q) < mpf(10) ** -25: break
        q = q2
    return q2, over, cap
if __name__ == '__main__':
    c0 = price_bank(tuned, 111, 8, 439, 4)[0]
    print('control K=4 all hosted', mp.nstr(c0, 12), '%+.3f%%' % float((c0 / ref - 1) * 100))
    for K in (2, 3, 4, 5):
        for nhf in (None,):
            c, over, cap = price_bank(tuned, 111, 8, 439, K)
            print('K', K, 'stages', 2 * K + 1, 'banked residuals/replica', over, 'cap', cap,
                  (mp.nstr(c, 10) + ' %+.2f%%' % float((c / ref - 1) * 100)) if c else 'no root')
    # K=4: what if some helpers banked instead of hosted (sanity: hosting should help)
    for nh in (3951, 3000, 2000, 0):
        c, over, cap = price_bank(tuned, 111, 8, 439, 4, nh=nh)
        print('K=4 hosted', nh, 'banked', over, mp.nstr(c, 10), '%+.2f%%' % float((c / ref - 1) * 100))
