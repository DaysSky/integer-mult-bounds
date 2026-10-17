"""Punctured E8 (v=111, 9 rank-7 totals) 4-section chains with W extra (wasted) helpers, each wasted helper paying the
same chain as a delivered copy but ending at FULL from its last node (no t-perp stop): break-even vs P111-tuned."""
from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
v, h = 111, 8
def loc(nodes, waste, copystop=True, tot_fresh=9):
    L = {}
    def add(ch, n):
        for a, b in zip(ch, ch[1:]): L[b - a] = L.get(b - a, 0) + n
    pre = [0, 1, 2] if copystop else [0, 2]
    add([1, 2] + nodes + [6, 8], v)
    add(pre + nodes + [6, 7, 8], 3 * v)
    add(pre + nodes + [8], waste)            # wasted middle helper: picks up, mixes, dies at FULL
    add([0, 8], tot_fresh)
    add([0, 6, 7], v)
    L[7] = L.get(7, 0) + 9
    return L
for nodes in ([3], [4], [3, 5], [4, 5]):
    row = []
    for waste in (0, 30, 60, 90, 102):
        R = 3 * v + 9 + waste
        c = price(loc(nodes, waste), v, h, R)[0]
        row.append('R=%d %+.2f%%' % (R, float((c / P - 1) * 100)))
    print('middle', nodes, ' | '.join(row), flush=True)
