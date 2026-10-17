import sys
sys.path.insert(0, '/home/user/integer-mult-bounds/research/lorentzian-frame-cell-handoff/code/price')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def pc(h, v, R):
    c = price(h, v, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
def mk(paths):
    h = {}
    for ch, k in paths:
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    h[10] = h.get(10, 0) + 11
    return h
v = 220
for R in (440, 550, 660, 700, 740, 770, 800, 900):
    # shape A: sources 1->2->9->10->11, helpers 0->2->9->10->11 (one cell stop, one section stop), targets 0->2->10
    A = mk([([1, 2, 9, 10, 11], v), ([0, 2, 9, 10, 11], R), ([0, 2, 10], v)])
    # shape B: add a rank-5 hub stop for everything
    B = mk([([1, 2, 5, 9, 10, 11], v), ([0, 2, 5, 9, 10, 11], R), ([0, 2, 10], v)])
    # shape C: minimal: sources 1->10->11, helpers 0->9->10->11, targets 0->10
    C = mk([([1, 10, 11], v), ([0, 9, 10, 11], R), ([0, 10], v)])
    print('R', R, 'C(min) %+.2f%%' % pc(C, v, R), 'A(cell+section) %+.2f%%' % pc(A, v, R), 'B(+hub5) %+.2f%%' % pc(B, v, R))
