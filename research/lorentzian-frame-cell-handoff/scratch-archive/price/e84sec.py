"""E8 analogue: 4-section architecture chains at R = 3v (+9 total hosts), copy stops forced, one middle node level."""
from mpmath import mp
from pricer import price
P = mp.mpf('0.001733427039589844234749')
for v, cst_rank, extra in ((120, 8, 9), (111, 7, 9)):
    R = 3 * v + extra; h = 8
    for nodes in ([], [3], [4], [5], [3, 5], [4, 5]):
        loc = {}
        def add(ch, n):
            for a, b in zip(ch, ch[1:]): loc[b - a] = loc.get(b - a, 0) + n
        add([1, 2] + nodes + [6, 8], v)                 # sources: in-chain-ended
        add([0, 1, 2] + nodes + [6, 7, 8], 3 * v)       # copies: delivered at t-perp
        add([0, 8], extra)                              # total hosts (fresh)
        add([0, 6, 7], v)                               # targets
        loc[cst_rank] = loc.get(cst_rank, 0) + 9
        c = price(loc, v, h, R)[0]
        print('E8 v=%d R=%d middle %-7s c = %s (%+.2f%% vs P111t)' % (v, R, nodes, mp.nstr(c, 8), float((c / P - 1) * 100)), flush=True)
