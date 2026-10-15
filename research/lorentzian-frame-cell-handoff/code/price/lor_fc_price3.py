"""Lorentzian frame-cell chain shapes where ALL helpers are carriers/extra branches (0-1-2-mid-9-[10]-11),
sources 1-2-mid-9-[10]-11, 660 deliveries (end 9-10-11), the rest die (9-11); targets 0-2-9-10 (or 0-9-10)."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(v, R, mids, ndel, tcell=True):
    h = {}
    def add(ch):
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + 1
    regs = [[1, 2] + mids + [9] for _ in range(v)] + [[0, 1, 2] + mids + [9] for _ in range(R)]
    for i, ch in enumerate(regs): add(ch + ([10, 11] if i < ndel else [11]))
    for _ in range(v): add([0, 2, 9, 10] if tcell else [0, 9, 10])
    h[10] = h.get(10, 0) + 11
    return h
for mids in ([5], [6], [4, 7]):
    for tc in (True, False):
        row = []
        for R in (540, 572, 600, 630):
            c = price(hist(220, R, mids, 660, tc), 220, 11, R)[0]
            row.append('R=%d %+.1f%%' % (R, float((c / P111t - 1) * 100)))
        print('mids', mids, 'target cell read' if tc else 'no target cell read', ' '.join(row), flush=True)
