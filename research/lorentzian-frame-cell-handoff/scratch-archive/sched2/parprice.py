"""Parallel schedules: s_inv local invocations on L levels (several pairs active per level).  Same deficit
D = T(2Kv - s_inv cst) (checked by the mass identity), m = 1 + L a.  Price with whole hosting + banks."""
import sys, math
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
import pricer as P
from mpmath import mpf, mp
ref = mpf('0.001733427039589844')
tuned = {1: 1323, 2: 1342, 3: 79, 4: 44, 5: 102, 6: 11, 7: 19}
def price_par(local, v, h, R, L, sinv, K, idle, T=32, cst=63):
    a = h - 1; m = 1 + L * a; w = h
    slots = {}
    for c in idle: slots[c] = slots.get(c, 0) + 2 * v
    nres = R * sinv
    cap = sum(n * (c // w) for c, n in slots.items())
    nh = min(nres, cap); over = nres - nh
    nb = math.ceil(over * w / m); pad = nb * m - over * w
    W = 2 * K * v * T + nb * T
    q = mpf('0.0017')
    for _ in range(60):
        rem = P.host_greedy(slots, nh, w, q, m) if nh else dict((c, n) for c, n in slots.items())
        prof = {}
        for r, z in local.items(): prof[r] = prof.get(r, 0) + z * T * sinv
        for r, z in rem.items(): prof[r] = prof.get(r, 0) + z * T
        if pad: prof[pad] = prof.get(pad, 0) + T
        mass = sum(r * z for r, z in prof.items())
        D = m * W - mass
        q2 = P.root(prof, m, W, env=False)
        if q2 is None: return None, over, D
        if abs(q2 - q) < mpf(10) ** -25: break
        q = q2
    return q2, over, D
if __name__ == '__main__':
    K = 4; sinv = 9
    for L, idle_units in ((9, [7, 6, 5, 4, 3, 2]), (8, [6, 6, 5, 4, 2]), (8, [7, 6, 5, 3, 2]), (7, [6, 5, 4, 3, 1]), (7, [5, 5, 4, 3, 2]),
                          (6, [5, 4, 3, 2, 1]), (6, [4, 4, 3, 2, 2]), (5, [4, 3, 3, 1]), (5, [3, 3, 3, 2])):
        assert sum(idle_units) == 4 * L - sinv, (L, idle_units)
        c, over, D = price_par(tuned, 111, 8, 439, L, sinv, K, [7 * g for g in idle_units])
        print('L', L, 'idle', idle_units, 'banked', over, 'D/T', float(D) / 32, (mp.nstr(c, 8) + ' %+.2f%%' % float((c / ref - 1) * 100)) if c else 'no root')
