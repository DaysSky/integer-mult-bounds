"""T_11 (the 165 T lines of I_{11,1}, h = 11, point-total decoder) priced with rank-7 triangle-node shapes:
3 delivered pieces per target (495 = 165 sources + 330 helpers), in-chain node read, extras X as full pieces.
Chains: pieces pre + mid + [7, 10, 11] (node = triangle perp, rank 7 inside T_11), targets [0, 7, 10].
usage: run from code/price"""
import sys
sys.path.insert(0, '.')
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
v = 165
def pct(X, pre_s, pre_c, mid, node=7):
    h = {}; R = 2 * v + X
    def add(ch, k):
        assert all(b > a for a, b in zip(ch, ch[1:])), ch
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    add(pre_s + mid + [node, 10, 11], v); add(pre_c + mid + [node, 10, 11], 2 * v + X)
    add([0, node, 10], v); h[10] = h.get(10, 0) + 11
    c = price(h, v, 11, R)[0]
    return R, float((c / P111t - 1) * 100) if c else None
for nm, ps, pc_, mid in (('cells,3,5', [1, 2], [0, 1, 2], [3, 5]), ('cells,3', [1, 2], [0, 1, 2], [3]), ('cells,5', [1, 2], [0, 1, 2], [5]),
                         ('nocell,3,5', [1], [0, 1], [3, 5]), ('cells,3,5,6', [1, 2], [0, 1, 2], [3, 5, 6])):
    row = []
    for X in (0, 50, 100, 150):
        R, p = pct(X, ps, pc_, mid); row.append('X=%d R=%d %+.2f%%' % (X, R, p))
    be = next((X for X in range(0, 600, 5) if pct(X, ps, pc_, mid)[1] < 0), None)
    print('%-12s' % nm, ' | '.join(row), ' break-even X ~', be, flush=True)
