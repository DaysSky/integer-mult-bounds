"""Rank-8 frame sections (F-perp, F a rank-3 frame through t; users = lines of F), 4 per target (1 in-chain at rank 8,
3 delivered), distinct parts per delivered user, in-chain users read combinations -> every cell-stage register is a
delivered piece (660 deliveries), no copies.  R = 440 ideal; extra dead empties [0,9,11] beyond.  Pieces climb
cell -> middle stops -> F-perp (8) -> t-perp (10) -> 11.  Targets 0 -> F0-perp (8) -> t-perp."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(R, pre_s, pre_c, mid, tgt=(0, 8, 10)):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add(pre_s + mid + [8, 10, 11], 220); add(pre_c + mid + [8, 10, 11], 440)
    add([0, 9, 11], R - 440); add(list(tgt), 220)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(R, *a, **k):
    c = price(hist(R, *a, **k), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for name, ps, pc_, mid in (('cells, 3, 5', [1, 2], [0, 1, 2], [3, 5]), ('cells, 5', [1, 2], [0, 1, 2], [5]), ('cells, 3', [1, 2], [0, 1, 2], [3]),
                           ('no cell, 3, 5', [1], [0, 1], [3, 5]), ('no cell, 5', [1], [0, 1], [5]), ('no cell, 3', [1], [0, 1], [3])):
    row = []
    for R in (440, 500, 550, 600, 650, 700):
        row.append('R=%d %+.2f%%' % (R, pct(R, ps, pc_, mid)))
    be = next((R - 2 for R in range(440, 880, 4) if (pct(R, ps, pc_, mid) or -1) < 0), None)
    print('%-15s' % name, ' | '.join(row), ' break-even ~', be, flush=True)
