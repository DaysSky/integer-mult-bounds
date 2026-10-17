"""Bank-overflow price of a gcheck word as a function of the stage count K (L = 2K+1), same model as
code/price/bankprice.py (which fixes K = 4)."""
import sys, bisect, math, json
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp
P111 = mp.mpf('0.001733427039589844')
T = 32
def price(local, v, h, widths, K):
    L = 2 * K + 1; a = h - 1; m = 1 + L * a
    res = sorted([w for w in widths for _ in range(L)], reverse=True)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2 * v))
    hosted = 0; banked = []
    for w in res:
        i = bisect.bisect_left(free, w)
        if i == len(free): banked.append(w); continue
        c = free.pop(i); hosted += 1
        if c > w: bisect.insort(free, c - w)
    over = sum(banked); nb = math.ceil(over / m); pad = nb * m - over
    rem = {}
    for c in free: rem[c] = rem.get(c, 0) + 1
    prof = {}
    for r_, z in local.items(): prof[int(r_)] = prof.get(int(r_), 0) + z * T * L
    for r_, z in rem.items(): prof[r_] = prof.get(r_, 0) + z * T
    if pad: prof[pad] = prof.get(pad, 0) + T
    W = 2 * K * v * T + nb * T
    return root(prof, m, W, env=False), nb
out = json.load(open(sys.argv[1]))
hist = out['local_histogram']; v, h, R = out['v'], out['h'], out['R']
for K in range(3, 13):
    c, nb = price(hist, v, h, [h] * R, K)
    print('K', K, 'c', mp.nstr(c, 10) if c else None, ('%+.2f%%' % float((c / P111 - 1) * 100)) if c else '', 'banks', nb, flush=True)
