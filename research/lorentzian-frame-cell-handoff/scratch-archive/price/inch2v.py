"""4-section architecture with in-chain section reads (3v arrivals, all delivered at t-perp), zero waste R = 2v
(+ total hosts), copies stop at <s>, one middle node level; break-even R vs P111-tuned (wasted helpers end at FULL)."""
from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
def run(name, v, h, sec, tot_rank, ntot, tot_fresh, node):
    def loc(waste):
        L = {}
        def add(ch, n):
            for a, b in zip(ch, ch[1:]): L[b - a] = L.get(b - a, 0) + n
        add([1, 2] + node + [sec, sec + 1, h], v)             # sources delivered
        add([0, 1, 2] + node + [sec, sec + 1, h], 2 * v)      # copies delivered
        add([0, 1, 2] + node + [h], waste)                    # wasted
        add([0, h], tot_fresh)
        add([0, sec, sec + 1], v)                              # targets: in-chain section, then t-perp
        L[tot_rank] = L.get(tot_rank, 0) + ntot
        return L
    R0 = 2 * v + tot_fresh
    f = lambda w: price(loc(w), v, h, R0 + w)[0]
    c0 = f(0)
    lo, hi = 0, 4 * v - R0
    if f(hi) is not None and f(hi) >= P:
        be = '>= wall %d' % (R0 + hi)
    else:
        while hi - lo > 1:
            mid = (lo + hi) // 2
            c = f(mid)
            if c is not None and c >= P: lo = mid
            else: hi = mid
        be = 'R <= %d' % (R0 + lo)
    print('%-28s node %-4s zero-waste R=%d: c=%s (%+.2f%%); beats P111t iff %s' % (name, node, R0, mp.nstr(c0, 8), float((c0 / P - 1) * 100), be), flush=True)
for node in ([3], [4], [5]):
    run('E8 punctured v=111', 111, 8, 6, 7, 9, 9, node)
    run('E8 v=120', 120, 8, 6, 8, 9, 9, node)
for node in ([3], [5], [7]):
    run('I_{11,1} v=220', 220, 11, 9, 10, 11, 0, node)
