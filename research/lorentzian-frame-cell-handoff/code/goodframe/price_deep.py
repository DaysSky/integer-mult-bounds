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
for R in (440, 500, 550, 600, 650, 700):
    row = []
    for mid in ([5], [3, 5], [3, 6], [4, 7], [3, 5, 7]):
        H = mk([([1, 2] + mid + [9, 10, 11], v), ([0, 2] + mid + [9, 10, 11], R), ([0, 2, 9, 10], v)])
        p = pc(H, v, R); row.append('%s:%s' % ('-'.join(map(str, mid)), 'wall' if p is None else '%+.1f%%' % p))
    print('R', R, ' '.join(row))
