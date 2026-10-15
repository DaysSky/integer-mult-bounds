"""E8 (v=120, h=8) exact-count prices: R420 control (published histogram) and the A3-parity architecture shape.
A3 shape (ranks: line 1, cell 2, node 4, section 6, t-perp 7, full 8):
 pieces = all 360 branch registers via a rank-4 node: sources 1-2-4-6-[7]-8, carriers 0-1-2-4-6-[7]-8;
 delivered pieces 140 (one per section), dead 220;  Q-delivery empties 120: 0-1-4-6-7-8;  copy empties C: 0-6-7-8;
 extra overhead empties X: 0-6-8 (dead);  targets 120: 0-1-7;  9 totals at rank 8.
 R = 240 + 120 + C + X.  Mass check: 7*120 + 8*R + 7*120 + 8*9."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
r420 = {1: 1320, 2: 1440, 4: 60, 5: 120, 8: 9}
c = price(r420, 120, 8, 420)[0]; print('R420 control c', mp.nstr(c, 12), '%+.2f%%' % float((c / P111t - 1) * 100))
def hist(C, X, node=4):
    h = {}
    def add(ch, k):
        assert k >= 0
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    # dead pieces 220: sources 120 + carriers 100 ; delivered pieces 140 = carriers
    add([1, 2, node, 6, 8], 120); add([0, 1, 2, node, 6, 8], 100); add([0, 1, 2, node, 6, 7, 8], 140)
    add([0, 1, node, 6, 7, 8], 120)
    add([0, 6, 7, 8], C); add([0, 6, 8], X)
    add([0, 1, 7], 120)
    h[8] = h.get(8, 0) + 9
    R = 240 + 120 + C + X
    mass = sum(k * v for k, v in h.items())
    assert mass == 7 * 120 + 8 * R + 7 * 120 + 8 * 9, (mass, R)
    return h, R
for node in (3, 4, 5):
    out = []
    for X in (0, 20, 40, 60):
        hh, R = hist(100, X, node)
        c = price(hh, 120, 8, R)[0]
        out.append('R=%d %s' % (R, '%+.2f%%' % float((c / P111t - 1) * 100) if c else 'n/a'))
    print('E8 A3 shape, node rank', node, ' | '.join(out), flush=True)
