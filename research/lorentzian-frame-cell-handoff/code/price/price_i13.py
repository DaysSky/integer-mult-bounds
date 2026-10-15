"""Break-even R vs P111-tuned for I_{n,1} frame-cell chain shapes (v lines, h = n): one-level rank m, two-level.
I_{13,1}: v = 78 + 286 = 364, h = 13; I_{10,1}: v = 45 + 120 = 165, h = 10; I_{11,1} control."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, h, R, mids, ndel):
    hh = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): hh[b - a] = hh.get(b - a, 0) + 1
    regs = [[1, 2] + mids + [h - 2] for _ in range(v)] + [[0, 1, 2] + mids + [h - 2] for _ in range(R)]
    for i, ch in enumerate(regs): add(ch + ([h - 1, h] if i < ndel else [h]))
    for _ in range(v): add([0, 2, h - 2, h - 1])
    hh[h - 1] = hh.get(h - 1, 0) + h
    return hh
def be(v, h, mids):
    lo, hi = int(1.0 * v), int(5 * v)
    def gain(R):
        c = price(hist(v, h, R, mids, 3 * v), v, h, R)
        return None if c is None or c[0] is None else float(c[0] / P111t - 1)
    g_lo = gain(lo)
    if g_lo is None or g_lo < 0: return None
    for _ in range(16):
        mid = (lo + hi) // 2
        gm = gain(mid)
        if gm is not None and gm > 0: lo = mid
        else: hi = mid
    return lo
for name, v, h in (('I11,1', 220, 11), ('I10,1', 165, 10), ('I13,1', 364, 13)):
    for mids in ([], [3], [h // 2], [3, h - 3]):
        r = be(v, h, mids)
        print(name, 'mids', mids, 'break-even R', r, '= %.2f v' % (r / v) if r else '', flush=True)
