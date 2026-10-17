"""Exact nine-stage price with mixed-width best-fit hosting and bank overflow (banks.py model: an unhosted residual goes
to a width-m bank stream; a bank adds m to m*W per replica; its residual coordinates are executed by the local helper
climbs already in the local profile; leftover bank capacity is one padding child).
price(local_hist, v, h, widths, nhost=None): widths = residual width of every helper (L residuals each)."""
import sys, bisect, math, json, gzip
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import idle_slots, root
from mpmath import mp, mpf
P111 = mp.mpf('0.001733427039589844')
K, T = 4, 32; L = 2 * K + 1
def price(local, v, h, widths, nhost=None):
    a = h - 1; m = 1 + L * a
    res = sorted([w for w in widths for _ in range(L)], reverse=True)
    free = sorted(c for c in idle_slots(K, a) for _ in range(2 * v))
    hosted = 0; banked = []
    for w in res:
        if nhost is not None and hosted >= nhost: banked.append(w); continue
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
    return root(prof, m, W, env=False), dict(hosted=hosted, banked=len(banked), banks=nb)
if __name__ == '__main__':
    out = json.load(open(sys.argv[1]))          # gcheck JSON output
    hist = out['local_histogram']; v, h, R = out['v'], out['h'], out['R']
    widths = [h] * R
    c, d = price(hist, v, h, widths)
    print('R', R, 'hist', hist, 'c', mp.nstr(c, 12) if c else None, ('%+.2f%%' % float((c / P111 - 1) * 100)) if c else '', d)
