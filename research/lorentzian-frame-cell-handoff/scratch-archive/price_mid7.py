import sys
sys.path.insert(0, '.')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist2(X, pre_s, pre_c, mid, tgt=(0, 8, 10)):
    h = {}; R = 440 + X
    def add(ch, k):
        assert all(b > a for a, b in zip(ch, ch[1:]))
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add(pre_s + mid + [8, 10, 11], 220); add(pre_c + mid + [8, 10, 11], 440 + X)
    add(list(tgt), 220); h[10] = h.get(10, 0) + 11
    return h, R
def pct(X, *a):
    h, R = hist2(X, *a)
    c = price(h, 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
for nm, ps, pc_, mid in (('cells,3,5', [1, 2], [0, 1, 2], [3, 5]), ('cells,3,5,7', [1, 2], [0, 1, 2], [3, 5, 7]), ('cells,3,7', [1, 2], [0, 1, 2], [3, 7]),
                         ('cells,5,7', [1, 2], [0, 1, 2], [5, 7]), ('cells,4,7', [1, 2], [0, 1, 2], [4, 7]), ('cells,3,6', [1, 2], [0, 1, 2], [3, 6]), ('cells,7', [1, 2], [0, 1, 2], [7]),
                         ('nocell,3,5,7', [1], [0, 1], [3, 5, 7]), ('nocell,3,7', [1], [0, 1], [3, 7]), ('nocell,3,5', [1], [0, 1], [3, 5])):
    row = ['X=%d %+.2f%%' % (X, pct(X, ps, pc_, mid)) for X in (0, 50, 100, 150)]
    be = next((X for X in range(0, 400, 5) if pct(X, ps, pc_, mid) < 0), None)
    print('%-13s' % nm, ' | '.join(row), ' break-even X ~', be, flush=True)
