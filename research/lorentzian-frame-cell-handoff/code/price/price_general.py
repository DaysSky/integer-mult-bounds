"""General one/two-level frame-cell shape with the cheap-chain rules (dead pieces skip t-perp, copies are empties
0-9-10-11, targets read in-chain).  Parameters: R (helpers), D = delivered registers (alive pieces + copies),
X = extra cell-stage registers (third cell registers etc.), target chain, node rank, low stop m1 with fraction phi.
Pieces = 660 + X cell-stage registers (220 sources + 440 carriers + X extra carriers); alive = min(pieces, D);
copies = D - alive; dead = pieces - alive; remaining helpers = dead empties [0,9,11]."""
from pricer import price
from mpmath import mp
P111t = mp.mpf('0.001733427039589844')
def hist(R, D, X=0, tgt=(0, 9, 10), node=8, m1=3, phi=1.0):
    h = {}
    def add(ch, k):
        assert k >= 0 and all(b > a for a, b in zip(ch, ch[1:])), (ch, k)
        for a, b in zip(ch, ch[1:]): h[b - a] = h.get(b - a, 0) + k
    def add2(pre, post, k):
        kl = round(phi * k); add(pre + [m1] + post, kl); add(pre + post, k - kl)
    pieces = 660 + X
    alive = min(pieces, D); copies = D - alive; dead = pieces - alive
    # sources are dead first (cheapest), then carriers
    ds = min(220, dead); add2([1, 2], [node, 9, 11], ds); add2([1, 2], [node, 9, 10, 11], 220 - ds)
    dc = dead - ds; add2([0, 1, 2], [node, 9, 11], dc); add2([0, 1, 2], [node, 9, 10, 11], 440 + X - dc)
    add([0, 9, 10, 11], copies)
    extra = R - 440 - X - copies; assert extra >= 0, (R, X, copies)
    add([0, 9, 11], extra)
    add(list(tgt), 220)
    h[10] = h.get(10, 0) + 11
    assert sum(k * c for k, c in h.items()) == 10 * 220 + 11 * R + 10 * 220 + 10 * 11
    return h
def pct(*a, **k):
    R = a[0]
    c = price(hist(*a, **k), 220, 11, R)[0]
    return float((c / P111t - 1) * 100) if c else None
if __name__ == '__main__':
    print('ideal frame in-chain (D=440, X=0): R=550', '%+.2f%%' % pct(550, 440))
    for tgt in ((0, 9, 10), (0, 2, 9, 10)):
        for (node, m1, phi) in ((8, 3, 1.0), (8, 3, 0.75), (7, 3, 1.0), (8, 5, 1.0)):
            row = []
            for R, D, X in ((660, 667, 0), (660, 667, 108), (700, 667, 108), (700, 700, 108), (750, 750, 108)):
                p = pct(R, D, X, tgt=tgt, node=node, m1=m1, phi=phi)
                row.append('R%d D%d X%d %+.2f%%' % (R, D, X, p))
            print('tgt', tgt, 'node', node, 'm1', m1, 'phi', phi, ' | '.join(row), flush=True)
