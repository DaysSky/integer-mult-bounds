"""Break-even shift when carriers copy at the cell (0 -> 2) instead of 0 -> 1 -> 2; one-level mids and two-level."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, mids, ndel, tchain, carrier_start):
    h = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + 1
    regs = [[1, 2] + mids + [9] for _ in range(v)] + [carrier_start + mids + [9] for _ in range(R)]
    for i, ch in enumerate(regs): add(ch + ([10, 11] if i < ndel else [11]))
    for _ in range(v): add(tchain)
    h[10] = h.get(10, 0) + 11
    return h
def be(mids, cs, tch):
    lo, hi = 400, 900
    def gain(R): return float(price(hist(220, R, mids, 660, tch, cs), 220, 11, R)[0] / P111t - 1)
    for _ in range(14):
        mid = (lo + hi) // 2
        if gain(mid) > 0: lo = mid
        else: hi = mid
    return lo
for mids in ([], [3], [5], [3, 8], [4, 6]):
    print('mids', mids, 'carriers 0-1-2: R_be', be(mids, [0, 1, 2], [0, 2, 9, 10]), '| carriers 0-2: R_be', be(mids, [0, 2], [0, 2, 9, 10]), flush=True)
