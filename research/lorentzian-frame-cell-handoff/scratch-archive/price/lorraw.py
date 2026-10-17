"""I_{11,1} 4-section, raw middle (copies line -> node -> section -> t-perp -> FULL), in-chain section + node reads
(targets 0 -> node -> section -> t-perp), 11 totals rank 10 on fresh helpers (0 -> 11).  Zero-waste R = 2v + 11;
wasted helpers 0 -> 1 -> node -> 11.  Break-even vs P111-tuned."""
from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
v, h = 220, 11
def loc(node, tnode, waste, tot_fresh=11):
    L = {}
    def add(ch, n):
        for a, b in zip(ch, ch[1:]): L[b - a] = L.get(b - a, 0) + n
    add([1, node, 9, 10, 11], v)
    add([0, 1, node, 9, 10, 11], 2 * v)
    add([0, 1, node, 11], waste)
    add([0, 11], tot_fresh)
    add([0, tnode, 9, 10], v)
    L[10] = L.get(10, 0) + 11
    return L
for node in (5, 6, 7, 8):
    for tnode in (node,):
        R0 = 2 * v + 11
        f = lambda w: price(loc(node, tnode, w), v, h, R0 + w)[0]
        c0 = f(0); lo, hi = 0, 4 * v - R0
        if f(hi) >= P: be = 'beats at the wall R=%d' % (R0 + hi)
        else:
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if f(mid) >= P: lo = mid
                else: hi = mid
            be = 'beats P111t iff R <= %d' % (R0 + lo)
        print('node rank %d (target in-chain node rank %d): zero-waste R=%d c=%s (%+.2f%%); %s' % (node, tnode, R0, mp.nstr(c0, 8), float((c0 / P - 1) * 100), be), flush=True)
